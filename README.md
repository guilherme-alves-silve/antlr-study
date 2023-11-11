# ANTLR Study

How to create programming languages and interpreters from scratch

- [ ] [ANTLR Programming Masterclass with Python](https://www.udemy.com/course/antlr-programming-masterclass-with-python)
    - Course introduction
    - Compiler Fundamentals
    - ANTLR4 and Python3 installation
    - Introduction to ANTLR
    - Elementary Interpreters
    - Interpreter with Variables
    - Interpreter with Condition Recognition
    - Interpreters with While
    - Final Programming Language

## Linux

`antlr4 -Dlanguage=Python3 -no-listener -visitor Expr.g`

## Windows CMD
```
CLASSPATH=.;%ANTLR4_PATH%\antlr.jar
antlr4 -Dlanguage=Python3 -no-listener -visitor Expr.g
```

## Windows Git Bash
```
CLASSPATH=.;%ANTLR4_PATH%\antlr.jar
antlr4.bat -Dlanguage=Python3 -no-listener -visitor Expr.g
```
