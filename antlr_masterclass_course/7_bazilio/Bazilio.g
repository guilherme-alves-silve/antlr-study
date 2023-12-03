grammar Bazilio;

root: procdef*;

procdef: PROCEDURE VAR* LB instructions RB;
instructions: instruction*;
instruction: (assignment | input | output)
           | (reproduction | conditional | while)
           | (proc | addinglist | cutlist)
           ;

assignment: VAR ASSIGN expr;
input: INPUT VAR;
output: OUTPUT expr+;
conditional: 'if' expr LB instructions RB ('elif' expr LB instructions RB)* ('else' LB instructions RB)?;
while: 'while' expr LB instructions RB;
reproduction: REPROD expr;
proc: PROCEDURE expr*;
addinglist: VAR ADDL expr;
cutlist: CUTL query;

expr: expr POW expr
    | expr MUL expr
    | expr DIV expr
    | expr MOD expr
    | expr ADD expr
    | expr SUB expr
    | expr EQ expr
    | expr GT expr
    | expr LT expr
    | expr GTE expr
    | expr LTE expr
    | expr DIF expr
    | NUM
    | VAR
    | STRING
    | initlist
    | sizelist
    | query
    | NOTE
    | LP expr RP
    ;

query: VAR LK expr RK;
sizelist: SIZELIST VAR;
initlist: '{' expr* '}';

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
POW: ('^'|'**');
MOD: '%';
EQ: '=';
GT: '>';
LT: '<';
GTE: '>=';
LTE: '<=';
DIF: ('!='|'<>');
SIZELIST: '#';
NUM: [-]?[0-9]+('.'[0-9]+)?;
VAR: [a-z]+[a-zA-Z0-9]*;
STRING: '"' ( '\\' . | ~('\\'|'"'))* '"';
ASSIGN: '<-';
INPUT: '<?>';
OUTPUT: '<w>';
REPROD: '(:)';
NOTE: [A-G][0-9]*;
PROCEDURE: [A-Z][a-z0-9]*;
ADDL: '<<';
CUTL: '|<';

LB: '|:';
RB: ':|';
LK: '[';
RK: ']';
LP: '(';
RP: ')';

COMMENT: '###' ~[\r\n]* -> skip;
WS: [ \r\n] -> skip;
