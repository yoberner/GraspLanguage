/**
 * <h1>RuntimeDisplay</h1>
 * <p>The interpreter's runtime display.</p>
 * <p>Adapted from</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 */
package edu.yu.compilers.backend.interpreter;

import java.util.ArrayList;


public class RuntimeDisplay extends ArrayList<StackFrame> {
    /**
     * Constructor.
     */
    public RuntimeDisplay() {
        add(null);  // dummy element 0 (never used)
    }

    /**
     * Get the stack frame at a given nesting level.
     *
     * @param nestingLevel the nesting level.
     * @return the stack frame.
     */
    public StackFrame getStackFrame(int nestingLevel) {
        return get(nestingLevel);
    }

    /**
     * Update the display for a call to a routine at a given nesting level.
     *
     * @param nestingLevel the nesting level.
     * @param frame        the stack frame for the routine.
     */
    public void callUpdate(int nestingLevel, StackFrame frame) {
        // Next higher nesting level: Append a new element at the top.
        if (nestingLevel >= size()) add(frame);

            // Existing nesting level: Set at the specified level.
        else {
            StackFrame prevFrame = get(nestingLevel);
            set(nestingLevel, frame.createBacklink(prevFrame));
        }
    }

    /**
     * Update the display for a return from a routine at a given nesting level.
     *
     * @param nestingLevel the nesting level.
     */
    public void returnUpdate(int nestingLevel) {
        int topIndex = size() - 1;
        StackFrame frame = get(nestingLevel);     // frame about to be popped off
        StackFrame prevFrame = frame.backlink();  // previous frame it points to

        // Point the element at that nesting level
        // to the previous stack frame.
        if (prevFrame != null) set(nestingLevel, prevFrame);

            // The top element has become null, so remove it.
        else if (nestingLevel == topIndex) remove(topIndex);
    }
}
