from edu.yu.compilers.intermediate.symtable.SymTable import SymTable
from edu.yu.compilers.intermediate.symtable.SymTable import SymTableEntry

from Form import Form


class Typespec:

    def __init__(self, form: Form):
        self.form = form
        self.identifier = None

        # Initialize the appropriate type information.
        if self.form == Form.ENUMERATION:
            self.info = EnumerationInfo()
            self.info.constants = []
        elif self.form == Form.SUBRANGE:
            self.info = SubrangeInfo()
            self.info.minValue = 0
            self.info.maxValue = 0
            self.info.baseType = None
        elif self.form == Form.ARRAY:
            self.info = ArrayInfo()
            self.info.indexType = None
            self.info.elementType = None
            self.info.elementCount = 0
        elif self.form == Form.RECORD:
            self.info = RecordInfo()
            self.info.typePath = None
            self.info.symTable = None
        else:
            self.info = None

    # Determine whether the type is structured (array or record).
    # @return true if structured, false if not.

    def isStructured(self):
        return (self.form == Form.ARRAY) or (self.form == Form.RECORD)

    # Get the type form.
    # @return the form.

    def getForm(self):
        return self.form

    # Get the type identifier.
    # @return the identifier's symbol table entry.

    def getIdentifier(self):
        return self.identifier

    # Setter.
    # @param identifier the type identifier (symbol table entry).

    def setIdentifier(self, identifier):
        self.identifier = identifier

    # Get the base type of this type.
    # @return the base type.

    def baseType(self):
        if self.form == Form.SUBRANGE:
            return self.info.baseType
        else:
            return self

        # return self.info.baseType if self.form == Form.SUBRANGE else self

        # return form == Form.SUBRANGE ? self.info.baseType : this

    # Get the subrange base type.
    # @return the base type.

    def getSubrangeBaseType(self):
        return self.info.baseType

    # Set the subrange base type.
    # @param baseType the base type to set.

    def setSubrangeBaseType(self, baseType):
        self.info.baseType = baseType

    # Get the subrange minimum value.
    # @return the value.

    def getSubrangeMinValue(self):
        return self.info.minValue

    # Set the subrange minimum value.
    # @param minValue the value to set.

    def setSubrangeMinValue(self, minValue):
        self.info.minValue = minValue

    # Get the subrange maximum value.
    # @return the value.

    def getSubrangeMaxValue(self):
        return self.info.maxValue

    # Set the subrange maximum value.
    # @param maxValue the value to set.

    def setSubrangeMaxValue(self, maxValue):
        self.info.maxValue = maxValue

    # Get the arraylist of symbol table entries of enumeration constants.
    # @return the arraylist.

    def getEnumerationConstants(self):
        return self.info.constants

    # Set the vector of enumeration constants symbol table entries.
    # @param constants the vector to set.

    def setEnumerationConstants(self, constants):
        self.info.constants = constants

    # Get the array index data type.
    # @return the data type.

    def getArrayIndexType(self):
        return self.info.indexType

    # Set the array index data type.
    # @param indexType the data type to set.

    def setArrayIndexType(self, indexType):
        self.info.indexType = indexType

    # Get the array element data type.
    # @return the data type.

    def getArrayElementType(self):
        return self.info.elementType

    # Set the array element data type.
    # @param elementType the data type to set.

    def setArrayElementType(self, elementType):
        self.info.elementType = elementType

    # Get the array element count.
    # @return the count.

    def getArrayElementCount(self):
        return self.info.elementCount

    # Set the array element count.
    # @param elementCount the count to set.

    def setArrayElementCount(self, elementCount):
        self.info.elementCount = elementCount

    # Get the base type of array.
    # @return the base type of its final dimension.

    def getArrayBaseType(self):
        elemType = self

        while elemType.form == self.ARRAY:
            elemType = elemType.getArrayElementType()

        return elemType.baseType()

    # Get the record's symbol table.
    # @return the symbol table.
    def getRecordSymTable(self):
        return self.info.symTable

    # Set the record's symbol table.
    # @param symTable the symbol table to set.
    def setRecordSymTable(self, symTable):
        self.info.symTable = symTable

    # Get a record type's fully qualified type path.
    # @return the path.
    def getRecordTypePath(self):
        return self.info.typePath

    # Set a record type's fully qualified type path.
    # @param typePath the path to set.
    def setRecordTypePath(self, typePath):
        self.info.typePath = typePath




class TypeInfo:
    pass

class EnumerationInfo(TypeInfo):
    def __init__(self):
        self.constants = []

class SubrangeInfo(TypeInfo):
    def __init__(self):
        self.baseType = None
        self.minValue = 0
        self.maxValue = 0

class ArrayInfo(TypeInfo):
    def __init__(self):
        self.indexType = None
        self.elementType = None
        self.elementCount = 0

class RecordInfo(TypeInfo):
    def __init__(self):
        self.typePath = ""
        self.symTable = None
