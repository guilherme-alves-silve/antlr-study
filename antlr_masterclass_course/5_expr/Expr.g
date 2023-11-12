grammar Expr;

root: action+ EOF;

action: 'iff' expr action ('otherwise' action)? # Condition
      | NAME ':=' expr                          # Value
      | 'write' (expr|NAME)                     # Write
      | 'next' expr                             # Next
      ;

expr: <assoc=right> expr POW expr # Pow
    | expr MUL expr               # Mul
    | expr DIV expr               # Div
    | expr ADD expr               # Add
    | expr SUB expr               # Sub
    | expr EQ  expr               # Eq
    | expr DIF expr               # Dif
    | expr GT  expr               # Gt
    | expr LT  expr               # Lt
    | NUM                         # Num
    ;

POW:  ('^'|'**');
MUL:  '*';
DIV:  '/';
ADD:  '+';
SUB:  '-';
EQ:   '==';
DIF:  ('!='|'<>');
GT:   '>';
LT:   '<';
NUM:  [0-9]+;
NAME: [a-zA-Z]+;
WS:  [ \t\r\n] -> skip;
