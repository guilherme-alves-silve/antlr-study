# [ANTLR](https://github.com/antlr/antlr4) Study

How to create programming languages and interpreters from scratch

## Technology

- [ANTLR4](https://github.com/antlr/antlr4)
- [Python 3+](https://www.python.org/)
- [LilyPond](https://lilypond.org/)
- [FFmpeg](https://ffmpeg.org/)

## Summary

- [ ] [ANTLR Programming Masterclass with Python](https://www.udemy.com/course/antlr-programming-masterclass-with-python)
  - Course introduction
  - Compiler Fundamentals
  - ANTLR4 and Python3 installation
    - doc/
  - Introduction to ANTLR
    - antlr_masterclass_course/1_expr/
  - Elementary Interpreters
    - antlr_masterclass_course/2_expr/
  - Interpreter with Variables
    - antlr_masterclass_course/3_expr/
  - Interpreter with Condition Recognition
    - antlr_masterclass_course/4_expr/
    - antlr_masterclass_course/5_expr/
  - Interpreters with While
    - antlr_masterclass_course/6_lang/
  - Final Programming Language
    - antlr_masterclass_course/7_bazilio/
- [ ] [Build SQL parser using ANTLR4](https://github.com/codersasi/pocketsDB)
  - [Build SQL parser using ANTLR4 -Part1](https://medium.com/@sasidharc/build-sql-parser-using-antlr4-part1-2044916a8406)
  - [Build SQL parser using ANTLR4 -Part2](https://medium.com/@sasidharc/build-sql-parser-using-antlr4-part2-1f8cdb011721)

## Linux

`antlr4 -Dlanguage=Python3 -no-listener -visitor Expr.g`
`antlr4 -Dlanguage=Python3 -no-listener -visitor Lang.g`
`antlr4 -Dlanguage=Python3 -no-listener -visitor YourLanguageNameHere.g`

## Windows CMD
```
CLASSPATH=.;%ANTLR4_PATH%\antlr.jar
antlr4 -Dlanguage=Python3 -no-listener -visitor Expr.g
antlr4 -Dlanguage=Python3 -no-listener -visitor Lang.g
antlr4 -Dlanguage=Python3 -no-listener -visitor YourLanguageNameHere.g
```

## Windows Git Bash
```
CLASSPATH=.;%ANTLR4_PATH%\antlr.jar
antlr4.bat -Dlanguage=Python3 -no-listener -visitor Expr.g
antlr4.bat -Dlanguage=Python3 -no-listener -visitor Lang.g
antlr4.bat -Dlanguage=Python3 -no-listener -visitor YourLanguageNameHere.g
```
