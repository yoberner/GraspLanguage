/**
 * <h1>MemoryMap</h1>
 * <p>The interpreter's runtime memory map.</p>
 * <p>Adapted from</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 */

package edu.yu.compilers.backend.interpreter;

import edu.yu.compilers.intermediate.symtable.SymTable;
import edu.yu.compilers.intermediate.symtable.SymTableEntry;
import edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind;
import edu.yu.compilers.intermediate.type.Typespec;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class MemoryMap extends HashMap<String, Cell> {
    /**
     * Constructor.
     * Create a memory map and allocate its memory cells
     * based on the entries in a symbol table.
     *
     * @param symTable the symbol table.
     */
    public MemoryMap(SymTable symTable) {
        ArrayList<SymTableEntry> entries = symTable.sortedEntries();

        // Loop for each entry of the symbol table.
        for (SymTableEntry entry : entries) {
            Kind kind = entry.getKind();

            switch (kind) {
                case VARIABLE:
                case FUNCTION:
                case VALUE_PARAMETER:
                case RECORD_FIELD: {
                    // Not a reference parameter: Allocate cells for the
                    //                            value in the hashmap.
                    String name = entry.getName();
                    Typespec type = entry.getType();
                    put(name, new Cell(allocateCellValue(type)));
                    break;
                }

                case REFERENCE_PARAMETER: {
                    // Reference parameter: Allocate a single cell to hold a 
                    //                      reference in the hashmap.
                    String name = entry.getName();
                    put(name, new Cell(null));
                }

                default:
                    break;
            }
        }
    }

    /**
     * Return the memory cell with the given name.
     *
     * @param name the name.
     * @return the cell.
     */
    public Cell getCell(String name) {
        return get(name);
    }

    /**
     * Replace the memory cell with the given name.
     *
     * @param name the name.
     * @param cell the replacement cell.
     */
    public void replaceCell(String name, Cell cell) {
        put(name, cell);
    }

    /**
     * Get an arraylist of all the names in the memory map.
     *
     * @return the arraylist.
     */
    public ArrayList<String> getAllNames() {

        Set<String> names = keySet();

        return new ArrayList<>(names);
    }

    /**
     * Make an allocation for a value of a given data type for a memory cell.
     *
     * @param type the data type.
     * @return the allocation.
     */
    private Object allocateCellValue(Typespec type) {
        return switch (type.getForm()) {
            case ARRAY -> allocateArrayCells(type);
            case RECORD -> allocateRecordMap(type);
            default -> null;  // uninitialized scalar value
        };
    }

    /**
     * Allocate the memory cells of an array.
     *
     * @param type the array type.
     * @return the allocation.
     */
    private Object[] allocateArrayCells(Typespec type) {
        int elemCount = type.getArrayElementCount();
        Typespec elemType = type.getArrayElementType();
        Cell[] allocation = new Cell[elemCount];

        for (int i = 0; i < elemCount; ++i) {
            allocation[i] = new Cell(allocateCellValue(elemType));
        }

        return allocation;
    }

    /**
     * Allocate the memory map for a record.
     *
     * @param type the record type.
     * @return the allocation.
     */
    private MemoryMap allocateRecordMap(Typespec type) {
        SymTable symTable = type.getRecordSymTable();

        return new MemoryMap(symTable);
    }
}
