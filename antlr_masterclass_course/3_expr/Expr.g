grammar Expr;

root: action+ EOF;

action: NAME ':=' expr
      | 'write' NAME
      ;

expr: <assoc=right> expr '^' expr
    | expr ('*'|'/') expr
    | expr ('+'|'-') expr
    | NUM
    ;

NAME: [a-zA-Z]+;
NUM: [0-9]+;
WS: [ \n\r]+ -> skip;
