grammar Pascal;

@header {
    package antlr4;
    import java.util.HashMap;
    import edu.yu.compilers.intermediate.symtable.SymTableEntry;
    import edu.yu.compilers.intermediate.type.Typespec;
}

program           : programHeader block '.' ;
programHeader     : PROGRAM programIdentifier programParameters? ';' ; 
programParameters : '(' IDENTIFIER ( ',' IDENTIFIER )* ')' ;

programIdentifier   locals [ SymTableEntry entry = null ]
    : IDENTIFIER ;

block         : declarations compoundStatement ;
declarations  : ( constantsPart ';' )? ( typesPart ';' )? 
                ( variablesPart ';' )? ( routinesPart ';')? ;

constantsPart           : CONST constantDefinitionsList ;
constantDefinitionsList : constantDefinition ( ';' constantDefinition )* ;
constantDefinition      : constantIdentifier '=' constant ;

constantIdentifier  locals [ Typespec type = null, SymTableEntry entry = null ]
    : IDENTIFIER ;

constant            locals [ Typespec type = null, Object value = null ]  
    : sign? ( IDENTIFIER | unsignedNumber )
    | characterConstant
    | stringConstant
    ;

sign : '-' | '+' ;

typesPart           : TYPE typeDefinitionsList ;
typeDefinitionsList : typeDefinition ( ';' typeDefinition )* ;
typeDefinition      : typeIdentifier '=' typeSpecification ;

typeIdentifier      locals [ Typespec type = null, SymTableEntry entry = null ]
    : IDENTIFIER ;

typeSpecification   locals [ Typespec type = null ]
    : simpleType        # simpleTypespec
    | arrayType         # arrayTypespec 
    | recordType        # recordTypespec
    ;

simpleType          locals [ Typespec type = null ] 
    : typeIdentifier    # typeIdentifierTypespec 
    | enumerationType   # enumerationTypespec
    | subrangeType      # subrangeTypespec
    ;
           
enumerationType     : '(' enumerationConstant ( ',' enumerationConstant )* ')' ;
enumerationConstant : constantIdentifier ;
subrangeType        : constant '..' constant ;

arrayType
    : ARRAY '[' arrayDimensionList ']' OF typeSpecification ;
arrayDimensionList : simpleType ( ',' simpleType )* ;

recordType          locals [ SymTableEntry entry = null ]   
    : BLUEPRINT '{' recordFields ';'? '}' ;
recordFields : variableDeclarationsList ;
           
variablesPart            : VAR variableDeclarationsList ;
variableDeclarationsList : variableDeclarations ( ';' variableDeclarations )* ;
variableDeclarations     : variableIdentifierList ':' typeSpecification ;
variableIdentifierList   : variableIdentifier ( ',' variableIdentifier )* ;

variableIdentifier  locals [ Typespec type = null, SymTableEntry entry = null ] 
    : IDENTIFIER ;

routinesPart      : routineDefinition ( ';' routineDefinition)* ;
routineDefinition : ( procedureHead | functionHead ) ';' block ;
procedureHead     : PROCEDURE routineIdentifier parameters? ;
functionHead      : FUNCTION  routineIdentifier parameters? ':' typeIdentifier ;

routineIdentifier   locals [ Typespec type = null, SymTableEntry entry = null ]
    : IDENTIFIER ;

parameters                : '(' parameterDeclarationsList ')' ;
parameterDeclarationsList : parameterDeclarations ( ';' parameterDeclarations )* ;
parameterDeclarations     : VAR? parameterIdentifierList ':' typeIdentifier ;
parameterIdentifierList   : parameterIdentifier ( ',' parameterIdentifier )* ;

parameterIdentifier   locals [ Typespec type = null, SymTableEntry entry = null ]
    : IDENTIFIER ;

statement : compoundStatement
          | assignmentStatement
          | ifStatement
          | caseStatement
          | repeatStatement
          | whileStatement
          | forStatement
          | writeStatement
          | writelnStatement
          | readStatement
          | readlnStatement
          | procedureCallStatement
          | emptyStatement
          ;

compoundStatement : BEGIN statementList END ;
emptyStatement : ;
     
statementList       : statement ( ';' statement )* ;
assignmentStatement : lhs ':=' rhs ;

lhs locals [ Typespec type = null ] 
    : variable ;
rhs : expression ;

ifStatement    : IF expression IS TRUE DO trueStatement ( ELSE falseStatement )? ( ELSE JUST DO falseStatement)? ;
trueStatement  : statement ;
falseStatement : statement ;

caseStatement
    locals [ HashMap<Object, PascalParser.StatementContext> jumpTable = null ]
    : IF expression caseBranchList (DEFAULT DO statement';')? ;
    
caseBranchList   : caseBranch ( ';' caseBranch )* ;
caseBranch       : IS caseConstantList DO statement | ;
caseConstantList : caseConstant ( ',' caseConstant )* ;

caseConstant    locals [ Typespec type = null, Object value = null ]
    : constant ;

repeatStatement : REPEAT statementList UNTIL expression ;
whileStatement  : WHILE expression IS TRUE KEEP DOING statement ;

forStatement : FOR INDEX variable START AT expression AND WHILE expression
               DO statement UPDATE assignmentStatement ;
doStatement : DO expression TIMES statement ;

procedureCallStatement : procedureName '(' argumentList? ')' ;

procedureName   locals [ SymTableEntry entry = null ] 
    : IDENTIFIER ;

argumentList : argument ( ',' argument )* ;
argument     : expression ;

writeStatement   : PRINT writeArguments ;
writelnStatement : PRINTLN writeArguments? ;
writeArguments   : '(' writeArgument (',' writeArgument)* ')' ;
writeArgument    : expression (':' fieldWidth)? ;
fieldWidth       : sign? integerConstant (':' decimalPlaces)? ;
decimalPlaces    : integerConstant ;

readStatement   : READ readArguments ;
readlnStatement : READLN readArguments ;
readArguments   : '(' variable ( ',' variable )* ')' ;

expression          locals [ Typespec type = null ] 
    : simpleExpression (relOp simpleExpression)? ;
    
simpleExpression    locals [ Typespec type = null ] 
    : sign? term (addOp term)* ;
    
term                locals [ Typespec type = null ]
    : factor (mulOp factor)* ;

factor              locals [ Typespec type = null ] 
    : variable             # variableFactor
    | number               # numberFactor
    | characterConstant    # characterFactor
    | stringConstant       # stringFactor
    | functionCall         # functionCallFactor
    | NOT factor           # notFactor
    | '(' expression ')'   # parenthesizedFactor
    ;

variable            locals [ Typespec type = null, SymTableEntry entry = null ] 
    : variableIdentifier modifier* ;

modifier  : '[' indexList ']' | '.' field ;
indexList : index ( ',' index )* ;
index     : expression ; 

field               locals [ Typespec type = null, SymTableEntry entry = null ]     
    : IDENTIFIER ;

functionCall : functionName '(' argumentList? ')' ;
functionName        locals [ Typespec type = null, SymTableEntry entry = null ] 
    : IDENTIFIER ;
     
number          : sign? unsignedNumber ;
unsignedNumber  : integerConstant | decConstant ;
integerConstant : INTEGER ;
decConstant     : DEC;
characterConstant : CHARACTER ;
stringConstant    : STRING ;
       
relOp : '=' | '<>' | '<' | '<=' | '>' | '>=' ;
addOp : '+' | '-' | OR ;
mulOp : '*' | '/' | DIV | MOD | AND ;

fragment A : ('a' | 'A') ;
fragment B : ('b' | 'B') ;
fragment C : ('c' | 'C') ;
fragment D : ('d' | 'D') ;
fragment E : ('e' | 'E') ;
fragment F : ('f' | 'F') ;
fragment G : ('g' | 'G') ;
fragment H : ('h' | 'H') ;
fragment I : ('i' | 'I') ;
fragment J : ('j' | 'J') ;
fragment K : ('k' | 'K') ;
fragment L : ('l' | 'L') ;
fragment M : ('m' | 'M') ;
fragment N : ('n' | 'N') ;
fragment O : ('o' | 'O') ;
fragment P : ('p' | 'P') ;
fragment Q : ('q' | 'Q') ;
fragment R : ('r' | 'R') ;
fragment S : ('s' | 'S') ;
fragment T : ('t' | 'T') ;
fragment U : ('u' | 'U') ;
fragment V : ('v' | 'V') ;
fragment W : ('w' | 'W') ;
fragment X : ('x' | 'X') ;
fragment Y : ('y' | 'Y') ;
fragment Z : ('z' | 'Z') ;

PROGRAM   : P R O G R A M ;
CONST     : C O N S T ;
TYPE      : T Y P E ;
ARRAY     : A R R A Y ;
OF        : O F ;
RECORD    : R E C O R D ;
VAR       : V A R ;
BEGIN     : B E G I N ;
END       : E N D ;
DIV       : D I V ;
MOD       : M O D ;
AND       : A N D ;
OR        : O R ;
NOT       : N O T ;
IF        : I F ;
IS        : I S ;
TRUE      : T R U E ;
JUST      : J U S T ;
THIS      : T H I S ;
THEN      : T H E N ;
ELSE      : E L S E ;
DEFAULT   : D E F A U L T ;
KEEP      : K E E P ;
DOING     : D O I N G ;
INDEX     : I N D E X ;
START     : S T A R T ;
AT        : A T ;
TIMES     : T I M E S;
UPDATE    : U P D A T E;
PRINT     : P R I N T;
PRINTLN   : P R I N T L N;
CASE      : C A S E ;
REPEAT    : R E P E A T ;
UNTIL     : U N T I L ;
WHILE     : W H I L E ;
DO        : D O ;
FOR       : F O R ;
TO        : T O ;
DOWNTO    : D O W N T O ;
WRITE     : W R I T E ;
WRITELN   : W R I T E L N ;
READ      : R E A D ;
READLN    : R E A D L N ;
PROCEDURE : P R O C E D U R E ;
FUNCTION  : F U N C T I O N ;

IDENTIFIER : [a-zA-Z][a-zA-Z0-9]* ;
INTEGER    : [0-9]+ ;

DEC        : INTEGER '.' INTEGER
           | INTEGER ('e' | 'E') ('+' | '-')? INTEGER
           | INTEGER '.' INTEGER ('e' | 'E') ('+' | '-')? INTEGER
           ;

NEWLINE : '\r'? '\n' -> skip  ;
WS      : [ \t]+ -> skip ; 

QUOTE     : '\'' ;
CHARACTER : QUOTE CHARACTER_CHAR QUOTE ;
STRING    : QUOTE STRING_CHAR* QUOTE ;

fragment CHARACTER_CHAR : ~('\'')   // any non-quote character
                        ;

fragment STRING_CHAR : QUOTE QUOTE  // two consecutive quotes
                     | ~('\'')      // any non-quote character
                     ;

COMMENT : '{' COMMENT_CHARACTER* '}' -> skip ;

fragment COMMENT_CHARACTER : ~('}') ;


BLUEPRINT : B L U E P R I N T;