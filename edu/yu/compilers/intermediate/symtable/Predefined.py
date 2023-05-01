from edu.yu.compilers.intermediate.type.Typespec import Typespec


# <h1>Predefined</h1>
# <p>Enter the predefined Pascal types, identifiers, and constants
# into the symbol table.</p>
# <p>Adapted from:</p>
# <p>Copyright (c) 2020 by Ronald Mak</p>
# <p>For instructional purposes only.  No warranties.</p>


# import edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind;
# import edu.yu.compilers.intermediate.symtable.SymTableEntry.Routine;
# import edu.yu.compilers.intermediate.type.Typespec;
#
# import java.util.ArrayList;
#
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
        initializeTypes(symTableStack)
        initializeConstants(symTableStack)
        initializeStandardRoutines(symTableStack)

    # Initialize the predefined types.
    #
    # @param symTableStack the symbol table stack to initialize.
    @staticmethod
    def initializeTypes(symTableStack):
        # Type integer.
        integerId = symTableStack.enterLocal("integer", TYPE)
        integerType = Typespec(SCALAR)
        integerType.setIdentifier(integerId);
        integerId.setType(integerType)

        # // Type real.
        realId = symTableStack.enterLocal("real", TYPE)
        realType = Typespec(SCALAR)
        realType.setIdentifier(realId)
        realId.setType(realType)

        # Type boolean.
        booleanId = symTableStack.enterLocal("boolean", TYPE)
        booleanType = Typespec(ENUMERATION)
        booleanType.setIdentifier(booleanId)
        booleanId.setType(booleanType)

        # Type char.
        charId = symTableStack.enterLocal("char", TYPE)
        charType = Typespec(SCALAR)
        charType.setIdentifier(charId)
        charId.setType(charType)

        # Type string.
        stringId = symTableStack.enterLocal("string", TYPE)
        stringType = Typespec(SCALAR)
        stringType.setIdentifier(stringId)
        stringId.setType(stringType)

        # Undefined type.
        undefinedType = Typespec(SCALAR)

    # Initialize the predefined constant.
    #
    # @param symTabStack the symbol table stack to initialize.
    @staticmethod
    def initializeConstants(symTabStack):
        # Boolean enumeration constant false.
        falseId = symTabStack.enterLocal("false", ENUMERATION_CONSTANT)
        falseId.setType(booleanType)
        falseId.setValue(0)

        # Boolean enumeration constant true.
        trueId = symTabStack.enterLocal("true", ENUMERATION_CONSTANT)
        trueId.setType(booleanType)
        trueId.setValue(1)

        # Add false and true to the boolean enumeration type.
        constants = booleanType.getEnumerationConstants()
        constants.add(falseId)
        constants.add(trueId)

    # Initialize the standard procedures and functions.
    #
    # @param symTableStack the symbol table stack to initialize.
    @staticmethod
    def initializeStandardRoutines(symTableStack):
        readId = Predefined.enterStandard(symTableStack, PROCEDURE, "read", READ)
        readlnId = Predefined.enterStandard(symTableStack, PROCEDURE, "readln", READLN)
        writeId = Predefined.enterStandard(symTableStack, PROCEDURE, "write", WRITE)
        writelnId = Predefined.enterStandard(symTableStack, PROCEDURE, "writeln", WRITELN)
        absId = Predefined.enterStandard(symTableStack, FUNCTION, "abs", ABS)
        arctanId = Predefined.enterStandard(symTableStack, FUNCTION, "arctan", ARCTAN)
        chrId = Predefined.enterStandard(symTableStack, FUNCTION, "chr", CHR)
        cosId = Predefined.enterStandard(symTableStack, FUNCTION, "cos", COS)
        eofId = Predefined.enterStandard(symTableStack, FUNCTION, "eof", EOF)
        eolnId = Predefined.enterStandard(symTableStack, FUNCTION, "eoln", EOLN)
        expId = Predefined.enterStandard(symTableStack, FUNCTION, "exp", EXP)
        lnId = Predefined.enterStandard(symTableStack, FUNCTION, "ln", LN)
        oddId = Predefined.enterStandard(symTableStack, FUNCTION, "odd", ODD)
        ordId = Predefined.enterStandard(symTableStack, FUNCTION, "ord", ORD)
        predId = Predefined.enterStandard(symTableStack, FUNCTION, "pred", PRED)
        roundId = Predefined.enterStandard(symTableStack, FUNCTION, "round", ROUND)
        sinId = Predefined.enterStandard(symTableStack, FUNCTION, "sin", SIN)
        sqrId = Predefined.enterStandard(symTableStack, FUNCTION, "sqr", SQR)
        sqrtId = Predefined.enterStandard(symTableStack, FUNCTION, "sqrt", SQRT)
        succId = Predefined.enterStandard(symTableStack, FUNCTION, "succ", SUCC)
        truncId = Predefined.enterStandard(symTableStack, FUNCTION, "trunc", TRUNC)

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
