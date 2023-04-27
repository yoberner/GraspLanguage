grammar Grasp;

@header {
    // package antlr4;
    // import java.util.HashMap;
    // import edu.yu.compilers.intermediate.symtable.SymTableEntry;
    // import edu.yu.compilers.intermediate.type.Typespec;
}

program           : programHeader block ;
programHeader     : PROGRAM programIdentifier programParameters? ';' ; 
programParameters : '(' IDENTIFIER ( ',' IDENTIFIER )* ')' ;

programIdentifier   locals [ SymTableEntry entry = null ]
    : IDENTIFIER ;

block         : declarations compoundStatement ;
declarations  : ( constantsPart )? ( typesPart )?
                ( variablesPart )? ( routinesPart)? ;

constantsPart           : FINAL '{' constantDefinitionsList '}' ;
constantDefinitionsList : constantDefinition ';' ( constantDefinition ';' )* ;
constantDefinition      : typeSpecification constantIdentifier '=' constant ;

constantIdentifier  locals [ Typespec type = null, SymTableEntry entry = null ]
    : IDENTIFIER ;

constant            locals [ Typespec type = null, Object value = null ]
    : sign? ( IDENTIFIER | unsignedNumber )
    | characterConstant
    | stringConstant
    ;

sign : '-' | '+' ;

typesPart           : TYPE '{' typeDefinitionsList '}' ;
typeDefinitionsList : typeDefinition* ;
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
    ;

arrayType
    : (simpleType | recordType ) ('['']')* ;

recordType          locals [ SymTableEntry entry = null ]
    : BLUEPRINT '{' recordFields ';'? '}' ;
recordFields : variableDeclarationsList ;

variablesPart            : VAR '{' variableDeclarationsList '}';
variableDeclarationsList : variableDeclarations ';' ( variableDeclarations ';')* ;
variableDeclarations     : typeSpecification variableIdentifierList;
variableIdentifierList   : variableIdentifier ( ',' variableIdentifier )* ;

variableIdentifier  locals [ Typespec type = null, SymTableEntry entry = null ]
    : IDENTIFIER ;

routinesPart      : routineDefinition ( ';' routineDefinition)* ;
routineDefinition : ( functionHead ) block ;
functionHead      : FUNCTION  routineIdentifier parameters? RETURNS typeIdentifier ;

routineIdentifier   locals [ Typespec type = null, SymTableEntry entry = null ]
    : IDENTIFIER ;

parameters                : '(' parameterDeclarationsList ')' ;
parameterDeclarationsList : parameterDeclarations ( ',' parameterDeclarations )* ;
parameterDeclarations     : VAR? typeIdentifier parameterIdentifier ;


parameterIdentifier   locals [ Typespec type = null, SymTableEntry entry = null ]
    : IDENTIFIER ;

statement : compoundStatement
          | assignmentStatement ';'
	      | declareAndAssignStatement ';'
          | ifStatement
          | caseStatement
          | whileStatement
          | forStatement
          | printStatement ';'
          | printlnStatement ';'
          | readStatement ';'
          | readlnStatement ';'
          | emptyStatement ';'
          | returnStatement ';'
          ;

compoundStatement : (DO)? '{' statementList '}' ;
emptyStatement : ;

statementList       : statement* ;
declareAndAssignStatement : typeSpecification variableIdentifier '=' rhs ;
assignmentStatement : lhs '=' rhs ;

returnStatement : RETURN expression ;

lhs locals [ Typespec type = null ]
    : variable ;
rhs : expression ;

ifStatement    : IF expression IS TRUE DO trueStatement ( ELSE falseStatement )? ;
trueStatement  : statement ;
falseStatement : statement ;

caseStatement
    locals [ HashMap<Object, PascalParser.StatementContext> jumpTable = null ]
    : IF expression caseBranchList (DEFAULT DO statement)? ;

caseBranchList   : caseBranch* ;
caseBranch       : IS caseConstantList DO statement ;
caseConstantList : caseConstant ( ',' caseConstant )* ;

caseConstant    locals [ Typespec type = null, Object value = null ]
    : constant ;

whileStatement  : WHILE expression IS TRUE KEEP DOING statement ;

forStatement : FOR INDEX variable START AT expression AND WHILE expression
               KEEP DOING statement UPDATE assignmentStatement ';' ;
doStatement : DO expression TIMES statement ;

argumentList : argument ( ',' argument )* ;
argument     : expression ;

printStatement   : PRINT writeArguments ;
printlnStatement : PRINTLN writeArguments? ;
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
decConstant     : DECIMAL;
characterConstant : CHARACTER ;
stringConstant    : STRING ;
booleanConstant   : BOOLEAN ;
       
relOp : '==' | '!=' | '<' | '<=' | '>' | '>=' ;
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
FINAL     : F I N A L ;
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
BLUEPRINT : B L U E P R I N T ;
RETURNS    : R E T U R N S ;
RETURN    : R E T U R N ;

IDENTIFIER : [a-zA-Z][a-zA-Z0-9]*;
INTEGER    : [0-9]+ ;
BOOLEAN    : [0-1] ;

DECIMAL    : INTEGER '.' INTEGER
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

COMMENT : '/*' COMMENT_CHARACTER* '*/' -> skip ;
SINGLE_COMMENT : '//' ~[\r\n]* -> skip ;

// fragment COMMENT_CHARACTER : ~('}')  ;
fragment COMMENT_CHARACTER : ~('@')  ; //todo
