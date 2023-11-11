grammar Expr;

root: expr EOF;

expr: expr PLUS expr
    | expr SUB expr
    | NUM
    ;

NUM: [0-9]+;
PLUS: '+';
SUB: '-';
WS: [ \n] -> skip;
