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

`x=2 y= 2 print(x+y)`
---

2. Lexical Analysis

The interpreter reads the file line by line.
The built in lexer scans characters and group them in meaningful sequences;
`x,=,2,NEWLINE, y, =, 3, NEWLINE,.....`

These are tokens.

| Token type | Value|
|-----|-----|
|NAME| x|
|OP|=|
|NUMBER|2|
|NEWLINE|\n|
|....|....|

Python has tokenizer module that does this:

```python
{
    import tokenize
    code = b"x=2\ny=3\nprint(x+y)"
    for token in tokenize.tokenize(BytesIO(code).readline):
        print(token)
}
```

Output:
```python
Tokenizer
TokenInfo(type=63 (ENCODING), string='utf-8', start=(0, 0), end=(0, 0), line='')
TokenInfo(type=1 (NAME), string='x', start=(1, 0), end=(1, 1), line='x = 2\n')
TokenInfo(type=54 (OP), string='=', start=(1, 2), end=(1, 3), line='x = 2\n')
TokenInfo(type=2 (NUMBER), string='2', start=(1, 4), end=(1, 5), line='x = 2\n')
TokenInfo(type=4 (NEWLINE), string='\n', start=(1, 5), end=(1, 6), line='x = 2\n')
```

3. Parsing(Building AST )
    Parser takes the stream of tokens and construct an Abstract Syntax tree- structures, hierarchical represerntation of the code's 
    grammatical meaning.

    For example print(x+y) becomes:

    ```python
        Call(
            func=Name(id='print', ctx = Load())
            args=[
                BinOp(
                    left = Name('id'='x', ctx=Load()),
                    op=Add(),
                    right=Name(id='y', ctx=Load())
                )
            ],
            keywords = []
        )
    ```
    Python uses LL(1) or PEG-style parsing 
    The grammar rules are defined in /Grammar/python.gram
    Errors like SyntaxError occur  if something doesn't follow the grammar.

    Code:
    ```python
        import ast
        tree = ast.parse("print(x+y)")
        print(ast.dump(tree, indent=2))
    ```
    Output:

    ```python
                Module(
        body=[
            Expr(
            value=Call(
                func=Name(id='print', ctx=Load()),
                args=[
                BinOp(
                    left=Name(id='x', ctx=Load()),
                    op=Add(),
                    right=Name(id='y', ctx=Load()))],
                keywords=[]))],
        type_ignores=[])
    ```

4. Compilation to Bytecode

    Once parsing is completed the interpreter compiles the AST into bytescode, a sequence of low-levl instructions for the PVM.
    Following happens during the compiler case:
    - Each node in the AST is walked.
    - Corresponding opcodes(operation codes) are generated.
    - The result is code object, containing:
        - co_code(bytecode)
        - co_consts(constants)
        - co_names(variable/function names)
        - co_varnames, co_filename, etc

    Example:

    ```python
        code_obj =  compile("x=2; y= 3; print(x+y)", "<string>", "exec")
        print(code_obj)
    ``` 
    Output:
        `<code object <module> at 0x7c4209f44b30, file "<string>", line 1>`
    
    Bytecode:

    ```python
        import dis
        dis.dis(code_obj)
    ```

    Output
    ```python
          1           0 LOAD_CONST               0 (2)
              2 STORE_NAME               0 (x)
              4 LOAD_CONST               1 (3)
              6 STORE_NAME               1 (y)
              8 LOAD_NAME                2 (print)
             10 LOAD_NAME                0 (x)
             12 LOAD_NAME                1 (y)
             14 BINARY_ADD
             16 CALL_FUNCTION            1
             18 POP_TOP
             20 LOAD_CONST               2 (None)
             22 RETURN_VALUE
    ```

    Each opcode represents one virtual machine instruction.
    