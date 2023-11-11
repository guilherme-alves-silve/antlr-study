# ANTLR Study

How to create programming languages and interpreters from scratch

- [ ] [ANTLR Programming Masterclass with Python](https://www.udemy.com/course/antlr-programming-masterclass-with-python)
    1. Course introduction
      - antlr_masterclass_course/
    2. Compiler Fundamentals
    3. ANTLR4 and Python3 installation
    4. Introduction to ANTLR
    5. Elementary Interpreters
    6. Interpreter with Variables
    7. Interpreter with Condition Recognition
    8. Interpreters with While
    9. Final Programming Language
- [ ] [Build SQL parser using ANTLR4](https://github.com/codersasi/pocketsDB)
  1. [Build SQL parser using ANTLR4 -Part1](https://medium.com/@sasidharc/build-sql-parser-using-antlr4-part1-2044916a8406)
  2. [Build SQL parser using ANTLR4 -Part2](https://medium.com/@sasidharc/build-sql-parser-using-antlr4-part2-1f8cdb011721)

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
