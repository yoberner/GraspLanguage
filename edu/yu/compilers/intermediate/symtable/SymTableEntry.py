# <h1>SymTableEntryImpl</h1>
# <p>An implementation of a symbol table entry.</p>
# <p>Adapted from:</p>
# <p>Copyright (c) 2020 by Ronald Mak</p>
# <p>For instructional purposes only.  No warranties.</p>
import abc
from enum import Enum

# import edu.yu.compilers.intermediate.type.Typespec;
#
# import java.util.ArrayList;


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
        kind = SymTableEntry.Kind
        if kind ==  kind.CONSTANT or kind == kind.ENUMERATION_CONSTANT or kind == kind.VARIABLE or kind == kind.RECORD_FIELD or kind == kind.VALUE_PARAMETER :
            self.info = self.ValueInfo()
        elif kind == kind.PROGRAM or kind == kind.PROCEDURE or kind == kind.FUNCTION:
            self.info = self.RoutineInfo()
            self.info.parameters = []
            self.info.subroutines = []

    # Get the name of the entry.
    # @return the name.
    def getName(self):
        return self.name


    # Get the kind of entry.
    #
    # @return the kind.

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
        self.lineNumbers.add(lineNumber)


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
        self.info.subroutines.add(subroutineId)

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

    # What kind of identifier.

    class Kind(Enum):
        CONSTANT = 1
        ENUMERATION_CONSTANT = 2
        TYPE = 3
        VARIABLE = 4
        RECORD_FIELD = 5
        VALUE_PARAMETER = 6
        REFERENCE_PARAMETER = 7
        PROGRAM_PARAMETER = 8
        PROGRAM = 9
        PROCEDURE = 10
        FUNCTION = 11
        UNDEFINED = 12

        def __str__(self):
          return self.name.lower()

    # Which routine.
    class Routine(Enum):
        DECLARED = 1
        FORWARD = 2
        READ = 3
        READLN = 4
        WRITE = 5
        WRITELN = 6
        ABS = 7
        ARCTAN = 8
        CHR = 9
        COS = 10
        EOF = 11
        EOLN = 12
        EXP = 13
        LN = 14
        ODD = 15
        ORD = 16
        PRED = 17
        ROUND = 18
        SIN = 19
        SQR = 20
        SQRT = 21
        SUCC = 22
        TRUNC = 23

