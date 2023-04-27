/**
 * <h1>CrossReferencer</h1>
 * <p>Generate a cross-reference listing.</p>
 * <p>Adapted from</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 */

package edu.yu.compilers.intermediate.util;

import edu.yu.compilers.intermediate.symtable.Predefined;
import edu.yu.compilers.intermediate.symtable.SymTable;
import edu.yu.compilers.intermediate.symtable.SymTableEntry;
import edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind;
import edu.yu.compilers.intermediate.symtable.SymTableStack;
import edu.yu.compilers.intermediate.type.Typespec;
import edu.yu.compilers.intermediate.type.Typespec.Form;

import java.util.ArrayList;

import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind.TYPE;
import static edu.yu.compilers.intermediate.type.Typespec.Form.RECORD;

public class CrossReferencer {
    private static final int NAME_WIDTH = 16;

    private static final String NAME_FORMAT = "%-" + NAME_WIDTH + "s";
    private static final String NUMBERS_LABEL = " Line numbers    ";
    private static final String NUMBERS_UNDERLINE = " ------------    ";
    private static final String NUMBER_FORMAT = " %03d";

    private static final int LABEL_WIDTH = NUMBERS_LABEL.length();
    private static final int INDENT_WIDTH = NAME_WIDTH + LABEL_WIDTH;

    private static final StringBuilder INDENT = new StringBuilder(INDENT_WIDTH);
    private static final String ENUM_CONST_FORMAT = "%" + NAME_WIDTH + "s = %s";

    static {
        INDENT.append(" ".repeat(INDENT_WIDTH));
    }

    /**
     * Print the cross-reference table.
     *
     * @param symTableStack the symbol table stack.
     */
    public void print(SymTableStack symTableStack) {
        System.out.println("\n===== CROSS-REFERENCE TABLE =====");

        SymTableEntry programId = symTableStack.getProgramId();
        printRoutine(programId);
    }

    /**
     * Print a cross-reference table for a routine.
     *
     * @param routineId the routine identifier's symbol table entry.
     */
    private void printRoutine(SymTableEntry routineId) {
        SymTableEntry.Kind kind = routineId.getKind();
        System.out.println("\n*** " + kind.toString().toUpperCase() + " " + routineId.getName() + " ***");
        printColumnHeadings();

        // Print the entries in the routine's symbol table.
        SymTable symTable = routineId.getRoutineSymTable();
        printSymTable(symTable);

        // Print any procedures and functions defined in the routine.
        ArrayList<SymTableEntry> subroutineIds = routineId.getSubroutines();
        if (subroutineIds != null) {
            for (SymTableEntry rtnId : subroutineIds) printRoutine(rtnId);
        }
    }

    /**
     * Print column headings.
     */
    private void printColumnHeadings() {
        System.out.println();
        System.out.println(String.format(NAME_FORMAT, "Identifier") + NUMBERS_LABEL + "Type specification");
        System.out.println(String.format(NAME_FORMAT, "----------") + NUMBERS_UNDERLINE + "------------------");
    }

    /**
     * Print the entries in a symbol table.
     *
     * @param symTable the symbol table.
     */
    private void printSymTable(SymTable symTable) {
        ArrayList<SymTableEntry> sorted = symTable.sortedEntries();

        // Loop over the sorted list of table entries
        // to print each entry of this symbol table.
        for (SymTableEntry entry : sorted) {
            ArrayList<Integer> lineNumbers = entry.getLineNumbers();

            // For each entry, print the identifier name
            // followed by the line numbers.
            System.out.printf(NAME_FORMAT, entry.getName());
            if (lineNumbers != null) {
                for (Integer lineNumber : lineNumbers) {
                    System.out.printf(NUMBER_FORMAT, lineNumber);
                }
            }

            // Print the symbol table entry.
            System.out.println();
            printEntry(entry);
        }

        // Loop over the sorted list of entries again
        // to print each nested record's symbol table.
        for (SymTableEntry entry : sorted) {
            if (entry.getKind() == TYPE) {
                Typespec type = entry.getType();
                if (type.getForm() == RECORD) printRecord(type);
            }
        }
    }

    /**
     * Print a symbol table entry.
     *
     * @param entry the symbol table entry.
     */
    private void printEntry(SymTableEntry entry) {
        Kind kind = entry.getKind();
        int nestingLevel = entry.getSymTable().getNestingLevel();
        System.out.println(INDENT + "Kind: " + kind.toString().replace("_", " "));
        System.out.println(INDENT + "Scope nesting level: " + nestingLevel);

        // Print the type specification.
        Typespec type = entry.getType();
        printType(type);

        switch (kind) {
            case CONSTANT -> {
                Object value = entry.getValue();
                System.out.println(INDENT + "Value: " + toString(value, type));

                // Print the type details only if the type is unnamed.
                if (type.getIdentifier() == null) {
                    printTypeDetail(type);
                }

            }
            case ENUMERATION_CONSTANT -> {
                Object value = entry.getValue();
                System.out.println(INDENT + "Value: " + toString(value, type));

            }
            case TYPE -> {
                // Print the type details only when the type is first defined.
                if (entry == type.getIdentifier()) {
                    printTypeDetail(type);
                }

            }
            case VARIABLE -> {
                // Print the type details only if the type is unnamed.
                if (type.getIdentifier() == null) {
                    printTypeDetail(type);
                }

            }
            case RECORD_FIELD -> printTypeDetail(type);
            default -> {
            }
        }
    }

    /**
     * Print a type specification.
     *
     * @param type the type specification.
     */
    private void printType(Typespec type) {
        if (type != null) {
            Form form = type.getForm();
            SymTableEntry typeId = type.getIdentifier();
            String typeName = typeId != null ? typeId.getName() : "<unnamed>";

            System.out.println(INDENT + "Type form: " + form + ", Type id: " + typeName);
        }
    }

    /**
     * Print the details of a type specification.
     *
     * @param type the type specification.
     */
    private void printTypeDetail(Typespec type) {
        Form form = type.getForm();

        switch (form) {
            case ENUMERATION -> {
                ArrayList<SymTableEntry> constantIds = type.getEnumerationConstants();

                System.out.println(INDENT + "--- Enumeration constants ---");

                // Print each enumeration constant and its value.
                for (SymTableEntry constantId : constantIds) {
                    String name = constantId.getName();
                    Object value = constantId.getValue();

                    System.out.println(INDENT + String.format(ENUM_CONST_FORMAT, name, value));
                }

            }
            case SUBRANGE -> {
                Object minValue = type.getSubrangeMinValue();
                Object maxValue = type.getSubrangeMaxValue();
                Typespec baseType = type.baseType();

                System.out.println(INDENT + "--- Base type ---");
                printType(baseType);

                // Print the base type details only if the type is unnamed.
                if (baseType.getIdentifier() == null) {
                    printTypeDetail(baseType);
                }

                System.out.print(INDENT + "Range: ");
                System.out.println(toString(minValue, baseType) + ".." + toString(maxValue, baseType));

            }
            case ARRAY -> {
                Typespec indexType = type.getArrayIndexType();
                Typespec elementType = type.getArrayElementType();
                int count = type.getArrayElementCount();

                System.out.println(INDENT + "--- INDEX TYPE ---");
                printType(indexType);

                // Print the index type details only if the type is unnamed.
                if (indexType.getIdentifier() == null) {
                    printTypeDetail(indexType);
                }

                System.out.println(INDENT + "--- ELEMENT TYPE ---");
                printType(elementType);
                System.out.println(INDENT.toString() + count + " elements");

                // Print the element type details only if the type is unnamed.
                if (elementType.getIdentifier() == null) {
                    printTypeDetail(elementType);
                }

            }
            default -> {
            }
        }
    }

    /**
     * Print the cross-reference table for a record type.
     *
     * @param recordType the RECORD type specification.
     */
    private void printRecord(Typespec recordType) {
        SymTableEntry recordId = recordType.getIdentifier();
        String name = recordId != null ? recordId.getName() : "<unnamed>";

        System.out.println("\n--- RECORD " + name + " ---");
        printColumnHeadings();

        // Print the entries in the record's symbol table.
        SymTable symTable = recordType.getRecordSymTable();
        printSymTable(symTable);
    }

    /**
     * Convert a value to a string.
     *
     * @param value the value.
     * @param type  the value's datatype.
     * @return the string.
     */
    private String toString(Object value, Typespec type) {
        return type == Predefined.stringType ? "'" + value + "'" : value.toString();
    }
}
