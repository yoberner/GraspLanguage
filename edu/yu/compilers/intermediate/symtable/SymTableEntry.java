/**
 * <h1>SymTableEntryImpl</h1>
 * <p>An implementation of a symbol table entry.</p>
 * <p>Adapted from:</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 * <p>For instructional purposes only.  No warranties.</p>
 */

package edu.yu.compilers.intermediate.symtable;

import edu.yu.compilers.intermediate.type.Typespec;

import java.util.ArrayList;


public class SymTableEntry {
    private final String name;                     // entry name
    private final SymTable symTable;                   // parent symbol table
    private final ArrayList<Integer> lineNumbers;  // source line numbers
    private Kind kind;                       // what kind of identifier
    private Typespec typespec;               // type specification
    private int slotNumber;                  // local variables array slot number
    private EntryInfo info;                  // entry information

    /**
     * Constructor.
     *
     * @param name     the name of the entry.
     * @param kind     the kind of entry.
     * @param symTable the symbol table that contains this entry.
     */
    public SymTableEntry(String name, Kind kind, SymTable symTable) {
        this.name = name;
        this.kind = kind;
        this.symTable = symTable;
        this.lineNumbers = new ArrayList<>();

        // Initialize the appropriate entry information.
        switch (kind) {
            case CONSTANT, ENUMERATION_CONSTANT, VARIABLE, RECORD_FIELD, VALUE_PARAMETER -> info = new ValueInfo();
            case PROGRAM, PROCEDURE, FUNCTION -> {
                info = new RoutineInfo();
                ((RoutineInfo) info).parameters = new ArrayList<>();
                ((RoutineInfo) info).subroutines = new ArrayList<>();
            }
            default -> {
            }
        }
    }

    /**
     * Get the name of the entry.
     *
     * @return the name.
     */
    public String getName() {
        return name;
    }

    /**
     * Get the kind of entry.
     *
     * @return the kind.
     */
    public Kind getKind() {
        return kind;
    }

    /**
     * Set the kind of entry.
     *
     * @param kind the kind to set.
     */
    public void setKind(Kind kind) {
        this.kind = kind;
    }

    /**
     * Get the symbol table that contains this entry.
     *
     * @return the symbol table.
     */
    public SymTable getSymTable() {
        return symTable;
    }

    /**
     * Get the slot number of the local variables array.
     *
     * @return the number.
     */
    public int getSlotNumber() {
        return slotNumber;
    }

    /**
     * Set the slot number of the local variables array.
     *
     * @param slotNumber the number to set.
     */
    public void setSlotNumber(int slotNumber) {
        this.slotNumber = slotNumber;
    }

    /**
     * Get the type specification of the entry.
     *
     * @return the type specification.
     */
    public Typespec getType() {
        return typespec;
    }

    /**
     * Set the type specification.
     *
     * @param typespec the type specification to set.
     */
    public void setType(Typespec typespec) {
        this.typespec = typespec;
    }

    /**
     * Get the arraylist of source line numbers for the entry.
     *
     * @return the arraylist.
     */
    public ArrayList<Integer> getLineNumbers() {
        return lineNumbers;
    }

    /**
     * Append a source line number to the entry.
     *
     * @param lineNumber the line number to append.
     */
    public void appendLineNumber(int lineNumber) {
        lineNumbers.add(lineNumber);
    }

    /**
     * Get the data value stored with this entry.
     *
     * @return the data value.
     */
    public Object getValue() {
        return ((ValueInfo) info).value;
    }

    /**
     * Set the data value into this entry.
     *
     * @param value the value to set.
     */
    public void setValue(Object value) {
        ((ValueInfo) info).value = value;
    }

    /**
     * Get the routine code.
     *
     * @return the code.
     */
    public Routine getRoutineCode() {
        return ((RoutineInfo) info).code;
    }

    /**
     * Set the routine code.
     *
     * @param code the code to set.
     */
    public void setRoutineCode(Routine code) {
        ((RoutineInfo) info).code = code;
    }

    /**
     * Get the routine's symbol table.
     *
     * @return the symbol table.
     */
    public SymTable getRoutineSymTable() {
        return ((RoutineInfo) info).symTable;
    }

    /**
     * Set the routine's symbol table.
     *
     * @param symTable the symbol table to set.
     */
    public void setRoutineSymTable(SymTable symTable) {
        ((RoutineInfo) info).symTable = symTable;
    }

    /**
     * Get the arraylist of symbol table entries of the routine's formal parameters.
     *
     * @return the arraylist.
     */
    public ArrayList<SymTableEntry> getRoutineParameters() {
        return ((RoutineInfo) info).parameters;
    }

    /**
     * Set the arraylist symbol table entries of parameters of the routine.
     *
     * @param parameters the arraylist to set.
     */
    public void setRoutineParameters(ArrayList<SymTableEntry> parameters) {
        ((RoutineInfo) info).parameters = parameters;
    }

    /**
     * Get the arraylist of symbol table entries of the nested subroutines.
     *
     * @return the arraylist.
     */
    public ArrayList<SymTableEntry> getSubroutines() {
        return ((RoutineInfo) info).subroutines;
    }

    /**
     * Append to the arraylist of symbol table entries of the nested subroutines.
     *
     * @param subroutineId the symbol table entry of the subroutine to append.
     */
    public void appendSubroutine(SymTableEntry subroutineId) {
        ((RoutineInfo) info).subroutines.add(subroutineId);
    }

    /**
     * Get the routine's executable code.
     *
     * @return the executable code.
     */
    public Object getExecutable() {
        return ((RoutineInfo) info).executable;
    }

    /**
     * Set the routine's executable code.
     *
     * @param executable the executable code to set.
     */
    public void setExecutable(Object executable) {
        ((RoutineInfo) info).executable = executable;
    }

    /**
     * What kind of identifier.
     */
    public enum Kind {
        CONSTANT, ENUMERATION_CONSTANT, TYPE, VARIABLE, RECORD_FIELD, VALUE_PARAMETER, REFERENCE_PARAMETER, PROGRAM_PARAMETER, PROGRAM, PROCEDURE, FUNCTION, UNDEFINED;

        public String toString() {
            return super.toString().toLowerCase();
        }
    }

    /**
     * Which routine.
     */
    public enum Routine {
        DECLARED, FORWARD, READ, READLN, WRITE, WRITELN, ABS, ARCTAN, CHR, COS, EOF, EOLN, EXP, LN, ODD, ORD, PRED, ROUND, SIN, SQR, SQRT, SUCC, TRUNC,
    }

    /**
     * Entry information interface.
     */
    private interface EntryInfo {
    }

    /**
     * Value information.
     */
    private static class ValueInfo implements EntryInfo {
        private Object value;
    }

    /**
     * Routine information.
     */
    private static class RoutineInfo implements EntryInfo {
        private Routine code;                          // routine code
        private SymTable symTable;                     // routine's symbol table
        private ArrayList<SymTableEntry> parameters;   // routine's formal parameters
        private ArrayList<SymTableEntry> subroutines;  // symTable entries of subroutines
        private Object executable;                     // routine's executable code
    }
}
