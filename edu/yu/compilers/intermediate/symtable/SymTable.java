/**
 * <h1>SymTable</h1>
 * <p>The symbol table.</p>
 * <p>Adapted from</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 */
package edu.yu.compilers.intermediate.symtable;

import edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.TreeMap;

import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind.VARIABLE;

public class SymTable
        extends TreeMap<String, SymTableEntry> {
    public static final String UNNAMED_PREFIX = "_unnamed_";
    private static final long serialVersionUID = 0L;
    private static int unnamedIndex = 0;
    private final int nestingLevel;       // scope nesting level
    private int slotNumber;         // local variables array slot number
    private int maxSlotNumber;      // max slot number value
    private SymTableEntry ownerId;    // symbol table entry of this symTable owner

    /**
     * Constructor.
     *
     * @param nestingLevel the symbol table's nesting level.
     */
    public SymTable(int nestingLevel) {
        this.nestingLevel = nestingLevel;
        this.slotNumber = -1;
    }

    /**
     * Generate a name for an unnamed type.
     *
     * @return the name;
     */
    public static String generateUnnamedName() {
        unnamedIndex++;
        return UNNAMED_PREFIX + unnamedIndex;
    }

    /**
     * Get the scope nesting level.
     *
     * @return the nesting level.
     */
    public int getNestingLevel() {
        return nestingLevel;
    }

    /**
     * Get the maximum local variables array slot number.
     *
     * @return the maximum slot number.
     */
    public int getMaxSlotNumber() {
        return maxSlotNumber;
    }

    /**
     * Compute and return the next local variables array slot number
     *
     * @return the slot number.
     */
    public int nextSlotNumber() {
        maxSlotNumber = ++slotNumber;
        return slotNumber;
    }

    /**
     * Getter.
     *
     * @return the owner of this symbol table.
     */
    public SymTableEntry getOwner() {
        return ownerId;
    }

    /**
     * Set the owner of this symbol table.
     *
     * @param ownerId the symbol table entry of the owner.
     */
    public void setOwner(SymTableEntry ownerId) {
        this.ownerId = ownerId;
    }

    /**
     * Create and enter a new entry into the symbol table.
     *
     * @param name the name of the entry.
     * @param kind the kind of entry.
     * @return the new entry.
     */
    public SymTableEntry enter(String name, Kind kind) {
        SymTableEntry entry = new SymTableEntry(name, kind, this);
        put(name, entry);

        return entry;
    }

    /**
     * Look up an existing symbol table entry.
     *
     * @param name the name of the entry.
     * @return the entry, or null if it does not exist.
     */
    public SymTableEntry lookup(String name) {
        return get(name);
    }

    /**
     * Return an arraylist of entries sorted by name.
     *
     * @return the sorted arraylist.
     */
    public ArrayList<SymTableEntry> sortedEntries() {
        Collection<SymTableEntry> entries = values();
        Iterator<SymTableEntry> iter = entries.iterator();
        ArrayList<SymTableEntry> list = new ArrayList<>(size());

        // Iterate over the sorted entries and append them to the list.
        while (iter.hasNext()) list.add(iter.next());

        return list;  // sorted list of entries
    }

    /**
     * Reset all the variable entries to a kind.
     *
     * @param kind the kind to set.
     */
    public void resetVariables(Kind kind) {
        Collection<SymTableEntry> entries = values();

        // Iterate over the entries and reset their kind.
        for (SymTableEntry entry : entries) {
            if (entry.getKind() == VARIABLE) entry.setKind(kind);
        }
    }
}
