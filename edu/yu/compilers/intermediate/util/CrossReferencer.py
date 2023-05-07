from edu.yu.compilers.intermediate.symtable.Predefined import Predefined
from edu.yu.compilers.intermediate.symtable.SymTable import SymTable
from edu.yu.compilers.intermediate.symtable.SymTableEntry import SymTableEntry
from edu.yu.compilers.intermediate.type.Typespec import Typespec


# /**
#  * <h1>CrossReferencer</h1>
#  * <p>Generate a cross-reference listing.</p>
#  * <p>Adapted from</p>
#  * <p>Copyright (c) 2020 by Ronald Mak</p>
#  */

class CrossReferencer:
    NAME_WIDTH = 16
    NAME_FORMAT = "%-{NAME_WIDTH}s"
    NUMBERS_LABEL = " Line numbers    "
    NUMBERS_UNDERLINE = " ------------    "
    NUMBER_FORMAT = " %03d"

    LABEL_WIDTH = len(NUMBERS_LABEL)
    INDENT_WIDTH = NAME_WIDTH + LABEL_WIDTH

    INDENT = str(INDENT_WIDTH) + (" " * INDENT_WIDTH)
    ENUM_CONST_FORMAT = "%" + str(NAME_WIDTH) + "s = %s"

    # Print the cross-reference table.
    # @param symTableStack the symbol table stack.
    def _print(self, symTableStack):
        print("\n===== CROSS-REFERENCE TABLE =====")

        programId = symTableStack.getProgramId()
        printRoutine(programId)

    # Print a cross-reference table for a routine.
    # @param routineId the routine identifier's symbol table entry.
    def printRoutine(self, routineId):
        kind = routineId.getKind()
        print("\n*** ", str(kind).upper(), " ", routineId.getName(), " ***")
        printColumnHeadings()

        # Print the entries in the routine's symbol table.
        symTable = routineId.getRoutineSymTable()
        printSymTable(symTable)

        # Print any procedures and functions defined in the routine.
        subroutineIds = routineId.getSubroutines()
        if subroutineIds != None:
            for rtnId in subroutineIds:
                printRoutine(rtnId)

    #
    # /**
    #  * Print column headings.
    #  */
    # private void printColumnHeadings() {
    #     System.out.println();
    #     System.out.println(String.format(NAME_FORMAT, "Identifier") + NUMBERS_LABEL + "Type specification");
    #     System.out.println(String.format(NAME_FORMAT, "----------") + NUMBERS_UNDERLINE + "------------------");
    # }
    #
    # /**
    #  * Print the entries in a symbol table.
    #  *
    #  * @param symTable the symbol table.
    #  */
    # private void printSymTable(SymTable symTable) {
    #     ArrayList<SymTableEntry> sorted = symTable.sortedEntries();
    #
    #     // Loop over the sorted list of table entries
    #     // to print each entry of this symbol table.
    #     for (SymTableEntry entry : sorted) {
    #         ArrayList<Integer> lineNumbers = entry.getLineNumbers();
    #
    #         // For each entry, print the identifier name
    #         // followed by the line numbers.
    #         System.out.printf(NAME_FORMAT, entry.getName());
    #         if (lineNumbers != null) {
    #             for (Integer lineNumber : lineNumbers) {
    #                 System.out.printf(NUMBER_FORMAT, lineNumber);
    #             }
    #         }
    #
    #         // Print the symbol table entry.
    #         System.out.println();
    #         printEntry(entry);
    #     }
    #
    #     // Loop over the sorted list of entries again
    #     // to print each nested record's symbol table.
    #     for (SymTableEntry entry : sorted) {
    #         if (entry.getKind() == TYPE) {
    #             Typespec type = entry.getType();
    #             if (type.getForm() == RECORD) printRecord(type);
    #         }
    #     }
    # }
    #
    # /**
    #  * Print a symbol table entry.
    #  *
    #  * @param entry the symbol table entry.
    #  */
    # private void printEntry(SymTableEntry entry) {
    #     Kind kind = entry.getKind();
    #     int nestingLevel = entry.getSymTable().getNestingLevel();
    #     System.out.println(INDENT + "Kind: " + kind.toString().replace("_", " "));
    #     System.out.println(INDENT + "Scope nesting level: " + nestingLevel);
    #
    #     // Print the type specification.
    #     Typespec type = entry.getType();
    #     printType(type);
    #
    #     switch (kind) {
    #         case CONSTANT -> {
    #             Object value = entry.getValue();
    #             System.out.println(INDENT + "Value: " + toString(value, type));
    #
    #             // Print the type details only if the type is unnamed.
    #             if (type.getIdentifier() == null) {
    #                 printTypeDetail(type);
    #             }
    #
    #         }
    #         case ENUMERATION_CONSTANT -> {
    #             Object value = entry.getValue();
    #             System.out.println(INDENT + "Value: " + toString(value, type));
    #
    #         }
    #         case TYPE -> {
    #             // Print the type details only when the type is first defined.
    #             if (entry == type.getIdentifier()) {
    #                 printTypeDetail(type);
    #             }
    #
    #         }
    #         case VARIABLE -> {
    #             // Print the type details only if the type is unnamed.
    #             if (type.getIdentifier() == null) {
    #                 printTypeDetail(type);
    #             }
    #
    #         }
    #         case RECORD_FIELD -> printTypeDetail(type);
    #         default -> {
    #         }
    #     }
    # }

    # Print a type specification.
    # @param type the type specification.
    def printType(self, type):
        if type is not None:
            form = type.getForm()
            typeId = type.getIdentifier()

            typeName = None
            if typeId is not None:
                typeName = typeId.getName()
            else:
                typeName = "<unnamed>"

            print(INDENT + "Type form: ", str(form), ", Type id: ", str(typeName))

    # Print the details of a type specification.
    # @param type the type specification.
    def printTypeDetail(self, type: Typespec):
        global INDENT
        global ENUM_CONST_FORMAT
        form = type.getForm()

        if form == ENUMERATION:
            constantIds = type.getEnumerationConstants()

            print(INDENT, "--- Enumeration constants ---");

            # Print each enumeration constant and its value.
            for constantId in constantIds:
                name = constantId.getName()
                value = constantId.getValue()

                print(INDENT, ENUM_CONST_FORMAT % (name, value))
        elif form == SUBRANGE:
            minValue = type.getSubrangeMinValue()
            maxValue = type.getSubrangeMaxValue()
            baseType = type.baseType()

            print(INDENT + "--- Base type ---")
            printType(baseType)

            # Print the base type details only if the type is unnamed.
            if baseType.getIdentifier() == None:
                printTypeDetail(baseType)

            print(INDENT, "Range: ", end="")
            print(toString(minValue, baseType), "..", toString(maxValue, baseType))
        elif form == ARRAY:
            indexType = type.getArrayIndexType()
            elementType = type.getArrayElementType()
            count = type.getArrayElementCount()

            print(INDENT, "--- INDEX TYPE ---")
            printType(indexType)

            # Print the index type details only if the type is unnamed.
            if indexType.getIdentifier() == None:
                printTypeDetail(indexType)

            print(INDENT, "--- ELEMENT TYPE ---")
            printType(elementType);
            print(str(INDENT), str(count), " elements")

            # Print the element type details only if the type is unnamed.
            if elementType.getIdentifier() == None:
                printTypeDetail(elementType)

    # Print the cross-reference table for a record type.
    # @param recordType the RECORD type specification.
    def printRecord(self, recordType):
        recordId = recordType.getIdentifier()
        if recordId is not None:
            name = recordId.getName()
        else:
            name = "<unnamed>"

        print("\n--- RECORD ", name, " ---")
        printColumnHeadings()

        # Print the entries in the record's symbol table.
        symTable = recordType.getRecordSymTable()
        printSymTable(symTable)

    # Convert a value to a string.
    # @param value the value.
    # @param type  the value's datatype.
    # @return the string.
    def toString(self, value, _type):
        if _type == Predefined.stringType:
            return "'" + value + "'"
        else:
            str(value)
