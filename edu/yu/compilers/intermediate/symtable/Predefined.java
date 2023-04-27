/**
 * <h1>Predefined</h1>
 * <p>Enter the predefined Pascal types, identifiers, and constants
 * into the symbol table.</p>
 * <p>Adapted from:</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 * <p>For instructional purposes only.  No warranties.</p>
 */

package edu.yu.compilers.intermediate.symtable;

import edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind;
import edu.yu.compilers.intermediate.symtable.SymTableEntry.Routine;
import edu.yu.compilers.intermediate.type.Typespec;

import java.util.ArrayList;

import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind.*;
import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Routine.*;
import static edu.yu.compilers.intermediate.type.Typespec.Form.ENUMERATION;
import static edu.yu.compilers.intermediate.type.Typespec.Form.SCALAR;

public class Predefined {
    // Predefined types.
    public static Typespec integerType;
    public static Typespec realType;
    public static Typespec booleanType;
    public static Typespec charType;
    public static Typespec stringType;
    public static Typespec undefinedType;

    // Predefined identifiers.
    public static SymTableEntry integerId;
    public static SymTableEntry realId;
    public static SymTableEntry booleanId;
    public static SymTableEntry charId;
    public static SymTableEntry stringId;
    public static SymTableEntry falseId;
    public static SymTableEntry trueId;
    public static SymTableEntry readId;
    public static SymTableEntry readlnId;
    public static SymTableEntry writeId;
    public static SymTableEntry writelnId;
    public static SymTableEntry absId;
    public static SymTableEntry arctanId;
    public static SymTableEntry chrId;
    public static SymTableEntry cosId;
    public static SymTableEntry eofId;
    public static SymTableEntry eolnId;
    public static SymTableEntry expId;
    public static SymTableEntry lnId;
    public static SymTableEntry oddId;
    public static SymTableEntry ordId;
    public static SymTableEntry predId;
    public static SymTableEntry roundId;
    public static SymTableEntry sinId;
    public static SymTableEntry sqrId;
    public static SymTableEntry sqrtId;
    public static SymTableEntry succId;
    public static SymTableEntry truncId;

    /**
     * Initialize a symbol table stack with predefined identifiers.
     *
     * @param symTableStack the symbol table stack to initialize.
     */
    public static void initialize(SymTableStack symTableStack) {
        initializeTypes(symTableStack);
        initializeConstants(symTableStack);
        initializeStandardRoutines(symTableStack);
    }

    /**
     * Initialize the predefined types.
     *
     * @param symTableStack the symbol table stack to initialize.
     */
    private static void initializeTypes(SymTableStack symTableStack) {
        // Type integer.
        integerId = symTableStack.enterLocal("integer", TYPE);
        integerType = new Typespec(SCALAR);
        integerType.setIdentifier(integerId);
        integerId.setType(integerType);

        // Type real.
        realId = symTableStack.enterLocal("real", TYPE);
        realType = new Typespec(SCALAR);
        realType.setIdentifier(realId);
        realId.setType(realType);

        // Type boolean.
        booleanId = symTableStack.enterLocal("boolean", TYPE);
        booleanType = new Typespec(ENUMERATION);
        booleanType.setIdentifier(booleanId);
        booleanId.setType(booleanType);

        // Type char.
        charId = symTableStack.enterLocal("char", TYPE);
        charType = new Typespec(SCALAR);
        charType.setIdentifier(charId);
        charId.setType(charType);

        // Type string.
        stringId = symTableStack.enterLocal("string", TYPE);
        stringType = new Typespec(SCALAR);
        stringType.setIdentifier(stringId);
        stringId.setType(stringType);

        // Undefined type.
        undefinedType = new Typespec(SCALAR);
    }

    /**
     * Initialize the predefined constant.
     *
     * @param symTabStack the symbol table stack to initialize.
     */
    private static void initializeConstants(SymTableStack symTabStack) {
        // Boolean enumeration constant false.
        falseId = symTabStack.enterLocal("false", ENUMERATION_CONSTANT);
        falseId.setType(booleanType);
        falseId.setValue(0);

        // Boolean enumeration constant true.
        trueId = symTabStack.enterLocal("true", ENUMERATION_CONSTANT);
        trueId.setType(booleanType);
        trueId.setValue(1);

        // Add false and true to the boolean enumeration type.
        ArrayList<SymTableEntry> constants = booleanType.getEnumerationConstants();
        constants.add(falseId);
        constants.add(trueId);
    }

    /**
     * Initialize the standard procedures and functions.
     *
     * @param symTableStack the symbol table stack to initialize.
     */
    private static void initializeStandardRoutines(SymTableStack symTableStack) {
        readId = enterStandard(symTableStack, PROCEDURE, "read", READ);
        readlnId = enterStandard(symTableStack, PROCEDURE, "readln", READLN);
        writeId = enterStandard(symTableStack, PROCEDURE, "write", WRITE);
        writelnId = enterStandard(symTableStack, PROCEDURE, "writeln", WRITELN);

        absId = enterStandard(symTableStack, FUNCTION, "abs", ABS);
        arctanId = enterStandard(symTableStack, FUNCTION, "arctan", ARCTAN);
        chrId = enterStandard(symTableStack, FUNCTION, "chr", CHR);
        cosId = enterStandard(symTableStack, FUNCTION, "cos", COS);
        eofId = enterStandard(symTableStack, FUNCTION, "eof", EOF);
        eolnId = enterStandard(symTableStack, FUNCTION, "eoln", EOLN);
        expId = enterStandard(symTableStack, FUNCTION, "exp", EXP);
        lnId = enterStandard(symTableStack, FUNCTION, "ln", LN);
        oddId = enterStandard(symTableStack, FUNCTION, "odd", ODD);
        ordId = enterStandard(symTableStack, FUNCTION, "ord", ORD);
        predId = enterStandard(symTableStack, FUNCTION, "pred", PRED);
        roundId = enterStandard(symTableStack, FUNCTION, "round", ROUND);
        sinId = enterStandard(symTableStack, FUNCTION, "sin", SIN);
        sqrId = enterStandard(symTableStack, FUNCTION, "sqr", SQR);
        sqrtId = enterStandard(symTableStack, FUNCTION, "sqrt", SQRT);
        succId = enterStandard(symTableStack, FUNCTION, "succ", SUCC);
        truncId = enterStandard(symTableStack, FUNCTION, "trunc", TRUNC);
    }

    /**
     * Enter a standard procedure or function into the symbol table stack.
     *
     * @param symTableStack the symbol table stack to initialize.
     * @param kind          either PROCEDURE or FUNCTION.
     * @param name          the procedure or function name.
     * @param routineCode   the routine code.
     */
    private static SymTableEntry enterStandard(SymTableStack symTableStack,
                                               Kind kind, String name,
                                               Routine routineCode) {
        SymTableEntry routineId = symTableStack.enterLocal(name, kind);
        routineId.setRoutineCode(routineCode);

        return routineId;
    }

}
