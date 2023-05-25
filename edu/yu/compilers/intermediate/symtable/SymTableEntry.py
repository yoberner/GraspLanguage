import abc
from edu.yu.compilers.intermediate.symtable.Kind import Kind
from edu.yu.compilers.intermediate.symtable.Routine import Routine
from enum import Enum
from edu.yu.compilers.intermediate.type.Typespec import Typespec



class SymTableEntry:
    # Entry information interface.
    class EntryInfo(abc.ABC):
        dud = None


    # Value information.
    class ValueInfo(EntryInfo):
        value = None

    # Routine information.
    class RoutineInfo(EntryInfo):
        code = None  # routine code
        symtable = None  # routine's symbol table
        parameters = None  # routine's formal parameters
        subroutines = None  # symTable entries of subroutines
        executable = None  # routine's executable code
        inline = False

    # Constructor.
      #
      # @param name     the name of the entry.
      # @param kind     the kind of entry.
      # @param symTable the symbol table that contains this entry.

    def __init__(self, name, kind, symTable) :
        self.name = name
        self.kind = kind
        self.symTable = symTable
        self.lineNumbers = []
        self.typeSpec = None
        self.slotNumber = None

        # Initialize the appropriate entry information.
        if self.kind == Kind.CONSTANT or self.kind == Kind.ENUMERATION_CONSTANT or self.kind == Kind.VARIABLE or self.kind == Kind.RECORD_FIELD or self.kind == Kind.VALUE_PARAMETER :
            self.info = self.ValueInfo()
        elif self.kind == Kind.PROGRAM or self.kind == Kind.PROCEDURE or self.kind == Kind.FUNCTION:
            self.info = self.RoutineInfo()
            self.info.inline = False
            self.info.parameters = []
            self.info.subroutines = []

    # Get the name of the entry.
    # @return the name.
    def getName(self):
        return self.name


    # Get the kind of entry.
    #
    # @return the 

    def getKind(self) :
        return self.kind

    # Set the kind of entry.
    #
    # @param kind the kind to set.

    def setKind(self, kind) :
        self.kind = kind


    # Get the symbol table that contains this entry.
    #
    # @return the symbol table.

    def getSymTable(self) :
        return self.symTable


    # Get the slot number of the local variables array.
    #
    # @return the number.

    def getSlotNumber(self) :
        return self.slotNumber


    # Set the slot number of the local variables array.
    #
    # @param slotNumber the number to set.

    def setSlotNumber(self, slotNumber) :
        self.slotNumber = slotNumber


    # Get the type specification of the entry.
    #
    # @return the type specification.

    def getType(self) :
        return self.typespec


    # Set the type specification.
    #
    # @param typespec the type specification to set.

    def setType(self, typespec) :
        self.typespec = typespec



    # Get the arraylist of source line numbers for the entry.
    #
    # @return the arraylist.

    def getLineNumbers(self) :
        return self.lineNumbers


    # Append a source line number to the entry.
    #
    # @param lineNumber the line number to append.

    def appendLineNumber(self, lineNumber) :
        self.lineNumbers.append(lineNumber)


    # Get the data value stored with this entry.
    #
    # @return the data value.

    def getValue(self) :
        return self.info.value


    # Set the data value into this entry.
    #
    # @param value the value to set.

    def setValue(self, value) :
        self.info.value = value


    # Get the routine code.
    #
    # @return the code.

    def getRoutineCode(self) :
        return self.info.code


    # Set the routine code.
    #
    # @param code the code to set.

    def setRoutineCode(self, code) :
        self.info.code = code


    # Get the routine's symbol table.
    #
    # @return the symbol table.

    def getRoutineSymTable(self) :
        return self.info.symTable


     # Set the routine's symbol table.
     #
     # @param symTable the symbol table to set.

    def setRoutineSymTable(self, symTable) :
        self.info.symTable = symTable

    # Get the arraylist of symbol table entries of the routine's formal parameters.
    #
    # @return the arraylist.

    def getRoutineParameters(self) :
        return self.info.parameters

    # Set the arraylist symbol table entries of parameters of the routine.
    #
    # @param parameters the arraylist to set.
    def setRoutineParameters(self, parameters) :
        self.info.parameters = parameters

    # Get the arraylist of symbol table entries of the nested subroutines.
    #
    # @return the arraylist.

    def getSubroutines(self) :
        return self.info.subroutines

    # Append to the arraylist of symbol table entries of the nested subroutines.
    #
    # @param subroutineId the symbol table entry of the subroutine to append.

    def appendSubroutine(self, subroutineId) :
        self.info.subroutines.append(subroutineId)

    # Get the routine's executable code.
    #
    # @return the executable code.
    def getExecutable(self) :
        return self.info.executable

    # Set the routine's executable code.
    #
    # @param executable the executable code to set.
    def setExecutable(self, executable) :
        self.info.executable = executable

    def isInline(self):
        return self.info.inline;

    def setInline(self, inline):
        self.info.inline = inline

