Python Interpreter is the program that reads and execute Python code. 
It translates Python codes into machine-readable form line by line, so the computer can understand and 
run them.
---
When we run the Python programs:
    - Checks the code for the errors
    - Converts the code into an intermediate form called bytecode
    - Sends to Python Virtual Environment(PVM) for execution.

---
Working of the Interpreter:
    1. Source Input (.py text)
    2. Lexical Analysis(Splits text into tokens)
    3. Parsing( Converts tokens -> Abstract Syntax Tree (AST))
    4. Bytecode Compilation( Compile  AST -> Python bytecode)
    5.Execution(Evaluation Loop) PVM executes bytecode
    6.  Memory Management And GC( Objects created, reference-counted or collected)
---
1. Source code
`
x = 2
y = 2
print(x+y)
`
---

2. Lexical Analysis
