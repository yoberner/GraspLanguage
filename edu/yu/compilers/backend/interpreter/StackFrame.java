/**
 * <h1>StackFrame</h1>
 * <p>The runtime stack frame.</p>
 * <p>Adapted from</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 */

package edu.yu.compilers.backend.interpreter;

import edu.yu.compilers.intermediate.symtable.SymTable;
import edu.yu.compilers.intermediate.symtable.SymTableEntry;

import java.util.ArrayList;

public class StackFrame {
    private final SymTableEntry routineId;  // symbol table entry of the routine's name
    private final int nestingLevel;       // scope nesting level of this frame
    private final MemoryMap memoryMap;    // memory map of this stack frame
    private StackFrame backlink;    // backlink to the previous frame

    /**
     * Constructor.
     *
     * @param routineId the symbol table entry of the routine's name.
     */
    public StackFrame(SymTableEntry routineId) {
        SymTable symTable = routineId.getRoutineSymTable();

        this.routineId = routineId;
        this.backlink = null;
        this.nestingLevel = symTable.getNestingLevel();
        this.memoryMap = new MemoryMap(symTable);
    }

    /**
     * Get the symbol table entry of the routine's name.
     *
     * @return the symbol table entry.
     */
    public SymTableEntry getRoutineId() {
        return routineId;
    }

    /**
     * Get the memory cell for the given name from the memory map.
     *
     * @param name the name.
     * @return the cell.
     */
    public Cell getCell(String name) {
        return memoryMap.getCell(name);
    }

    /**
     * Replace the memory cell with the given name in the memory map.
     *
     * @param name the name.
     * @param cell the replacement cell.
     */
    public void replaceCell(String name, Cell cell) {
        memoryMap.replaceCell(name, cell);
    }

    /**
     * Get the list of all the names in the memory map.
     *
     * @return the list of names.
     */
    public ArrayList<String> getAllNames() {
        return memoryMap.getAllNames();
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
     * Get the stack frame to which this frame is dynamically linked.
     *
     * @return the link.
     */
    public StackFrame backlink() {
        return backlink;
    }

    /**
     * Make a backlink from this stack frame to another one.
     *
     * @param frame the stack frame to link to.
     * @return this stack frame.
     */
    public StackFrame createBacklink(StackFrame frame) {
        backlink = frame;
        return this;
    }
}
