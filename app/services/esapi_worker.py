import threading
import queue
import time
import atexit
import pythoncom
from fastapi import HTTPException
from app.core.config import logger

# ESAPI Request Queue
esapi_request_queue = queue.Queue()

# Global event to signal ESAPI readiness
esapi_ready = threading.Event()

def esapi_worker_loop():
    """
    Main loop for the ESAPI worker thread.
    Initializes the ESAPI Application and processes requests from the queue.
    """
    threading.current_thread().name = "ESAPI-Worker"
    # Ensure this thread is initialized as STA for COM/ESAPI
    pythoncom.CoInitialize()
    
    logger.info(">>> Hilo Worker iniciado. Intentando importar pyesapi...")
    
    app_esapi = None
    
    try:
        import pyesapi
        logger.info("pyesapi importado. Creando Application (esto puede tardar)...")
        
        start_time = time.time()
        
        # 'FastAPI_Debug' acts as the script name for logging purposes
        app_esapi = pyesapi.CustomScriptExecutable.CreateApplication('FastAPI_Debug')
        
        elapsed = time.time() - start_time
        logger.info(f"!!! ESAPI Application creada exitosamente en {elapsed:.2f} segundos.")
        
        # Register cleanup on exit
        atexit.register(app_esapi.Dispose)
        
        # Signal readiness
        esapi_ready.set()
        
    except Exception as e:
        logger.error(f"ERROR FATAL iniciando ESAPI: {e}")
        # We don't return here to allow the thread to stay alive or we could exit.
        # If we exit, the main server might continue but ESAPI calls will fail.
        return

    logger.info("Entrando en el bucle de escucha de tareas...")
    
    while True:
        try:
            # Poll with timeout to allow checking for exit signals or just logging idle
            try:
                task = esapi_request_queue.get(timeout=5)
            except queue.Empty:
                continue

            if task is None:
                logger.info("Recibida señal de apagado. Cerrando Worker.")
                if app_esapi:
                    app_esapi.Dispose()
                break
                
            logger.info("Tarea recibida. Procesando...")
            future_result, func, kwargs = task
            
            try:
                # Execute ESAPI logic
                result = func(app_esapi, **kwargs)
                logger.info(f"Tarea {func.__name__} completada con éxito.")
                future_result.put({"success": True, "data": result})
            except Exception as e:
                logger.error(f"Error ejecutando tarea {func.__name__}: {e}")
                future_result.put({"success": False, "error": str(e)})
            finally:
                esapi_request_queue.task_done()
                
        except Exception as e:
            logger.error(f"Error inesperado en el bucle del worker: {e}")

def start_worker_thread():
    """Starts the background worker thread."""
    worker_thread = threading.Thread(target=esapi_worker_loop, daemon=True)
    worker_thread.start()
    return worker_thread

def run_in_esapi(func, **kwargs):
    """
    Helper to send a function to be executed in the ESAPI thread.
    The function `func` must accept `app_esapi` as its first argument.
    """
    if not esapi_ready.is_set():
        raise HTTPException(status_code=503, detail="ESAPI aún se está inicializando, intenta de nuevo en unos segundos.")
    
    logger.info(f"Enviando solicitud para: {func.__name__}")
    result_queue = queue.Queue()
    esapi_request_queue.put((result_queue, func, kwargs))
    
    response = result_queue.get()
    if not response["success"]:
        # If the inner function failed, re-raise as an Exception (or HTTPException)
        raise Exception(response["error"])
    return response["data"]
