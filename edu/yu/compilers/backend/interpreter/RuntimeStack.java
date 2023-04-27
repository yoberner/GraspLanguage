/**
 * <h1>RuntimeStackImpl</h1>
 * <p>The interpreter's runtime stack.</p>
 * <p>Adapted from</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 */
package edu.yu.compilers.backend.interpreter;

import java.util.ArrayList;


public class RuntimeStack extends ArrayList<StackFrame> {
    private final RuntimeDisplay display;  // runtime display

    /**
     * Constructor.
     */
    public RuntimeStack() {
        display = new RuntimeDisplay();
    }

    /**
     * Get the topmost stack frame at a given nesting level.
     *
     * @param nestingLevel the nesting level.
     * @return the stack frame.
     */
    public StackFrame getTopmost(int nestingLevel) {
        return display.getStackFrame(nestingLevel);
    }

    /**
     * Get the current nesting level.
     *
     * @return the current level.
     */
    public int currentNestingLevel() {
        int topIndex = size() - 1;
        return topIndex >= 0 ? get(topIndex).getNestingLevel() : -1;
    }

    /**
     * Push a stack frame onto the stack for a routine being called.
     *
     * @param frame the stack frame to push.
     */
    public void push(StackFrame frame) {
        int nestingLevel = frame.getNestingLevel();

        add(frame);
        display.callUpdate(nestingLevel, frame);
    }

    /**
     * Pop a stack frame off the stack for a returning routine.
     */
    public void pop() {
        display.returnUpdate(currentNestingLevel());
        remove(size() - 1);
    }
}
