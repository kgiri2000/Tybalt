import ast
import inspect


#Basic Parsing and Inspection
code = """
def greet(name):
    message = f"Hello, {name}!"
    return message

result = greet("World")
"""

# Parse the code into an AST
tree = ast.parse(code)

# View the AST structure
print("=" * 50)
print("EXAMPLE 1: AST Structure")
print("=" * 50)
print(ast.dump(tree, indent=2))
print("\n")



# EXAMPLE 2: Using NodeVisitor to Analyze Code
class FunctionAnalyzer(ast.NodeVisitor):
    """Visitor that finds all function definitions"""
    
    def __init__(self):
        self.functions = []
        self.variables = []
        
    def visit_FunctionDef(self, node):
        """Called when a function definition is encountered"""
        func_info = {
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'lineno': node.lineno
        }
        self.functions.append(func_info)
        # Continue visiting child nodes
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """Called when an assignment is encountered"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.append(target.id)
        self.generic_visit(node)

print("=" * 50)
print("EXAMPLE 2: Analyzing Functions and Variables")
print("=" * 50)

analyzer = FunctionAnalyzer()
analyzer.visit(tree)

print(f"Functions found: {analyzer.functions}")
print(f"Variables assigned: {analyzer.variables}")
print("\n")



# EXAMPLE 3: Transforming Code with NodeTransformer
class NameReplacer(ast.NodeTransformer):
    """Replaces variable names in the AST"""
    
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name
    
    def visit_Name(self, node):
        """Replace name nodes"""
        if node.id == self.old_name:
            node.id = self.new_name
        return node

print("=" * 50)
print("EXAMPLE 3: Code Transformation")
print("=" * 50)

simple_code = "x = 5\ny = x + 10\nprint(x)"
print(f"Original code:\n{simple_code}\n")

tree2 = ast.parse(simple_code)
transformer = NameReplacer('x', 'my_variable')
new_tree = transformer.visit(tree2)

# Fix missing locations after transformation
ast.fix_missing_locations(new_tree)

# Convert back to code
new_code = ast.unparse(new_tree)
print(f"Transformed code:\n{new_code}")
print("\n")



# EXAMPLE 4: Extracting All Function Calls
class CallExtractor(ast.NodeVisitor):
    """Extract all function calls from code"""
    
    def __init__(self):
        self.calls = []
    
    def visit_Call(self, node):
        """Called when a function call is encountered"""
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.append(f"{ast.unparse(node.func.value)}.{node.func.attr}")
        self.generic_visit(node)

complex_code = """
import math
x = math.sqrt(16)
y = len([1, 2, 3])
result = max(x, y)
print(result)
"""

print("=" * 50)
print("EXAMPLE 4: Extracting Function Calls")
print("=" * 50)
print(f"Code:\n{complex_code}")

tree3 = ast.parse(complex_code)
extractor = CallExtractor()
extractor.visit(tree3)
print(f"Function calls found: {extractor.calls}")
print("\n")



# EXAMPLE 5: Building AST Programmatically
print("=" * 50)
print("EXAMPLE 5: Building AST from Scratch")
print("=" * 50)

# Create: def add(a, b): return a + b
func_def = ast.FunctionDef(
    name='add',
    args=ast.arguments(
        args=[ast.arg(arg='a'), ast.arg(arg='b')],
        posonlyargs=[],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[]
    ),
    body=[
        ast.Return(
            value=ast.BinOp(
                left=ast.Name(id='a', ctx=ast.Load()),
                op=ast.Add(),
                right=ast.Name(id='b', ctx=ast.Load())
            )
        )
    ],
    decorator_list=[]
)

# Wrap in a Module node
module = ast.Module(body=[func_def], type_ignores=[])
ast.fix_missing_locations(module)

# Convert to source code
generated_code = ast.unparse(module)
print(f"Generated code:\n{generated_code}")

# Compile and execute
code_obj = compile(module, filename="<ast>", mode="exec")
namespace = {}
exec(code_obj, namespace)
print(f"Executing add(5, 3): {namespace['add'](5, 3)}")
print("\n")



# EXAMPLE 6: Advanced Analysis - Complexity
class ComplexityAnalyzer(ast.NodeVisitor):
    """Calculate cyclomatic complexity"""
    
    def __init__(self):
        self.complexity = 1  # Base complexity
    
    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

complex_func = """
def process_data(data):
    if data is None:
        return None
    
    for item in data:
        if item > 0:
            try:
                result = item * 2
            except:
                result = 0
        else:
            result = -1
    
    while result < 100:
        result += 10
    
    return result
"""

print("=" * 50)
print("EXAMPLE 6: Cyclomatic Complexity")
print("=" * 50)
print(f"Code:\n{complex_func}")

tree4 = ast.parse(complex_func)
complexity_analyzer = ComplexityAnalyzer()
complexity_analyzer.visit(tree4)
print(f"Cyclomatic Complexity: {complexity_analyzer.complexity}")
print("\n")



# EXAMPLE 7: Finding Imports
class ImportFinder(ast.NodeVisitor):
    """Find all imports in code"""
    
    def __init__(self):
        self.imports = []
    
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                'type': 'import',
                'module': alias.name,
                'alias': alias.asname
            })
    
    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.append({
                'type': 'from',
                'module': node.module,
                'name': alias.name,
                'alias': alias.asname
            })

import_code = """
import os
import sys as system
from pathlib import Path
from collections import defaultdict as dd
"""

print("=" * 50)
print("EXAMPLE 7: Import Analysis")
print("=" * 50)

tree5 = ast.parse(import_code)
import_finder = ImportFinder()
import_finder.visit(tree5)
for imp in import_finder.imports:
    print(f"  {imp}")
print("\n")



# EXAMPLE 8: Safety Checker
class SafetyChecker(ast.NodeVisitor):
    """Check for potentially unsafe operations"""
    
    def __init__(self):
        self.unsafe_operations = []
    
    def visit_Call(self, node):
        # Check for eval, exec, __import__
        if isinstance(node.func, ast.Name):
            if node.func.id in ['eval', 'exec', '__import__']:
                self.unsafe_operations.append({
                    'operation': node.func.id,
                    'line': node.lineno
                })
        self.generic_visit(node)

unsafe_code = """
user_input = input("Enter code: ")
eval(user_input)
exec("print('hello')")
"""

print("=" * 50)
print("EXAMPLE 8: Safety Analysis")
print("=" * 50)

tree6 = ast.parse(unsafe_code)
safety_checker = SafetyChecker()
safety_checker.visit(tree6)
print(f"Unsafe operations found: {safety_checker.unsafe_operations}")
print("\n")

print("=" * 50)
print("Summary: AST is powerful for:")
print("  - Static code analysis")
print("  - Code transformation")
print("  - Building DSLs")
print("  - Metaprogramming")
print("  - Linting and security checks")
print("=" * 50)