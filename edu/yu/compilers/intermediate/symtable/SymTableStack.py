from multipledispatch import dispatch
from edu.yu.compilers.intermediate.symtable.SymTable import SymTable


class SymTableStack(list):
    serialVersionUID = 0

    def __init__(self):
        super().__init__()
        self.currentNestingLevel = 0
        super().append(SymTable(self.currentNestingLevel))
        self.programId = None

    def getCurrentNestingLevel(self):
        return self.currentNestingLevel

    def getProgramId(self):
        return self.programId

    def setProgramId(self, id):
        self.programId = id

    def getLocalSymTable(self):
        return super.pop(self.currentNestingLevel)

    @dispatch()
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

    def _pop(self):
        symTable = super().pop(self.currentNestingLevel)
        self.currentNestingLevel -= 1
        super().remove(self.currentNestingLevel)

        return symTable

    def enterLocal(self, name, kind):
        return super().pop(self.currentNestingLevel).enter(name, kind)  # This is correct

    def lookupLocal(self, name):
        return super().pop(self.currentNestingLevel).lookup(name)  # This is correct

    def lookup(self, name):
        foundEntry = None

        # Search the current and enclosing scopes.
        i = self.currentNestingLevel
        while ((i >= 0) and (foundEntry == None)):
            foundEntry = super().pop(i).lookup(name)
            i += 1

        return foundEntry
