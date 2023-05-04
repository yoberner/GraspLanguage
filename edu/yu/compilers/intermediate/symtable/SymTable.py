# <h1>SymTable</h1>
# <p>The symbol table.</p>
# <p>Adapted from</p>
# <p>Copyright (c) 2020 by Ronald Mak</p>
from collections import OrderedDict

from edu.yu.compilers.intermediate.symtable.SymTableEntry import SymTableEntry


# import edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind;
# import java.util.ArrayList;
# import java.util.Collection;
# import java.util.Iterator;
# import java.util.TreeMap;
# import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind.VARIABLE;

class SymTable(OrderedDict) :
    UNNAMED_PREFIX = "_unnamed_"
    serialVersionUID = 0 #will convert to long automatically when needed via python
    unnamedIndex = 0

    # Constructor.
    # @param nestingLevel the symbol table's nesting level.
    def __init__(self, nestingLevel):
        super().__init__()
        self.nestingLevel = nestingLevel
        self.slotNumber = -1
        self.maxSlotNumber = None
        self.ownerId = None


    # Generate a name for an unnamed type.
    # @return the name;
    @staticmethod
    def generateUnnamedName(self) :
        self.unnamedIndex += 1
        return self.UNNAMED_PREFIX + self.unnamedIndex


    # Get the scope nesting level.
    # @return the nesting level.
    def getNestingLevel(self):
        return self.nestingLevel


    # Get the maximum local variables array slot number.
    #     @return the maximum slot number.
    def getMaxSlotNumber(self):
        return self.maxSlotNumber


    # Compute and return the next local variables array slot number
    # @return the slot number.
    def nextSlotNumber(self):
        self.maxSlotNumber = self.slotNumber + 1
        return self.slotNumber


    # Getter.
    # @return the owner of this symbol table.
    def getOwner(self):
        return self.ownerId


    # Set the owner of this symbol table.
    # @param ownerId the symbol table entry of the owner.
    def setOwner(self, ownerId) :
        self.ownerId = ownerId


    # Create and enter a new entry into the symbol table.
    # @param name the name of the entry.
    # @param kind the kind of entry.
    # @return the new entry.
    def enter(self, name, kind) :
        entry = SymTableEntry(name, kind, self)
        super().__setitem__(name, entry)
        return entry

    # Look up an existing symbol table entry.
    #     @param name the name of the entry.
    # @return the entry, or null if it does not exist.
    def lookup(self, name) :
        return super().__getitem__(name)

    # Return an arraylist of entries sorted by name.
    # @return the sorted arraylist.
    def sortedEntries(self):
        entries = super().values()
        list = []

        # Iterate over the entries and append them to the list.
        for entry in entries:
            list.append(entry)

        return list

    # Reset all the variable entries to a kind.
    # @param kind the kind to set.
    def resetVariables(self, kind):
        entries = super().values()

        # Iterate over the entries and reset their kind.
        for entry in entries:
            if entry.getKind() == SymTableEntry.Kind.VARIABLE:
                entry.setKind(kind)
