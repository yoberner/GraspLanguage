# package edu.yu.compilers.backend.converter;

# import antlr4.PascalBaseVisitor;
# import antlr4.PascalParser;
# import antlr4.PascalParser.CaseConstantContext;
# import edu.yu.compilers.intermediate.symtable.Predefined;
# import edu.yu.compilers.intermediate.symtable.SymTable;
# import edu.yu.compilers.intermediate.symtable.SymTableEntry;
# import edu.yu.compilers.intermediate.type.Typespec;
# import edu.yu.compilers.intermediate.type.Typespec.Form;

# import java.io.PrintWriter;
# import java.io.StringWriter;
# import java.util.Hashtable;

# import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind.*;
# import static edu.yu.compilers.intermediate.type.Typespec.Form.*;

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

#     /**
#      * Emit a pair of empty brackets for each dimension.
#      *
#      * @param type the array datatype.
#      */
#     private void emitArraySpecifier(Typespec type) {
#         StringBuilder brackets = new StringBuilder();

#         while (type.getForm() == ARRAY) {
#             brackets.append("[]");
#             type = type.getArrayElementType();
#         }

#         code.emit(brackets.toString());
#     }

#     /**
#      * Convert a Pascal type name to the equivalent Java type name.
#      *
#      * @param pascalType the datatype name.
#      * @return the Java type name.
#      */
#     private String typeName(Typespec pascalType) {
#         Form form = pascalType.getForm();
#         SymTableEntry typeId = pascalType.getIdentifier();
#         String pascalTypeName = typeId != null ? typeId.getName() : null;

#         if (form == ARRAY) {
#             Typespec elemType = pascalType.getArrayBaseType();
#             pascalTypeName = elemType.getIdentifier().getName();
#             String javaTypeName = typeNameTable.get(pascalTypeName);
#             return javaTypeName != null ? javaTypeName : pascalTypeName;
#         } else if (form == SUBRANGE) {
#             Typespec baseType = pascalType.baseType();
#             pascalTypeName = baseType.getIdentifier().getName();
#             return typeNameTable.get(pascalTypeName);
#         } else if (form == ENUMERATION) {
#             return pascalTypeName != null ? pascalTypeName : "int";
#         } else if (form == RECORD) return pascalTypeName;
#         else return typeNameTable.get(pascalTypeName);
#     }

#     @Override
#     public Object visitTypeIdentifier(PascalParser.TypeIdentifierContext ctx) {
#         Typespec pascalType = ctx.type;
#         String javaTypeName = typeName(pascalType);
#         code.emit(javaTypeName);

#         return null;
#     }

#     @Override
#     public Object visitVariableIdentifierList(
#             PascalParser.VariableIdentifierListContext ctx) {
#         String separator = " ";

#         for (PascalParser.VariableIdentifierContext varCtx :
#                 ctx.variableIdentifier()) {
#             code.emit(separator);
#             code.emit(varCtx.getText());
#             separator = ", ";
#         }

#         return null;
#     }

#     /**
#      * Emit code to allocate data for structured (array or record) variables.
#      *
#      * @param lhsPrefix the prefix for the target variable name.
#      * @param symTable  the symbol table containing the variable names.
#      */
#     private void emitAllocateStructuredVariables(String lhsPrefix, SymTable symTable) {
#         // Loop over all the symbol table's identifiers to emit
#         // code to allocate array and record variables.
#         for (SymTableEntry id : symTable.sortedEntries()) {
#             if (id.getKind() == VARIABLE) {
#                 emitAllocateStructuredData(lhsPrefix, id);
#             }
#         }
#     }

#     /**
#      * Emit code to allocate structured (array or record) data.
#      *
#      * @param lhsPrefix  the prefix for the target variable name.
#      * @param variableId the symbol table entry of the target variable.
#      */
#     private void emitAllocateStructuredData(String lhsPrefix,
#                                             SymTableEntry variableId) {
#         Typespec variableType = variableId.getType();
#         Form form = variableType.getForm();
#         String variableName = variableId.getName();

#         if (form == ARRAY) {
#             code.emitStart(lhsPrefix + variableName + " = ");
#             Typespec elemType = emitNewArray(variableType);
#             code.emitEnd(";");

#             if (elemType.isStructured()) {
#                 emitNewArrayElement(lhsPrefix, variableName, variableType);
#             }
#         } else if (form == RECORD) {
#             code.emitStart(lhsPrefix + variableName + " = ");
#             emitNewRecord(lhsPrefix, variableName, variableType);
#         }
#     }

#     /**
#      * Emit a string of bracketed dimension sizes for the array datatype.
#      * followed by the "new" array allocation.
#      *
#      * @param type the array datatype.
#      * @return the base datatype of the array.
#      */
#     private Typespec emitNewArray(Typespec type) {
#         StringBuilder sizes = new StringBuilder();

#         while (type.getForm() == ARRAY) {
#             sizes.append("[").append(type.getArrayElementCount()).append("]");
#             type = type.getArrayElementType();
#         }

#         type = type.baseType();
#         String pascalTypeName = type.getIdentifier().getName();
#         String javaTypeName = typeNameTable.get(pascalTypeName);

#         if (javaTypeName == null) javaTypeName = pascalTypeName;
#         code.emit("new " + javaTypeName + sizes);

#         return type;
#     }

#     /**
#      * Emit code to allocate an array element.
#      *
#      * @param lhsPrefix    the prefix for the target variable name.
#      * @param variableName the name of the target variable.
#      * @param elemType     the element's datatype.
#      */
#     private void emitNewArrayElement(String lhsPrefix, String variableName,
#                                      Typespec elemType) {
#         int dimensionCount = 0;

#         StringBuilder variableNameBuilder = new StringBuilder(variableName);
#         do {
#             int elemCount = elemType.getArrayElementCount();
#             ++dimensionCount;
#             String subscript = "_i" + dimensionCount;
#             variableNameBuilder.append("[").append(subscript).append("]");

#             code.emitLine("for (int " + subscript + " = 0; " +
#                     subscript + " < " + elemCount +
#                     "; " + subscript + "++)");
#             code.emitStart("{");
#             code.indent();

#             elemType = elemType.getArrayElementType();
#         } while (elemType.getForm() == ARRAY);
#         variableName = variableNameBuilder.toString();

#         String typeName = elemType.getIdentifier().getName();
#         code.emitStart(lhsPrefix + variableName + " = new " + typeName + "()");
#         code.emitEnd(";");

#         emitNewRecordFields(lhsPrefix + variableName + ".", elemType);

#         while (--dimensionCount >= 0) {
#             code.dedent();
#             code.emitLine("}");
#         }
#     }

#     /**
#      * Emit code to allocate a new record.
#      *
#      * @param lhsPrefix    the prefix for the target variable name.
#      * @param variableName the name of the target variable.
#      * @param recordType   the record's datatype.
#      */
#     private void emitNewRecord(String lhsPrefix, String variableName,
#                                Typespec recordType) {
#         String typePath = recordType.getRecordTypePath();
#         int index = typePath.indexOf('$');

#         // Don't include the program name in the record type path.
#         // Replace each $ with a period.
#         typePath = typePath.substring(index + 1).replace('$', '.');
#         code.emit("new " + typePath + "();");

#         emitNewRecordFields(lhsPrefix + variableName + ".", recordType);
#     }

#     /**
#      * Emit code to allocate a record's fields.
#      *
#      * @param lhsPrefix  the prefix for the target variable name.
#      * @param recordType the record's datatype.
#      */
#     private void emitNewRecordFields(String lhsPrefix, Typespec recordType) {
#         for (SymTableEntry fieldId : recordType.getRecordSymTable().sortedEntries()) {
#             if (fieldId.getKind() == RECORD_FIELD) {
#                 Typespec type = fieldId.getType();

#                 if (type.isStructured()) {
#                     emitAllocateStructuredData(lhsPrefix, fieldId);
#                 }
#             }
#         }
#     }

#     @Override
#     public Object visitStatementList(PascalParser.StatementListContext ctx) {
#         for (PascalParser.StatementContext stmtCtx : ctx.statement()) {
#             if (stmtCtx.emptyStatement() == null) {
#                 code.emitStart();
#                 visit(stmtCtx);
#             }
#         }

#         return null;
#     }

#     @Override
#     public Object visitCompoundStatement(
#             PascalParser.CompoundStatementContext ctx) {
#         code.emit("{");
#         code.indent();
#         visitChildren(ctx);
#         code.dedent();
#         code.emitLine("}");

#         return null;
#     }

#     @Override
#     public Object visitAssignmentStatement(
#             PascalParser.AssignmentStatementContext ctx) {
#         String lhs = (String) visit(ctx.lhs().variable());
#         String expr = (String) visit(ctx.rhs().expression());
#         code.emit(lhs + " = " + expr);
#         code.emitEnd(";");

#         return null;
#     }

#     @Override
#     public Object visitRepeatStatement(PascalParser.RepeatStatementContext ctx) {
#         boolean needBraces = ctx.statementList().statement().size() > 1;

#         code.emit("do");
#         if (needBraces) code.emitLine("{");
#         code.indent();

#         visit(ctx.statementList());

#         code.dedent();
#         if (needBraces) code.emitLine("}");

#         code.emitStart("while (!(");
#         code.emit((String) visit(ctx.expression()));
#         code.emitEnd("));");

#         return null;
#     }

#     @Override
#     public Object visitProcedureCallStatement(
#             PascalParser.ProcedureCallStatementContext ctx) {
#         PascalParser.ProcedureNameContext procNameCtx = ctx.procedureName();
#         String procedureName = procNameCtx.entry.getName();

#         code.emit(procedureName);
#         code.emit("(");

#         if (ctx.argumentList() != null) {
#             code.emit((String) visit(ctx.argumentList()));
#         }

#         code.emitEnd(");");
#         return null;
#     }

#     @Override
#     public Object visitArgumentList(PascalParser.ArgumentListContext ctx) {
#         StringBuilder text = new StringBuilder();
#         String separator = "";

#         for (PascalParser.ArgumentContext argCtx : ctx.argument()) {
#             text.append(separator);
#             text.append((String) visit(argCtx.expression()));
#             separator = ", ";
#         }

#         return text.toString();
#     }

#     @Override
#     public Object visitExpression(PascalParser.ExpressionContext ctx) {
#         PascalParser.SimpleExpressionContext simpleCtx1 =
#                 ctx.simpleExpression().get(0);
#         PascalParser.RelOpContext relOpCtx = ctx.relOp();
#         String simpleText1 = (String) visit(simpleCtx1);
#         String text = simpleText1;

#         // Second simple expression?
#         if (relOpCtx != null) {
#             String op = relOpCtx.getText();

#             if (op.equals("=")) op = "==";
#             else if (op.equals("<>")) op = "!=";

#             PascalParser.SimpleExpressionContext simpleCtx2 =
#                     ctx.simpleExpression().get(1);
#             String simpleText2 = (String) visit(simpleCtx2);

#             // Java uses the compareTo method for strings.
#             if (simpleCtx1.type == Predefined.stringType) {
#                 text = "(" + simpleText1 + ")."
#                         + "compareTo(" + simpleText2 + ") "
#                         + op + " 0";
#             } else {
#                 text = simpleText1 + " " + op + " " + simpleText2;
#             }
#         }

#         return text;
#     }

#     @Override
#     public Object visitSimpleExpression(PascalParser.SimpleExpressionContext ctx) {
#         int count = ctx.term().size();
#         StringBuilder text = new StringBuilder();

#         if ((ctx.sign() != null) && (ctx.sign().getText().equals("-"))) {
#             text.append("-");
#         }

#         // Loop over the simple expressions.
#         for (int i = 0; i < count; i++) {
#             PascalParser.TermContext termCtx = ctx.term().get(i);
#             text.append((String) visit(termCtx));

#             if (i < count - 1) {
#                 String addOp = ctx.addOp().get(i).getText().toLowerCase();
#                 if (addOp.equals("or")) addOp = "||";

#                 text.append(" ").append(addOp).append(" ");
#             }
#         }

#         return text.toString();
#     }

#     @Override
#     public Object visitTerm(PascalParser.TermContext ctx) {
#         int count = ctx.factor().size();
#         StringBuilder text = new StringBuilder();

#         // Loop over the terms.
#         for (int i = 0; i < count; i++) {
#             PascalParser.FactorContext factorCtx = ctx.factor().get(i);
#             text.append((String) visit(factorCtx));

#             if (i < count - 1) {
#                 String mulOpStr = ctx.mulOp().get(i).getText().toLowerCase();
#                 String mulOp = switch (mulOpStr) {
#                     case "and" -> " && ";
#                     case "div" -> "/";
#                     case "mod" -> "%";
#                     default -> mulOpStr;
#                 };

#                 text.append(mulOp);
#             }
#         }

#         return text.toString();
#     }

#     @Override
#     public Object visitVariableFactor(PascalParser.VariableFactorContext ctx) {
#         return visit(ctx.variable());
#     }

#     @Override
#     public Object visitVariable(PascalParser.VariableContext ctx) {
#         PascalParser.VariableIdentifierContext idCtx = ctx.variableIdentifier();
#         SymTableEntry variableId = idCtx.entry;
#         StringBuilder variableName = new StringBuilder(variableId.getName());
#         Typespec type = ctx.variableIdentifier().type;

#         if ((type != Predefined.booleanType)
#                 && (variableId.getKind() == ENUMERATION_CONSTANT)) {
#             variableName.insert(0, type.getIdentifier().getName() + ".");
#         }

#         // Loop over any subscript and field modifiers.
#         for (PascalParser.ModifierContext modCtx : ctx.modifier()) {
#             // Subscripts.
#             if (modCtx.indexList() != null) {
#                 for (PascalParser.IndexContext indexCtx :
#                         modCtx.indexList().index()) {
#                     Typespec indexType = type.getArrayIndexType();
#                     int minIndex = 0;

#                     if (indexType.getForm() == SUBRANGE) {
#                         minIndex = indexType.getSubrangeMinValue();
#                     }

#                     PascalParser.ExpressionContext exprCtx =
#                             indexCtx.expression();
#                     String expr = (String) visit(exprCtx);
#                     String subscript =
#                             (minIndex == 0) ? expr
#                                     : (minIndex < 0) ? "(" + expr + ")+" + (-minIndex)
#                                     : "(" + expr + ")-" + minIndex;

#                     variableName.append("[").append(subscript).append("]");

#                     type = type.getArrayElementType();
#                 }
#             }

#             // Record field.
#             else {
#                 PascalParser.FieldContext fieldCtx = modCtx.field();
#                 String fieldName = fieldCtx.entry.getName();
#                 variableName.append(".").append(fieldName);
#                 type = fieldCtx.type;
#             }
#         }

#         return variableName.toString();
#     }

#     @Override
#     public Object visitNumberFactor(PascalParser.NumberFactorContext ctx) {
#         return ctx.getText();
#     }

#     @Override
#     public Object visitCharacterFactor(PascalParser.CharacterFactorContext ctx) {
#         return ctx.getText();
#     }

#     @Override
#     public Object visitStringFactor(PascalParser.StringFactorContext ctx) {
#         String pascalString = ctx.stringConstant().STRING().getText();
#         return '"' + convertString(pascalString) + '"';
#     }

#     /**
#      * Convert a Pascal string to a Java string.
#      *
#      * @param pascalString the Pascal string.
#      * @return the Java string.
#      */
#     private String convertString(String pascalString) {
#         String unquoted = pascalString.substring(1, pascalString.length() - 1);
#         return unquoted.replace("''", "'").replace("\"", "\\\"");
#     }

#     @Override
#     public Object visitFunctionCallFactor(
#             PascalParser.FunctionCallFactorContext ctx) {
#         PascalParser.FunctionCallContext callCtx = ctx.functionCall();
#         PascalParser.FunctionNameContext funcNameCtx = callCtx.functionName();
#         String functionName = funcNameCtx.entry.getName();

#         String text = functionName + "(";

#         if (callCtx.argumentList() != null) {
#             text += (String) visit(callCtx.argumentList());
#         }

#         text += ")";
#         return text;
#     }

#     @Override
#     public Object visitNotFactor(PascalParser.NotFactorContext ctx) {
#         return "!" + visit(ctx.factor());
#     }

#     @Override
#     public Object visitParenthesizedFactor(
#             PascalParser.ParenthesizedFactorContext ctx) {
#         return "(" + visit(ctx.expression()) + ")";
#     }

#     @Override
#     public Object visitWriteStatement(PascalParser.WriteStatementContext ctx) {
#         code.emit("System.out.printf(");
#         code.mark();

#         String format = createWriteFormat(ctx.writeArguments());
#         String arguments = createWriteArguments(ctx.writeArguments());

#         code.emit('"' + format + '"');

#         if (arguments.length() > 0) {
#             code.emit(", ");
#             code.split(60);
#             code.emit(arguments);
#         }

#         code.emitEnd(");");
#         return null;
#     }

#     @Override
#     public Object visitWritelnStatement(PascalParser.WritelnStatementContext ctx) {
#         if (ctx.writeArguments() != null) {
#             code.emit("System.out.printf(");
#             code.mark();

#             String format = createWriteFormat(ctx.writeArguments());
#             String arguments = createWriteArguments(ctx.writeArguments());

#             code.emit('"' + format + "\\n\"");  // append line feed

#             if (arguments.length() > 0) {
#                 code.emit(", ");
#                 code.split(60);
#                 code.emit(arguments);
#             }

#             code.emitEnd(");");
#         } else {
#             code.emitEnd("System.out.println();");
#         }

#         return null;
#     }

#     /**
#      * Create the printf format string.
#      *
#      * @param ctx the WriteArgumentsContext.
#      * @return the format string.
#      */
#     private String createWriteFormat(PascalParser.WriteArgumentsContext ctx) {
#         StringBuilder format = new StringBuilder();

#         // Loop over the "write" arguments.
#         for (PascalParser.WriteArgumentContext argCtx : ctx.writeArgument()) {
#             Typespec type = argCtx.expression().type;
#             String argText = argCtx.getText();

#             // Append any literal strings.
#             if (argText.charAt(0) == '\'') {
#                 format.append(convertString(argText));
#             }

#             // For any other expressions, append a field specifier.
#             else {
#                 format.append("%");

#                 PascalParser.FieldWidthContext fwCtx = argCtx.fieldWidth();
#                 if (fwCtx != null) {
#                     String sign = ((fwCtx.sign() != null)
#                             && (fwCtx.sign().getText().equals("-")))
#                             ? "-" : "";
#                     format.append(sign)
#                             .append(fwCtx.integerConstant().getText());

#                     PascalParser.DecimalPlacesContext dpCtx =
#                             fwCtx.decimalPlaces();
#                     if (dpCtx != null) {
#                         format.append(".")
#                                 .append(dpCtx.integerConstant().getText());
#                     }
#                 }

#                 String typeFlag = type == Predefined.integerType ? "d"
#                         : type == Predefined.realType ? "f"
#                         : type == Predefined.booleanType ? "b"
#                         : type == Predefined.charType ? "c"
#                         : "s";
#                 format.append(typeFlag);
#             }
#         }

#         return format.toString();
#     }

#     /**
#      * Create the string of write arguments.
#      *
#      * @param ctx the WriteArgumentsContext.
#      * @return the string of arguments.
#      */
#     private String createWriteArguments(PascalParser.WriteArgumentsContext ctx) {
#         StringBuilder arguments = new StringBuilder();
#         String separator = "";

#         // Loop over "write" arguments.
#         for (PascalParser.WriteArgumentContext argCtx : ctx.writeArgument()) {
#             String argText = argCtx.getText();

#             // Not a literal string.
#             if (argText.charAt(0) != '\'') {
#                 arguments.append(separator).append(visit(argCtx.expression()));
#                 separator = ", ";
#             }
#         }

#         return arguments.toString();
#     }

#     @Override
#     public Object visitReadStatement(PascalParser.ReadStatementContext ctx) {
#         if (ctx.readArguments().variable().size() == 1) {
#             visit(ctx.readArguments());
#         } else {
#             code.emit("{");
#             code.indent();
#             code.emitStart();

#             visit(ctx.readArguments());

#             code.dedent();
#             code.emitLine("}");
#         }

#         return null;
#     }

#     @Override
#     public Object visitReadlnStatement(PascalParser.ReadlnStatementContext ctx) {
#         code.emit("{");
#         code.indent();
#         code.emitStart();

#         visit(ctx.readArguments());
#         code.emitLine("_sysin.nextLine();");

#         code.dedent();
#         code.emitLine("}");

#         return null;
#     }

#     @Override
#     public Object visitReadArguments(PascalParser.ReadArgumentsContext ctx) {
#         int size = ctx.variable().size();

#         // Loop over the read arguments.
#         for (int i = 0; i < size; i++) {
#             PascalParser.VariableContext varCtx = ctx.variable().get(i);
#             String varName = varCtx.getText();
#             Typespec type = varCtx.type;

#             // Read a character.
#             if (type == Predefined.charType) {
#                 code.emit("{");
#                 code.indent();

#                 code.emitStart("_sysin.useDelimiter(\"\");");
#                 code.emitStart(varName + " = _sysin.next().charAt(0);");
#                 code.emitStart("_sysin.reset();");

#                 code.dedent();
#                 code.emitLine("}");
#             }

#             // Read any other value.
#             else {
#                 String typeName = type == Predefined.integerType ? "Int"
#                         : type == Predefined.realType ? "Double"
#                         : type == Predefined.booleanType ? "Boolean"
#                         : "";

#                 code.emit(varName + " = _sysin.next" + typeName + "();");
#             }

#             if (i < size - 1) code.emitStart();
#         }

#         return null;
#     }
# }
