grammar Lang;

root: instructions* EOF;

instructions: instruction+;

instruction: (while | output | assign);

while: 'while' expr instructions ('break')?;

output: 'send' expr;

assign: VAR ASSIGN expr;

expr: expr ADD expr # Add
    | expr SUB expr # Sub
    | expr GT expr  # Gt
    | expr LT expr  # Lt
    | expr EQ expr  # Eq
    | VAR           # Var
    | NUM           # Num
    ;

ADD: '+';
SUB: '-';
GT:  '>';
LT:  '<';
EQ:  '==';
VAR: [a-zA-Z][a-zA-Z0-9]*;
NUM: [0-9]+;
ASSIGN: '<-';
WS:  [ \t\r\n] -> skip;
