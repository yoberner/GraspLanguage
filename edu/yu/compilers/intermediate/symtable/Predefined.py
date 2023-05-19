from edu.yu.compilers.intermediate.symtable.Kind import Kind
from edu.yu.compilers.intermediate.symtable.Routine import Routine
from edu.yu.compilers.intermediate.type.Form import Form
from edu.yu.compilers.intermediate.type.Typespec import Typespec
from edu.yu.compilers.intermediate.symtable.SymTableEntry import SymTableEntry


# static import?
# import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind.*;
# import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Routine.*;
# import static edu.yu.compilers.intermediate.type.Typespec.Form.ENUMERATION;
# import static edu.yu.compilers.intermediate.type.Typespec.Form.SCALAR;

class Predefined:
    # Predefined types.
    integerType = None
    realType = None
    booleanType = None
    charType = None
    stringType = None
    undefinedType = None

    # Predefined identifiers.
    integerId = None
    realId = None
    booleanId = None
    charId = None
    stringId = None
    falseId = None
    trueId = None
    readId = None
    readlnId = None
    writeId = None
    writelnId = None
    absId = None
    arctanId = None
    chrId = None
    cosId = None
    eofId = None
    eolnId = None
    expId = None
    lnId = None
    oddId = None
    ordId = None
    predId = None
    roundId = None
    sinId = None
    sqrId = None
    sqrtId = None
    succId = None
    truncId = None

    # Initialize a symbol table stack with predefined identifiers.
    #
    # @param symTableStack the symbol table stack to initialize.
    @staticmethod
    def initialize(symTableStack):
        Predefined.initializeTypes(symTableStack)
        Predefined.initializeConstants(symTableStack)
        Predefined.initializeStandardRoutines(symTableStack)

    # Initialize the predefined types.
    #
    # @param symTableStack the symbol table stack to initialize.
    @staticmethod
    def initializeTypes(symTableStack):
        # Type integer.
        Predefined.integerId = symTableStack.enterLocal("integer", Kind.TYPE)
        Predefined.integerType = Typespec(Form.SCALAR)
        Predefined.integerType.setIdentifier(Predefined.integerId.getName(), Predefined.integerId.getSymTable())
        Predefined.integerId.setType(Predefined.integerType)

        # // Type real.
        Predefined.realId = symTableStack.enterLocal("decimal", Kind.TYPE)
        Predefined.realType = Typespec(Form.SCALAR)
        Predefined.realType.setIdentifier(Predefined.realId.getName(), Predefined.realId.getSymTable())
        Predefined.realId.setType(Predefined.realType)

        # Type boolean.
        Predefined.booleanId = symTableStack.enterLocal("boolean", Kind.TYPE)
        Predefined.booleanType = Typespec(Form.ENUMERATION)
        Predefined.booleanType.setIdentifier(Predefined.booleanId.getName(), Predefined.booleanId.getSymTable())
        Predefined.booleanId.setType(Predefined.booleanType)

        # Type char.
        Predefined.charId = symTableStack.enterLocal("char", Kind.TYPE)
        Predefined.charType = Typespec(Form.SCALAR)
        Predefined.charType.setIdentifier(Predefined.charId.getName(), Predefined.charId.getSymTable())
        Predefined.charId.setType(Predefined.charType)

        # Type string.
        Predefined.stringId = symTableStack.enterLocal("string", Kind.TYPE)
        Predefined.stringType = Typespec(Form.SCALAR)
        Predefined.stringType.setIdentifier(Predefined.stringId.getName(), Predefined.stringId.getSymTable())
        Predefined.stringId.setType(Predefined.stringType)

        # Undefined type.
        undefinedType = Typespec(Form.SCALAR)

    # Initialize the predefined constant.
    #
    # @param symTabStack the symbol table stack to initialize.
    @staticmethod
    def initializeConstants(symTabStack):
        # Boolean enumeration constant false.
        Predefined.falseId = symTabStack.enterLocal("false", Kind.ENUMERATION_CONSTANT)
        Predefined.falseId.setType(Predefined.booleanType)
        Predefined.falseId.setValue(0)

        # Boolean enumeration constant true.
        Predefined.trueId = symTabStack.enterLocal("true", Kind.ENUMERATION_CONSTANT)
        Predefined.trueId.setType(Predefined.booleanType)
        Predefined.trueId.setValue(1)

        # Add false and true to the boolean enumeration type.
        constants = Predefined.booleanType.getEnumerationConstants()
        constants.append(Predefined.falseId)
        constants.append(Predefined.trueId)

    # Initialize the standard procedures and functions.
    #
    # @param symTableStack the symbol table stack to initialize.
    @staticmethod
    def initializeStandardRoutines(symTableStack):
        Predefined.readId = Predefined.enterStandard(symTableStack, Kind.PROCEDURE, "read", Routine.READ)
        Predefined.readlnId = Predefined.enterStandard(symTableStack, Kind.PROCEDURE, "readln", Routine.READLN)
        Predefined.writeId = Predefined.enterStandard(symTableStack, Kind.PROCEDURE, "write", Routine.WRITE)
        Predefined.writelnId = Predefined.enterStandard(symTableStack, Kind.PROCEDURE, "writeln", Routine.WRITELN)
        Predefined.absId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "abs", Routine.ABS)
        Predefined.arctanId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "arctan", Routine.ARCTAN)
        Predefined.chrId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "chr", Routine.CHR)
        Predefined.cosId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "cos", Routine.COS)
        Predefined.eofId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "eof", Routine.EOF)
        Predefined.eolnId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "eoln", Routine.EOLN)
        Predefined.expId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "exp", Routine.EXP)
        Predefined.lnId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "ln", Routine.LN)
        Predefined.oddId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "odd", Routine.ODD)
        Predefined.ordId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "ord", Routine.ORD)
        Predefined.predId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "pred", Routine.PRED)
        Predefined.roundId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "round", Routine.ROUND)
        Predefined.sinId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "sin", Routine.SIN)
        Predefined.sqrId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "sqr", Routine.SQR)
        Predefined.sqrtId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "sqrt", Routine.SQRT)
        Predefined.succId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "succ", Routine.SUCC)
        Predefined.truncId = Predefined.enterStandard(symTableStack, Kind.FUNCTION, "trunc", Routine.TRUNC)

    # Enter a standard procedure or function into the symbol table stack.
    #
    # @param symTableStack the symbol table stack to initialize.
    # @param kind          either PROCEDURE or FUNCTION.
    # @param name          the procedure or function name.
    # @param routineCode   the routine code.
    @staticmethod
    def enterStandard(symTableStack, kind, name, routineCode):
        routineId = symTableStack.enterLocal(name, kind)
        routineId.setRoutineCode(routineCode)

        return routineId
