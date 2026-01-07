from fastapi import APIRouter, HTTPException
from app.services.esapi_worker import run_in_esapi
from app.core.config import logger
import pyesapi
import numpy as np

router = APIRouter()

# --- Internal ESAPI Helper Functions ---
# These functions MUST accept app_esapi as first argument and run inside the worker thread.

def _get_system_info(app_esapi):
    return {
        "User": str(app_esapi.CurrentUser),
        "PatientCount": len(app_esapi.PatientSummaries) if app_esapi.PatientSummaries else 0
    }

def _test_aria_db_connection(app_esapi):
    """
    Realiza una consulta real a la base de datos ARIA.
    Obtiene los primeros 3 pacientes para confirmar lectura de datos.
    """
    try:
        # Acceder a PatientSummaries fuerza una consulta a la DB
        summaries = list(app_esapi.PatientSummaries)
        
        # Tomamos solo los 3 primeros para no saturar la respuesta
        sample_patients = []
        for p in summaries[:3]:
            sample_patients.append({
                "Id": p.Id, 
                "LastName": p.LastName, 
                "FirstName": p.FirstName
            })
            
        return {
            "connection_status": "OK",
            "total_patients_found": len(summaries),
            "current_user_aria": str(app_esapi.CurrentUser),
            "sample_data": sample_patients
        }
    except Exception as e:
        return {
            "connection_status": "FAILED",
            "error_details": str(e)
        }

def _get_patient_plans(app_esapi, patient_id: str):
    """
    Busca un paciente y lista todos sus planes de tratamiento aprobados o en curso.
    """
    patient = app_esapi.OpenPatientById(patient_id)
    
    if patient is None:
        return None
    
    try:
        courses_data = []
        for course in patient.Courses:
            plans_data = []
            for plan in course.PlanSetups:
                planned_dose = 0.0
                if plan.TotalPrescribedDose is not None:
                    planned_dose = plan.TotalPrescribedDose.Dose

                plans_data.append({
                    "PlanId": plan.Id,
                    "PlanName": plan.Name,
                    "TargetVolume": plan.TargetVolumeID if plan.TargetVolumeID else "",
                    "PlannedDose": planned_dose,
                    "Status": str(plan.ApprovalStatus) 
                })
            
            courses_data.append({
                "CourseId": course.Id,
                "Diagnoses": [d.ClinicalDescription for d in course.Diagnoses],
                "Plans": plans_data
            })
            
        return {
            "PatientId": patient.Id,
            "FullName": f"{patient.LastName}, {patient.FirstName}",
            "Courses": courses_data
        }
        
    finally:
        app_esapi.ClosePatient()

def _get_plan_dose_slice(app_esapi, patient_id: str, plan_id: str, slice_idx: int = -1):
    """
    Recupera dosis cambiando el modo de presentación del plan a Absoluto.
    """
    patient = app_esapi.OpenPatientById(patient_id)
    if patient is None:
        return None
    
    try:
        # 1. Buscar el plan
        target_plan = None
        for course in patient.Courses:
            target_plan = next((p for p in course.PlanSetups if p.Id == plan_id), None)
            if target_plan: break
        
        if target_plan is None:
            return {"found": False, "reason": "Plan ID no encontrado"}
            
        if target_plan.Dose is None:
            return {"found": True, "has_dose": False, "reason": "No hay dosis calculada"}

        # 2. CAMBIO DE MODO: Forzamos al plan a entregarnos Gy/cGy
        original_presentation = target_plan.DoseValuePresentation
        
        try:
            target_plan.DoseValuePresentation = pyesapi.DoseValuePresentation.Absolute
            dose_np = target_plan.Dose.np_array_like()
            unit_name = target_plan.TotalPrescribedDose.UnitAsString if target_plan.TotalPrescribedDose else "Absolute"
            
        finally:
            target_plan.DoseValuePresentation = original_presentation

        # 3. Procesar el slice
        x_dim, y_dim, z_dim = dose_np.shape
        
        if slice_idx < 0 or slice_idx >= z_dim:
            selected_slice = z_dim // 2
        else:
            selected_slice = slice_idx
            
        # Transponer para visualización [Y, X]
        slice_data = dose_np[:, :, selected_slice].T.tolist()
        max_dose = float(np.max(dose_np))
        
        return {
            "found": True,
            "has_dose": True,
            "plan_id": target_plan.Id,
            "slice_z_index": selected_slice,
            "unit": unit_name, 
            "method": "Direct_Absolute_Switch",
            "max_dose": max_dose,
            "data": slice_data
        }

    finally:
        app_esapi.ClosePatient()

# --- Endpoints ---

@router.get("/info", tags=["System"])
def get_info():
    """Get basic system info and current user."""
    try:
        return run_in_esapi(_get_system_info)
    except Exception as e:
        logger.error(f"Error en endpoint /info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/aria-test", tags=["System"])
def aria_test():
    """Endpoint específico para validar comunicación con ARIA"""
    try:
        logger.info("Iniciando prueba de conexión a ARIA...")
        result = run_in_esapi(_test_aria_db_connection)
        
        if result["connection_status"] == "FAILED":
            raise HTTPException(status_code=500, detail=result["error_details"])
            
        return result
    except Exception as e:
        logger.error(f"Error en test ARIA: {e}")
        raise HTTPException(status_code=500, detail=str(e))        

@router.get("/patients/{patient_id}/plans", tags=["Patient"])
def get_patient_plans(patient_id: str):
    """Get all plans for a specific patient."""
    try:
        logger.info(f"Consultando planes para paciente: {patient_id}")
        data = run_in_esapi(_get_patient_plans, patient_id=patient_id)
        
        if data is None:
            raise HTTPException(status_code=404, detail=f"Paciente {patient_id} no encontrado")
            
        return data
    except Exception as e:
        logger.error(f"Error recuperando planes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patients/{patient_id}/plans/{plan_id}/dose", tags=["Patient"])
def get_dose_slice(patient_id: str, plan_id: str, z: int = -1):
    """
    Obtiene un mapa de calor (array 2D) de la dosis del plan.
    Param 'z': Índice del corte axial (0 a N). Si se omite, devuelve el central.
    """
    try:
        logger.info(f"Solicitando dosis para plan {plan_id}, slice {z}")
        result = run_in_esapi(_get_plan_dose_slice, patient_id=patient_id, plan_id=plan_id, slice_idx=z)
        
        if result is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
            
        if not result["found"]:
            raise HTTPException(status_code=404, detail=result["reason"])
            
        if not result["has_dose"]:
            raise HTTPException(status_code=400, detail=result["reason"])
            
        return result
        
    except Exception as e:
        logger.error(f"Error obteniendo dosis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
