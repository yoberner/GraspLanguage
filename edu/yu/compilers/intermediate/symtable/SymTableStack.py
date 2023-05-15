from multipledispatch import dispatch
from edu.yu.compilers.intermediate.symtable.SymTable import SymTable
from edu.yu.compilers.intermediate.symtable.SymTableEntry import SymTableEntry


class SymTableStack(list):
    serialVersionUID = 0

    def __init__(self):
        super().__init__()
        self.currentNestingLevel = 0
        # change all below super() to self if doesnt work
        super().append(SymTable(self.currentNestingLevel))  # ChatGPT used self instead of super()
        self.programId = None

    def getCurrentNestingLevel(self) -> int:  # chatGPT used - > <ret type> :
        return self.currentNestingLevel

    def getProgramId(self):
        return self.programId

    def setProgramId(self, _id: SymTableEntry):
        self.programId = _id

    def getLocalSymTable(self):
        return super()[self.currentNestingLevel]

    # ChatGPT Did not seem to properly override the methods in Python

    @dispatch()  # Not sure if this will work
    def push(self):
        self.currentNestingLevel += 1
        symTable = SymTable(self.currentNestingLevel)
        super().append(symTable)
        return symTable

    @dispatch(SymTable)  # FIXME
    def push(self, symTable):
        self.currentNestingLevel += 1
        super().append(symTable)

        return symTable

    def _pop(self): # TODO no issues?
        symTable = super()[self.currentNestingLevel]
        self.currentNestingLevel -= 1
        super().remove(self.currentNestingLevel)
        # We differ slightly but may be functionally identical - I remove by index
        # ChatGPT simply pops - but I think same effect is achieved.

        return symTable

    def enterLocal(self, name, kind):
        return super()[self.currentNestingLevel].enter(name, kind)  # This is correct

    def lookupLocal(self, name):
        return super()[self.currentNestingLevel].lookup(name)  # This is correct

    def lookup(self, name):
        foundEntry = None

        # Search the current and enclosing scopes.
        i = self.currentNestingLevel
        while (i >= 0) and (foundEntry is None):
            foundEntry = super()[i].lookup(name)
            i += 1
            # it also added a break statement

        # ChatGPT's loop - very nice
        # for i in range(self.currentNestingLevel, -1, -1):
        #     foundEntry = self[i].lookup(name)
        #     if foundEntry:
        #         break

        return foundEntry
