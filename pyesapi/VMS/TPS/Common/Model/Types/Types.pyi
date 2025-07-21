"""
Type stubs for VMS.TPS.Common.Model.Types
Generated from .NET XML documentation
"""

from typing import Any, List, Optional, Union, Dict, Iterable, TypeVar, Generic, overload
from datetime import datetime
from System import Array, Double, Single, Int32, Boolean, String
from System.Collections.Generic import KeyValuePair
from System import Collections

# Generic type variables
T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')

class BeamNumber:
    """
    Represents a unique identifier for a beam of a plan. The identifier is unique within the scope of the plan.

    Attributes:
        Number (int): The beam number.
        IsValid (bool): Returns true if the given BeamNumber is valid. Otherwise false.
    """
    # Constructs a new beam number from a numeric beam number.
    @overload
    def __init__(self, number: int) -> None:
        """
        Args:
            number: Make sure that the beam number corresponds to the real beam number, otherwise use NotABeamNumber.
        """
        ...


    # Constructs a new beam number from another BeamNumber.
    @overload
    def __init__(self, other: BeamNumber) -> None:
        """
        Args:
            other: Another BeamNumber.
        """
        ...


    Number: int

    IsValid: bool

    # Compares two beam numbers for equality.
    def op_Equality(self, a: BeamNumber, b: BeamNumber) -> bool:
        """
        Args:
            a: The first object to compare.
            b: The second object to compare.
        """
        ...


    # Compares two BeamNumbers for inequality.
    def op_Inequality(self, a: BeamNumber, b: BeamNumber) -> bool:
        """
        Args:
            a: The first object to compare.
            b: The second object to compare.
        """
        ...


    # Compares two BeamNumbers, a and b, to determine if a is greater than b.
    def op_GreaterThan(self, a: BeamNumber, b: BeamNumber) -> bool:
        """
        Args:
            a: The first object to compare.
            b: The second object to compare.
        """
        ...


    # Compares two BeamNumbers, a and b, to determine if a is smaller than b.
    def op_LessThan(self, a: BeamNumber, b: BeamNumber) -> bool:
        """
        Args:
            a: The first object to compare.
            b: The second object to compare.
        """
        ...


    # Compares two BeamNumbers, a and b, to determine if a is greater than or equal to b.
    def op_GreaterThanOrEqual(self, a: BeamNumber, b: BeamNumber) -> bool:
        """
        Args:
            a: The first object to compare.
            b: The second object to compare.
        """
        ...


    # Compares two BeamNumbers, a and b, to determine if a is smaller than or equal to b.
    def op_LessThanOrEqual(self, a: BeamNumber, b: BeamNumber) -> bool:
        """
        Args:
            a: The first object to compare.
            b: The second object to compare.
        """
        ...


    # Converts a BeamNumber to an int.
    def op_Implicit(self, bn: Int32) -> int:
        """
        Args:
            bn: The converted BeamNumber object.
        """
        ...


    # Provides a hash code for the item, see
    def GetHashCode(self) -> int:
        ...


    # Determines whether the specified object is equal to the current object.
    def Equals(self, other: Any) -> bool:
        """
        Args:
            other: The other object to compare.
        """
        ...


    # Indicates whether the current object is equal to another object of the same type.
    def Equals(self, other: BeamNumber) -> bool:
        """
        Args:
            other: An object to compare with this object.
        """
        ...


    # This member is internal to the Eclipse Scripting API.
    def GetSchema(self) -> Xml.Schema.XmlSchema:
        ...


    # This member is internal to the Eclipse Scripting API.
    def ReadXml(self, reader: Xml.XmlReader) -> None:
        """
        Args:
            reader: The XmlReader stream from which the object is deserialized.
        """
        ...


    # Serialization support.
    def WriteXml(self, writer: Xml.XmlWriter) -> None:
        """
        Args:
            writer: The System.Xml.XmlWriter stream to which the object is serialized.
        """
        ...



class StructureMarginGeometry:
    """
    Specifies whether a margin operation expands (outer margin) or shrinks (inner margin) the volume.
    """
    def __init__(self) -> None: ...


class AxisAlignedMargins:
    """
    Represents margins aligned to the axes of the image coordinate system, in mm. Negative margins are not allowed, but it is possible to specify whether the margins represent an inner or outer margin.
    """
    # Constructs a new AxisAlignedMargins instance. The given margins are aligned to the axes of the image coordinate system, in mm.
    def __init__(self, geometry: StructureMarginGeometry, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> None:
        """
        Args:
            geometry: Specifies whether the margin operation expands (outer margin) or shrinks (inner margin) the volume.
            x1: A non-negative value defining the margin towards the negative X axis, in mm.
            y1: A non-negative value defining the margin towards the negative Y axis, in mm.
            z1: A non-negative value defining the margin towards the negative Z axis, in mm.
            x2: A non-negative value defining the margin towards the positive X axis, in mm.
            y2: A non-negative value defining the margin towards the positive Y axis, in mm.
            z2: A non-negative value defining the margin towards the positive Z axis, in mm.
        """
        ...


    # A string that represents the current object.
    def ToString(self) -> str:
        ...



class ChangeBrachyTreatmentUnitResult:
    """
    Return value for
    """
    def __init__(self) -> None: ...


class ObjectiveGoalType:
    """
    Clinical goal Objective type
    """
    def __init__(self) -> None: ...


class ObjectiveOperator:
    """
    Clinical goal Objective operator
    """
    def __init__(self) -> None: ...


class ObjectiveUnit:
    """
    Clinical goal Objective Unit
    """
    def __init__(self) -> None: ...


class Objective:
    """
    Represents a clinical goal objective.

    Attributes:
        Type (ObjectiveGoalType): Objective type
        Value (float): Objective value
        ValueUnit (ObjectiveUnit): Objective value
        Operator (ObjectiveOperator): Objective operator
        Limit (float): Objective limit
        LimitUnit (ObjectiveUnit): Objective limit unit
    """
    # Clinical Goal Objective constructor
    def __init__(self, type: ObjectiveGoalType, value: float, valueUnit: ObjectiveUnit, oper: ObjectiveOperator, limit: float, limitUnit: ObjectiveUnit) -> None:
        """
        Args:
            type: Objective type.
            value: Objective value.
            valueUnit: Value unit.
            oper: Operator.
            limit: Limit.
            limitUnit: Limit unit.
        """
        ...


    Type: ObjectiveGoalType

    Value: float

    ValueUnit: ObjectiveUnit

    Operator: ObjectiveOperator

    Limit: float

    LimitUnit: ObjectiveUnit

    # This member is internal to the Eclipse Scripting API.
    def GetSchema(self) -> Xml.Schema.XmlSchema:
        ...


    # This member is internal to the Eclipse Scripting API.
    def ReadXml(self, reader: Xml.XmlReader) -> None:
        """
        Args:
            reader: XmlReader.
        """
        ...


    # Serialization support. TODO: Convert unit and operator to human form.
    def WriteXml(self, writer: Xml.XmlWriter) -> None:
        """
        Args:
            writer: The System.Xml.XmlWriter stream to which the object is serialized.
        """
        ...



class ClinicalGoal:
    """
    Represents a clinical goal.

    Attributes:
        MeasureType (MeasureType): Clinical goal measure type
        StructureId (str): Clinical goal structure Id
        Objective (Objective): Clinical goal objective
        ObjectiveAsString (str): String representation of clinical goal objective
        Priority (GoalPriority): Goal priority (0-4), where 0 is Most Important
        VariationAcceptable (float): Clinical goal Variation Acceptable (tolerance)
        VariationAcceptableAsString (str): String representation of clinical goal Variation Acceptable (tolerance)
        ActualValue (float): Clinical goal actual value
        ActualValueAsString (str): String representation of clinical goal actual value
        EvaluationResult (GoalEvalResult): Evaluation result.
    """
    # Construct a ClinicalGoal
    def __init__(self, measureType: MeasureType, structureId: str, objective: Objective, objAsString: str, priority: GoalPriority, tolerance: float, toleranceAsString: str, actual: float, actualAsString: str, evalResult: GoalEvalResult) -> None:
        """
        Args:
            measureType: Measure Type.
            structureId: Structure ID.
            objective: Objective.
            objAsString: Objective as a string.
            priority: Priority.
            tolerance: Tolerance.
            toleranceAsString: Tolerance as a string.
            actual: Actual value.
            actualAsString: Actual value as a string.
            evalResult: Goal evaluation result.
        """
        ...


    MeasureType: MeasureType

    StructureId: str

    Objective: Objective

    ObjectiveAsString: str

    Priority: GoalPriority

    VariationAcceptable: float

    VariationAcceptableAsString: str

    ActualValue: float

    ActualValueAsString: str

    EvaluationResult: GoalEvalResult

    # This member is internal to the Eclipse Scripting API.
    def GetSchema(self) -> Xml.Schema.XmlSchema:
        ...


    # This member is internal to the Eclipse Scripting API.
    def ReadXml(self, reader: Xml.XmlReader) -> None:
        """
        Args:
            reader: XmlReader.
        """
        ...


    # Serialization support.
    def WriteXml(self, writer: Xml.XmlWriter) -> None:
        """
        Args:
            writer: The System.Xml.XmlWriter stream to which the object is serialized.
        """
        ...



class IDoseValueDisplaySettings:
    """
    Application specific dose value display settings.
    """
    def __init__(self) -> None: ...

    # Determines how many decimals to use to display a dosevalue with specified unit.
    def Decimals(self, unit: DoseUnit) -> int:
        """
        Args:
            unit: DoseUnit for which the number of decimals is requested.
        """
        ...



class DoseValueDisplayConfig:
    """
    Configure the settings related to the dose value display for the application. Defaults to the same settings as Eclipse.

    Attributes:
        DisplaySettings (IDoseValueDisplaySettings): Get and set current dosevalue display settings. Set settings controller to null reverts to default display settings.
    """
    def __init__(self) -> None: ...

    DisplaySettings: IDoseValueDisplaySettings

    # Get number of decimals to user for dosevalue of the defined dose unit
    def Decimals(self, unit: DoseUnit) -> int:
        """
        Args:
            unit: DoseUnit for which the number of decimals is requested.
        """
        ...



class DoseValue:
    """
    Represents a dose value. DoseValue semantics follows the semantics of System.Double, with DoseValue.Undefined corresponding to Double.NaN.

    Attributes:
        Dose (float): The value of this instance.
        Unit (DoseValue+DoseUnit): The unit of this instance.
        UnitAsString (str): The unit of this instance as a string.
        ValueAsString (str): The value of this instance as a string.
        IsAbsoluteDoseValue (bool): Returns true if the unit of the dose value is absolute (Gy or cGy).
        IsRelativeDoseValue (bool): Returns true if the unit of the dose value is relative (%).
        Decimals (int): The display precision of this value
    """
    # Constructs a DoseValue.
    @overload
    def __init__(self, value: float, unitName: str) -> None:
        """
        Args:
            value: Value for this instance.
            unitName: String that corresponds to one of the enumeration values of DoseUnit.
        """
        ...


    # Constructs a DoseValue.
    @overload
    def __init__(self, value: float, unit: DoseUnit) -> None:
        """
        Args:
            value: Value for this instance
            unit: Unit of this instance.
        """
        ...


    Dose: float

    Unit: DoseValue+DoseUnit

    UnitAsString: str

    ValueAsString: str

    IsAbsoluteDoseValue: bool

    IsRelativeDoseValue: bool

    Decimals: int

    # Equality comparison of DoseValue and Object. This method considers two instances of DoseValue.Undefined to be equal to each other. Otherwise, a dose value is equal to an object only if the object is a DoseValue and the units and the values are equal. For epsilon-equal comparison, use
    def Equals(self, obj: Any) -> bool:
        """
        Args:
            obj: Object to compare this to.
        """
        ...


    # A hash code for the current object.
    def GetHashCode(self) -> int:
        ...


    # Equality comparison of dose values. This method considers two instances of DoseValue.Undefined to be equal to each other. Otherwise, two dose values are equal only if the units and the values are equal. For epsilon-equal comparison, use
    def Equals(self, other: DoseValue) -> bool:
        """
        Args:
            other: Dose value to compare this to.
        """
        ...


    # Epsilon-equality comparison of dose values. This method considers two instances of DoseValue.Undefined to be equal to each other. Otherwise, two dose values are equal only if the units are equal and the values are within epsilon.
    def Equals(self, other: DoseValue, epsilon: float) -> bool:
        """
        Args:
            other: Dose value to compare this to.
            epsilon: Epsilon to use for the dose value comparison.
        """
        ...


    # Equality operator for dose values. This operator considers two instances of DoseValue.Undefined to be inequal. For epsilon-equal comparison, use
    def op_Equality(self, dv1: DoseValue, dv2: DoseValue) -> bool:
        """
        Args:
            dv1: First operand.
            dv2: Second operand.
        """
        ...


    # Inequality operator for dose values. This operator considers two instances of DoseValue.Undefined to be inequal. For epsilon-equal comparison, use
    def op_Inequality(self, dv1: DoseValue, dv2: DoseValue) -> bool:
        """
        Args:
            dv1: First operand.
            dv2: Second operand.
        """
        ...


    # Comparison of dose values. DoseValue.Undefined preceeds other values. Otherwise, different units cause an exception to be thrown. The values are compared using Double.CompareTo(Double).
    def CompareTo(self, other: DoseValue) -> int:
        """
        Args:
            other: Dose value to compare this to.
        """
        ...


    # Less-than comparison of dose values. Comparison with DoseValue.Undefined is false.
    def op_LessThan(self, dv1: DoseValue, dv2: DoseValue) -> bool:
        """
        Args:
            dv1: First operand.
            dv2: Second operand.
        """
        ...


    # Less-than-or-equal comparison of dose values. Comparison with DoseValue.Undefined is false.
    def op_LessThanOrEqual(self, dv1: DoseValue, dv2: DoseValue) -> bool:
        """
        Args:
            dv1: First operand.
            dv2: Second operand.
        """
        ...


    # Greater-than comparison of dose values. Comparison with DoseValue.Undefined is false.
    def op_GreaterThan(self, dv1: DoseValue, dv2: DoseValue) -> bool:
        """
        Args:
            dv1: First operand.
            dv2: Second operand.
        """
        ...


    # Greater-than comparison of dose values. Comparison with DoseValue.Undefined is false.
    def op_GreaterThanOrEqual(self, dv1: DoseValue, dv2: DoseValue) -> bool:
        """
        Args:
            dv1: First operand.
            dv2: Second operand.
        """
        ...


    # Subtraction of dose values. If either of the operands is DoseValue.Undefined, the result will be DoseValue.Undefined.
    def op_Subtraction(self, dv1: DoseValue, dv2: DoseValue) -> DoseValue:
        """
        Args:
            dv1: First operand.
            dv2: Second operand.
        """
        ...


    # Addition of dose values. If either of the operands is DoseValue.Undefined, the result will be DoseValue.Undefined.
    def op_Addition(self, dv1: DoseValue, dv2: DoseValue) -> DoseValue:
        """
        Args:
            dv1: First operand.
            dv2: Second operand.
        """
        ...


    # Multiplication of a dose value and a double. If the dose value is DoseValue.Undefined, the result will be DoseValue.Undefined.
    def op_Multiply(self, dv: DoseValue, dbl: float) -> DoseValue:
        """
        Args:
            dv: DoseValue to multiply.
            dbl: Multiplier.
        """
        ...


    # Multiplication of a dose value and a double. If the dose value is DoseValue.Undefined, the result will be DoseValue.Undefined.
    def op_Multiply(self, dbl: float, dv: DoseValue) -> DoseValue:
        """
        Args:
            dbl: Multiplier.
            dv: DoseValue to multiply.
        """
        ...


    # Division of a dose value by a double. If the dose value is DoseValue.Undefined, the result will be DoseValue.Undefined.
    def op_Division(self, dv: DoseValue, dbl: float) -> DoseValue:
        """
        Args:
            dv: Dividend.
            dbl: Divisor.
        """
        ...


    # Division of two dose values. If either of the operands is DoseValue.Undefined, the result will be Double.NaN.
    def op_Division(self, dv1: DoseValue, dv2: DoseValue) -> DoseValue:
        """
        Args:
            dv1: Dividend.
            dv2: Divisor.
        """
        ...


    # Returns true if the dose unit is absolute (Gy or cGy).
    def IsAbsoluteDoseUnit(self, doseUnit: DoseUnit) -> bool:
        """
        Args:
            doseUnit: The dose unit that is evaluated.
        """
        ...


    # Returns true if the dose unit is relative (%).
    def IsRelativeDoseUnit(self, doseUnit: DoseUnit) -> bool:
        """
        Args:
            doseUnit: The dose unit that is evaluated.
        """
        ...


    # A string that represents the current object.
    def ToString(self) -> str:
        ...


    # A dose value, for which the value is Double.NaN and the unit is unknown.
    def UndefinedDose(self) -> DoseValue:
        ...


    # Returns true if this dose value is equal to DoseValue.Undefined, false otherwise.
    def IsUndefined(self) -> bool:
        ...


    # This member is internal to the Eclipse Scripting API.
    def GetSchema(self) -> Xml.Schema.XmlSchema:
        ...


    # This member is internal to the Eclipse Scripting API.
    def ReadXml(self, reader: Xml.XmlReader) -> None:
        """
        Args:
            reader: XmlReader.
        """
        ...


    # Serialization support.
    def WriteXml(self, writer: Xml.XmlWriter) -> None:
        """
        Args:
            writer: The System.Xml.XmlWriter stream to which the object is serialized.
        """
        ...



class SingleLayerParameters:
    """
    One layer or group of DRR calculation parameters.

    Attributes:
        LayerOn (bool): Defines whether the layer of parameters are selected.
        Weight (float): Weight factor of the DRR layer. Value must be between -100.0 and 100.0.
        CTFrom (float): Lower end of the CT window. Value must be between -1024.0 and 6000.0.
        CTTo (float): Upper end of the CT window. Value must be between -1024.0 and 6000.0.
        GeoClipping (bool): Image volume type on which the DRR calculation is based. If calculation is based on partial image volume as specified by
        GeoFrom (float): Starting distance from the isocenter. Value must be between -10000 and 10000 mm.
        GeoTo (float): Ending distance from the isocenter. Value must be between -10000 and 10000 mm.
    """
    def __init__(self) -> None: ...

    LayerOn: bool

    Weight: float

    CTFrom: float

    CTTo: float

    GeoClipping: bool

    GeoFrom: float

    GeoTo: float


class DRRCalculationParameters:
    """
    Parameters for DRR calculation.

    Attributes:
        DRRSize (float): DRR size. Decreasing the size of the DRR effectively increases the resolution of the DRR. Value must be between 5 and 5120 mm.
        StructureOutlines (bool): Defines if structure outlines are added as layers in the DRR.
        FieldOutlines (bool): Defines if field outlines (MLC, CIAO etc.) are added as layers in the DRR.
    """
    # Creates a new set of DRR calculation parameters with default values.
    @overload
    def __init__(self) -> None:
        ...


    # Creates a new set of DRR calculation parameters with a specified DRR size.
    @overload
    def __init__(self, drrSize: float) -> None:
        """
        Args:
            drrSize: DRR size in mm.
        """
        ...


    # Creates a new set of DRR calculation parameters.
    @overload
    def __init__(self, drrSize: float, weight: float, ctFrom: float, ctTo: float) -> None:
        """
        Args:
            drrSize: DRR size in mm. Value must be between 5 and 5120 mm.
            weight: DRR layer weight. Value must be between -100.0 and 100.0.
            ctFrom: Lower end of the CT window. Value must be between -1024.0 and 6000.0.
            ctTo: Upper end of the CT window. Value must be between -1024.0 and 6000.0.
        """
        ...


    # Creates a new set of DRR calculation parameters.
    @overload
    def __init__(self, drrSize: float, weight: float, ctFrom: float, ctTo: float, geoFrom: float, geoTo: float) -> None:
        """
        Args:
            drrSize: DRR size in mm. Value must be between 5 and 5120 mm.
            weight: DRR layer weight. Value must be between -100.0 and 100.0.
            ctFrom: Lower end of the CT window. Value must be between -1024.0 and 6000.0.
            ctTo: Upper end of the CT window. Value must be between -1024.0 and 6000.0.
            geoFrom: Starting distance from the isocenter. Value must be between -10000 and 10000 mm.
            geoTo: Ending distance from the isocenter. Value must be between -10000 and 10000 mm.
        """
        ...


    DRRSize: float

    StructureOutlines: bool

    FieldOutlines: bool

    # Gets a single layer of editable DRR calculation parameters.
    def GetLayerParameters(self, index: int) -> SingleLayerParameters:
        """
        Args:
            index: Layer index. Value must be between 0 and 2.
        """
        ...


    # Sets parameters for
    def SetLayerParameters(self, index: int, weight: float, ctFrom: float, ctTo: float) -> None:
        """
        Args:
            index: Layer index.
            weight: DRR layer weight. Value must be between -100.0 and 100.0.
            ctFrom: Lower end of the CT window. Value must be between -1024.0 and 6000.0.
            ctTo: Upper end of the CT window. Value must be between -1024.0 and 6000.0.
        """
        ...


    # Sets parameters for
    def SetLayerParameters(self, index: int, weight: float, ctFrom: float, ctTo: float, geoFrom: float, geoTo: float) -> None:
        """
        Args:
            index: Layer index.
            weight: DRR layer weight. Value must be between -100.0 and 100.0.
            ctFrom: Lower end of the CT window. Value must be between -1024.0 and 6000.0.
            ctTo: Upper end of the CT window. Value must be between -1024.0 and 6000.0.
            geoFrom: Starting distance from the isocenter. Value must be between -10000 and 10000 mm.
            geoTo: Ending distance from the isocenter. Value must be between -10000 and 10000 mm.
        """
        ...



class DVHPoint:
    """
    Represents a value on a Dose Volume Histogram (DVH) curve.

    Attributes:
        DoseValue (DoseValue): The dose value of the point.
        Volume (float): The volume value of the point.
        VolumeUnit (str): The volume unit of the point.
    """
    # Constructs a DVHPoint.
    def __init__(self, dose: DoseValue, volume: float, volumeUnit: str) -> None:
        """
        Args:
            dose: Dose value of the point.
            volume: Volume value of the point.
            volumeUnit: Unit of volume.
        """
        ...


    DoseValue: DoseValue

    Volume: float

    VolumeUnit: str

    # This member is internal to the Eclipse Scripting API.
    def GetSchema(self) -> Xml.Schema.XmlSchema:
        ...


    # This member is internal to the Eclipse Scripting API.
    def ReadXml(self, reader: Xml.XmlReader) -> None:
        """
        Args:
            reader: XmlReader.
        """
        ...


    # Serialization support.
    def WriteXml(self, writer: Xml.XmlWriter) -> None:
        """
        Args:
            writer: The System.Xml.XmlWriter stream to which the object is serialized.
        """
        ...



class ExternalBeamMachineParameters:
    """
    The parameters for the external beam treatment unit.

    Attributes:
        MachineId (str): The treatment unit identifier.
        EnergyModeId (str): The energy mode identifier. For example, "6X", or "18X".
        DoseRate (int): Dose rate value.
        PrimaryFluenceModeId (str): Primary Fluence Mode identifier. Acceptable values are: null, empty string, "SRS","FFF".
        TechniqueId (str): Technique identifier. Typically "STATIC" or "ARC".
        MLCId (str): Optional MLC identifier. If null (which is the default) then the single MLC of the treatment unit is selected.
    """
    # Assigns the parameters to the properties for external beams.
    @overload
    def __init__(self, doseRate: str, energyModeId: str, machineId: int, primaryFluenceModeId: str, techniqueId: str) -> None:
        """
        Args:
            doseRate: Dose rate value.
            energyModeId: The energy mode identifier. For example, "6X", or "18X".
            machineId: The treatment unit identifier.
            primaryFluenceModeId: Primary Fluence Mode ID. Acceptable values are: null, empty string, "SRS","FFF".
            techniqueId: Technique identifier. Typically "STATIC" or "ARC".
        """
        ...


    # Assigns the Treatment Unit ID to the properties. Rest of the properties are left empty. These parameters will work for Halcyon machine when adding imaging setup or Fixed Sequence beam. For other types of beams, define all properties.
    @overload
    def __init__(self, machineId: str) -> None:
        """
        Args:
            machineId: The treatment unit identifier.
        """
        ...


    MachineId: str

    EnergyModeId: str

    DoseRate: int

    PrimaryFluenceModeId: str

    TechniqueId: str

    MLCId: str


class FitToStructureMarginType:
    """
    Margin type
    """
    def __init__(self) -> None: ...


class FitToStructureMargins:
    """
    Margins that are used when fitting a field device to a structure from the BEV perspective
    """
    # Constructs a new FitToStructureMargins instance with elliptical margin type.
    @overload
    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """
        Args:
            x1: Margin x1 in mm
            y1: Margin y1 in mm
            x2: Margin x2 in mm
            y2: Margin y2 in mm
        """
        ...


    # Constructs a new FitToStructureMargins instance with circular margin type.
    @overload
    def __init__(self, margin: float) -> None:
        """
        Args:
            margin: Uniform margin for all directions in mm
        """
        ...


    # A string that represents the current object.
    def ToString(self) -> str:
        ...



class Fluence:
    """
    Represents the fluence for a beam. The resolution in the fluence matrix is 2.5 mm in x and y directions. In the fluence matrix, x dimension is the number of columns, and y dimension is the number of rows.

    Attributes:
        MaxSizePixel (int): The maximum size of pixels for x or y dimension in the fluence.
        XSizePixel (int): The size of x dimension in pixels for the fluence. This corresponds to the number of columns in the pixels matrix.
        YSizePixel (int): The size of y dimension in pixels for the fluence. This corresponds to the number of rows in the pixels matrix.
        XSizeMM (float): The size of x dimension in mm for the fluence. The resolution is 2.5 mm in x and y directions.
        YSizeMM (float): The size of y dimension in mm for the fluence. The resolution is 2.5 mm in x and y directions.
        XOrigin (float): The x coordinate of the first pixel in a fluence map. The value is measured in millimeters from the field isocenter to the center of the first pixel. The coordinate axes are the same as in the IEC BEAM LIMITING DEVICE coordinate system.
        YOrigin (float): The y coordinate of the first pixel in a fluence map. The value is measured in millimeters from the field isocenter to the center of the first pixel. The coordinate axes are the same as in the IEC BEAM LIMITING DEVICE coordinate system.
        MLCId (str): The identifier of the MLC that is related to the fluence. The value can be empty or null.
    """
    # Constructor.
    @overload
    def __init__(self, fluenceMatrix: Array[float], xOrigin: float, yOrigin: float) -> None:
        """
        Args:
            fluenceMatrix: Contains the pixel values for the fluence. x dimension is the number of columns, and y dimension is the number of rows in the matrix. The minimum number of rows and columns is 2, and the maximum is 1024. For the optimal fluence of a beam, the values in the fluence matrix are floats, 4 bytes per pixel. The pixel values are determined as follows: fluence value 1 produces a dose of 1 Gy at the depth of 10 cm in a water phantom with a 10 x 10 cm open field. Correspondingly, fluence value 2 produces 2 Gy, fluence value 3 produces 3 Gy, etc. at the depth of 10 cm in a water phantom with a 10 x 10 cm open field. Pixel values are positive.
            xOrigin: The x coordinate of the first pixel in a fluence map. The value is measured in millimeters from the field isocenter to the center of the first pixel. The coordinate axes are the same as in the IEC BEAM LIMITING DEVICE coordinate system.
            yOrigin: The y coordinate of the first pixel in a fluence map. The value is measured in millimeters from the field isocenter to the center of the first pixel. The coordinate axes are the same as in the IEC BEAM LIMITING DEVICE coordinate system.
        """
        ...


    # Constructor.
    @overload
    def __init__(self, fluenceMatrix: Array[float], xOrigin: float, yOrigin: float, mlcId: str) -> None:
        """
        Args:
            fluenceMatrix: Contains the pixel values for the fluence. x dimension is the number of columns, and y dimension is the number of rows in the matrix. The minimum number of rows and columns is 2, and the maximum is 1024. The pixel values are determined as follows: fluence value 1 produces a dose of 1 Gy at the depth of 10 cm in a water phantom with a 10 x 10 cm open field. Correspondingly, fluence value 2 produces 2 Gy, fluence value 3 produces 3 Gy, etc. at the depth of 10 cm in a water phantom with a 10 x 10 cm open field. Pixel values are positive.
            xOrigin: The x coordinate of the first pixel in a fluence map. The value is measured in millimeters from the field isocenter to the center of the first pixel. The coordinate axes are the same as in the IEC BEAM LIMITING DEVICE coordinate system.
            yOrigin: The y coordinate of the first pixel in a fluence map. The value is measured in millimeters from the field isocenter to the center of the first pixel. The coordinate axes are the same as in the IEC BEAM LIMITING DEVICE coordinate system.
            mlcId: The identifier of the MLC that is related to the fluence. This parameter is optional. If the identifier is empty, the system tries to find the MLC from the treatment unit configuration. This happens when you call one of the
        """
        ...


    MaxSizePixel: int

    XSizePixel: int

    YSizePixel: int

    XSizeMM: float

    YSizeMM: float

    XOrigin: float

    YOrigin: float

    MLCId: str

    # Returns the fluence matrix.
    def GetPixels(self) -> Array[float]:
        ...



class ImagingBeamSetupParameters:
    """
    Setup parameters for imaging fields.

    Attributes:
        ImagingSetup (ImagingSetup): Identifier for the imaging setup.
        FitMarginX1 (float): Fit margin in x-direction in mm.
        FitMarginX2 (float): Fit margin in x-direction in mm.
        FitMarginY1 (float): Fit margin in y-direction in mm.
        FitMarginY2 (float): Fit margin in y-direction in mm.
        FieldSizeX (float): Field size in x-direction in mm.
        FieldSizeY (float): Field size in y-direction in mm.
    """
    # Constructor for imaging beam setup parameters.
    def __init__(self, imagingSetup: ImagingSetup, fitMarginX1_mm: float, fitMarginX2_mm: float, fitMarginY1_mm: float, fitMarginY2_mm: float, fieldSizeX_mm: float, fieldSizeY_mm: float) -> None:
        """
        Args:
            imagingSetup: Setup technique
            fitMarginX1_mm: Fit margin left side (in mm)
            fitMarginX2_mm: Fit margin right side (in mm)
            fitMarginY1_mm: Fit margin top (in mm)
            fitMarginY2_mm: Fit margin bottom (in mm)
            fieldSizeX_mm: Field size in x direction (in mm)
            fieldSizeY_mm: Field size in y direction (in mm)
        """
        ...


    ImagingSetup: ImagingSetup

    FitMarginX1: float

    FitMarginX2: float

    FitMarginY1: float

    FitMarginY2: float

    FieldSizeX: float

    FieldSizeY: float


class ProfilePoint:
    """
    Represents a point of a line profile.

    Attributes:
        Position (VVector): The position of the point.
        Value (float): The value of the point.
    """
    # Constructs a ProfilePoint.
    def __init__(self, position: VVector, value: float) -> None:
        """
        Args:
            position: Position of the point.
            value: Value of the point.
        """
        ...


    Position: VVector

    Value: float


class LineProfile:
    """
    Represents values along a line segment.

    Attributes:
        Count (int): The number of points in the profile.
    """
    # Constructs a LineProfile.
    def __init__(self, origin: VVector, step: VVector, data: Array[Double]) -> None:
        """
        Args:
            origin: Origin, i.e. position of first point of the profile.
            step: Step length and direction between points on the profile.
            data: Array of values of the profile.
        """
        ...


    Count: int

    # An enumerator for the points in the profile.
    def GetEnumerator(self) -> Iterable[ProfilePoint]:
        ...


    # A non-generic version of the enumerator for the points in the profile.
    def GetEnumerator(self) -> Iterable[ProfilePoint]:
        ...



class ImageProfile:
    """
    Represents an image line profile.

    Attributes:
        Unit (str): The unit of the points on the image profile.
    """
    # Constructs an ImageProfile.
    def __init__(self, origin: VVector, step: VVector, data: Array[Double], unit: str) -> None:
        """
        Args:
            origin: Origin, i.e. position of first point of the profile.
            step: Step length and direction between points on the profile.
            data: Array of values of the profile.
            unit: Unit of values in the profile.
        """
        ...


    Unit: str


class DoseProfile:
    """
    Represents a dose profile.

    Attributes:
        Unit (DoseValue+DoseUnit): The unit of the points on this dose profile.
    """
    # Constructs a DoseProfile.
    def __init__(self, origin: VVector, step: VVector, data: Array[Double], unit: DoseUnit) -> None:
        """
        Args:
            origin: Origin, i.e. position of first point of the profile.
            step: Step length and direction between points on the profile.
            data: Array of values of the profile.
            unit: Unit of values in the profile.
        """
        ...


    Unit: DoseValue+DoseUnit


class LMCVOptions:
    """
    Options for calculating leaf motions using the Varian Leaf Motion Calculator (LMCV) algorithm.

    Attributes:
        FixedJaws (bool): Use the Fixed jaws option.
    """
    # Constructor.
    def __init__(self, fixedJaws: bool) -> None:
        """
        Args:
            fixedJaws: Use the Fixed jaws option.
        """
        ...


    FixedJaws: bool


class SmartLMCOptions:
    """
    Options for calculating leaf motions using the Varian Smart LMC algorithm.

    Attributes:
        FixedFieldBorders (bool): Use the Fixed field borders option. See details in Eclipse Photon and Electron Algorithms Reference Guide.
        JawTracking (bool): Use the Jaw tracking option. See details in Eclipse Photon and Electron Algorithms Reference Guide.
    """
    # Constructor.
    def __init__(self, fixedFieldBorders: bool, jawTracking: bool) -> None:
        """
        Args:
            fixedFieldBorders: Use the Fixed field borders option. See details in Eclipse Photon and Electron Algorithms Reference Guide.
            jawTracking: Use the Jaw tracking option. See details in Eclipse Photon and Electron Algorithms Reference Guide.
        """
        ...


    FixedFieldBorders: bool

    JawTracking: bool


class LMCMSSOptions:
    """
    Options for calculating leaf motions using the non-Varian MSS Leaf Motion Calculator (LMCMSS) algorithm.

    Attributes:
        NumberOfIterations (int): The number of calculation iterations.
    """
    # Constructor.
    def __init__(self, numberOfIterations: int) -> None:
        """
        Args:
            numberOfIterations: The number of calculation iterations.
        """
        ...


    NumberOfIterations: int


class DosimeterUnit:
    """
    The dosimeter unit.
    """
    def __init__(self) -> None: ...


class MetersetValue:
    """
    Represents a meterset value.

    Attributes:
        Value (float): The value of this instance.
        Unit (DosimeterUnit): The unit of this instance.
    """
    # Constructs a MetersetValue.
    def __init__(self, value: float, unit: DosimeterUnit) -> None:
        """
        Args:
            value: Value for this instance.
            unit: Unit for this instance.
        """
        ...


    Value: float

    Unit: DosimeterUnit

    # This member is internal to the Eclipse Scripting API.
    def GetSchema(self) -> Xml.Schema.XmlSchema:
        ...


    # This member is internal to the Eclipse Scripting API.
    def ReadXml(self, reader: Xml.XmlReader) -> None:
        """
        Args:
            reader: XmlReader.
        """
        ...


    # Serialization support.
    def WriteXml(self, writer: Xml.XmlWriter) -> None:
        """
        Args:
            writer: The System.Xml.XmlWriter stream to which the object is serialized.
        """
        ...



class OptimizationAvoidanceSector:
    """
    Avoidance sector details.

    Attributes:
        StartAngle (float): Start angle.
        StopAngle (float): Stop angle.
        Valid (bool): Is Avoidance Sector valid.
        ValidationError (str): Validation error.
        IsDefined (bool): Is Avoidance Sector defined. True if either startAngle or stopAngle is defined.
    """
    # OptimizationAvoidanceSector constructor.
    @overload
    def __init__(self, startAngle: float, stopAngle: float) -> None:
        ...


    # OptimizationAvoidanceSector constructor.
    @overload
    def __init__(self, startAngle: float, stopAngle: float, isValid: bool, validationError: str) -> None:
        ...


    StartAngle: float

    StopAngle: float

    Valid: bool

    ValidationError: str

    IsDefined: bool


class OptimizationOptionsBase:
    """
    Abstract base class for IMRT and VMAT optimization options.

    Attributes:
        MLC (str): Identifier for the Multileaf Collimator (MLC). This can be left empty if there is exactly one MLC configured.
        StartOption (OptimizationOption): The state at the beginning of the optimization.
        IntermediateDoseOption (OptimizationIntermediateDoseOption): Use of intermediate dose in optimization.
    """
    def __init__(self) -> None: ...

    MLC: str

    StartOption: OptimizationOption

    IntermediateDoseOption: OptimizationIntermediateDoseOption


class OptimizationOptionsIMPT:
    """
    Options for IMPT optimization.

    Attributes:
        MaximumNumberOfIterations (int): Maximum number of iterations for the IMPT optimizer.
    """
    # Specify the initial state at the beginning of optimization. The calculation terminates upon convergence before the maximum number of iterations is reached or the maximum time has elapsed.
    def __init__(self, maxIterations: int, initialState: OptimizationOption) -> None:
        """
        Args:
            maxIterations: Maximum number of iterations for IMRT optimization.
            initialState: Initial state at the beginning of optimization.
        """
        ...


    MaximumNumberOfIterations: int


class OptimizationOptionsIMRT:
    """
    Options for IMRT optimization.

    Attributes:
        ConvergenceOption (OptimizationConvergenceOption): Terminate the optimization early if it is converged.
        NumberOfStepsBeforeIntermediateDose (int): Number of steps before the intermediate dose is calculated.
        MaximumNumberOfIterations (int): Maximum number of iterations for the IMRT optimizer.
    """
    # Specify the initial state at the beginning of optimization and use intermediate dose after a specified number of iterations. The user specifies if the calculation terminates upon convergence before the maximum number of iterations is reached. If the intermediate dose is selected, the intermediate dose is calculated at least once. The subsequent cycles may be terminated early if the iteration has been converged.
    @overload
    def __init__(self, maxIterations: int, initialState: OptimizationOption, numberOfStepsBeforeIntermediateDose: int, convergenceOption: OptimizationConvergenceOption, mlcId: str) -> None:
        """
        Args:
            maxIterations: Maximum number of iterations for IMRT optimization.
            initialState: Initial state at the beginning of optimization.
            numberOfStepsBeforeIntermediateDose: Number of steps before the intermediate dose is calculated.
            convergenceOption: Option to terminate optimization early if the iteration is converged.
            mlcId: Identifier for the Multileaf Collimator (MLC).
        """
        ...


    # Specify the initial state at the beginning of optimization and use intermediate dose after a specified number of iterations. The user specifies if the calculation terminates upon convergence before the maximum number of iterations is reached. If the intermediate dose is selected, the intermediate dose is calculated once after which the optimization is restarted. This option is the same as the "Automatic Intermediate Dose" option in External Beam Planning.
    @overload
    def __init__(self, maxIterations: int, initialState: OptimizationOption, convergenceOption: OptimizationConvergenceOption, intermediateDoseOption: OptimizationIntermediateDoseOption, mlcId: str) -> None:
        """
        Args:
            maxIterations: Maximum number of iterations for IMRT optimization.
            initialState: Initial state at the beginning of optimization.
            convergenceOption: Option to terminate optimization early if the iteration is converged.
            intermediateDoseOption: Specify if intermediate dose is calculated.
            mlcId: Identifier for the Multileaf Collimator (MLC).
        """
        ...


    # Specify the initial state before optimization and whether the algorithm can terminate early if the iteration has already been converged. No intermediate dose is used in the optimization.
    @overload
    def __init__(self, maxIterations: int, initialState: OptimizationOption, convergenceOption: OptimizationConvergenceOption, mlcId: str) -> None:
        """
        Args:
            maxIterations: Maximum number of iterations for IMRT optimization.
            initialState: Initial state at the beginning of optimization.
            convergenceOption: Option to terminate optimization early if the iteration is converged.
            mlcId: Identifier for the Multileaf Collimator (MLC).
        """
        ...


    ConvergenceOption: OptimizationConvergenceOption

    NumberOfStepsBeforeIntermediateDose: int

    MaximumNumberOfIterations: int


class OptimizationOptionsVMAT:
    """
    Options for VMAT optimization.

    Attributes:
        NumberOfOptimizationCycles (int): Number of VMAT optimization cycles.
    """
    # Perform VMAT optimization using a specific starting condition.
    @overload
    def __init__(self, startOption: OptimizationOption, mlcId: str) -> None:
        """
        Args:
            startOption: Initial state for the optimizer.
            mlcId: Identifier for the Multileaf Collimator (MLC).
        """
        ...


    # Perform a single cycle of VMAT optimization. Intermediate dose is optionally calculated after multi-resolution level 3.
    @overload
    def __init__(self, intermediateDoseOption: OptimizationIntermediateDoseOption, mlcId: str) -> None:
        """
        Args:
            intermediateDoseOption: Intermediate dose option.
            mlcId: Identifier for the Multileaf Collimator (MLC).
        """
        ...


    # Perform a user-specified number of VMAT optimization cycles. During the first round, the intermediate dose is calculated after multi-resolution level 3, and the optimization re-starts at multi-resolution level 4. The subsequent rounds calculate first the intermediate dose and start the optimization from multi-resolution level 4.
    @overload
    def __init__(self, numberOfCycles: int, mlcId: str) -> None:
        """
        Args:
            numberOfCycles: Number of VMAT optimization cycles.
            mlcId: Identifier for the Multileaf Collimator (MLC).
        """
        ...


    # For the internal use of the Eclipse Scripting API.
    @overload
    def __init__(self, startOption: OptimizationOption, mlcId: OptimizationIntermediateDoseOption, param3: int, param4: str) -> None:
        ...


    # Copy Constructor.
    @overload
    def __init__(self, options: OptimizationOptionsVMAT) -> None:
        """
        Args:
            options: An options object that is copied.
        """
        ...


    NumberOfOptimizationCycles: int


class PlanValidationResult:
    """
    Represents plan validatation result

    Attributes:
        InfoCount (int): The info count of this instance.
        WarningCount (int): The warning count of this instance.
        ErrorCount (int): The error count of this instance.
        Details (Collections.Generic.ICollection[PlanValidationResultDetail]): The validation details of this instance.
        StringPresentation (str): String representation of this instance.
    """
    # Constructs empty PlanValidationResult.
    @overload
    def __init__(self) -> None:
        ...


    # Constructs a PlanValidationResult.
    @overload
    def __init__(self, details: Collections.Generic.ICollection[PlanValidationResultDetail]) -> None:
        """
        Args:
            details: Collection of validation details.
        """
        ...


    InfoCount: int

    WarningCount: int

    ErrorCount: int

    Details: Collections.Generic.ICollection[PlanValidationResultDetail]

    StringPresentation: str

    # Add validation detail to this instance.
    def Add(self, detail: PlanValidationResultDetail) -> None:
        """
        Args:
            detail: New validation detail.
        """
        ...


    # Add validation component to this instance.
    def Add(self, componentResult: PlanValidationResult) -> None:
        """
        Args:
            componentResult: Plan validation result component.
        """
        ...



class PlanValidationResultDetail:
    """
    Represents plan validation detail.

    Attributes:
        Plan (str): Identifies the plan of this instance.
        MessageForUser (str): Localized message for user of this instance.
        Classification (PlanValidationResultDetail+ResultClassification): Result classification of this instance.
        Code (str): Unique validation detail code of this instance.
        StringPresentation (str): String representation of this instance.
    """
    # Constructs PlanValidationDetail.
    def __init__(self, plan: str, messageForUser: str, classification: ResultClassification, code: str) -> None:
        """
        Args:
            plan: Identifies plan.
            messageForUser: Localized message for user.
            classification: Class of validation detail.
            code: Unique validation detail code.
        """
        ...


    Plan: str

    MessageForUser: str

    Classification: PlanValidationResultDetail+ResultClassification

    Code: str

    StringPresentation: str

    # Result classification (static).
    def GetClassification(self, detail: PlanValidationResultDetail) -> PlanValidationResultDetail+ResultClassification:
        ...



class PlanValidationResultEsapiDetail:
    """
    A class for detailed plan validation result

    Attributes:
        MessageForUser (str): Message for the user about the validation result detail.
        Code (str): Detail code.
        IsError (bool): Check if the result is a error (true) or a warning (false).
    """
    # Constructor for PlanValidationResultEsapiDetail class.
    def __init__(self, messageForUser: str, isError: bool, code: str) -> None:
        """
        Args:
            messageForUser: Message for the user.
            isError: Is this reported as a error or as a warning.
            code: Result code.
        """
        ...


    MessageForUser: str

    Code: str

    IsError: bool


class ProtonBeamMachineParameters:
    """
    The parameters for the proton beam treatment unit.

    Attributes:
        MachineId (str): The treatment unit identifier.
        TechniqueId (str): Technique identifier. For example, "MODULAT_SCANNING", or "UNIFORM_SCANNING".
        ToleranceId (str): Tolerance identifier.
    """
    # Assigns the parameters to the properties for proton beams.
    def __init__(self, machineId: str, techniqueId: str, toleranceId: str) -> None:
        """
        Args:
            machineId: The treatment unit identifier.
            techniqueId: Technique identifier. "MODULAT_SCANNING" or "UNIFORM_SCANNING" for proton beams.
            toleranceId: Tolerance identifier.
        """
        ...


    MachineId: str

    TechniqueId: str

    ToleranceId: str


class IonPlanNormalizationParameters:
    """
    The parameters for proton plan normalization.

    Attributes:
        NormalizationMode (PlanNormalizationMode): Normalization mode.
        NormalizationValue (float): The treatment unit identifier.
        VolumePercentage (float): Volume percentage factor.
    """
    # Plan normalization parameters for user-defined target volume percentage and plan normalization value. For more information refer to the plan normalization options in the Eclipse Proton Reference Guide.
    @overload
    def __init__(self, normalizationMode: PlanNormalizationMode, normalizationValue: float, volumePercentage: float) -> None:
        ...


    # Plan normalization parameters user-defined plan normalization value. For more information refer to the plan normalization options in the Eclipse Proton Reference Guide.
    @overload
    def __init__(self, normalizationMode: PlanNormalizationMode, normalizationValue: float) -> None:
        ...


    # Plan normalization parameters for normalizing the maximum, mean, minimum dose of the target volume to 100%, or to no normalization. For more information refer to the plan normalization options in the Eclipse Proton Reference Guide.
    @overload
    def __init__(self, normalizationMode: PlanNormalizationMode) -> None:
        ...


    NormalizationMode: PlanNormalizationMode

    NormalizationValue: float

    VolumePercentage: float


class RailPosition:
    """
    Setting for the moveable rail position (in or out) used for couch modeling in Eclipse.
    """
    def __init__(self) -> None: ...


class SegmentProfilePoint:
    """
    Represents a point of a segment profile.

    Attributes:
        Position (VVector): The position of the point.
        Value (bool): The value of the point: true if the point is inside the segment, false otherwise.
    """
    # Constructs a SegmentProfilePoint.
    def __init__(self, position: VVector, value: bool) -> None:
        """
        Args:
            position: Position of the point.
            value: Value of the point.
        """
        ...


    Position: VVector

    Value: bool


class SegmentProfile:
    """
    Represents the segment values along a line segment.

    Attributes:
        Count (int): The number of points in the profile.
        EdgeCoordinates (List[VVector]): Returns the coordinates of the edges of the segment along the segment profile.
    """
    # Constructs a SegmentProfile.
    def __init__(self, origin: VVector, step: VVector, data: Collections.BitArray) -> None:
        """
        Args:
            origin: Origin, i.e. position of first point of the profile.
            step: Step length and direction between points on the profile.
            data: Array of values of the profile.
        """
        ...


    Count: int

    EdgeCoordinates: List[VVector]

    # An enumerator for points in the profile.
    def GetEnumerator(self) -> Iterable[SegmentProfilePoint]:
        ...


    # A non-generic version of the enumerator for points in the profile.
    def GetEnumerator(self) -> Iterable[SegmentProfilePoint]:
        ...



class LogSeverity:
    """
    The enumeration of log severities.
    """
    def __init__(self) -> None: ...


class PlanType:
    """
    The enumeration of plan types.
    """
    def __init__(self) -> None: ...


class MLCPlanType:
    """
    The enumeration of Multileaf Collimator (MLC) techniques.
    """
    def __init__(self) -> None: ...


class PlanSetupApprovalStatus:
    """
    The enumeration of plan approval statuses.
    """
    def __init__(self) -> None: ...


class StructureApprovalStatus:
    """
    The enumeration of structure approval statuses.
    """
    def __init__(self) -> None: ...


class ProtonDeliveryTimeStatus:
    """
    The enumeration of proton delivery time statuses.
    """
    def __init__(self) -> None: ...


class ImageApprovalStatus:
    """
    The enumeration of image approval statuses.
    """
    def __init__(self) -> None: ...


class PlanSumOperation:
    """
    PlanSum operation for PlanSetups in PlanSum. Indicates whether the plan is summed with (“+”) or subtracted from (“-”) the other plans in the sum.
    """
    def __init__(self) -> None: ...


class DoseValuePresentation:
    """
    Types of presentation for dose values.
    """
    def __init__(self) -> None: ...


class VolumePresentation:
    """
    Types of presentation for volume values.
    """
    def __init__(self) -> None: ...


class PatientOrientation:
    """
    The enumeration of patient orientations.
    """
    def __init__(self) -> None: ...


class SeriesModality:
    """
    The enumeration of series modalities.
    """
    def __init__(self) -> None: ...


class BeamTechnique:
    """
    An enumeration of beam techniques.
    """
    def __init__(self) -> None: ...


class SetupTechnique:
    """
    The enumeration of setup techniques for a beam.
    """
    def __init__(self) -> None: ...


class GantryDirection:
    """
    The enumeration of gantry rotation directions.
    """
    def __init__(self) -> None: ...


class ImagingSetup:
    """
    Set of available imaging setups.
    """
    def __init__(self) -> None: ...


class BlockType:
    """
    A type flag that tells whether a block is an aperture block or a shielding block. An aperture block is used to limit the radiated area while a shielding block is made to protect a sensitive organ.
    """
    def __init__(self) -> None: ...


class CalculationType:
    """
    Calculation type.
    """
    def __init__(self) -> None: ...


class OptimizationObjectiveOperator:
    """
    Optimization Objective Operator, which is used for setting the upper and lower optimization objectives.
    """
    def __init__(self) -> None: ...


class OptimizationOption:
    """
    Options for Optimization.
    """
    def __init__(self) -> None: ...


class OptimizationIntermediateDoseOption:
    """
    Options for using intermediate dose in optimization.
    """
    def __init__(self) -> None: ...


class OptimizationConvergenceOption:
    """
    Options for terminating optimization upon convergence.
    """
    def __init__(self) -> None: ...


class DVHEstimateType:
    """
    Represents the type of a DVH estimate curve
    """
    def __init__(self) -> None: ...


class PlanUncertaintyType:
    """
    Plan uncertainty type indicates the usage of associated uncertainty parameters, see
    """
    def __init__(self) -> None: ...


class IonBeamScanMode:
    """
    The method of beam scanning to be used during treatment. Used with IonBeams.
    """
    def __init__(self) -> None: ...


class RangeShifterType:
    """
    Type of the range shifter.
    """
    def __init__(self) -> None: ...


class LateralSpreadingDeviceType:
    """
    Type of the lateral spreading device.
    """
    def __init__(self) -> None: ...


class PlanNormalizationMode:
    """
    Plan normalization options for SetPlanNormalization
    """
    def __init__(self) -> None: ...


class IonPlanOptimizationMode:
    """
    Proton plan optimization mode.
    """
    def __init__(self) -> None: ...


class RangeModulatorType:
    """
    Type of the range modulator.
    """
    def __init__(self) -> None: ...


class PatientSupportType:
    """
    Patient support type.
    """
    def __init__(self) -> None: ...


class ApplicationScriptType:
    """
    The type of the application script.
    """
    def __init__(self) -> None: ...


class ApplicationScriptApprovalStatus:
    """
    The approval statuses of the application script.
    """
    def __init__(self) -> None: ...


class RTPrescriptionTargetType:
    """
    The type of the prescription target definition
    """
    def __init__(self) -> None: ...


class RTPrescriptionConstraintType:
    """
    Type of the RT prescription constraint.
    """
    def __init__(self) -> None: ...


class PrescriptionType:
    """
    Enumeration of prescription types.
    """
    def __init__(self) -> None: ...


class PrescriptionModifier:
    """
    Prescription modifier.
    """
    def __init__(self) -> None: ...


class MeasureType:
    """
    Enumeration of plan measure types.
    """
    def __init__(self) -> None: ...


class MeasureModifier:
    """
    Measure modifier
    """
    def __init__(self) -> None: ...


class RegistrationApprovalStatus:
    """
    The enumeration of registration approval statuses.
    """
    def __init__(self) -> None: ...


class ApprovalHistoryEntry:
    """
    An entry in the plan approval history.
    """
    def __init__(self) -> None: ...


class StructureApprovalHistoryEntry:
    """
    An entry in the structure approval history.
    """
    def __init__(self) -> None: ...


class ImageApprovalHistoryEntry:
    """
    An entry in the image approval history.
    """
    def __init__(self) -> None: ...


class OpenLeavesMeetingPoint:
    """
    Specifies where the open MLC leaves meet the structure outline in an MLC leaf fit operation.
    """
    def __init__(self) -> None: ...


class ClosedLeavesMeetingPoint:
    """
    Specifies where the closed MLC leaf pairs are parked in an MLC leaf fit operation. Bank_One: Varian = B, IEC MLCX = X1, IEC MLCY = Y1; Bank_Two: Varian = A, IEC MLCX = X2, IEC MLCY = Y2
    """
    def __init__(self) -> None: ...


class JawFitting:
    """
    Specifies where collimator jaws are positioned in an MLC leaf fit operation.
    """
    def __init__(self) -> None: ...


class RendererStrings:
    """
    """
    def __init__(self) -> None: ...


class TreatmentSessionStatus:
    """
    Status of the treatment session.
    """
    def __init__(self) -> None: ...


class GoalPriority:
    """
    Clinical Goal Priority
    """
    def __init__(self) -> None: ...


class GoalEvalResult:
    """
    Clinical Goal Evaluation Result
    """
    def __init__(self) -> None: ...


class DVHEstimationStructureType:
    """
    Structure type as defined in Planning Model Library: PTV or OAR
    """
    def __init__(self) -> None: ...


class ParticleType:
    """
    Particle types
    """
    def __init__(self) -> None: ...


class ProtonBeamLineStatus:
    """
    Status of proton beam line
    """
    def __init__(self) -> None: ...


class CourseClinicalStatus:
    """
    Clinical Status of Course
    """
    def __init__(self) -> None: ...


class ResetSourcePositionsResult:
    """
    Return value for
    """
    def __init__(self) -> None: ...


class SetSourcePositionsResult:
    """
    Return value for
    """
    def __init__(self) -> None: ...


class BrachyTreatmentTechniqueType:
    """
    The enumeration of Brachytherapy treatment techniques.
    """
    def __init__(self) -> None: ...


class StructureCodeInfo:
    """
    Represents structure code information.

    Attributes:
        CodingScheme (str): The coding scheme of the structure code.
        Code (str): The structure code as defined in the associated coding scheme.
    """
    # Constructs a StructureCodeInfo.
    def __init__(self, codingScheme: str, code: str) -> None:
        """
        Args:
            codingScheme: The coding scheme of the structure code.
            code: The structure code as defined in the associated coding scheme.
        """
        ...


    CodingScheme: str

    Code: str

    # A string that represents the current object.
    def ToString(self) -> str:
        ...


    # Checks if this object is equal to another object.
    def Equals(self, obj: Any) -> bool:
        """
        Args:
            obj: The other object to compare.
        """
        ...


    # Returns the hash code for this instance. Overrides Object.GetHashCode.
    def GetHashCode(self) -> int:
        ...


    # Equality operator for StructureCodeInfo.
    def op_Equality(self, left: StructureCodeInfo, right: StructureCodeInfo) -> bool:
        """
        Args:
            left: The first object to compare.
            right: The second object to compare.
        """
        ...


    # Inequality operator for StructureCodeInfo.
    def op_Inequality(self, left: StructureCodeInfo, right: StructureCodeInfo) -> bool:
        """
        Args:
            left: The first object to compare.
            right: The second object to compare.
        """
        ...


    # Indicates whether the current object is equal to another object of the same type.
    def Equals(self, other: StructureCodeInfo) -> bool:
        """
        Args:
            other: An object to compare with this object.
        """
        ...


    # This member is internal to the Eclipse Scripting API.
    def GetSchema(self) -> Xml.Schema.XmlSchema:
        ...


    # This member is internal to the Eclipse Scripting API.
    def ReadXml(self, reader: Xml.XmlReader) -> None:
        """
        Args:
            reader: The XmlReader stream from which the object is deserialized.
        """
        ...


    # Serialization support.
    def WriteXml(self, writer: Xml.XmlWriter) -> None:
        """
        Args:
            writer: The System.Xml.XmlWriter stream to which the object is serialized.
        """
        ...



class UserIdentity:
    """
    Represents the identity of an user, including the identifier (username) and the display name.
    """
    # Creates a new UserIdentity value.
    def __init__(self, id: str, displayName: str) -> None:
        """
        Args:
            id: The user identifier including the domain name, such as 'domain\user'.
            displayName: The display name of the user.
        """
        ...



class ValidationException:
    """
    ValidationException.
    """
    # Exception thrown when data validation fails.
    def __init__(self, reason: str) -> None:
        """
        Args:
            reason: A message that describes the failure.
        """
        ...



class VRect[T](Generic[T]):
    """
    Represents a rectangle.

    Attributes:
        X1 (T): The X1-coordinate of the rectangle.
        Y1 (T): The Y1-coordinate of the rectangle.
        X2 (T): The X2-coordinate of the rectangle.
        Y2 (T): The Y2-coordinate of the rectangle.

    Note:
        Currently limited to value types.
    """
    # Constructs a VRect.
    def __init__(self, x1: T, y1: T, x2: T, y2: T) -> None:
        """
        Args:
            x1: X1 coordinate of the rectangle.
            y1: Y1 coordinate of the rectangle.
            x2: X2 coordinate of the rectangle.
            y2: Y2 coordinate of the rectangle.
        """
        ...


    X1: T

    Y1: T

    X2: T

    Y2: T

    # A string that represents the current object.
    def ToString(self) -> str:
        ...


    # Checks if this object is equal to another object.
    def Equals(self, obj: Any) -> bool:
        """
        Args:
            obj: The other object to compare.
        """
        ...


    # Checks if this object is equal to another VRect object.
    def Equals(self, other: VRect[T]) -> bool:
        """
        Args:
            other: The other object to compare.
        """
        ...


    # Equality operator for VRect.
    def op_Equality(self, a: VRect[T], b: VRect[T]) -> bool:
        """
        Args:
            a: The first object to compare.
            b: The second object to compare.
        """
        ...


    # Inequality operator for VRect.
    def op_Inequality(self, a: VRect[T], b: VRect[T]) -> bool:
        """
        Args:
            a: The first object to compare.
            b: The second object to compare.
        """
        ...


    # Returns the hash code for this instance. Overrides Object.GetHashCode.
    def GetHashCode(self) -> int:
        ...



class VVector:
    """
    Represents a displacement in 3D space.

    Attributes:
        LengthSquared (float): The square of the length of the VVector.
        Length (float): The length of the VVector.
        x (float): The X component of the VVector.
        y (float): The Y component of the VVector.
        z (float): The Z component of the VVector.
    """
    # Constructs a VVector.
    def __init__(self, xi: float, yi: float, zi: float) -> None:
        """
        Args:
            xi: X component.
            yi: Y component.
            zi: Z component.
        """
        ...


    LengthSquared: float

    Length: float

    x: float

    y: float

    z: float

    # Updating VVector component value using VectorComponent indexing.
    def Update(self, vc: Component, value: float) -> VVector:
        """
        Args:
            vc: Component enum that correspond to x,y and z components.
            value: Value of 0,1 or 2 that correspond to x,y and z components.
        """
        ...


    # The distance between the locations represented by the given VVectors.
    def Distance(self, left: VVector, right: VVector) -> float:
        """
        Args:
            left: First operand.
            right: Second operand
        """
        ...


    # Scales this VVector so that its length becomes equal to unity.
    def ScaleToUnitLength(self) -> None:
        ...


    # Scales this VVector so that its length becomes equal to unity.
    def GetUnitLengthScaledVector(self) -> VVector:
        ...


    # The scalar product of this VVector and the given VVector.
    def ScalarProduct(self, left: VVector) -> float:
        """
        Args:
            left: VVector that is second operand of the scalar product.
        """
        ...


    # The subtraction of VVectors.
    def op_Subtraction(self, left: VVector, right: VVector) -> VVector:
        """
        Args:
            left: First operand.
            right: Second operand.
        """
        ...


    # The addition of VVectors.
    def op_Addition(self, left: VVector, right: VVector) -> VVector:
        """
        Args:
            left: First operand.
            right: Second operand.
        """
        ...


    # The multiplication of a VVector and a double.
    def op_Multiply(self, val: VVector, mul: float) -> VVector:
        """
        Args:
            val: VVector to multiply.
            mul: Multiplier.
        """
        ...


    # The multiplication of a VVector and a double.
    def op_Multiply(self, val: float, mul: VVector) -> VVector:
        """
        Args:
            val: VVector to multiply.
            mul: Multiplier.
        """
        ...


    # The division of a VVector by a double.
    def op_Division(self, val: VVector, div: float) -> VVector:
        """
        Args:
            val: VVector to divide.
            div: Divisor.
        """
        ...


    # Equality comparison of VVector and Object. This method considers two instances of VVector.Undefined to be equal to each other. Otherwise, a vector is equal to an object only if the object is a VVector and vectors are equal. For epsilon-equal comparison, use
    def Equals(self, obj: Any) -> bool:
        """
        Args:
            obj: Object to compare this to.
        """
        ...


    # Equality comparison of vectors. This method considers two instances of VVector.Undefined to be equal to each other. Otherwise, two vectors are equal only if the vectors components are equal. a == b, b == c, => a has to be equal to c. Epsilon equality comparison does not fulfill this condition with epsilon > 0.0. For epsilon-equal comparison, use
    def Equals(self, other: VVector) -> bool:
        """
        Args:
            other: vector to compare this to.
        """
        ...


    # Epsilon-equality comparison of vectors. This method considers two instances of VVector.Undefined to be equal to each other. Otherwise, two vectors are equal only if the vectors components are within epsilon.
    def EpsilonEqual(self, other: VVector, epsilon: float) -> bool:
        """
        Args:
            other: Vector to compare this to.
            epsilon: Epsilon to use for the vector component comparison.
        """
        ...


    # Returns true if at least one of this vector components are equal to double.IsNaN or double.IsInfinity, false otherwise.
    def IsUndefined(self) -> bool:
        ...


    # A hash code for the current object.
    def GetHashCode(self) -> int:
        ...


    # Equality operator for vectors. This method considers two instances of VVector.Undefined to be equal to each other. Otherwise, two vectors are equal only if the vectors components are equal. For epsilon-equal comparison, use
    def op_Equality(self, vv1: VVector, vv2: VVector) -> bool:
        """
        Args:
            vv1: First operand.
            vv2: Second operand.
        """
        ...


    # Inequality operator for vectors. This method considers two instances of VVector.Undefined to be equal to each other. This operator considers two instances of vectors with undefined components to be inequal. For epsilon-equal comparison, use
    def op_Inequality(self, vv1: VVector, vv2: VVector) -> bool:
        """
        Args:
            vv1: First operand.
            vv2: Second operand.
        """
        ...



