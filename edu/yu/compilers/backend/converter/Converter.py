# Convert Pascal programs to Java.
class Converter(PascalBaseVisitor):

    # Map a Pascal datatype name to the Java datatype name.
    type_name_table = {
        "integer": "int",
        "real": "double",
        "boolean": "boolean",
        "char": "char",
        "string": "String",
    }

    def __init__(self):
        self.code = None
        self.program_name = None
        self.program_variables = True
        self.record_fields = False
        self.current_separator = ""

    def get_program_name(self):
        return self.program_name

    def visitRoutineDefinition(self, ctx):
        return None

    def visit_case_statement(self, ctx):
        var_name = self.visit(ctx.expression())
        self.code.emit_line(f"switch ({var_name}) {{")
        self.code.indent()

        for branch in ctx.caseBranchList().caseBranch():
            if branch.caseConstantList() is None:
                continue

            self.code.emit_start("case ")
            obj1 = branch.caseConstantList().caseConstant(0)
            str1 = obj1.getText()
            if obj1.type == Predefined.stringType:
                str1 = "\"" + self.convert_string(str1) + "\""
            self.code.emit(str1)

            for i in range(1, len(branch.caseConstantList().caseConstant())):
                if branch.caseConstantList() is None:
                    continue

                obj2 = branch.caseConstantList().caseConstant(i)
                str2 = obj2.getText()
                if obj2.type == Predefined.stringType:
                    str2 = "\"" + self.convert_string(str2) + "\""
                self.code.emit(", " + str2)

            self.code.emit_line(":")
            self.visit(branch.statement())
            self.code.emit_line("break;")

        self.code.dedent()
        self.code.emit_line("}")

        return None

    def visitForStatement(self, ctx):
        self.code.emitStart("for (")
        varName = ctx.variable().getText()
        self.code.emit(f"int {varName} = ")
        self.code.emit(visit(ctx.expression(0)).toString())
        self.code.emit("; ")

        self.code.emitStart(varName)

        upto = ctx.TO() != None
        if upto:
            self.code.emit(" <= ")
        else:
            self.code.emit(" >= ")

        self.code.emit(visit(ctx.expression(1)).toString())
        self.code.emit("; ")

        self.code.emitStart(varName)

        if upto:
            self.code.emitEnd("++)")
        else:
            self.code.emitEnd("--)")

        self.code.emitLine("{")
        self.code.indent()
        self.visit(ctx.statement())
        self.code.dedent()
        self.code.emitLine("}")

        return None

    def visitIfStatement(self, ctx):
        self.code.emitLine(f"if ({self.visit(ctx.expression())})")
        self.code.emitLine("{")
        self.code.indent()
        self.visit(ctx.trueStatement())
        self.code.dedent()
        self.code.emitLine("}")

        if ctx.ELSE() is not None:
            self.code.emitLine("else")
            self.code.emitLine("{")
            self.code.indent()
            self.visit(ctx.falseStatement())
            self.code.dedent()
            self.code.emitLine("}")

        return None


    def visitWhileStatement(self, ctx):
        self.code.emitLine(f"while ({ctx.expression().getText()})")
        self.code.emitLine("{")
        self.code.indent()
        self.visit(ctx.statement())
        self.code.dedent()
        self.code.emitLine("}")

        return None

    def visitProgram(self, ctx):
        sw = io.StringIO()
        self.code = CodeGenerator(sw)

        self.visit(ctx.programHeader)

        # Execution timer and runtime standard input.
        self.code.indent()
        self.code.emitLine("private static java.util.Scanner _sysin = " +
                            "new java.util.Scanner(System.in);")
        self.code.emitLine()

        # Level 1 declarations.
        idCtx = ctx.programHeader.programIdentifier
        self.visit(ctx.block.declarations)
        self.emitUnnamedRecordDefinitions(idCtx.entry.getRoutineSymTable())

        # Main.
        self.code.emitLine()
        self.code.emitLine("public static void main(String[] args)")
        self.code.emitLine("{")
        self.code.indent()

        # Allocate structured data.
        self.emitAllocateStructuredVariables("", idCtx.entry.getRoutineSymTable())
        self.code.emitLine()

        # Main compound statement.
        self.visit(ctx.block.compoundStatement.statementList)

        self.code.dedent()
        self.code.emitLine("}")

        self.code.dedent()
        self.code.emitLine("}")

        self.code.close()
        return sw.getvalue()

    def visitProgramHeader(self, ctx):
        programName = ctx.programIdentifier().entry.getName()

        # Emit the Python program class.
        self.code.emitLine(f"class {programName}:")
        self.code.indent()

        return None

    def visitConstantDefinition(self, ctx):
        idCtx = ctx.constantIdentifier()
        constCtx = ctx.constant()
        constantName = idCtx.entry.getName()
        type = constCtx.type
        pascalTypeName = type.getIdentifier().getName()
        javaTypeName = self.typeNameTable[pascalTypeName]

        self.code.emitStart()

        if self.programVariables:
            self.code.emit("global ")
        self.code.emitEnd(f"{constantName} = {constCtx.getText()}")

        # Java version:
        # if self.programVariables:
        #     self.code.emit("private static ")
        # self.code.emitEnd("final " + javaTypeName + " " + constantName + " = " + constCtx.getText() + ";")

        return None

    def visitTypeDefinition(self, ctx):
        idCtx = ctx.typeIdentifier()
        typeName = idCtx.entry.getName()
        typeCtx = ctx.typeSpecification()
        form = typeCtx.type.getForm()

        if form == ENUMERATION:
            self.code.emitStart()
            if self.programVariables:
                self.code.emit("private static ")
            self.code.emit("enum " + typeName)
            self.visit(typeCtx)
        elif form == RECORD:
            self.code.emitStart()
            if self.programVariables:
                self.code.emit("public static ")
            self.code.emitEnd("class " + typeName)
            self.code.emitLine("{")
            self.code.indent()

            self.emitUnnamedRecordDefinitions(typeCtx.type.getRecordSymTable())
            self.visit(typeCtx)

            self.code.dedent()
            self.code.emitLine("}")
            self.code.emitLine()

        return None

    def visitEnumerationTypespec(self, ctx):
        separator = " {"

        for constCtx in ctx.enumerationType().enumerationConstant():
            self.code.emit(separator + constCtx.constantIdentifier().entry.getName())
            separator = ", "

        self.code.emitEnd("};")
        return None

    def emitUnnamedRecordDefinitions(symTable):
        for id in symTable.sortedEntries():
            if (id.getKind() == TYPE) and (id.getType().getForm() == RECORD) and (id.getName().startswith(SymTable.UNNAMED_PREFIX)):
                code.emitStart()
                if programVariables:
                    code.emit("public static ")
                code.emitEnd("class " + id.getName())
                code.emitLine("{")
                code.indent()
                emitRecordFields(id.getType().getRecordSymTable())
                code.dedent()
                code.emitLine("}")
                code.emitLine()


    def emitRecordFields(symTable):
        emitUnnamedRecordDefinitions(symTable)

        for fieldId in symTable.sortedEntries():
            if fieldId.getKind() == RECORD_FIELD:
                code.emitStart(typeName(fieldId.getType()))
                code.emit(" " + fieldId.getName())
                code.emitEnd(";")

    def visitRecordTypespec(self, ctx):
        fieldsCtx = ctx.recordType().recordFields()
        self.recordFields = True
        self.visit(fieldsCtx.variableDeclarationsList())
        self.recordFields = False
        return None

    def visitVariableDeclarations(self, ctx):
        typeCtx = ctx.typeSpecification()
        listCtx = ctx.variableIdentifierList()

        for varCtx in listCtx.variableIdentifier():
            self.code.emitStart()
            if self.programVariables and not self.recordFields:
                self.code.emit("private static ")
            self.code.emit(typeName(typeCtx.type))
            self.code.emit(" " + varCtx.entry.getName())
            if typeCtx.type.getForm() == ARRAY:
                self.emitArraySpecifier(typeCtx.type)
            self.code.emitEnd(";")

        return None

def emitArraySpecifier(self, pascalType):
    brackets = ""

    while pascalType.getForm() == ARRAY:
        brackets += "[]"
        pascalType = pascalType.getArrayElementType()

    self.code.emit(brackets)

def typeName(self, pascalType):
    form = pascalType.getForm()
    typeId = pascalType.getIdentifier()
    pascalTypeName = typeId.getName() if typeId is not None else None

    if form == ARRAY:
        elemType = pascalType.getArrayBaseType()
        pascalTypeName = elemType.getIdentifier().getName()
        javaTypeName = self.typeNameTable.get(pascalTypeName)
        return javaTypeName if javaTypeName is not None else pascalTypeName
    elif form == SUBRANGE:
        baseType = pascalType.baseType()
        pascalTypeName = baseType.getIdentifier().getName()
        return self.typeNameTable.get(pascalTypeName)
    elif form == ENUMERATION:
        return pascalTypeName if pascalTypeName is not None else "int"
    elif form == RECORD:
        return pascalTypeName
    else:
        return self.typeNameTable.get(pascalTypeName)

    def visitTypeIdentifier(self, ctx):
        pascalType = ctx.type
        javaTypeName = self.typeName(pascalType)
        self.code.emit(javaTypeName)

        return None

    def visitVariableIdentifierList(self, ctx):
        separator = " "

        for varCtx in ctx.variableIdentifier():
            self.code.emit(separator)
            self.code.emit(varCtx.getText())
            separator = ", "

        return None

    def emitAllocateStructuredVariables(lhsPrefix, symTable):
        for id in symTable.sortedEntries():
            if id.getKind() == VARIABLE:
                emitAllocateStructuredData(lhsPrefix, id)

    def emitAllocateStructuredData(lhsPrefix, variableId):
        variableType = variableId.getType()
        form = variableType.getForm()
        variableName = variableId.getName()

        if form == ARRAY:
            code.emitStart(lhsPrefix + variableName + " = ")
            elemType = emitNewArray(variableType)
            code.emitEnd(";")

            if elemType.isStructured():
                emitNewArrayElement(lhsPrefix, variableName, variableType)
        elif form == RECORD:
            code.emitStart(lhsPrefix + variableName + " = ")
            emitNewRecord(lhsPrefix, variableName, variableType)

    def emitNewArray(type):
        sizes = ""
        while type.getForm() == ARRAY:
            sizes += "[" + str(type.getArrayElementCount()) + "]"
            type = type.getArrayElementType()

        type = type.baseType()
        pascalTypeName = type.getIdentifier().getName()
        javaTypeName = typeNameTable.get(pascalTypeName)
        if javaTypeName is None:
            javaTypeName = pascalTypeName
        code.emit("new " + javaTypeName + sizes)

        return type

    def emitNewArrayElement(lhsPrefix, variableName, elemType):
        dimensionCount = 0
        variableNameBuilder = variableName

        while elemType.getForm() == ARRAY:
            elemCount = elemType.getArrayElementCount()
            dimensionCount += 1
            subscript = "_i" + str(dimensionCount)
            variableNameBuilder += "[" + subscript + "]"

            code.emitLine("for " + subscript + " in range(" + str(elemCount) + "):")
            code.emitStart()
            code.indent()

            elemType = elemType.getArrayElementType()

        variableName = variableNameBuilder

        typeName = elemType.getIdentifier().getName()
        code.emitStart(lhsPrefix + variableName + " = " + typeName + "()")
        code.emitEnd()

        emitNewRecordFields(lhsPrefix + variableName + ".", elemType)

        while dimensionCount > 0:
            code.dedent()
            code.emitLine("}")
            dimensionCount -= 1

    def emitNewRecord(lhsPrefix, variableName, recordType):
        typePath = recordType.getRecordTypePath()
        index = typePath.index('$')

        # Don't include the program name in the record type path.
        # Replace each $ with a period.
        typePath = typePath[index + 1:].replace('$', '.')
        code.emit("new " + typePath + "()")

        emitNewRecordFields(lhsPrefix + variableName + ".", recordType)

    def emitNewRecordFields(lhsPrefix, recordType):
        for fieldId in recordType.getRecordSymTable().sortedEntries():
            if fieldId.getKind() == RECORD_FIELD:
                type = fieldId.getType()

                if type.isStructured():
                    emitAllocateStructuredData(lhsPrefix, fieldId)

    def visitStatementList(ctx):
        for stmtCtx in ctx.statement():
            if stmtCtx.emptyStatement() is None:
                code.emitStart()
                visit(stmtCtx)
        return None

    def visitCompoundStatement(ctx):
        code.emit("{")
        code.indent()
        visitChildren(ctx)
        code.dedent()
        code.emitLine("}")
        return None

    def visitAssignmentStatement(ctx):
        lhs = visit(ctx.lhs().variable())
        expr = visit(ctx.rhs().expression())
        code.emit(lhs + " = " + expr)
        code.emitEnd(";")
        return None

    def visitRepeatStatement(ctx):
        needBraces = len(ctx.statementList().statement()) > 1

        code.emit("do")
        if needBraces:
            code.emitLine("{")
        code.indent()

        visit(ctx.statementList())

        code.dedent()
        if needBraces:
            code.emitLine("}")

        code.emitStart("while (not (")
        code.emit(visit(ctx.expression()))
        code.emitEnd("));")

        return None

    def visitProcedureCallStatement(ctx):
        procNameCtx = ctx.procedureName()
        procedureName = procNameCtx.entry.getName()

        code.emit(procedureName)
        code.emit("(")

        if ctx.argumentList() is not None:
            code.emit(visit(ctx.argumentList()))

        code.emitEnd(");")
        return None

    def visitArgumentList(ctx):
        text = ""
        separator = ""

        for argCtx in ctx.argument():
            text += separator
            text += visit(argCtx.expression())
            separator = ", "

        return text

    def visitExpression(ctx):
        simpleCtx1 = ctx.simpleExpression()[0]
        relOpCtx = ctx.relOp()
        simpleText1 = visit(simpleCtx1)
        text = simpleText1

        # Second simple expression?
        if relOpCtx is not None:
            op = relOpCtx.getText()

            if op == "=":
                op = "=="
            elif op == "<>":
                op = "!="

            simpleCtx2 = ctx.simpleExpression()[1]
            simpleText2 = visit(simpleCtx2)

            # Python uses the == operator for strings.
            if simpleCtx1.type == Predefined.stringType:
                text = "(" + simpleText1 + ")." + "compare(" + simpleText2 + ") " + op + " 0"
            else:
                text = simpleText1 + " " + op + " " + simpleText2

        return text

    def visitSimpleExpression(ctx):
        count = len(ctx.term())
        text = ""

        if ctx.sign() is not None and ctx.sign().getText() == "-":
            text += "-"

        # Loop over the simple expressions.
        for i in range(count):
            termCtx = ctx.term()[i]
            text += visit(termCtx)

            if i < count - 1:
                addOp = ctx.addOp()[i].getText().lower()
                if addOp == "or":
                    addOp = "||"

                text += " " + addOp + " "

        return text


    def visitTerm(ctx):
        count = len(ctx.factor())
        text = ""

        # Loop over the terms.
        for i in range(count):
            factorCtx = ctx.factor()[i]
            text += visit(factorCtx)

            if i < count - 1:
                mulOpStr = ctx.mulOp()[i].getText().lower()
                mulOp = ""
                if mulOpStr == "and":
                    mulOp = " && "
                elif mulOpStr == "div":
                    mulOp = "/"
                elif mulOpStr == "mod":
                    mulOp = "%"
                else:
                    mulOp = mulOpStr

                text += mulOp

        return text

    def visitVariableFactor(ctx):
        return visit(ctx.variable())


    def visitVariable(ctx):
        idCtx = ctx.variableIdentifier()
        variableId = idCtx.entry
        variableName = variableId.getName()
        type = ctx.variableIdentifier().type
        variableNameBuilder = [variableName]

        if (
            type != Predefined.booleanType
            and variableId.getKind() == ENUMERATION_CONSTANT
        ):
            variableNameBuilder.insert(0, type.getIdentifier().getName() + ".")

        # Loop over any subscript and field modifiers.
        for modCtx in ctx.modifier():
            # Subscripts.
            if modCtx.indexList() is not None:
                for indexCtx in modCtx.indexList().index():
                    indexType = type.getArrayIndexType()
                    minIndex = 0

                    if indexType.getForm() == SUBRANGE:
                        minIndex = indexType.getSubrangeMinValue()

                    exprCtx = indexCtx.expression()
                    expr = visit(exprCtx)
                    subscript = (
                        expr
                        if minIndex == 0
                        else "(" + expr + ")+" + (-minIndex)
                        if minIndex < 0
                        else "(" + expr + ")-" + minIndex
                    )

                    variableNameBuilder.append("[" + subscript + "]")

                    type = type.getArrayElementType()

            # Record field.
            else:
                fieldCtx = modCtx.field()
                fieldName = fieldCtx.entry.getName()
                variableNameBuilder.append("." + fieldName)
                type = fieldCtx.type

        return "".join(variableNameBuilder)

    def visitNumberFactor(ctx):
        return ctx.getText()


    def visitCharacterFactor(ctx):
        return ctx.getText()


    def visitStringFactor(ctx):
        pascalString = ctx.stringConstant().STRING().getText()
        return '"' + convertString(pascalString) + '"'


    def convertString(pascalString):
        unquoted = pascalString[1:-1]
        return unquoted.replace("''", "'").replace("\"", "\\\"")

    def visitFunctionCallFactor(ctx):
        callCtx = ctx.functionCall()
        funcNameCtx = callCtx.functionName()
        functionName = funcNameCtx.entry.getName()

        text = functionName + "("

        if callCtx.argumentList() is not None:
            text += visit(callCtx.argumentList())

        text += ")"
        return text


    def visitNotFactor(ctx):
        return "!" + visit(ctx.factor())


    def visitParenthesizedFactor(ctx):
        return "(" + visit(ctx.expression()) + ")"

    def visitWriteStatement(ctx):
        code.emit("System.out.printf(")
        code.mark()

        format = createWriteFormat(ctx.writeArguments())
        arguments = createWriteArguments(ctx.writeArguments())

        code.emit('"' + format + '"')

        if len(arguments) > 0:
            code.emit(", ")
            code.split(60)
            code.emit(arguments)

        code.emitEnd(");")
        return None


    def visitWritelnStatement(ctx):
        if ctx.writeArguments() is not None:
            code.emit("System.out.printf(")
            code.mark()

            format = createWriteFormat(ctx.writeArguments())
            arguments = createWriteArguments(ctx.writeArguments())

            code.emit('"' + format + "\\n\"")  # append line feed

            if len(arguments) > 0:
                code.emit(", ")
                code.split(60)
                code.emit(arguments)

            code.emitEnd(");")
        else:
            code.emitEnd("System.out.println();")

        return None

    def createWriteFormat(ctx):
        format = ""

        # Loop over the "write" arguments.
        for argCtx in ctx.writeArgument():
            type = argCtx.expression().type
            argText = argCtx.getText()

            # Append any literal strings.
            if argText[0] == '\'':
                format += convertString(argText)

            # For any other expressions, append a field specifier.
            else:
                format += "%"

                fwCtx = argCtx.fieldWidth()
                if fwCtx is not None:
                    sign = "-" if fwCtx.sign() is not None and fwCtx.sign().getText() == "-" else ""
                    format += sign + fwCtx.integerConstant().getText()

                    dpCtx = fwCtx.decimalPlaces()
                    if dpCtx is not None:
                        format += "." + dpCtx.integerConstant().getText()

                typeFlag = "d" if type == Predefined.integerType else "f" if type == Predefined.realType else "b" if type == Predefined.booleanType else "c" if type == Predefined.charType else "s"
                format += typeFlag

        return format

    def createWriteArguments(ctx):
        arguments = ""
        separator = ""

        # Loop over "write" arguments.
        for argCtx in ctx.writeArgument():
            argText = argCtx.getText()

            # Not a literal string.
            if argText[0] != '\'':
                arguments += separator + visit(argCtx.expression())
                separator = ", "

        return arguments


    def visitReadStatement(ctx):
        if len(ctx.readArguments().variable()) == 1:
            visit(ctx.readArguments())
        else:
            code.emit("{")
            code.indent()
            code.emitStart()

            visit(ctx.readArguments())

            code.dedent()
            code.emitLine("}")

        return None

    def visitReadlnStatement(ctx):
        code.emit("{")
        code.indent()
        code.emitStart()

        visit(ctx.readArguments())
        code.emitLine("_sysin.nextLine();")

        code.dedent()
        code.emitLine("}")

        return None


    def visitReadArguments(ctx):
        size = len(ctx.variable())

        # Loop over the read arguments.
        for i in range(size):
            varCtx = ctx.variable()[i]
            varName = varCtx.getText()
            type = varCtx.type

            # Read a character.
            if type == Predefined.charType:
                code.emit("{")
                code.indent()

                code.emitStart("_sysin.useDelimiter('');")
                code.emitStart(varName + " = _sysin.next().charAt(0);")
                code.emitStart("_sysin.reset();")

                code.dedent()
                code.emitLine("}")

            # Read any other value.
            else:
                typeName = "Int" if type == Predefined.integerType else \
                        "Double" if type == Predefined.realType else \
                        "Boolean" if type == Predefined.booleanType else ""

                code.emit(varName + " = _sysin.next" + typeName + "();")

            if i < size - 1:
                code.emitStart()

        return None
