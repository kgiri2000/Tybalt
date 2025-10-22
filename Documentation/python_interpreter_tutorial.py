

print("*"*20)
#Tokenizer
print("Tokenizer")
import tokenize
from io import BytesIO

code = b"x = 2\ny = 3\nprint(x + y)"
for token in tokenize.tokenize(BytesIO(code).readline):
    print(token)

print("*"*20)


#Parsing(AST)
print("Parsing")
import ast
tree = ast.parse("print(x + y)")
print(ast.dump(tree, indent=2))
print("*" * 50)


#Compilation to Bytecode
print("Compilation to Bytecode")
code_obj = compile("x = 2; y = 3; print(x + y)", "<string>", "exec")
print(code_obj)
print("*" * 50)
import dis
dis.dis(code_obj)
