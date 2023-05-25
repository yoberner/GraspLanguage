# Convert Pascal programs to Java.
import io

from gen.GraspParser import GraspParser
from edu.yu.compilers.backend.converter.CodeGenerator import CodeGenerator
from edu.yu.compilers.intermediate.symtable.Kind import Kind
from edu.yu.compilers.intermediate.symtable.Predefined import Predefined
from edu.yu.compilers.intermediate.symtable.SymTable import SymTable
from edu.yu.compilers.intermediate.type.Form import Form
from gen.GraspVisitor import GraspVisitor


class Converter(GraspVisitor):
    # Map a Pascal datatype name to the Java datatype name.
    type_name_table = {
        "integer": "int",
        "decimal": "double",
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
        self.visit(ctx.functionHead())
        varDecs = ctx.block().declarations().variablesPart()
        if varDecs is not None:
            for varDec in varDecs.variableDeclarationsList().variableDeclarations() :
                for id_ in varDec.variableIdentifierList().variableIdentifier() :
                    self.code.emit_start()
                    self.visit(varDec.typeSpecification())
                    self.code.emit(" " + id_.getText() + ";")
        self.code.emit_start()
        stmts = ctx.block().compoundStatement().statementList().statement()
        for i in range(len(stmts)) :
            self.visit(stmts[i])

        self.code.emit("}")
        return None

    def visitProgram(self, ctx):
        sw = io.StringIO()
        self.code = CodeGenerator(sw)

        self.visit(ctx.programHeader())

        # Execution timer and runtime standard input.
        self.code.indent()
        self.code.emit_line("private static java.util.Scanner _sysin = " +
                            "new java.util.Scanner(System.in);")
        self.code.emit_line()

        # Level 1 declarations.
        idCtx = ctx.programHeader().programIdentifier()
        self.visit(ctx.block().declarations())
        self.emitUnnamedRecordDefinitions(idCtx.entry.getRoutineSymTable())

        # Main.
        self.code.emit_line()
        self.code.emit_line("public static void main(String[] args)")
        self.code.emit_line("{")
        self.code.indent()

        # Allocate structured data.
        self.emitAllocateStructuredVariables("", idCtx.entry.getRoutineSymTable())
        self.code.emit_line()

        # Main compound statement.
        self.visit(ctx.block().compoundStatement().statementList())

        self.code.dedent()
        self.code.emit_line("}")

        self.code.dedent()
        self.code.emit_line("}")
        result = sw.getvalue()
        self.code.close()
        return result

    def visitProgramHeader(self, ctx):
        programName = ctx.programIdentifier().entry.getName()

        # Emit the Python program class.
        self.code.emit_line(f"public class {programName}")
        self.code.emit_line("{")

        return None

    def visitConstantDefinition(self, ctx):
        idCtx = ctx.constantIdentifier()
        constCtx = ctx.constant()
        constantName = idCtx.entry.getName()
        type_ = constCtx.type_
        graspTypeName = type_.getName()
        javaTypeName = self.type_name_table[graspTypeName]

        self.code.emit_start()

        if self.program_variables:
            self.code.emit("global ")
        self.code.emit_end(f"final {javaTypeName} {constantName} = {constCtx.getText()};")

        # Java version:
        # if self.programVariables:
        #     self.code.emit("private static ")
        # self.code.emit_end("final " + javaTypeName + " " + constantName + " = " + constCtx.getText() + ";")

        return None

    def visitTypeDefinition(self, ctx):
        idCtx = ctx.typeIdentifier()
        typeName = idCtx.entry.getName()
        typeCtx = ctx.typeSpecification()
        form = typeCtx.type_.getForm()

        if form == Form.ENUMERATION:
            self.code.emit_start()
            if self.program_variables:
                self.code.emit("private static ")
            self.code.emit("enum " + typeName)
            self.visit(typeCtx)
        elif form == Form.RECORD:
            self.code.emit_start()
            if self.program_variables:
                self.code.emit("public static ")
            self.code.emit_end("class " + typeName)
            self.code.emit_line("{")
            self.code.indent()

            self.emitUnnamedRecordDefinitions(typeCtx.type_.getRecordSymTable())
            self.visit(typeCtx)

            self.code.dedent()
            self.code.emit_line("}")
            self.code.emit_line()

        return None

    # def visitEnumerationTypespec(self, ctx):
    #     separator = " {"
    #
    #     for constCtx in ctx.enumerationType().enumerationConstant():
    #         self.code.emit(separator + constCtx.constantIdentifier().entry.getName())
    #         separator = ", "
    #
    #     self.code.emit_end("};")
    #     return None

    def emitUnnamedRecordDefinitions(self, symTable):
        for id in symTable.sortedEntries():
            if (id.getKind() == Kind.TYPE) and (id.getType().getForm() == Form.RECORD) and (
                    id.getName().startswith(SymTable.UNNAMED_PREFIX)):
                self.code.emit_start()
                if self.program_variables:
                    self.code.emit("public static ")
                self.code.emit_end("class " + id.getName())
                self.code.emit_line("{")
                self.code.indent()
                self.emitRecordFields(id.getType().getRecordSymTable())
                self.code.dedent()
                self.code.emit_line("}")
                self.code.emit_line()

    def emitRecordFields(self, symTable):
        self.emitUnnamedRecordDefinitions(symTable)

        for fieldId in symTable.sortedEntries():
            if fieldId.getKind() == Kind.RECORD_FIELD:
                self.code.emit_start(self.typeName(fieldId.getType()))
                self.code.emit(" " + fieldId.getName())
                self.code.emit_end(";")

    def visitRecordTypespec(self, ctx):
        fieldsCtx = ctx.recordType().recordFields()
        self.record_fields = True
        self.visit(fieldsCtx.variableDeclarationsList())
        self.record_fields = False
        return None

    def visitVariableDeclarations(self, ctx):
        typeCtx = ctx.typeSpecification()
        listCtx = ctx.variableIdentifierList()

        for varCtx in listCtx.variableIdentifier():
            self.code.emit_start()
            if self.program_variables and not self.record_fields:
                self.code.emit("private static ")
            self.code.emit(self.typeName(typeCtx.type_))
            self.code.emit(" " + varCtx.entry.getName())
            if typeCtx.type_.getForm() == Form.ARRAY:
                self.emitArraySpecifier(typeCtx.type_)
            self.code.emit_end(";")

        return None

    def emitArraySpecifier(self, graspType):
        brackets = ""

        while graspType.getForm() == Form.ARRAY:
            brackets += "[]"
            graspType = graspType.getArrayElementType()

        self.code.emit(brackets)

    def typeName(self, graspType):
        form = graspType.getForm()
        graspTypeName = graspType.getName()

        if form == Form.ARRAY:
            elemType = graspType.getArrayElementType()
            graspTypeName = elemType.getName()
            javaTypeName = self.type_name_table.get(graspTypeName)
            return javaTypeName if javaTypeName is not None else graspTypeName
        elif form == Form.SUBRANGE:
            baseType = graspType.baseType()
            graspTypeName = baseType.getName()
            return self.type_name_table.get(graspTypeName)
        elif form == Form.ENUMERATION:
            return graspTypeName if graspTypeName is not None else "int"
        elif form == Form.RECORD:
            return graspTypeName
        else:
            return self.type_name_table.get(graspTypeName)

    def visitTypeIdentifier(self, ctx):
        graspType = ctx.type_
        javaTypeName = self.typeName(graspType)
        self.code.emit(javaTypeName)

        return None

    # def visit_case_statement(self, ctx):
    #     var_name = self.visit(ctx.expression())
    #     self.code.emit_line(f"switch ({var_name}) {{")
    #     self.code.indent()
    #
    #     for branch in ctx.caseBranchList().caseBranch():
    #         if branch.caseConstantList() is None:
    #             continue
    #
    #         self.code.emit_start("case ")
    #         obj1 = branch.caseConstantList().caseConstant(0)
    #         str1 = obj1.getText()
    #         if obj1.type_ == Predefined.stringType:
    #             str1 = "\"" + self.convert_string(str1) + "\""
    #         self.code.emit(str1)
    #
    #         for i in range(1, len(branch.caseConstantList().caseConstant())):
    #             if branch.caseConstantList() is None:
    #                 continue
    #
    #             obj2 = branch.caseConstantList().caseConstant(i)
    #             str2 = obj2.getText()
    #             if obj2.type_ == Predefined.stringType:
    #                 str2 = "\"" + self.convert_string(str2) + "\""
    #             self.code.emit(", " + str2)
    #
    #         self.code.emit_line(":")
    #         self.visit(branch.statement())
    #         self.code.emit_line("break;")
    #
    #     self.code.dedent()
    #     self.code.emit_line("}")
    #
    #     return None

    def visitVariableIdentifierList(self, ctx):
        separator = " "

        for varCtx in ctx.variableIdentifier():
            self.code.emit(separator)
            self.code.emit(varCtx.getText())
            separator = ", "

        return None

    def emitAllocateStructuredVariables(self, lhsPrefix, symTable):
        for id in symTable.sortedEntries():
            if id.getKind() == Kind.VARIABLE:
                self.emitAllocateStructuredData(lhsPrefix, id)

    def emitAllocateStructuredData(self, lhsPrefix, variableId):
        variableType = variableId.getType()
        form = variableType.getForm()
        variableName = variableId.getName()

        if form == Form.ARRAY:
            declarationPart = lhsPrefix + str(variableName) + " = "
            self.code.emit_start(declarationPart)
            elemType = self.emitNewArray(variableType)
            self.code.emit_end(";")

            if elemType.isStructured():
                self.emitNewArrayElement(lhsPrefix, variableName, variableType)
        elif form == Form.RECORD:
            self.code.emit_start(lhsPrefix + variableName + " = ")
            self.emitNewRecord(lhsPrefix, variableName, variableType)

    def emitNewArray(self, type_):
        sizes = ""
        while type_.getForm() == Form.ARRAY:
            sizes += "[" + str(type_.getArrayElementCount()) + "]"
            type_ = type_.getArrayElementType()

        type_ = type_.baseType()
        graspTypeName = type_.getName()
        javaTypeName = self.type_name_table.get(graspTypeName)

        if javaTypeName is None:
            javaTypeName = graspTypeName
        self.code.emit("new " + javaTypeName + sizes)

        return type_

    def emitNewArrayElement(self, lhsPrefix, variableName, elemType):
        dimensionCount = 0
        variableNameBuilder = variableName

        #  TODO THIS IS NOT A DO WHILE LOOP AS IN THE JAVA CODE MIGHT BE IMPORTANT
        while elemType.getForm() == Form.ARRAY:
            elemCount = elemType.getArrayElementCount()
            dimensionCount += 1
            subscript = "_i" + str(dimensionCount)
            variableNameBuilder += "[" + subscript + "]"

            self.code.emit_line(
                "for (int " + subscript + " = 0; " + subscript + " < " + str(elemCount) + "; " + subscript + "++)")
            self.code.emit_start("{")
            self.code.indent()

            elemType = elemType.getArrayElementType()

        typeName = elemType.getName()
        self.code.emit_start(lhsPrefix + variableName + " = new" + typeName + "()")
        self.code.emit_end(";")

        self.emitNewRecordFields(lhsPrefix + variableName + ".", elemType)

        dimensionCount -= 1
        while dimensionCount > 0:
            self.code.dedent()
            self.code.emit_line("}")
            dimensionCount -= 1

    def emitNewRecord(self, lhsPrefix, variableName, recordType):
        typePath = recordType.getRecordTypePath()
        index = typePath.index('$')

        # Don't include the program name in the record type path.
        # Replace each $ with a period.
        typePath = typePath[index + 1:].replace('$', '.')
        self.code.emit("new " + typePath + "();")

        self.emitNewRecordFields(lhsPrefix + variableName + ".", recordType)

    def emitNewRecordFields(self, lhsPrefix, recordType):
        for fieldId in recordType.getRecordSymTable().sortedEntries():
            if fieldId.getKind() == Kind.RECORD_FIELD:
                type_ = fieldId.getType()

                if type_.isStructured():
                    self.emitAllocateStructuredData(lhsPrefix, fieldId)

    def visitStatementList(self, ctx):
        for stmtCtx in ctx.statement():
            if stmtCtx.emptyStatement() is None:
                self.code.emit_start()
                self.visit(stmtCtx)
        return None

    def visitCompoundStatement(self, ctx):
        self.code.emit("{")
        self.code.indent()
        self.visitChildren(ctx)
        self.code.dedent()
        self.code.emit_line("}")
        return None

    def visitAssignmentStatement(self, ctx):
        lhs = self.visit(ctx.lhs().variable())
        expr = self.visit(ctx.rhs().expression())
        self.code.emit(lhs + " = " + expr)
        self.code.emit_end(";")
        return None

    # def visitRepeatStatement(self, ctx):
    #     needBraces = len(ctx.statementList().statement()) > 1
    #
    #     self.code.emit("do")
    #     if needBraces:
    #         self.code.emit_line("{")
    #     self.code.indent()
    #
    #     self.visit(ctx.statementList())
    #
    #     self.code.dedent()
    #     if needBraces:
    #         self.code.emit_line("}")
    #
    #     self.code.emit_start("while (not (")
    #     self.code.emit(visit(ctx.expression()))
    #     self.code.emit_end("));")
    #
    #     return None

    def visitFunctionHead(self, ctx):
        funcName = str(ctx.routineIdentifier().IDENTIFIER())
        self.code.emit("private static ")
        self.visit(ctx.typeIdentifier())
        self.code.emit(" " + funcName + "(")

        if ctx.parameters() is not None:
            #
            parameterDeclarations = ctx.parameters().parameterDeclarationsList().parameterDeclaration()  # TODO YOULL NEED TO CHANGE THIS
            i = 0
            while i < len(parameterDeclarations):  # TODO CHANGED TO REG WHILE MIGHT NEED TO FIX
                paramDec = parameterDeclarations[i]
                parameterIdentifier = paramDec.parameterIdentifier()
                self.visit(paramDec.typeIdentifier())  # type
                if paramDec.paramTypeMod() is not None:
                    self.code.emit('[]')
                self.code.emit(" " + str(parameterIdentifier.IDENTIFIER()))
                if i < len(parameterDeclarations) - 1:
                    self.code.emit(", ")
                i += 1

        self.code.emit("){")
        return None

    # def visitProcedureCallStatement(self, ctx):
    #     procNameCtx = ctx.procedureName()
    #     procedureName = procNameCtx.entry.getName()
    #
    #     self.code.emit(procedureName)
    #     self.code.emit("(")
    #
    #     if ctx.argumentList() is not None:
    #         self.code.emit(visit(ctx.argumentList()))
    #
    #     self.code.emit_end(");")
    #     return None

    def visitForStatement(self, ctx):
        needBraces = ctx.statement().compoundStatement() is not None
        initialStmt = self.visit(ctx.variable()) + " = " + self.visit(ctx.expression(0))
        limit = self.visit(ctx.expression(1))
        updateString = self.visit(ctx.variable()) + "++" #  TODO NEED TO FIX
        self.code.emit("for ( " + initialStmt + "; " + limit + "; " + updateString + ")")
        if not needBraces:
            self.code.indent()
        self.code.emit_start()
        self.visit(ctx.statement())
        if not needBraces:
            self.code.dedent()
        return None

    # TODO every visit result needs to be casted to string
    def visitIfStatement(self, ctx):
        needBraces = ctx.trueStatement().statement().compoundStatement() is not None
        condition = str(self.visit(ctx.expression()))
        self.code.emit("if (" + condition + ")")
        if not needBraces:
            self.code.indent()

        self.code.emit_start()
        self.visit(ctx.trueStatement())
        if not needBraces:
            self.code.dedent()
        if ctx.falseStatement() is not None:
            needBraces = ctx.falseStatement().statement().compoundStatement() is not None
            self.code.emit_start("else ")
            if needBraces:
                self.code.emit("{")

            if not needBraces:
                self.code.indent()
            self.code.emit_start()
            self.visit(ctx.falseStatement())
            if not needBraces:
                self.code.dedent()
            if needBraces:
                self.code.emit("}")

        return None

    def visitWhileStatement(self, ctx):
        self.code.emit_line(f"while ({ctx.expression().getText()})")
        self.code.emit_line("{")
        self.code.indent()
        self.visit(ctx.statement())
        self.code.dedent()
        self.code.emit_line("}")

        return None

    def visitReturnStatement(self, ctx: GraspParser.ReturnStatementContext):
        self.code.emit_line(f"return {ctx.expression().getText()};")


    def visitArgumentList(self, ctx):
        text = ""
        separator = ""

        for argCtx in ctx.argument():
            text += separator
            text += str(self.visit(argCtx.expression()))
            separator = ", "

        return text
    def visitExpression(self, ctx):
        simpleCtx1 = ctx.simpleExpression()[0]
        relOpCtx = ctx.relOp()
        simpleText1 = str(self.visit(simpleCtx1))
        text = simpleText1

        # Second simple expression?
        if relOpCtx is not None:
            op = relOpCtx.getText()

            if op == "=":
                op = "=="
            elif op == "<>":
                op = "!="

            simpleCtx2 = ctx.simpleExpression()[1]
            simpleText2 = str(self.visit(simpleCtx2))

            # Python uses the == operator for strings.
            if simpleCtx1.type_ == Predefined.stringType:
                text = "(" + simpleText1 + ")." + "compareTo(" + simpleText2 + ") " + op + " 0"
            else:
                text = simpleText1 + " " + op + " " + simpleText2

        return text

    def visitSimpleExpression(self, ctx):
        count = len(ctx.term())
        text = ""

        if ctx.sign() is not None and ctx.sign().getText() == "-":
            text += "-"

        # Loop over the simple expressions.
        for i in range(count):
            termCtx = ctx.term()[i]
            text += str(self.visit(termCtx))

            if i < count - 1:
                addOp = ctx.addOp()[i].getText().lower()
                if addOp == "or":
                    addOp = "||"

                text += " " + addOp + " "

        return text

    def visitTerm(self, ctx):
        count = len(ctx.factor())
        text = ""

        # Loop over the terms.
        for i in range(count):
            factorCtx = ctx.factor()[i]
            text += str(self.visit(factorCtx))

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

    def visitVariableFactor(self, ctx):
        return self.visit(ctx.variable())

    def visitVariable(self, ctx):
        idCtx = ctx.variableIdentifier()
        variableId = idCtx.entry
        variableName = variableId.getName()
        type_ = ctx.variableIdentifier().type_
        variableNameBuilder = [variableName]

        if (
                type_ != Predefined.booleanType
                and variableId.getKind() == Kind.ENUMERATION_CONSTANT
        ):
            variableNameBuilder.insert(0, type_.getName() + ".")

        # Loop over any subscript and field modifiers.
        for modCtx in ctx.modifier():
            # Subscripts.
            if modCtx.indexList() is not None:
                for indexCtx in modCtx.indexList().index():
                    indexType = Predefined.integerType
                    minIndex = 0

                    if indexType.getForm() == Form.SUBRANGE:
                        minIndex = indexType.getSubrangeMinValue()

                    exprCtx = indexCtx.expression()
                    expr = self.visit(exprCtx)
                    subscript = (
                        expr
                        if minIndex == 0
                        else "(" + expr + ")+" + (-minIndex)
                        if minIndex < 0
                        else "(" + expr + ")-" + minIndex
                    )

                    variableNameBuilder.append("[" + subscript + "]")

                    type_ = Predefined.charType #type_.getArrayElementType()

            # Record field.
            else:
                fieldCtx = modCtx.field()
                fieldName = fieldCtx.entry.getName()
                variableNameBuilder.append("." + fieldName)
                type_ = fieldCtx.type_

        return "".join(variableNameBuilder)

    def visitNumberFactor(self, ctx):
        return ctx.getText()

    def visitCharacterFactor(self, ctx):
        return ctx.getText()

    def visitStringFactor(self, ctx):
        graspString = ctx.stringConstant().STRING().getText()
        return '"' + self.convertString(graspString) + '"'

    def convertString(self, graspString):
        unquoted = graspString[1:-1]
        return unquoted.replace("''", "'").replace("\"", "\\\"")

    def visitFunctionCallStatement(self, ctx:GraspParser.FunctionCallStatementContext):
        funcNameCtx = ctx.functionName()
        funcSTE = funcNameCtx.entry
        functionName = funcSTE.getName()

        if funcSTE.isInline():
            self.visit(funcSTE.getExecutable())
        else:
            text = functionName + "("

            if ctx.argumentList() is not None:
                text += self.visit(ctx.argumentList())

            text += ");"
            self.code.emit(text)



    def visitFunctionCallFactor(self, ctx):
        callCtx = ctx.functionCallStatement()
        funcNameCtx = callCtx.functionName()
        funcSTE = funcNameCtx.entry
        functionName = funcSTE.getName()

        text = functionName + "("

        if callCtx.argumentList() is not None:
            text += self.visit(callCtx.argumentList())

        text += ")"
        return text

    def visitNotFactor(self, ctx):
        return "!" + self.visit(ctx.factor())

    def visitParenthesizedFactor(self, ctx):
        return "(" + self.visit(ctx.expression()) + ")"

    def visitPrintStatement(self, ctx):
        self.code.emit("System.out.printf(")
        self.code.mark()

        format = self.createWriteFormat(ctx.writeArguments())
        arguments = self.createWriteArguments(ctx.writeArguments())

        self.code.emit('"' + format + '"')

        if len(arguments) > 0:
            self.code.emit(", ")
            self.code.split(60)
            self.code.emit(arguments)

        self.code.emit_end(");")
        return None

    def visitPrintlnStatement(self, ctx):
        if ctx.writeArguments() is not None:
            self.code.emit("System.out.printf(")
            self.code.mark()

            format = self.createWriteFormat(ctx.writeArguments())
            arguments = self.createWriteArguments(ctx.writeArguments())

            self.code.emit('"' + format + "\\n\"")  # append line feed

            if len(arguments) > 0:
                self.code.emit(", ")
                self.code.split(60)
                self.code.emit(arguments)

            self.code.emit_end(");")
        else:
            self.code.emit_end("System.out.println();")

        return None

    def createWriteFormat(self, ctx):
        format = ""

        # Loop over the "write" arguments.
        for argCtx in ctx.writeArgument():
            type_ = argCtx.expression().type_
            argText = argCtx.getText()

            # Append any literal strings.
            if argText[0] == '\'':
                format += self.convertString(argText)

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

                typeFlag = "d" if type_ == Predefined.integerType else "f" if type_ == Predefined.realType else "b" if type_ == Predefined.booleanType else "c" if type_ == Predefined.charType else "s"
                format += typeFlag

        return format

    def createWriteArguments(self, ctx):
        arguments = ""
        separator = ""

        # Loop over "write" arguments.
        for argCtx in ctx.writeArgument():
            argText = argCtx.getText()

            # Not a literal string.
            if argText[0] != '\'':
                arguments += separator + self.visit(argCtx.expression())
                separator = ", "

        return arguments

    def visitReadStatement(self, ctx):
        if len(ctx.readArguments().variable()) == 1:
            self.visit(ctx.readArguments())
        else:
            self.code.emit("{")
            self.code.indent()
            self.code.emit_start()

            self.visit(ctx.readArguments())

            self.code.dedent()
            self.code.emit_line("}")

        return None

    def visitReadlnStatement(self, ctx):
        self.code.emit("{")
        self.code.indent()
        self.code.emit_start()

        self.visit(ctx.readArguments())
        self.code.emit_line("_sysin.nextLine();")

        self.code.dedent()
        self.code.emit_line("}")

        return None

    def visitReadArguments(self, ctx):
        size = len(ctx.variable())

        # Loop over the read arguments.
        for i in range(size):
            varCtx = ctx.variable()[i]
            varName = varCtx.getText()
            type_ = varCtx.type_

            # Read a character.
            if type_ == Predefined.charType:
                self.code.emit("{")
                self.code.indent()

                self.code.emit_start("_sysin.useDelimiter(\"\");")
                self.code.emit_start(varName + " = _sysin.next().charAt(0);")
                self.code.emit_start("_sysin.reset();")

                self.code.dedent()
                self.code.emit_line("}")

            # Read any other value.
            else:
                typeName = "Int" if type_ == Predefined.integerType else \
                    "Double" if type_ == Predefined.realType else \
                        "Boolean" if type_ == Predefined.booleanType else ""

                self.code.emit(varName + " = _sysin.next" + typeName + "();")

            if i < size - 1:
                self.code.emit_start()

        return None
