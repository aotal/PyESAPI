#!/usr/bin/env python3
"""
XML Documentation to Python Stub Generator
Generates Python type stubs (.pyi) from .NET XML documentation files

Usage:
    python xml_to_stubs.py <xml_file> [out        # Handle malformed generic types like VRect{`0} -> VRect[T]
        malformed_generic = re.match(r'([^{<]+)[{<](`+\d+)[}>]', csharp_type)
        if malformed_generic:
            base_name = malformed_generic.group(1).split('.')[-1]
            param_ref = malformed_generic.group(2)
            param_num = int(re.search(r'\d+', param_ref).group())
            param_name = 'T' if param_num == 0 else f'T{param_num + 1}'
            return f'{base_name}[{param_name}]'
        
        # Handle full namespace generic types like VMS.TPS.Common.Model.Types.VRect{`0}
        namespace_generic = re.match(r'(VMS\.TPS\.Common\.Model\.[^{<]+)[{<](`+\d+)[}>]', csharp_type)
        if namespace_generic:
            full_type = namespace_generic.group(1)
            base_name = full_type.split('.')[-1]
            param_ref = namespace_generic.group(2)
            param_num = int(re.search(r'\d+', param_ref).group())
            param_name = 'T' if param_num == 0 else f'T{param_num + 1}'
            return f'{base_name}[{param_name}]'er]
"""

import os
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

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
        
        # Handle generic types and nested commas - work with original curly braces
        params = []
        current_param = ""
        bracket_depth = 0
        
        for char in params_str + ',':  # Add comma at end to process last param
            if char in '<{':
                bracket_depth += 1
                current_param += char
            elif char in '>}':
                bracket_depth -= 1
                current_param += char
            elif char == ',' and bracket_depth == 0:
                if current_param.strip():
                    params.append(current_param.strip())
                current_param = ""
            else:
                current_param += char
        
        return params
    
    def _convert_csharp_type_to_python(self, csharp_type: str, preserve_net_types: bool = False) -> str:
        """Convert C# type to Python type"""
        # Remove ref/out keywords
        csharp_type = re.sub(r'\b(ref|out)\s+', '', csharp_type)
        
        # Handle curly braces in the entire string recursively
        while '{' in csharp_type and '}' in csharp_type:
            csharp_type = csharp_type.replace('{', '<').replace('}', '>')
        
        # Handle C# generic type syntax with backticks (e.g., VRect`1 -> VRect[T])
        # Only match when backtick immediately follows the class name (not inside angle brackets)
        if '`' in csharp_type and '<' not in csharp_type:
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
                if base_type in ['System.Collections.Generic.List', 'System.Collections.Generic.IList', 
                               'System.Collections.Generic.ICollection', 'System.Collections.Generic.IEnumerable']:
                    arg_type = self._convert_csharp_type_to_python(generic_args, preserve_net_types)
                    return f'List[{arg_type}]'
                elif base_type in ['System.Collections.Generic.Dictionary', 'System.Collections.Generic.IDictionary']:
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
    
    def __init__(self):
        self.elements: List[XmlApiElement] = []
        self.types_by_namespace: Dict[str, List[XmlApiElement]] = defaultdict(list)
        self.members_by_class: Dict[str, List[XmlApiElement]] = defaultdict(list)
    
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
                
                elements.append(element)
                self.elements.append(element)
            
            print(f"Found {len(elements)} API elements")
            self._organize_elements()
            
            return elements
            
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            return []
    
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
            
            # Create __init__.py
            init_file = current_path / "__init__.py"
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
            
            # Write common array type aliases
            f.write("# Common array type aliases for Python.NET\n")
            f.write("DoubleArray = Array[Double]\n")
            f.write("SingleArray = Array[Single]\n") 
            f.write("IntArray = Array[Int32]\n")
            f.write("BoolArray = Array[Boolean]\n")
            f.write("StringArray = Array[String]\n")
            f.write("DoubleJaggedArray = Array[DoubleArray]\n")
            f.write("SingleJaggedArray = Array[SingleArray]\n")
            
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
        
        # Try to infer type from property name and summary
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
        
        # Infer return type from summary if available, otherwise use Any
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python xml_to_stubs.py <xml_file> [output_folder]")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else "xml_stubs"
    
    # Parse XML documentation
    parser = XmlDocumentationParser()
    elements = parser.parse_xml_file(xml_file)
    
    if not elements:
        print("No elements found in XML file")
        sys.exit(1)
    
    # Generate stubs
    generator = XmlStubGenerator(parser)
    generator.generate_stubs(output_folder)

if __name__ == "__main__":
    main()
