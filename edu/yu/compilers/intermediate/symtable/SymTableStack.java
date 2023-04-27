/**
 * <h1>SymTableStack</h1>
 * <p>The symbol table stack.</p>
 * <p>Adapted from:</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 * <p>For instructional purposes only.  No warranties.</p>
 */

package edu.yu.compilers.intermediate.symtable;

import edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind;

import java.util.ArrayList;

public class SymTableStack extends ArrayList<SymTable> {
    private static final long serialVersionUID = 0L;

    private int currentNestingLevel;  // current scope nesting level
    private SymTableEntry programId;    // entry for the main program id

    /**
     * Constructor.
     */
    public SymTableStack() {
        this.currentNestingLevel = 0;
        add(new SymTable(currentNestingLevel));
    }

    /**
     * Getter.
     *
     * @return the current nesting level.
     */
    public int getCurrentNestingLevel() {
        return currentNestingLevel;
    }

    /**
     * Getter.
     *
     * @return the symbol table entry for the main program identifier.
     */
    public SymTableEntry getProgramId() {
        return programId;
    }

    /**
     * Setter.
     *
     * @param id the symbol table entry for the main program identifier.
     */
    public void setProgramId(SymTableEntry id) {
        this.programId = id;
    }

    /**
     * Return the local symbol table which is at the top of the stack.
     *
     * @return the local symbol table.
     */
    public SymTable getLocalSymTable() {
        return get(currentNestingLevel);
    }

    /**
     * Push a new symbol table onto the symbol table stack.
     *
     * @return the pushed symbol table.
     */
    public SymTable push() {
        SymTable symTable = new SymTable(++currentNestingLevel);
        add(symTable);

        return symTable;
    }

    /**
     * Push a symbol table onto the symbol table stack.
     *
     * @return the pushed symbol table.
     */
    public SymTable push(SymTable symTable) {
        ++currentNestingLevel;
        add(symTable);

        return symTable;
    }

    /**
     * Pop a symbol table off the symbol table stack.
     *
     * @return the popped symbol table.
     */
    public SymTable pop() {
        SymTable symTable = get(currentNestingLevel);
        remove(currentNestingLevel--);

        return symTable;
    }

    /**
     * Create and enter a new entry into the local symbol table.
     *
     * @param name the name of the entry.
     * @param kind what kind of entry.
     * @return the new entry.
     */
    public SymTableEntry enterLocal(String name, Kind kind) {
        return get(currentNestingLevel).enter(name, kind);
    }

    /**
     * Look up an existing symbol table entry in the local symbol table.
     *
     * @param name the name of the entry.
     * @return the entry, or null if it does not exist.
     */
    public SymTableEntry lookupLocal(String name) {
        return get(currentNestingLevel).lookup(name);
    }

    /**
     * Look up an existing symbol table entry throughout the stack.
     *
     * @param name the name of the entry.
     * @return the entry, or null if it does not exist.
     */
    public SymTableEntry lookup(String name) {
        SymTableEntry foundEntry = null;

        // Search the current and enclosing scopes.
        for (int i = currentNestingLevel; (i >= 0) && (foundEntry == null); --i) {
            foundEntry = get(i).lookup(name);
        }

        return foundEntry;
    }
}
