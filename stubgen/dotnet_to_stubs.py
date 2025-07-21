#!/usr/bin/env python3
"""
XML Documentation to Python Stub Generator
Generates Python type stubs (.pyi) from .NET XML documentation files

Usage:
    python dotnet_to_stubs.py <library_folder> [output_folder]
    
Arguments:
    library_folder: Folder containing XML documentation and DLL files (will be searched recursively)
    output_folder: Output folder for generated stubs (default: stubs)

Example:
    python dotnet_to_stubs.py "C:\Program Files\Varian\RTM\18.0\esapi\API" stubs
"""

import os
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

try:
    import clr
    import System
    HAS_PYTHONNET = True
except ImportError:
    HAS_PYTHONNET = False
    print("Warning: pythonnet not available. Type introspection will be limited.")

def detect_pythonnet_conversions() -> Dict[str, str]:
    """
    Detect which .NET types pythonnet automatically converts to Python types.
    Returns a mapping of .NET type names to their Python equivalents.
    """
    if not HAS_PYTHONNET:
        return {}
    
    conversions = {}
    
    # Test basic types by creating instances and checking their Python types
    test_cases = [
        ('System.String', 'hello'),
        ('System.Boolean', True),
        ('System.Int32', 42),
        ('System.Int64', 42),
        ('System.Double', 3.14),
        ('System.Single', 3.14),
        ('System.Byte', 255),
    ]
    
    for net_type_name, test_value in test_cases:
        try:
            # Get the .NET type
            net_type = getattr(System, net_type_name.replace('System.', ''))
            
            # Create an instance (this may get converted by pythonnet)
            if net_type_name == 'System.String':
                instance = System.String(test_value)
            else:
                instance = net_type(test_value)
            
            # Check what Python type we actually get
            python_type = type(instance)
            
            if python_type == str:
                conversions[net_type_name] = 'str'
            elif python_type == bool:
                conversions[net_type_name] = 'bool'
            elif python_type == int:
                conversions[net_type_name] = 'int'
            elif python_type == float:
                conversions[net_type_name] = 'float'
            else:
                # If it's still a .NET type, don't convert it in stubs
                print(f"Type {net_type_name} remains as .NET type: {python_type}")
                
        except Exception as e:
            print(f"Could not test {net_type_name}: {e}")
    
    return conversions

# Type mappings from C# to Python
TYPE_MAPPINGS = {
    'System.String': 'str',
    'string': 'str',
    'String': 'str',
    'System.Int32': 'int',
    'int': 'int',
    'Int32': 'int',
    'System.Double': 'float',
    'double': 'float',
    'Double': 'Double',  # Keep as .NET type for array handling
    'System.Single': 'float', 
    'single': 'float',
    'Single': 'Single',  # Keep as .NET type for array handling
    'System.Boolean': 'bool',
    'bool': 'bool',
    'Boolean': 'Boolean',  # Keep as .NET type for array handling
    'void': 'None',
    'System.Void': 'None',
    'object': 'Any',
    'System.Object': 'Any',
    'Object': 'Any',
    'System.DateTime': 'datetime',
    'DateTime': 'datetime',
    'System.Collections.Generic.IEnumerable': 'List',
    'IEnumerable': 'List',
    'System.Collections.Generic.ICollection': 'List',
    'ICollection': 'List',
    'System.Collections.Generic.List': 'List',
    'List': 'List',
    'System.Array': 'Array',
    'Array': 'Array',
}

class DllTypeIntrospector:
    """Uses pythonnet to introspect DLL types for accurate type information"""
    
    def __init__(self, dll_paths: List[str] = None):
        self.dll_paths = dll_paths or []
        self.loaded_assemblies = {}
        self.type_cache = {}
        self.method_cache = {}
        
        # Detect what pythonnet actually converts
        self.pythonnet_conversions = detect_pythonnet_conversions() if HAS_PYTHONNET else {}
        
        if HAS_PYTHONNET:
            self._load_dlls()
    
    def _load_dlls(self):
        """Load DLLs using pythonnet"""
        if not HAS_PYTHONNET:
            return
        
        for dll_path in self.dll_paths:
            try:
                clr.AddReference(str(dll_path))
                print(f"Loaded DLL: {dll_path}")
            except Exception as e:
                print(f"Failed to load {dll_path}: {e}")
                continue
    
    def get_method_signature(self, class_full_name: str, method_name: str) -> Optional[Dict]:
        """Get method signature information from the DLL"""
        if not HAS_PYTHONNET:
            return None
        
        cache_key = f"{class_full_name}.{method_name}"
        if cache_key in self.method_cache:
            return self.method_cache[cache_key]
        
        try:
            # Try to import the type directly using pythonnet
            namespace_parts = class_full_name.split('.')
            if len(namespace_parts) < 2:
                return None
            
            module_name = '.'.join(namespace_parts[:-1])
            class_name = namespace_parts[-1]
            
            # Import the namespace module
            exec(f"import {module_name}")
            namespace_module = eval(module_name)
            
            if not hasattr(namespace_module, class_name):
                self.method_cache[cache_key] = None
                return None
            
            type_obj = getattr(namespace_module, class_name)
            clr_type = clr.GetClrType(type_obj)
            
            if not clr_type:
                self.method_cache[cache_key] = None
                return None
            
            signature = {
                'parameters': [],
                'return_type': 'Any'
            }
            
            if method_name == '__init__':
                # Get constructors
                constructors = clr_type.GetConstructors()
                constructor_sigs = []
                
                for ctor in constructors:
                    ctor_sig = {
                        'parameters': [],
                        'return_type': 'None'
                    }
                    
                    parameters = ctor.GetParameters()
                    for param in parameters:
                        param_type = self._convert_net_type_to_python(param.ParameterType)
                        ctor_sig['parameters'].append({
                            'name': param.Name,
                            'type': param_type
                        })
                    
                    constructor_sigs.append(ctor_sig)
                
                result = {'constructors': constructor_sigs}
                self.method_cache[cache_key] = result
                return result
            else:
                # Get regular methods
                methods = clr_type.GetMethods()
                for method in methods:
                    if method.Name == method_name:
                        parameters = method.GetParameters()
                        for param in parameters:
                            param_type = self._convert_net_type_to_python(param.ParameterType)
                            signature['parameters'].append({
                                'name': param.Name,
                                'type': param_type
                            })
                        
                        # Get return type
                        return_type = self._convert_net_type_to_python(method.ReturnType)
                        signature['return_type'] = return_type
                        
                        self.method_cache[cache_key] = signature
                        return signature
        
        except Exception as e:
            # Silently fail for now - we'll use XML fallback
            pass
        
        self.method_cache[cache_key] = None
        return None
    
    def _extract_method_signature(self, method_info) -> Optional[Dict]:
        """Extract signature information from a method object"""
        try:
            signature = {
                'parameters': [],
                'return_type': 'Any'
            }
            
            # Try to get parameter information
            if hasattr(method_info, '__annotations__'):
                annotations = method_info.__annotations__
                for param_name, param_type in annotations.items():
                    if param_name != 'return':
                        signature['parameters'].append({
                            'name': param_name,
                            'type': self._convert_net_type_to_python(param_type)
                        })
                
                if 'return' in annotations:
                    signature['return_type'] = self._convert_net_type_to_python(annotations['return'])
            
            # Try to get from .NET reflection if available
            if hasattr(method_info, 'GetParameters'):
                params = method_info.GetParameters()
                signature['parameters'] = []
                for param in params:
                    signature['parameters'].append({
                        'name': param.Name,
                        'type': self._convert_net_type_to_python(param.ParameterType)
                    })
                
                if hasattr(method_info, 'ReturnType'):
                    signature['return_type'] = self._convert_net_type_to_python(method_info.ReturnType)
            
            return signature
            
        except Exception:
            return None
    
    def _convert_net_type_to_python(self, net_type) -> str:
        """Convert .NET type to Python type string"""
        if net_type is None:
            return 'Any'
        
        # Get the full type name
        if hasattr(net_type, 'FullName') and net_type.FullName:
            type_name = net_type.FullName
        elif hasattr(net_type, 'Name') and net_type.Name:
            type_name = net_type.Name
        else:
            type_name = str(net_type)
        
        # First, check if pythonnet automatically converts this type
        if type_name in self.pythonnet_conversions:
            return self.pythonnet_conversions[type_name]
        
        # Handle types that we know pythonnet converts (fallback if detection failed)
        known_conversions = {
            # Basic types that pythonnet typically converts
            'System.String': 'str',
            'System.Boolean': 'bool',
            'System.Int32': 'int', 
            'System.Int64': 'int',
            'System.Int16': 'int',
            'System.UInt32': 'int',
            'System.UInt64': 'int',
            'System.UInt16': 'int',
            'System.Byte': 'int',
            'System.SByte': 'int',
            'System.Double': 'float',
            'System.Single': 'float',
            'System.Decimal': 'float',
            'System.DateTime': 'datetime',
            'System.TimeSpan': 'timedelta',
            'System.Guid': 'str',
            'System.Void': 'None',
            'System.Object': 'Any',
            
            # Nullable types - these get converted to Optional
            'System.Nullable`1[System.Int32]': 'Optional[int]',
            'System.Nullable`1[System.Double]': 'Optional[float]',
            'System.Nullable`1[System.Boolean]': 'Optional[bool]',
            'System.Nullable`1[System.DateTime]': 'Optional[datetime]',
            
            # Collections - these typically stay as .NET types but we provide Python-like interfaces
            'System.Collections.Generic.IEnumerable': 'Iterable[Any]',
            'System.Collections.Generic.ICollection': 'Collection[Any]',
            'System.Collections.Generic.IList': 'List[Any]',
            'System.Collections.Generic.IDictionary': 'Dict[Any, Any]',
            'System.Array': 'Array[Any]',
        }
        
        if type_name in known_conversions:
            return known_conversions[type_name]
        
        # Handle arrays
        if hasattr(net_type, 'IsArray') and net_type.IsArray:
            element_type = net_type.GetElementType()
            element_python_type = self._convert_net_type_to_python(element_type)
            
            # .NET Array is already multidimensional, so Array[float] can represent
            # both 1D and multidimensional arrays of float
            return f'Array[{element_python_type}]'
        
        # Handle generic types
        if hasattr(net_type, 'IsGenericType') and net_type.IsGenericType:
            generic_def = net_type.GetGenericTypeDefinition()
            generic_args = net_type.GetGenericArguments()
            
            generic_def_name = generic_def.FullName if hasattr(generic_def, 'FullName') else str(generic_def)
            
            # Handle VRect<T> specifically
            if 'VRect' in generic_def_name:
                if len(generic_args) > 0:
                    arg_type = self._convert_net_type_to_python(generic_args[0])
                    return f'VRect[{arg_type}]'  # Preserve the generic type parameter
                return 'VRect'
            
            # Handle KeyValuePair<T1, T2>
            if 'KeyValuePair' in generic_def_name:
                if len(generic_args) >= 2:
                    key_type = self._convert_net_type_to_python(generic_args[0])
                    value_type = self._convert_net_type_to_python(generic_args[1])
                    return f'KeyValuePair[{key_type}, {value_type}]'
                return 'KeyValuePair[Any, Any]'
            
            # Handle IEnumerator<T>
            if 'IEnumerator' in generic_def_name:
                if len(generic_args) > 0:
                    arg_type = self._convert_net_type_to_python(generic_args[0])
                    return f'Iterable[{arg_type}]'
                return 'Iterable[Any]'
            
            # Handle IReadOnlyCollection<T>
            if 'IReadOnlyCollection' in generic_def_name:
                if len(generic_args) > 0:
                    arg_type = self._convert_net_type_to_python(generic_args[0])
                    return f'Collections.Generic.IReadOnlyCollection[{arg_type}]'
                return 'Collections.Generic.IReadOnlyCollection[Any]'
            
            # Handle ICollection<T>
            if 'ICollection' in generic_def_name and 'IReadOnlyCollection' not in generic_def_name:
                if len(generic_args) > 0:
                    arg_type = self._convert_net_type_to_python(generic_args[0])
                    return f'Collections.Generic.ICollection[{arg_type}]'
                return 'Collections.Generic.ICollection[Any]'
            
            # Handle other VMS generic types
            if generic_def_name and 'VMS.TPS.Common.Model' in generic_def_name:
                # Extract just the class name from the generic definition
                simple_name = generic_def_name.split('.')[-1].split('`')[0]  # Remove `1 suffix
                
                # For specific VMS types that should preserve generic parameters
                if simple_name in ['VRect', 'VVector'] and len(generic_args) > 0:
                    converted_args = [self._convert_net_type_to_python(arg) for arg in generic_args]
                    return f'{simple_name}[{", ".join(converted_args)}]'
                
                # For other VMS types, just return the simple name
                return simple_name
            
            if 'List' in generic_def_name or 'IEnumerable' in generic_def_name:
                if len(generic_args) > 0:
                    arg_type = self._convert_net_type_to_python(generic_args[0])
                    return f'List[{arg_type}]'
                return 'List[Any]'
            elif 'Dictionary' in generic_def_name:
                if len(generic_args) >= 2:
                    key_type = self._convert_net_type_to_python(generic_args[0])
                    value_type = self._convert_net_type_to_python(generic_args[1])
                    return f'Dict[{key_type}, {value_type}]'
                return 'Dict[str, Any]'
            elif 'Nullable' in generic_def_name:
                if len(generic_args) > 0:
                    arg_type = self._convert_net_type_to_python(generic_args[0])
                    return f'Optional[{arg_type}]'
        
        # Handle VMS types - these remain as .NET objects, so keep class names
        if type_name and type_name.startswith('VMS.TPS.Common.Model'):
            return type_name.split('.')[-1]
        
        # Handle System types
        if type_name and type_name.startswith('System.'):
            system_type = type_name.replace('System.', '')
            return known_conversions.get(f'System.{system_type}', system_type)
        
        # For unknown types, extract the last part (class name)
        # These are likely complex .NET types that don't get converted
        if '.' in type_name:
            return type_name.split('.')[-1]
        
        return type_name or 'Any'
    
    def get_property_type(self, class_full_name: str, property_name: str) -> Optional[str]:
        """Get property type information from the DLL"""
        if not HAS_PYTHONNET:
            return None
        
        cache_key = f"{class_full_name}.{property_name}"
        if cache_key in self.type_cache:
            return self.type_cache[cache_key]
        
        try:
            # Try to import the type directly using pythonnet
            namespace_parts = class_full_name.split('.')
            if len(namespace_parts) < 2:
                return None
            
            module_name = '.'.join(namespace_parts[:-1])
            class_name = namespace_parts[-1]
            
            # Import the namespace module
            exec(f"import {module_name}")
            namespace_module = eval(module_name)
            
            if not hasattr(namespace_module, class_name):
                self.type_cache[cache_key] = None
                return None
            
            type_obj = getattr(namespace_module, class_name)
            clr_type = clr.GetClrType(type_obj)
            
            if not clr_type:
                self.type_cache[cache_key] = None
                return None
            
            # Get property info
            properties = clr_type.GetProperties()
            for prop in properties:
                if prop.Name == property_name:
                    prop_type = self._convert_net_type_to_python(prop.PropertyType)
                    self.type_cache[cache_key] = prop_type
                    return prop_type
            
            # Also check fields
            fields = clr_type.GetFields()
            for field in fields:
                if field.Name == property_name:
                    field_type = self._convert_net_type_to_python(field.FieldType)
                    self.type_cache[cache_key] = field_type
                    return field_type
        
        except Exception:
            pass
        
        self.type_cache[cache_key] = None
        return None

class XmlApiElement:
    """Represents a .NET API element parsed from XML documentation"""
    
    def __init__(self, member_name: str, element_type: str):
        self.member_name = member_name  # Full member name like "T:VMS.TPS.Common.Model.API.AddOn"
        self.element_type = element_type  # T, P, M, F, E
        self.namespace = ""
        self.class_name = ""
        self.name = ""
        self.return_type = "Any"
        self.parameters: List[Dict] = []
        self.summary = ""
        self.remarks = ""
        self.inheritance = []
        self.param_descriptions = {}  # Parameter descriptions from XML
        
        self._parse_member_name()
    
    def _parse_member_name(self):
        """Parse the member name to extract namespace, class, and element info"""
        # Remove the prefix (T:, P:, M:, F:)
        full_name = self.member_name[2:]  # Remove "T:", "P:", etc.
        
        if self.element_type == 'T':  # Type (class, interface, enum)
            # For types, the last part is the class name
            parts = full_name.split('.')
            self.namespace = '.'.join(parts[:-1])
            self.class_name = parts[-1]
            self.name = parts[-1]
        elif self.element_type == 'M':  # Method
            # Methods have parameters in parentheses
            if '(' in full_name:
                method_part, params_part = full_name.split('(', 1)
                params_part = params_part.rstrip(')')
                
                # Parse method name and class
                method_parts = method_part.split('.')
                self.name = method_parts[-1]
                
                # Handle constructor first (before interface cleanup)
                if self.name == '#ctor':
                    self.name = '__init__'
                elif '#' in self.name:
                    # Clean up explicit interface implementation names (remove Interface#Method -> Method)
                    # For explicit interface implementations like "System#Collections#IEnumerable#GetEnumerator"
                    # Extract just the method name after the last #
                    # Special case: #ctor should become __init__, not ctor
                    method_name = self.name.split('#')[-1]
                    if method_name == 'ctor':
                        self.name = '__init__'
                    else:
                        self.name = method_name
                
                # Remove C# method overload suffixes (``1, ``2, etc.)
                if '``' in self.name:
                    self.name = self.name.split('``')[0]
                
                if len(method_parts) > 1:
                    self.class_name = method_parts[-2]
                    self.namespace = '.'.join(method_parts[:-2])
                
                # Parse parameters
                if params_part.strip():
                    param_types = self._parse_parameter_types(params_part)
                    for i, param_type in enumerate(param_types):
                        self.parameters.append({
                            'name': f'param{i+1}',
                            'type': self._convert_csharp_type_to_python(param_type),
                            'csharp_type': param_type
                        })
            else:
                # Method without parameters
                parts = full_name.split('.')
                self.name = parts[-1]
                
                # Handle constructor first (before interface cleanup)
                if self.name == '#ctor':
                    self.name = '__init__'
                elif '#' in self.name:
                    # Clean up explicit interface implementation names (remove Interface#Method -> Method)
                    # For explicit interface implementations like "System#Collections#IEnumerable#GetEnumerator"
                    # Extract just the method name after the last #
                    # Special case: #ctor should become __init__, not ctor
                    method_name = self.name.split('#')[-1]
                    if method_name == 'ctor':
                        self.name = '__init__'
                    else:
                        self.name = method_name
                
                # Remove C# method overload suffixes (``1, ``2, etc.)
                if '``' in self.name:
                    self.name = self.name.split('``')[0]
                
                if len(parts) > 1:
                    self.class_name = parts[-2]
                    self.namespace = '.'.join(parts[:-2])
        else:
            # Properties and Fields
            parts = full_name.split('.')
            self.name = parts[-1]
            
            # Handle constructor first (before interface cleanup)
            if self.name == '#ctor':
                self.name = '__init__'
            elif '#' in self.name:
                # Clean up explicit interface implementation names (remove Interface#Method -> Method)
                # For explicit interface implementations like "System#Collections#IEnumerable#GetEnumerator"
                # Extract just the method name after the last #
                # Special case: #ctor should become __init__, not ctor
                method_name = self.name.split('#')[-1]
                if method_name == 'ctor':
                    self.name = '__init__'
                else:
                    self.name = method_name
            
            # Remove C# method overload suffixes (``1, ``2, etc.)
            if '``' in self.name:
                self.name = self.name.split('``')[0]
            
            if len(parts) > 1:
                self.class_name = parts[-2]
                self.namespace = '.'.join(parts[:-2])
    
    def _parse_parameter_types(self, params_str: str) -> List[str]:
        """Parse parameter types from method signature"""
        if not params_str.strip():
            return []
        
        # Handle generic types, arrays, and nested commas
        params = []
        current_param = ""
        bracket_depth = 0
        
        for char in params_str + ',':  # Add comma at end to process last param
            if char in '<{[':
                bracket_depth += 1
                current_param += char
            elif char in '>}]':
                bracket_depth -= 1
                current_param += char
            elif char == ',' and bracket_depth == 0:
                # Only split on comma if we're not inside brackets/braces
                # This handles cases like System.Single[0:,0:] where the comma is part of array bounds
                if current_param.strip():
                    params.append(current_param.strip())
                current_param = ""
            else:
                current_param += char
        
        return params
    
    def _convert_csharp_type_to_python(self, csharp_type: str, preserve_net_types: bool = False) -> str:
        """Convert C# type to Python type"""
        # If the type is already in Python format (from DLL introspector), don't convert it
        if (csharp_type.startswith('Array[') or csharp_type.startswith('List[') or 
            csharp_type.startswith('Dict[') or csharp_type.startswith('Optional[') or
            csharp_type.startswith('Iterable[') or csharp_type.startswith('KeyValuePair[') or
            csharp_type.startswith('Collections.Generic.IReadOnlyCollection[') or
            csharp_type.startswith('Collections.Generic.ICollection[')):
            return csharp_type
            
        # Remove ref/out keywords and & or @ suffix (@ indicates reference parameters in XML)
        csharp_type = re.sub(r'\b(ref|out)\s+', '', csharp_type)
        csharp_type = csharp_type.rstrip('&@')
        
        # More robust assembly-qualified cleanup for deeply nested generic types
        # Handle patterns like [[TypeName, Assembly, Version=...]] -> [TypeName]
        def clean_assembly_qualified(text):
            """Recursively clean assembly-qualified type names in nested generics"""
            # First, handle double brackets [[Type, Assembly...]] -> [Type]
            double_bracket_pattern = r'\[\[([^\[\],]+)(?:,\s*[^\[\]]*?)\]\]'
            text = re.sub(double_bracket_pattern, r'[\1]', text)
            
            # Then handle single brackets [Type, Assembly...] -> [Type] but only if it contains assembly info
            # Look for the pattern: [TypeName, something with Version or Culture or PublicKeyToken]
            single_bracket_assembly_pattern = r'\[([^,\[\]]+),\s*[^\[\]]*?(?:Version|Culture|PublicKeyToken)[^\[\]]*?\]'
            text = re.sub(single_bracket_assembly_pattern, r'[\1]', text)
            
            return text
        
        csharp_type = clean_assembly_qualified(csharp_type)
        
        # Handle assembly-qualified names - remove everything after the comma
        # Example: String, mscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089 -> String
        # But only do this AFTER cleaning nested brackets
        if ', ' in csharp_type and 'Version=' in csharp_type:
            csharp_type = csharp_type.split(', ')[0]
        
        # Handle curly braces in the entire string recursively
        while '{' in csharp_type and '}' in csharp_type:
            csharp_type = csharp_type.replace('{', '<').replace('}', '>')
        
        # Convert C# backtick generic syntax to angle bracket syntax for further processing
        # Example: List`1[String] -> List<String>
        backtick_generic_pattern = r'([^`\[]+)`\d+\[([^\]]+)\]'
        backtick_match = re.match(backtick_generic_pattern, csharp_type)
        if backtick_match:
            base_type = backtick_match.group(1)
            args = backtick_match.group(2)
            csharp_type = f'{base_type}<{args}>'
        
        # Handle .NET 2D array syntax like System.Single[0:,0:] -> System.Single with 2D array marker
        # This pattern: Type[bounds] where bounds contains comma(s) indicates multidimensional array
        array_bounds_match = re.match(r'([^[]+)\[([^\]]*:[^\]]*,.*?)\]', csharp_type)
        if array_bounds_match:
            base_type = array_bounds_match.group(1)
            bounds = array_bounds_match.group(2)
            # Count commas to determine dimensions (1 comma = 2D, 2 commas = 3D, etc.)
            dimensions = bounds.count(',') + 1
            
            # Convert the base type
            python_base_type = self._convert_csharp_type_to_python(base_type, preserve_net_types=False)
            
            # .NET Array is already multidimensional, so Array[float] represents all dimensions
            return f'Array[{python_base_type}]'
        
        # Handle C# generic type syntax with backticks
        # The number after backtick indicates how many type parameters the generic type takes
        
        # Case 1: Backtick with square brackets (e.g., List`1[String] -> List<String>)
        if '`' in csharp_type and '[' in csharp_type and ']' in csharp_type:
            # Convert backtick syntax to angle bracket syntax: List`1[String] -> List<String>
            backtick_match = re.match(r'([^`]+)`\d+(\[.+\])', csharp_type)
            if backtick_match:
                base_name = backtick_match.group(1)
                type_args = backtick_match.group(2)  # [String] or [String, Int32]
                # Convert [String] to <String>
                angle_bracket_args = type_args.replace('[', '<').replace(']', '>')
                csharp_type = f'{base_name}{angle_bracket_args}'
        
        # Case 2: Backtick without brackets (e.g., VRect`1 -> VRect[T])
        # Only match when backtick immediately follows the class name and there are no square brackets
        elif '`' in csharp_type and '<' not in csharp_type and '[' not in csharp_type:
            match = re.match(r'([^`]+)`(\d+)', csharp_type)
            if match:
                base_name = match.group(1).split('.')[-1]  # Get just the class name
                type_param_count = int(match.group(2))
                
                # Generate generic type parameters
                if type_param_count == 1:
                    return f'{base_name}[T]'
                else:
                    type_params = [f'T{i+1}' for i in range(type_param_count)]
                    return f'{base_name}[{", ".join(type_params)}]'
        
        # Handle C# generic type parameter references like `0, `1, ``0, ``1, etc.
        if re.match(r'^`+\d+$', csharp_type):
            # Extract the number after all the backticks
            param_num = int(re.search(r'\d+', csharp_type).group())
            if param_num == 0:
                return 'T'
            else:
                return f'T{param_num + 1}'
        
        # Handle malformed generic types like VRect{`0} or VRect<`0> -> VRect[T]
        malformed_generic = re.match(r'([^{<]+)[{<](`*\d+)[}>]', csharp_type)
        if malformed_generic:
            base_name = malformed_generic.group(1).split('.')[-1]
            param_ref = malformed_generic.group(2)
            param_num = int(re.search(r'\d+', param_ref).group())
            param_name = 'T' if param_num == 0 else f'T{param_num + 1}'
            return f'{base_name}[{param_name}]'
        
        # Handle array types first (before generic handling)
        if '[]' in csharp_type:
            # Count array dimensions
            array_count = csharp_type.count('[]')
            base_type = csharp_type.replace('[]', '')
            
            # Convert the base type, preserving .NET types for arrays
            python_base_type = self._convert_csharp_type_to_python(base_type, preserve_net_types=True)
            
            # Handle different array dimensions
            if array_count == 1:
                # Single-dimensional array: Type[] -> Array[Type]
                return f'Array[{python_base_type}]'
            elif array_count == 2:
                # Jagged array: Type[][] -> Array[Array[Type]]
                return f'Array[Array[{python_base_type}]]'
            else:
                # For higher dimensions, keep nesting Array types
                result = python_base_type
                for _ in range(array_count):
                    result = f'Array[{result}]'
                return result
        
        # Handle generic types
        if '<' in csharp_type and '>' in csharp_type:
            # Extract generic base type and arguments
            match = re.match(r'([^<]+)<(.+)>', csharp_type)
            if match:
                base_type = match.group(1)
                generic_args = match.group(2)
                
                # Convert collection types to Python equivalents
                # Handle specific collection types first (before generic handling)
                if base_type in ['System.Collections.Generic.IReadOnlyCollection', 'Collections.Generic.IReadOnlyCollection']:
                    # Preserve IReadOnlyCollection as a more specific type with full namespace
                    arg_type = self._convert_csharp_type_to_python(generic_args, preserve_net_types)
                    # For VMS types, extract just the class name
                    if arg_type.startswith('VMS.TPS.Common.Model'):
                        arg_type = arg_type.split('.')[-1]
                    return f'Collections.Generic.IReadOnlyCollection[{arg_type}]'
                elif base_type in ['System.Collections.Generic.ICollection', 'Collections.Generic.ICollection']:
                    # Preserve ICollection as a more specific type with full namespace
                    arg_type = self._convert_csharp_type_to_python(generic_args, preserve_net_types)
                    # For VMS types, extract just the class name
                    if arg_type.startswith('VMS.TPS.Common.Model'):
                        arg_type = arg_type.split('.')[-1]
                    return f'Collections.Generic.ICollection[{arg_type}]'
                elif base_type in ['System.Collections.Generic.List', 'System.Collections.Generic.IList', 
                               'System.Collections.Generic.IEnumerable',
                               'Collections.Generic.List', 'Collections.Generic.IList',
                               'Collections.Generic.IEnumerable']:
                    arg_type = self._convert_csharp_type_to_python(generic_args, preserve_net_types)
                    # For VMS types, extract just the class name
                    if arg_type.startswith('VMS.TPS.Common.Model'):
                        arg_type = arg_type.split('.')[-1]
                    return f'List[{arg_type}]'
                elif base_type in ['System.Collections.Generic.Dictionary', 'System.Collections.Generic.IDictionary',
                                 'Collections.Generic.Dictionary', 'Collections.Generic.IDictionary']:
                    # Handle Dictionary<K,V>
                    args = self._parse_parameter_types(generic_args)
                    if len(args) >= 2:
                        key_type = self._convert_csharp_type_to_python(args[0], preserve_net_types)
                        value_type = self._convert_csharp_type_to_python(args[1], preserve_net_types)
                        return f'Dict[{key_type}, {value_type}]'
                elif base_type == 'System.Nullable':
                    arg_type = self._convert_csharp_type_to_python(generic_args, preserve_net_types)
                    return f'Optional[{arg_type}]'
                else:
                    # For other generic types, preserve the .NET type with Python syntax
                    # Convert the argument types recursively
                    args = self._parse_parameter_types(generic_args)
                    converted_args = [self._convert_csharp_type_to_python(arg, preserve_net_types) for arg in args]
                    # Extract just the class name from the base type
                    if '.' in base_type:
                        base_name = base_type.split('.')[-1]
                    else:
                        base_name = base_type
                    return f'{base_name}[{", ".join(converted_args)}]'
        
        # For array element types, preserve .NET type names
        if preserve_net_types:
            net_type_mappings = {
                'System.Double': 'Double',
                'Double': 'Double',
                'System.Single': 'Single',
                'Single': 'Single',
                'System.Int32': 'Int32',
                'Int32': 'Int32',
                'System.Boolean': 'Boolean',
                'Boolean': 'Boolean',
                'System.String': 'String',
                'String': 'String',
            }
            if csharp_type in net_type_mappings:
                return net_type_mappings[csharp_type]
        
        # Direct type mappings
        if csharp_type in TYPE_MAPPINGS:
            return TYPE_MAPPINGS[csharp_type]
        
        # Handle VMS types - extract just the class name
        if csharp_type.startswith('VMS.TPS.Common.Model'):
            parts = csharp_type.split('.')
            return parts[-1]  # Return just the class name
        
        # Handle System types
        if csharp_type.startswith('System.'):
            system_type = csharp_type.replace('System.', '')
            return TYPE_MAPPINGS.get(system_type, system_type)
        
        # For unknown types, extract the last part (class name)
        if '.' in csharp_type:
            parts = csharp_type.split('.')
            return parts[-1]
        
        return csharp_type
    
    def get_qualified_name(self) -> str:
        """Get the fully qualified name"""
        if self.namespace:
            return f"{self.namespace}.{self.class_name}.{self.name}"
        else:
            return f"{self.class_name}.{self.name}"
    
    def __repr__(self):
        return f"XmlApiElement(name='{self.name}', type='{self.element_type}', class='{self.class_name}', namespace='{self.namespace}')"

class XmlDocumentationParser:
    """Parser for .NET XML documentation files"""
    
    def __init__(self, dll_paths: List[str] = None):
        self.elements: List[XmlApiElement] = []
        self.types_by_namespace: Dict[str, List[XmlApiElement]] = defaultdict(list)
        self.members_by_class: Dict[str, List[XmlApiElement]] = defaultdict(list)
        self.dll_introspector = DllTypeIntrospector(dll_paths) if HAS_PYTHONNET else None
    
    def parse_xml_file(self, xml_file: str) -> List[XmlApiElement]:
        """Parse XML documentation file and extract API elements"""
        if not os.path.exists(xml_file):
            print(f"XML file not found: {xml_file}")
            return []
        
        print(f"Parsing XML file: {xml_file}")
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Find the members section
            members = root.find('members')
            if members is None:
                print("No members section found in XML")
                return []
            
            elements = []
            for member in members.findall('member'):
                name = member.get('name', '')
                if not name:
                    continue
                
                # Determine element type from prefix
                element_type = name[0] if name else 'T'
                
                element = XmlApiElement(name, element_type)
                
                # Extract documentation
                summary = member.find('summary')
                if summary is not None:
                    element.summary = self._clean_text(summary.text or "")
                
                remarks = member.find('remarks')
                if remarks is not None:
                    element.remarks = self._clean_text(remarks.text or "")
                
                # Extract parameters for methods
                if element_type == 'M':
                    params = member.findall('param')
                    xml_param_info = {}
                    for param in params:
                        param_name = param.get('name', '')
                        param_desc = self._clean_text(param.text or "")
                        xml_param_info[param_name] = param_desc
                    
                    # Update parameter names and descriptions from XML if available
                    if xml_param_info and element.parameters:
                        for i, param in enumerate(element.parameters):
                            xml_name = list(xml_param_info.keys())[i] if i < len(xml_param_info) else None
                            if xml_name:
                                param['name'] = xml_name
                                param['description'] = xml_param_info[xml_name]
                    
                    # Store parameter info for methods without parsed parameters
                    element.param_descriptions = xml_param_info
                    
                    # Enhance with DLL introspection if available
                    if self.dll_introspector:
                        self._enhance_method_with_dll_info(element)
                
                # Enhance property types with DLL introspection
                elif element_type == 'P' and self.dll_introspector:
                    self._enhance_property_with_dll_info(element)
                
                elements.append(element)
                self.elements.append(element)
            
            print(f"Found {len(elements)} API elements")
            self._organize_elements()
            
            return elements
            
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            return []
    
    def _enhance_method_with_dll_info(self, element: XmlApiElement):
        """Enhance method element with DLL type information (only supplement missing types)"""
        if not element.namespace or not element.class_name:
            return
        
        class_full_name = f"{element.namespace}.{element.class_name}"
        method_signature = self.dll_introspector.get_method_signature(class_full_name, element.name)
        
        if method_signature:
            if element.name == '__init__' and 'constructors' in method_signature:
                # Handle constructor overloads
                constructors = method_signature['constructors']
                if constructors and len(constructors) > 0:
                    # Use the first constructor for now, could be enhanced to handle overloads
                    ctor_info = constructors[0]
                    if 'parameters' in ctor_info:
                        # Only update parameter types if they are "Any" (missing from XML)
                        for i, dll_param in enumerate(ctor_info['parameters']):
                            if i < len(element.parameters):
                                if element.parameters[i]['type'] == 'Any':
                                    element.parameters[i]['type'] = dll_param['type']
                                # Always update parameter names if DLL has better info
                                if dll_param['name'] and element.parameters[i]['name'].startswith('param'):
                                    element.parameters[i]['name'] = dll_param['name']
            else:
                # Regular method
                if 'parameters' in method_signature:
                    # Only update parameter types if they are "Any" (missing from XML)
                    for i, dll_param in enumerate(method_signature['parameters']):
                        if i < len(element.parameters):
                            if element.parameters[i]['type'] == 'Any':
                                element.parameters[i]['type'] = dll_param['type']
                            # Always update parameter names if DLL has better info
                            if dll_param['name'] and element.parameters[i]['name'].startswith('param'):
                                element.parameters[i]['name'] = dll_param['name']
                
                # Always update return type if it's "Any" (missing from XML)
                if 'return_type' in method_signature and element.return_type == 'Any':
                    raw_return_type = method_signature['return_type']
                    # The DLL introspector already returns properly formatted Python types,
                    # so we don't need to convert them again
                    element.return_type = raw_return_type
    
    def _enhance_property_with_dll_info(self, element: XmlApiElement):
        """Enhance property element with DLL type information (only supplement missing types)"""
        if not element.namespace or not element.class_name:
            return
        
        class_full_name = f"{element.namespace}.{element.class_name}"
        prop_type = self.dll_introspector.get_property_type(class_full_name, element.name)
        
        # Only update property type if it's "Any" (missing from XML)
        if prop_type and element.return_type == 'Any':
            element.return_type = prop_type
    
    def _clean_text(self, text: str) -> str:
        """Clean and format documentation text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove XML comments and tags
        text = re.sub(r'<!--.*?-->', '', text)
        text = re.sub(r'<see cref="[^"]*"/>', '', text)
        text = re.sub(r'<[^>]+>', '', text)
        
        return text.strip()
    
    def _organize_elements(self):
        """Organize elements by namespace and class for easier stub generation"""
        for element in self.elements:
            # Group by namespace
            self.types_by_namespace[element.namespace].append(element)
            
            # Group members by their parent class
            if element.element_type in ['P', 'M', 'F']:  # Properties, Methods, Fields
                class_key = f"{element.namespace}.{element.class_name}".strip('.')
                self.members_by_class[class_key].append(element)
            elif element.element_type == 'T' and '.' in element.name:
                # Handle nested types like VVector.Component
                parent_class = element.name.split('.')[0]
                parent_key = f"{element.namespace}.{parent_class}".strip('.')
                # Treat nested types as members of their parent class for now
                # This could be improved to handle them as actual nested classes
                element.element_type = 'NT'  # Nested Type
                self.members_by_class[parent_key].append(element)

class XmlStubGenerator:
    """Generates Python stub files from XML documentation"""
    
    def __init__(self, parser: XmlDocumentationParser):
        self.parser = parser
    
    def generate_stubs(self, output_dir: str):
        """Generate Python stub files organized by namespace"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"Generating stubs in {output_dir}")
        
        # Generate stubs for each namespace
        for namespace, elements in self.parser.types_by_namespace.items():
            if not namespace:  # Skip empty namespace
                continue
                
            self._generate_namespace_stubs(namespace, elements, output_path)
        
        print(f"Stub generation complete!")
        print(f"Namespaces generated: {len(self.parser.types_by_namespace)}")
        print(f"Total elements: {len(self.parser.elements)}")
    
    def _generate_namespace_stubs(self, namespace: str, elements: List[XmlApiElement], base_path: Path):
        """Generate stub files for a specific namespace"""
        # Create directory structure
        namespace_parts = namespace.split('.')
        current_path = base_path
        
        for part in namespace_parts:
            current_path = current_path / part
            current_path.mkdir(exist_ok=True)
            
            # Create __init__.pyi
            init_file = current_path / "__init__.pyi"
            if not init_file.exists():
                init_file.write_text("")
        
        # Group elements by type
        types = [e for e in elements if e.element_type == 'T']
        
        if types:
            # Generate main module file
            module_file = current_path / f"{namespace_parts[-1]}.pyi"
            self._write_module_stub(module_file, namespace, types)
    
    def _write_module_stub(self, file_path: Path, namespace: str, types: List[XmlApiElement]):
        """Write a module stub file with classes and their members"""
        with open(file_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write('"""\n')
            f.write(f'Type stubs for {namespace}\n')
            f.write('Generated from .NET XML documentation\n')
            f.write('"""\n\n')
            
            # Collect all type references used in this module
            type_references = self._collect_type_references(types, namespace)
            
            # Check if we need TypeVar and Generic for generic classes
            has_generics = any('`' in element.name for element in types)
            
            # Check if we need overload for classes with multiple constructors
            has_overloads = self._has_constructor_overloads(types, namespace)
            
            # Write basic imports
            imports = ["Any", "List", "Optional", "Union", "Dict", "Iterable"]
            if has_generics:
                imports.extend(["TypeVar", "Generic"])
            if has_overloads:
                imports.append("overload")
            
            f.write(f"from typing import {', '.join(imports)}\n")
            f.write("from datetime import datetime\n")
            f.write("from System import Array, Double, Single, Int32, Boolean, String\n")
            f.write("from System.Collections.Generic import KeyValuePair\n")
            f.write("from System import Collections\n")
            
            # Write TypeVar declarations for generic classes
            if has_generics:
                f.write("\n# Generic type variables\n")
                f.write("T = TypeVar('T')\n")
                f.write("T1 = TypeVar('T1')\n")
                f.write("T2 = TypeVar('T2')\n")
                f.write("T3 = TypeVar('T3')\n")
            
            # Write type imports
            if type_references:
                f.write("\n# Type imports\n")
                for import_line in sorted(type_references):
                    f.write(f"{import_line}\n")
            
            f.write("\n")
            
            # Write each type
            for type_element in types:
                self._write_type_stub(f, type_element)
                f.write("\n")
    
    def _collect_type_references(self, types: List[XmlApiElement], current_namespace: str) -> set:
        """Collect all type references that need to be imported"""
        imports = set()
        
        # Get all members for types in this namespace
        for type_element in types:
            class_key = f"{type_element.namespace}.{type_element.name}".strip('.')
            members = self.parser.members_by_class.get(class_key, [])
            
            # Check type references in method parameters
            for member in members:
                if member.element_type == 'M':  # Methods
                    for param in member.parameters:
                        param_type = param.get('csharp_type', '')
                        import_stmt = self._get_import_for_type(param_type, current_namespace)
                        if import_stmt:
                            imports.add(import_stmt)
                
                # For properties, check for explicit type references in documentation
                elif member.element_type == 'P':  # Properties
                    # Look for type references in the summary
                    if member.summary:
                        # Look for explicit type references like "See <see cref="T:VMS.TPS.Common.Model.Types.DoseValue"/>"
                        type_matches = re.findall(r'<see cref="T:([^"]+)"', member.summary)
                        for type_ref in type_matches:
                            import_stmt = self._get_import_for_type(type_ref, current_namespace)
                            if import_stmt:
                                imports.add(import_stmt)
        
        return imports
    
    def _has_constructor_overloads(self, types: List[XmlApiElement], current_namespace: str) -> bool:
        """Check if any class in this module has multiple constructors requiring @overload"""
        for type_element in types:
            class_key = f"{type_element.namespace}.{type_element.name}".strip('.')
            members = self.parser.members_by_class.get(class_key, [])
            
            # Count constructors for this class
            constructors = [m for m in members if m.element_type == 'M' and m.name == '__init__']
            if len(constructors) > 1:
                return True
        
        return False
    
    def _get_import_for_type(self, csharp_type: str, current_namespace: str) -> str:
        """Generate import statement for a C# type if needed"""
        if not csharp_type or csharp_type in ['System.String', 'System.Boolean', 'System.Int32', 'System.Double', 'System.Single', 'System.Void', 'System.Object']:
            return None
        
        # Clean up curly braces first
        clean_type = csharp_type.replace('{', '<').replace('}', '>')
        
        # Clean up the type name - remove generic parameters and array notation
        clean_type = re.sub(r'<.*?>', '', clean_type)  # Remove generics like List<T>
        clean_type = re.sub(r'\[\]', '', clean_type)   # Remove array notation
        clean_type = clean_type.strip()
        
        # Don't try to import array types or basic system types
        if clean_type.endswith('[]') or clean_type.startswith('Array['):
            return None
        
        # Handle VMS.TPS types
        if clean_type.startswith('VMS.TPS.Common.Model'):
            # Extract the namespace and class name
            parts = clean_type.split('.')
            if len(parts) < 2:
                return None
                
            type_namespace = '.'.join(parts[:-1])
            class_name = parts[-1]
            
            # Don't import from the same namespace
            if type_namespace == current_namespace:
                return None
            
            # Convert namespace to import path
            if type_namespace == 'VMS.TPS.Common.Model.Types':
                if current_namespace == 'VMS.TPS.Common.Model.API':
                    return f"from ..Types.Types import {class_name}"
                else:
                    return f"from .Types import {class_name}"
            elif type_namespace == 'VMS.TPS.Common.Model.API':
                if current_namespace == 'VMS.TPS.Common.Model.Types':
                    return f"from ..API.API import {class_name}"
                else:
                    return f"from .API import {class_name}"
        
        return None
    
    def _write_type_stub(self, f, type_element: XmlApiElement):
        """Write a stub for a single type (class/interface/enum)"""
        # Convert the class name to handle generics
        class_name = type_element._convert_csharp_type_to_python(type_element.name)
        
        # Write class definition
        f.write(f"class {class_name}")
        
        # Handle inheritance - for generic classes, inherit from Generic
        inheritance_list = []
        if '`' in type_element.name:
            # This is a generic class, add Generic[T] to inheritance
            if '[T]' in class_name:
                inheritance_list.append("Generic[T]")
            elif '[T1' in class_name:
                # Multiple type parameters
                type_params = []
                if 'T1' in class_name:
                    type_params.append('T1')
                if 'T2' in class_name:
                    type_params.append('T2')
                if 'T3' in class_name:
                    type_params.append('T3')
                inheritance_list.append(f"Generic[{', '.join(type_params)}]")
        
        if type_element.inheritance:
            inheritance_list.extend(type_element.inheritance)
            
        if inheritance_list:
            f.write(f"({', '.join(inheritance_list)})")
        f.write(":\n")
        
        # Get members for this class
        class_key = f"{type_element.namespace}.{type_element.class_name}".strip('.')
        members = self.parser.members_by_class.get(class_key, [])
        
        # Write class docstring with Google style format
        if type_element.summary or members:
            f.write('    """\n')
            if type_element.summary:
                f.write(f'    {type_element.summary}\n')
            
            # Add attributes section for properties
            properties = [m for m in members if m.element_type == 'P']
            if properties:
                f.write('\n    Attributes:\n')
                for prop in properties:
                    # Use DLL-enhanced type if available, otherwise infer
                    if prop.return_type and prop.return_type != "Any":
                        prop_type = prop.return_type
                    else:
                        prop_type = self._infer_property_type(prop.name, prop.summary)
                    
                    if prop.summary:
                        f.write(f'        {prop.name} ({prop_type}): {prop.summary}\n')
                    else:
                        f.write(f'        {prop.name} ({prop_type}): Property value.\n')
            
            if type_element.remarks:
                f.write(f'\n    Note:\n        {type_element.remarks}\n')
            f.write('    """\n')
        
        if not members:
            # Empty class
            f.write("    def __init__(self) -> None: ...\n")
        else:
            # Write constructors first
            constructors = [m for m in members if m.element_type == 'M' and m.name == '__init__']
            if constructors:
                # Only add @overload decorator if there are multiple constructors
                has_multiple_constructors = len(constructors) > 1
                for ctor in constructors:
                    self._write_method_stub(f, ctor, has_multiple_constructors)
                    f.write("\n")
            else:
                # No explicit constructors found, write default one
                f.write("    def __init__(self) -> None: ...\n\n")
            
            # Write properties
            properties = [m for m in members if m.element_type == 'P']
            for prop in properties:
                self._write_property_stub(f, prop)
                f.write("\n")
            
            # Write nested types
            nested_types = [m for m in members if m.element_type == 'NT']
            for nested_type in nested_types:
                self._write_nested_type_stub(f, nested_type)
                f.write("\n")
            
            # Write methods (excluding constructors, getters, and setters)
            methods = [m for m in members if m.element_type == 'M' and not m.name.startswith('get_') and not m.name.startswith('set_') and m.name != '__init__']
            for method in methods:
                self._write_method_stub(f, method)
                f.write("\n")
    
    def _write_property_stub(self, f, prop: XmlApiElement):
        """Write a property stub"""
        # Skip individual comments since they're now in the class docstring
        
        # Use DLL-enhanced type if available, otherwise infer from name/summary
        if prop.return_type and prop.return_type != "Any":
            prop_type = prop.return_type
        else:
            prop_type = self._infer_property_type(prop.name, prop.summary)
        
        f.write(f'    {prop.name}: {prop_type}\n')
    
    def _infer_property_type(self, prop_name: str, summary: str) -> str:
        """Infer property type from name and summary"""
        prop_name_lower = prop_name.lower()
        summary_lower = summary.lower() if summary else ""
        
        # Date/time properties
        if any(word in prop_name_lower for word in ['date', 'time', 'datetime', 'created', 'modified']):
            return 'datetime'
        
        # Boolean properties
        if (prop_name_lower.startswith('is') or prop_name_lower.startswith('has') or 
            prop_name_lower.startswith('can') or prop_name_lower.startswith('should') or
            any(word in summary_lower for word in ['true', 'false', 'boolean', 'whether'])):
            return 'bool'
        
        # String properties
        if (any(word in prop_name_lower for word in ['name', 'text', 'description', 'comment', 'note', 'id', 'uid']) or
            any(word in summary_lower for word in ['string', 'text', 'name', 'identifier'])):
            return 'str'
        
        # Numeric properties
        if (any(word in prop_name_lower for word in ['count', 'number', 'size', 'length', 'width', 'height', 'dose', 'value']) or
            any(word in summary_lower for word in ['number', 'count', 'value', 'dose', 'percentage'])):
            if 'dose' in prop_name_lower or 'dose' in summary_lower:
                return 'DoseValue'  # Specific ESAPI type
            return 'float'
        
        # Collection properties
        if (prop_name.endswith('s') and not prop_name.endswith('Status') and 
            any(word in summary_lower for word in ['collection', 'list', 'array', 'enumerable'])):
            return 'List[Any]'
        
        # Look for type references in summary (e.g., "See <see cref="T:VMS.TPS.Common.Model.Types.DoseValue"/>")
        type_match = re.search(r'<see cref="T:([^"]+)"', summary)
        if type_match:
            full_type = type_match.group(1)
            if full_type.startswith('VMS.TPS.Common.Model'):
                return full_type.split('.')[-1]  # Return just the class name
            return self._convert_csharp_type_to_python(full_type)
        
        return 'Any'
    
    def _write_method_stub(self, f, method: XmlApiElement, is_overload: bool = False):
        """Write a method stub"""
        if method.summary:
            f.write(f'    # {method.summary}\n')
        
        # Build parameter list using actual extracted types
        param_list = []
        for param in method.parameters:
            param_type = param.get('type', 'Any')
            param_list.append(f"{param['name']}: {param_type}")
        
        param_str = ", ".join(param_list)
        if param_str:
            param_str = ", " + param_str
        
        # Use DLL-enhanced return type if available, otherwise infer from summary
        if method.return_type and method.return_type != "Any":
            return_type = method.return_type
        else:
            return_type = self._infer_return_type_from_summary(method.summary)
        
        # Add @overload decorator for constructors only when there are multiple overloads
        if method.name == '__init__':
            if is_overload:
                f.write(f'    @overload\n')
            f.write(f'    def {method.name}(self{param_str}) -> None:\n')
        else:
            f.write(f'    def {method.name}(self{param_str}) -> {return_type}:\n')
        
        # Add Google style docstring with parameter descriptions if available
        param_docs = []
        if hasattr(method, 'param_descriptions') and method.param_descriptions:
            for param in method.parameters:
                param_name = param['name']
                if param_name in method.param_descriptions and method.param_descriptions[param_name]:
                    param_docs.append(f"            {param_name}: {method.param_descriptions[param_name]}")
        
        if param_docs:
            f.write('        """\n')
            f.write("        Args:\n")
            f.write('\n'.join(param_docs) + '\n')
            f.write('        """\n')
            f.write("        ...\n\n")
        else:
            f.write("        ...\n\n")
    
    def _write_nested_type_stub(self, f, nested_type: XmlApiElement):
        """Write a nested type (like enum or inner class)"""
        # Extract the nested type name (e.g., "Component" from "VVector.Component")
        nested_name = nested_type.name.split('.')[-1]
        
        if nested_type.summary:
            f.write(f'    # {nested_type.summary}\n')
        
        f.write(f'    class {nested_name}:\n')
        if nested_type.summary:
            f.write('        """\n')
            f.write(f'        {nested_type.summary}\n')
            f.write('        """\n')
        f.write('        pass\n')

    def _infer_type_from_summary(self, summary: str) -> str:
        """Infer type from summary text"""
        if not summary:
            return "Any"
        
        summary_lower = summary.lower()
        
        # Common type patterns
        if 'string' in summary_lower or 'text' in summary_lower:
            return 'str'
        elif 'number' in summary_lower or 'count' in summary_lower or 'size' in summary_lower:
            return 'int'
        elif 'date' in summary_lower or 'time' in summary_lower:
            return 'datetime'
        elif 'bool' in summary_lower or 'whether' in summary_lower or 'indicates' in summary_lower:
            return 'bool'
        elif 'list' in summary_lower or 'collection' in summary_lower or 'array' in summary_lower:
            return 'List[Any]'
        
        return "Any"
    
    def _infer_return_type_from_summary(self, summary: str) -> str:
        """Infer return type from method summary"""
        if not summary:
            return "Any"
        
        summary_lower = summary.lower()
        
        if 'returns' in summary_lower:
            # Try to extract type info after "returns"
            if 'string' in summary_lower:
                return 'str'
            elif 'bool' in summary_lower or 'whether' in summary_lower:
                return 'bool'
            elif 'number' in summary_lower or 'count' in summary_lower:
                return 'int'
        
        # Method name patterns
        if summary_lower.startswith('gets') or summary_lower.startswith('retrieves'):
            return self._infer_type_from_summary(summary)
        elif summary_lower.startswith('sets') or summary_lower.startswith('converts'):
            return 'None'
        
        return "Any"

def find_xml_files(library_folder: str) -> List[str]:
    """Find all XML documentation files in the library folder"""
    xml_files = []
    library_path = Path(library_folder)
    
    if not library_path.exists():
        print(f"Warning: Library folder does not exist: {library_folder}")
        return xml_files
    
    # Search for .xml files in the specified folder only
    for xml_file in library_path.glob("*.xml"):
        xml_files.append(str(xml_file))
    
    return xml_files

def find_dll_files(library_folder: str) -> List[str]:
    """Find all DLL files in the library folder"""
    dll_files = []
    library_path = Path(library_folder)
    
    if not library_path.exists():
        print(f"Warning: Library folder does not exist: {library_folder}")
        return dll_files
    
    # Search for .dll files in the specified folder only
    for dll_file in library_path.glob("*.dll"):
        dll_files.append(str(dll_file))
    
    return dll_files

def main():
    if len(sys.argv) < 2:
        print("Usage: python dotnet_to_stubs.py <library_folder> [output_folder]")
        print("  library_folder: Folder containing XML documentation and DLL files")
        print("  output_folder: Output folder for generated stubs (default: stubs)")
        print("Example: python dotnet_to_stubs.py C:/ARIA/bin stubs")
        sys.exit(1)
    
    library_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else "stubs"
    
    # Find XML and DLL files in the library folder
    print(f"Scanning library folder: {library_folder}")
    xml_files = find_xml_files(library_folder)
    dll_files = find_dll_files(library_folder)
    
    if not xml_files:
        print(f"No XML documentation files found in {library_folder}")
        sys.exit(1)
    
    print(f"Found {len(xml_files)} XML file(s):")
    for xml_file in xml_files:
        print(f"  - {xml_file}")
    
    print(f"Found {len(dll_files)} DLL file(s):")
    for dll_file in dll_files:
        print(f"  - {dll_file}")
    
    # Process each XML file
    all_elements = []
    parser = XmlDocumentationParser(dll_files)
    
    for xml_file in xml_files:
        print(f"\nProcessing XML file: {xml_file}")
        elements = parser.parse_xml_file(xml_file)
        
        if elements:
            all_elements.extend(elements)
            print(f"  Found {len(elements)} API elements")
        else:
            print(f"  No elements found in {xml_file}")
    
    if not all_elements:
        print("No elements found in any XML files")
        sys.exit(1)
    
    print(f"\nTotal elements found: {len(all_elements)}")
    
    # Generate stubs
    generator = XmlStubGenerator(parser)
    generator.generate_stubs(output_folder)

if __name__ == "__main__":
    main()
