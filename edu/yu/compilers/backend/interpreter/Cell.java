/**
 * <h1>Cell</h1>
 * <p>The interpreter's runtime memory cell.</p>
 * <p>Adapted from</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 */

package edu.yu.compilers.backend.interpreter;

public class Cell {
    private Object value;  // value contained in the memory cell

    /**
     * Constructor.
     *
     * @param value the value for the cell.
     */
    public Cell(Object value) {
        this.value = value;
    }

    /**
     * Get the value in the cell.
     *
     * @return the value.
     */
    public Object getValue() {
        return value;
    }

    /**
     * Set a new value into the cell.
     *
     * @param newValue the new value.
     */
    public void setValue(Object newValue) {
        value = newValue;
    }
}
