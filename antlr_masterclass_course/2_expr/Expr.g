grammar Expr;

root: expr EOF;

expr: expr MUL expr  # Mul
    | expr DIV expr  # Div
    | expr PLUS expr # Plus
    | expr SUB expr  # Sub
    | NUM            # Num
    ;

NUM: [0-9]+;
MUL: '*';
DIV: '/';
PLUS: '+';
SUB: '-';
WS: [ \n] -> skip;
