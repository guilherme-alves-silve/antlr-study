grammar Bazilio;

root: procDef*;

procDef: PROCEDURE paramsId LB instructions RB;
instructions: instruction*;
instruction: (assignment | input | output)
           | (reproduction | conditional | while)
           | (proc | addingList | cutList)
           ;

assignment: VAR ASSIGN expr;
input: INPUT VAR;
output: OUTPUT expr+;
conditional: 'if' expr LB instructions RB ('elif' expr LB instructions RB)* ('else' LB instructions RB)?;
while: 'while' expr LB instructions RB;
reproduction: REPROD expr;
proc: PROCEDURE paramsExpr;
addingList: VAR ADDL expr;
cutList: CUTL VAR LK expr RK;

expr: expr POW expr # Pow
    | expr MUL expr # Mul
    | expr DIV expr # Div
    | expr MOD expr # Mod
    | expr ADD expr # Add
    | expr SUB expr # Sub
    | expr EQ expr  # Eq
    | expr GT expr  # Gt
    | expr LT expr  # Lt
    | expr GTE expr # Gte
    | expr LTE expr # Lte
    | expr DIF expr # Dif
    | NUM           # Num
    | VAR           # Var
    | STRING        # String
    | '{' expr* '}' # InitList
    | SIZELIST VAR  # SizeList
    | query         # EvalQuery
    | NOTE          # Note
    | LP expr RP    # SubExpr
    ;

query: VAR LK expr RK;
paramsId: VAR*;
paramsExpr: expr*;

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
REPROD: ('(:)'|'<:>');
NOTE: [A-G][0-9]?;
PROCEDURE: [A-Z][a-zA-Z0-9]*;
ADDL: '<<';
CUTL: ('|<'|'8<');

LB: '|:';
RB: ':|';
LK: '[';
RK: ']';
LP: '(';
RP: ')';

COMMENT: '###' ~[\r\n]* -> skip;
WS: [ \r\n] -> skip;
