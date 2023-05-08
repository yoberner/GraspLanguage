#
#  Semantic operations.
#  Perform type checking and create symbol tables.
#
from GraspParser import GraspParser
from GraspVisitor import GraspVisitor
from edu.yu.compilers.frontend.SemanticErrorHandler import SemanticErrorHandler
from edu.yu.compilers.intermediate.symtable.Predefined import Predefined
from edu.yu.compilers.intermediate.symtable.SymTable import SymTable
from edu.yu.compilers.intermediate.symtable.SymTableStack import SymTableStack
from edu.yu.compilers.intermediate.type.Typespec import Typespec
from edu.yu.compilers.intermediate.util.CrossReferencer import CrossReferencer


# import antlr4.PascalBaseVisitor
# import antlr4.PascalParser
# import edu.yu.compilers.intermediate.symtable.Predefined
# import edu.yu.compilers.intermediate.symtable.SymTable
# import edu.yu.compilers.intermediate.symtable.SymTableEntry
# import edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind
# import edu.yu.compilers.intermediate.symtable.SymTableStack
# import edu.yu.compilers.intermediate.type.TypeChecker
# import edu.yu.compilers.intermediate.type.Typespec
# import edu.yu.compilers.intermediate.type.Typespec.Form
# import edu.yu.compilers.intermediate.util.BackendMode
# import edu.yu.compilers.intermediate.util.CrossReferencer
#
# import java.util.ArrayList
# import java.util.HashSet
#
# import static edu.yu.compilers.frontend.SemanticErrorHandler.Code.*
# import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind.*
# import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Routine.DECLARED
# import static edu.yu.compilers.intermediate.type.Typespec.Form.*
# import static edu.yu.compilers.intermediate.util.BackendMode.EXECUTOR


class Semantics(GraspVisitor) :


    def __init__(self, mode):
        # Create and initialize the symbol table stack.
        self.symTableStack = SymTableStack()
        Predefined.initialize(self.symTableStack)

        self.mode = mode
        self.error = SemanticErrorHandler()


    # Return the default value for a data type.
    #
    # @param type the data type.
    # @return the default value.
    @staticmethod
    def defaultValue(_type: Typespec) :
        _type = _type.baseType()

        if _type == Predefined.integerType:
            return 0
        elif _type == Predefined.realType: 
            return 0.0
        elif _type == Predefined.booleanType: 
            return False
        elif _type == Predefined.charType: 
            return '#'
        else:
            return "#"

    def getProgramId(self) :
        return self.programId
    

    def getErrorCount(self) :
        return self.error.get_count()
    

    def printSymbolTableStack(self) :
        # Print the cross-reference table.
        crossReferencer =  CrossReferencer()
        crossReferencer._print(self.symTableStack)
    

    
    def visitProgram(self, ctx) :
        self.self.visit(ctx.programHeader())
        self.self.visit(ctx.block().declarations())
        self.self.visit(ctx.block().compoundStatement())

        return None
    

    
    def visitProgramHeader(self, ctx) :
        idCtx = ctx.programIdentifier()
        programName = idCtx.IDENTIFIER().getText()  # don't shift case

        programId = self.symTableStack.enterLocal(programName, PROGRAM)
        programId.setRoutineSymTable(self.symTableStack.push())

        self.symTableStack.setProgramId(programId)
        self.symTableStack.getLocalSymTable().setOwner(programId)

        idCtx.entry = programId
        return None
    

    def visitConstantDefinition(self, ctx) :
        idCtx = ctx.constantIdentifier()
        constantName = idCtx.IDENTIFIER().getText().toLowerCase()
        constantId = self.symTableStack.lookupLocal(constantName)

        if constantId is None :
            constCtx = ctx.constant()
            constValue = self.visit(constCtx)

            constantId = self.symTableStack.enterLocal(constantName, CONSTANT)
            constantId.setValue(constValue)
            constantId.setType(constCtx.type)

            idCtx.entry = constantId
            idCtx.type = constCtx.type
        else :
            self.error.flag(REDECLARED_IDENTIFIER, ctx)

            idCtx.entry = constantId
            idCtx.type = Predefined.integerType

        constantId.appendLineNumber(ctx.start.getLine()) # TODO WHAT?
        return None
    


    def visitConstant(self, ctx) :
        if ctx.IDENTIFIER() is not None:
            constantName = ctx.IDENTIFIER().getText().toLowerCase()
            constantId = self.symTableStack.lookup(constantName)

            if constantId is not None:
                kind = constantId.getKind()
                if (kind != CONSTANT) and (kind != ENUMERATION_CONSTANT):
                    self.error.flag(INVALID_CONSTANT, ctx)
                

                ctx.type = constantId.getType()
                ctx.value = constantId.getValue()

                constantId.appendLineNumber(ctx.start.getLine())
            else :
                self.error.flag(UNDECLARED_IDENTIFIER, ctx)

                ctx.type = Predefined.integerType
                ctx.value = 0
            
        elif ctx.characterConstant() is not None:
            ctx.type = Predefined.charType
            ctx.value = ctx.getText().charAt(1)
        elif ctx.stringConstant() is not None:
            graspString = ctx.stringConstant().STRING().getText()
            unquoted = graspString[1, graspString.length() - 1]
            ctx.type = Predefined.stringType
            ctx.value = unquoted.replace("''", "'").replace("\"", "\\\"")
        else:
            if ctx.unsignedNumber().integerConstant() is not None:
                ctx.type = Predefined.integerType
                ctx.value = int(ctx.getText())
            else :
                ctx.type = Predefined.realType
                ctx.value = float(ctx.getText())
            
        

        return ctx.value
    


    def visitTypeDefinition(self, ctx) :
        idCtx = ctx.typeIdentifier()
        typeName = idCtx.IDENTIFIER().getText().toLowerCase()
        typeId = self.symTableStack.lookupLocal(typeName)

        typespecCtx = ctx.typeSpecification()

        # If it's a record type, create a named record type.
        if isinstance(typespecCtx, GraspParser.RecordTypespecContext) :
            typeId = createRecordType(typespecCtx, typeName)
        # Enter the type name of any other type into the symbol table.
        elif typeId is None:
            self.visit(typespecCtx)

            typeId = self.symTableStack.enterLocal(typeName, TYPE)
            typeId.setType(typespecCtx.type)
            typespecCtx.type.setIdentifier(typeId)
        # Redeclared identifier.
        else :
            self.error.flag(REDECLARED_IDENTIFIER, ctx)
        

        idCtx.entry = typeId
        idCtx.type = typespecCtx.type

        typeId.appendLineNumber(ctx.start.getLine())
        return None
    

    def visitRecordTypespec(self, ctx) :
        # Create an unnamed record type.
        recordTypeName = SymTable.generateUnnamedName()
        createRecordType(ctx, recordTypeName)

        return None
    

    
     # Create a new record type.
     
     # @param recordTypeSpecCtx the RecordTypespecContext.
     # @param recordTypeName    the name of the record type.
     # @return the symbol table entry of the record type identifier.
     
    private SymTableEntry createRecordType(PascalParser.RecordTypespecContext recordTypeSpecCtx, String recordTypeName) :
        PascalParser.RecordTypeContext recordTypeCtx = recordTypeSpecCtx.recordType()
        Typespec recordType = new Typespec(RECORD)

        SymTableEntry recordTypeId = self.symTableStack.enterLocal(recordTypeName, TYPE)
        recordTypeId.setType(recordType)
        recordType.setIdentifier(recordTypeId)

        String recordTypePath = createRecordTypePath(recordType)
        recordType.setRecordTypePath(recordTypePath)

        // Enter the record fields into the record type's symbol table.
        SymTable recordSymTable = createRecordSymTable(recordTypeCtx.recordFields(), recordTypeId)
        recordType.setRecordSymTable(recordSymTable)

        recordTypeCtx.entry = recordTypeId
        recordTypeSpecCtx.type = recordType

        return recordTypeId
    

    
     # Create the fully qualified type pathname of a record type.
     
     # @param recordType the record type.
     # @return the pathname.
     
    private String createRecordTypePath(Typespec recordType) :
        SymTableEntry recordId = recordType.getIdentifier()
        SymTableEntry parentId = recordId.getSymTable().getOwner()
        String path = recordId.getName()

        while ((parentId.getKind() == TYPE) and (parentId.getType().getForm() == RECORD)) :
            path = parentId.getName() + "$" + path
            parentId = parentId.getSymTable().getOwner()
        

        path = parentId.getName() + "$" + path
        return path
    

    
     # Create the symbol table for a record type.
     
     # @param ctx     the RecordFieldsContext,
     # @param ownerId the symbol table entry of the owner's identifier.
     # @return the symbol table.
     
    private SymTable createRecordSymTable(PascalParser.RecordFieldsContext ctx, SymTableEntry ownerId) :
        SymTable recordSymTable = self.symTableStack.push()

        recordSymTable.setOwner(ownerId)
        self.visit(ctx.variableDeclarationsList())
        recordSymTable.resetVariables(RECORD_FIELD)
        self.symTableStack.pop()

        return recordSymTable
    

    @Override
    public Object visitSimpleTypespec(PascalParser.SimpleTypespecContext ctx) :
        self.visit(ctx.simpleType())
        ctx.type = ctx.simpleType().type

        return None
    

    @Override
    public Object visitTypeIdentifierTypespec(PascalParser.TypeIdentifierTypespecContext ctx) :
        self.visit(ctx.typeIdentifier())
        ctx.type = ctx.typeIdentifier().type

        return None
    

    @Override
    public Object visitTypeIdentifier(PascalParser.TypeIdentifierContext ctx) :
        String typeName = ctx.IDENTIFIER().getText().toLowerCase()
        SymTableEntry typeId = self.symTableStack.lookup(typeName)

        if (typeId != None) :
            if (typeId.getKind() != TYPE) :
                self.error.flag(INVALID_TYPE, ctx)
                ctx.type = Predefined.integerType
             else :
                ctx.type = typeId.getType()
            

            typeId.appendLineNumber(ctx.start.getLine())
         else :
            self.error.flag(UNDECLARED_IDENTIFIER, ctx)
            ctx.type = Predefined.integerType
        

        ctx.entry = typeId
        return None
    

    @Override
    public Object visitEnumerationTypespec(PascalParser.EnumerationTypespecContext ctx) :
        Typespec enumType = new Typespec(ENUMERATION)
        ArrayList<SymTableEntry> constants = new ArrayList<>()
        int value = -1

        // Loop over the enumeration constants.
        for (PascalParser.EnumerationConstantContext constCtx : ctx.enumerationType().enumerationConstant()) :
            PascalParser.ConstantIdentifierContext constIdCtx = constCtx.constantIdentifier()
            String constantName = constIdCtx.IDENTIFIER().getText().toLowerCase()
            SymTableEntry constantId = self.symTableStack.lookupLocal(constantName)

            if (constantId == None) :
                constantId = self.symTableStack.enterLocal(constantName, ENUMERATION_CONSTANT)
                constantId.setType(enumType)
                constantId.setValue(++value)

                constants.add(constantId)
             else :
                self.error.flag(REDECLARED_IDENTIFIER, constCtx)
            

            constIdCtx.entry = constantId
            constIdCtx.type = enumType

            constantId.appendLineNumber(ctx.start.).getLine())
        

        enumType.setEnumerationConstants(constants)
        ctx.type = enumType

        return None
    

    @Override
    public Object visitSubrangeTypespec(PascalParser.SubrangeTypespecContext ctx) :
        Typespec type = new Typespec(SUBRANGE)
        PascalParser.SubrangeTypeContext subCtx = ctx.subrangeType()
        PascalParser.ConstantContext minCtx = subCtx.constant().get(0)
        PascalParser.ConstantContext maxCtx = subCtx.constant().get(1)

        Object minObj = self.visit(minCtx)
        Object maxObj = self.visit(maxCtx)

        Typespec minType = minCtx.type
        Typespec maxType = maxCtx.type

        if (((minType.getForm() != SCALAR) and (minType.getForm() != ENUMERATION)) || (minType == Predefined.realType) || (minType == Predefined.stringType)) :
            self.error.flag(INVALID_CONSTANT, minCtx)
            minType = Predefined.integerType
            minObj = 0
        

        int minValue
        int maxValue

        if (minType == Predefined.integerType) :
            minValue = (Integer) minObj
            maxValue = (Integer) maxObj
         else if (minType == Predefined.charType) :
            minValue = (Character) minObj
            maxValue = (Character) maxObj
         else  // enumeration constants
        :
            minValue = (Integer) minCtx.value
            maxValue = (Integer) maxCtx.value
        

        if ((maxType != minType) || (minValue > maxValue)) :
            self.error.flag(INVALID_CONSTANT, maxCtx)
            maxValue = minValue
        

        type.setSubrangeBaseType(minType)
        type.setSubrangeMinValue(minValue)
        type.setSubrangeMaxValue(maxValue)

        ctx.type = type
        return None
    

    @Override
    public Object visitArrayTypespec(PascalParser.ArrayTypespecContext ctx) :
        Typespec arrayType = new Typespec(ARRAY)
        PascalParser.ArrayTypeContext arrayCtx = ctx.arrayType()
        PascalParser.ArrayDimensionListContext listCtx = arrayCtx.arrayDimensionList()

        ctx.type = arrayType

        // Loop over the array dimensions.
        int count = listCtx.simpleType().size()
        for (int i = 0 i < count i++) :
            PascalParser.SimpleTypeContext simpleCtx = listCtx.simpleType().get(i)
            self.visit(simpleCtx)
            arrayType.setArrayIndexType(simpleCtx.type)
            arrayType.setArrayElementCount(typeCount(simpleCtx.type))

            if (i < count - 1) :
                Typespec elementType = new Typespec(ARRAY)
                arrayType.setArrayElementType(elementType)
                arrayType = elementType
            
        

        self.visit(arrayCtx.typeSpecification())
        Typespec elementType = arrayCtx.typeSpecification().type
        arrayType.setArrayElementType(elementType)

        return None
    

    
     # Return the number of values in a datatype.
     
     # @param type the datatype.
     # @return the number of values.
     
    private int typeCount(Typespec type) :
        int count

        if (type.getForm() == ENUMERATION) :
            ArrayList<SymTableEntry> constants = type.getEnumerationConstants()
            count = constants.size()
         else  // subrange
        :
            int minValue = type.getSubrangeMinValue()
            int maxValue = type.getSubrangeMaxValue()
            count = maxValue - minValue + 1
        

        return count
    

    @Override
    public Object visitVariableDeclarations(PascalParser.VariableDeclarationsContext ctx) :
        PascalParser.TypeSpecificationContext typeCtx = ctx.typeSpecification()
        self.visit(typeCtx)

        PascalParser.VariableIdentifierListContext listCtx = ctx.variableIdentifierList()

        // Loop over the variables being declared.
        for (PascalParser.VariableIdentifierContext idCtx : listCtx.variableIdentifier()) :
            int lineNumber = idctx.start.).getLine()
            String variableName = idCtx.IDENTIFIER().getText().toLowerCase()
            SymTableEntry variableId = self.symTableStack.lookupLocal(variableName)

            if (variableId == None) :
                variableId = self.symTableStack.enterLocal(variableName, VARIABLE)
                variableId.setType(typeCtx.type)

                // Assign slot numbers to local variables.
                SymTable symTable = variableId.getSymTable()
                if (symTable.getNestingLevel() > 1) :
                    variableId.setSlotNumber(symTable.nextSlotNumber())
                

                idCtx.entry = variableId
             else :
                self.error.flag(REDECLARED_IDENTIFIER, ctx)
            

            variableId.appendLineNumber(lineNumber)
        

        return None
    

    @Override
    @SuppressWarnings("unchecked")
    public Object visitRoutineDefinition(PascalParser.RoutineDefinitionContext ctx) :
        PascalParser.FunctionHeadContext funcCtx = ctx.functionHead()
        PascalParser.ProcedureHeadContext procCtx = ctx.procedureHead()
        PascalParser.RoutineIdentifierContext idCtx
        PascalParser.ParametersContext parameters
        boolean functionDefinition = funcCtx != None
        Typespec returnType = None
        String routineName

        if (functionDefinition) :
            idCtx = funcCtx.routineIdentifier()
            parameters = funcCtx.parameters()
         else :
            idCtx = procCtx.routineIdentifier()
            parameters = procCtx.parameters()
        

        routineName = idCtx.IDENTIFIER().getText().toLowerCase()
        SymTableEntry routineId = self.symTableStack.lookupLocal(routineName)

        if (routineId != None) :
            self.error.flag(REDECLARED_IDENTIFIER, ctx.start.).getLine(), routineName)
            return None
        

        routineId = self.symTableStack.enterLocal(routineName, functionDefinition ? FUNCTION : PROCEDURE)
        routineId.setRoutineCode(DECLARED)
        idCtx.entry = routineId

        // Append to the parent routine's list of subroutines.
        SymTableEntry parentId = self.symTableStack.getLocalSymTable().getOwner()
        parentId.appendSubroutine(routineId)

        routineId.setRoutineSymTable(symTableStack.push())
        idCtx.entry = routineId

        SymTable symTable = self.symTableStack.getLocalSymTable()
        symTable.setOwner(routineId)

        if (parameters != None) :
            ArrayList<SymTableEntry> parameterIds = (ArrayList<SymTableEntry>) self.visit(parameters.parameterDeclarationsList())
            routineId.setRoutineParameters(parameterIds)

            for (SymTableEntry paramId : parameterIds) :
                paramId.setSlotNumber(symTable.nextSlotNumber())
            
        

        if (functionDefinition) :
            PascalParser.TypeIdentifierContext typeIdCtx = funcCtx.typeIdentifier()
            self.visit(typeIdCtx)
            returnType = typeIdCtx.type

            if (returnType.getForm() != SCALAR) :
                self.error.flag(INVALID_RETURN_TYPE, typeIdCtx)
                returnType = Predefined.integerType
            

            routineId.setType(returnType)
            idCtx.type = returnType
         else :
            idCtx.type = None
        

        self.visit(ctx.block().declarations())

        // Enter the function's associated variable into its symbol table.
        if (functionDefinition) :
            SymTableEntry assocVarId = self.symTableStack.enterLocal(routineName, VARIABLE)
            assocVarId.setSlotNumber(symTable.nextSlotNumber())
            assocVarId.setType(returnType)
        

        self.visit(ctx.block().compoundStatement())
        routineId.setExecutable(ctx.block().compoundStatement())

        self.symTableStack.pop()
        return None
    

    @Override
    @SuppressWarnings("unchecked")
    public Object visitParameterDeclarationsList(PascalParser.ParameterDeclarationsListContext ctx) :
        ArrayList<SymTableEntry> parameterList = new ArrayList<>()

        // Loop over the parameter declarations.
        for (PascalParser.ParameterDeclarationsContext dclCtx : ctx.parameterDeclarations()) :
            ArrayList<SymTableEntry> parameterSublist = (ArrayList<SymTableEntry>) self.visit(dclCtx)
            parameterList.addAll(parameterSublist)
        

        return parameterList
    

    @Override
    public Object visitParameterDeclarations(PascalParser.ParameterDeclarationsContext ctx) :
        Kind kind = ctx.VAR() != None ? REFERENCE_PARAMETER : VALUE_PARAMETER
        PascalParser.TypeIdentifierContext typeCtx = ctx.typeIdentifier()

        self.visit(typeCtx)
        Typespec paramType = typeCtx.type

        ArrayList<SymTableEntry> parameterSublist = new ArrayList<>()

        // Loop over the parameter identifiers.
        PascalParser.ParameterIdentifierListContext paramListCtx = ctx.parameterIdentifierList()
        for (PascalParser.ParameterIdentifierContext paramIdCtx : paramListCtx.parameterIdentifier()) :
            int lineNumber = paramIdctx.start.).getLine()
            String paramName = paramIdCtx.IDENTIFIER().getText().toLowerCase()
            SymTableEntry paramId = self.symTableStack.lookupLocal(paramName)

            if (paramId == None) :
                paramId = self.symTableStack.enterLocal(paramName, kind)
                paramId.setType(paramType)

                if ((kind == REFERENCE_PARAMETER) and (mode != EXECUTOR) and (paramType.getForm() == SCALAR)) :
                    self.error.flag(INVALID_REFERENCE_PARAMETER, paramIdCtx)
                
             else :
                self.error.flag(REDECLARED_IDENTIFIER, paramIdCtx)
            

            paramIdCtx.entry = paramId
            paramIdCtx.type = paramType

            parameterSublist.add(paramId)
            paramId.appendLineNumber(lineNumber)
        

        return parameterSublist
    

    @Override
    public Object visitAssignmentStatement(PascalParser.AssignmentStatementContext ctx) :
        PascalParser.LhsContext lhsCtx = ctx.lhs()
        PascalParser.RhsContext rhsCtx = ctx.rhs()

        visitChildren(ctx)

        Typespec lhsType = lhsCtx.type
        Typespec rhsType = rhsCtx.expression().type

        if (!TypeChecker.areAssignmentCompatible(lhsType, rhsType)) :
            self.error.flag(INCOMPATIBLE_ASSIGNMENT, rhsCtx)
        

        return None
    

    @Override
    public Object visitLhs(PascalParser.LhsContext ctx) :
        PascalParser.VariableContext varCtx = ctx.variable()
        self.visit(varCtx)
        ctx.type = varCtx.type

        return None
    

    @Override
    public Object visitIfStatement(PascalParser.IfStatementContext ctx) :
        PascalParser.ExpressionContext exprCtx = ctx.expression()
        PascalParser.TrueStatementContext trueCtx = ctx.trueStatement()
        PascalParser.FalseStatementContext falseCtx = ctx.falseStatement()

        self.visit(exprCtx)
        Typespec exprType = exprCtx.type

        if (!TypeChecker.isBoolean(exprType)) :
            self.error.flag(TYPE_MUST_BE_BOOLEAN, exprCtx)
        

        self.visit(trueCtx)
        if (falseCtx != None) self.visit(falseCtx)

        return None
    

    @Override
    public Object visitCaseStatement(PascalParser.CaseStatementContext ctx) :
        PascalParser.ExpressionContext exprCtx = ctx.expression()
        self.visit(exprCtx)
        Typespec exprType = exprCtx.type
        Form exprTypeForm = exprType.getForm()

        if (((exprTypeForm != SCALAR) and (exprTypeForm != ENUMERATION) and (exprTypeForm != SUBRANGE)) || (exprType == Predefined.realType)) :
            self.error.flag(TYPE_MISMATCH, exprCtx)
            exprType = Predefined.integerType
        

        HashSet<Object> constants = new HashSet<>()
        PascalParser.CaseBranchListContext branchListCtx = ctx.caseBranchList()

        // Loop over the CASE branches.
        for (PascalParser.CaseBranchContext branchCtx : branchListCtx.caseBranch()) :
            PascalParser.CaseConstantListContext constListCtx = branchCtx.caseConstantList()
            PascalParser.StatementContext stmtCtx = branchCtx.statement()

            if (constListCtx != None) :
                // Loop over the CASE constants in each branch.
                for (PascalParser.CaseConstantContext caseConstCtx : constListCtx.caseConstant()) :
                    PascalParser.ConstantContext constCtx = caseConstCtx.constant()
                    Object constValue = self.visit(constCtx)

                    caseConstCtx.type = constCtx.type
                    caseConstCtx.value = None

                    if (constCtx.type != exprType) :
                        self.error.flag(TYPE_MISMATCH, constCtx)
                     else if ((constCtx.type == Predefined.integerType) || (constCtx.type.getForm() == ENUMERATION)) :
                        caseConstCtx.value = (Integer) constValue
                     else if (constCtx.type == Predefined.charType) :
                        caseConstCtx.value = (Character) constValue
                     else if (constCtx.type == Predefined.stringType) :
                        caseConstCtx.value = (String) constValue
                    

                    if (constants.contains(caseConstCtx.value)) :
                        self.error.flag(DUPLICATE_CASE_CONSTANT, constCtx)
                     else :
                        constants.add(caseConstCtx.value)
                    
                
            

            if (stmtCtx != None) self.visit(stmtCtx)
        

        return None
    

    @Override
    public Object visitRepeatStatement(PascalParser.RepeatStatementContext ctx) :
        PascalParser.ExpressionContext exprCtx = ctx.expression()
        self.visit(exprCtx)
        Typespec exprType = exprCtx.type

        if (!TypeChecker.isBoolean(exprType)) :
            self.error.flag(TYPE_MUST_BE_BOOLEAN, exprCtx)
        

        self.visit(ctx.statementList())
        return None
    

    @Override
    public Object visitWhileStatement(PascalParser.WhileStatementContext ctx) :
        PascalParser.ExpressionContext exprCtx = ctx.expression()
        self.visit(exprCtx)
        Typespec exprType = exprCtx.type

        if (!TypeChecker.isBoolean(exprType)) :
            self.error.flag(TYPE_MUST_BE_BOOLEAN, exprCtx)
        

        self.visit(ctx.statement())
        return None
    

    @Override
    public Object visitForStatement(PascalParser.ForStatementContext ctx) :
        PascalParser.VariableContext varCtx = ctx.variable()
        self.visit(varCtx)

        String controlName = varCtx.variableIdentifier().getText().toLowerCase()
        Typespec controlType = Predefined.integerType

        if (varCtx.entry != None) :
            controlType = varCtx.type

            if ((controlType.getForm() != SCALAR) || (controlType == Predefined.realType) || (controlType == Predefined.stringType) || (varCtx.modifier().size() != 0)) :
                self.error.flag(INVALID_CONTROL_VARIABLE, varCtx)
            
         else :
            self.error.flag(UNDECLARED_IDENTIFIER, ctx.start.).getLine(), controlName)
        

        PascalParser.ExpressionContext startCtx = ctx.expression().get(0)
        PascalParser.ExpressionContext endCtx = ctx.expression().get(1)

        self.visit(startCtx)
        self.visit(endCtx)

        if (startCtx.type != controlType) self.error.flag(TYPE_MISMATCH, startCtx)
        if (startCtx.type != endCtx.type) self.error.flag(TYPE_MISMATCH, endCtx)

        self.visit(ctx.statement())
        return None
    

    @Override
    public Object visitProcedureCallStatement(PascalParser.ProcedureCallStatementContext ctx) :
        PascalParser.ProcedureNameContext nameCtx = ctx.procedureName()
        PascalParser.ArgumentListContext listCtx = ctx.argumentList()
        String name = ctx.procedureName().getText().toLowerCase()
        SymTableEntry procedureId = self.symTableStack.lookup(name)
        boolean badName = false

        if (procedureId == None) :
            self.error.flag(UNDECLARED_IDENTIFIER, nameCtx)
            badName = true
         else if (procedureId.getKind() != PROCEDURE) :
            self.error.flag(NAME_MUST_BE_PROCEDURE, nameCtx)
            badName = true
        

        // Bad procedure name. Do a simple arguments check and then leave.
        if (badName) :
            for (PascalParser.ArgumentContext exprCtx : listCtx.argument()) :
                self.visit(exprCtx)
            
        

        // Good procedure name.
        else :
            ArrayList<SymTableEntry> params = procedureId.getRoutineParameters()
            checkCallArguments(listCtx, params)
        

        nameCtx.entry = procedureId
        return None
    

    @Override
    public Object visitFunctionCallFactor(PascalParser.FunctionCallFactorContext ctx) :
        PascalParser.FunctionCallContext callCtx = ctx.functionCall()
        PascalParser.FunctionNameContext nameCtx = callCtx.functionName()
        PascalParser.ArgumentListContext listCtx = callCtx.argumentList()
        String name = callCtx.functionName().getText().toLowerCase()
        SymTableEntry functionId = self.symTableStack.lookup(name)
        boolean badName = false

        ctx.type = Predefined.integerType

        if (functionId == None) :
            self.error.flag(UNDECLARED_IDENTIFIER, nameCtx)
            badName = true
         else if (functionId.getKind() != FUNCTION) :
            self.error.flag(NAME_MUST_BE_FUNCTION, nameCtx)
            badName = true
        

        // Bad function name. Do a simple arguments check and then leave.
        if (badName) :
            for (PascalParser.ArgumentContext exprCtx : listCtx.argument()) :
                self.visit(exprCtx)
            
        

        // Good function name.
        else :
            ArrayList<SymTableEntry> parameters = functionId.getRoutineParameters()
            checkCallArguments(listCtx, parameters)
            ctx.type = functionId.getType()
        

        nameCtx.entry = functionId
        nameCtx.type = ctx.type

        return None
    

    
     # Perform semantic operations on procedure and function call arguments.
     
     # @param listCtx    the ArgumentListContext.
     # @param parameters the arraylist of parameters to fill.
     
    private void checkCallArguments(PascalParser.ArgumentListContext listCtx, ArrayList<SymTableEntry> parameters) :
        int paramsCount = parameters.size()
        int argsCount = listCtx != None ? listCtx.argument().size() : 0

        if (paramsCount != argsCount) :
            self.error.flag(ARGUMENT_COUNT_MISMATCH, listCtx)
            return
        

        // Check each argument against the corresponding parameter.
        for (int i = 0 i < paramsCount i++) :
            PascalParser.ArgumentContext argCtx = listCtx.argument().get(i)
            PascalParser.ExpressionContext exprCtx = argCtx.expression()
            self.visit(exprCtx)

            SymTableEntry paramId = parameters.get(i)
            Typespec paramType = paramId.getType()
            Typespec argType = exprCtx.type

            // For a VAR parameter, the argument must be a variable
            // with the same datatype.
            if (paramId.getKind() == REFERENCE_PARAMETER) :
                if (expressionIsVariable(exprCtx)) :
                    if (paramType != argType) :
                        self.error.flag(TYPE_MISMATCH, exprCtx)
                    
                 else :
                    self.error.flag(ARGUMENT_MUST_BE_VARIABLE, exprCtx)
                
            

            // For a value parameter, the argument type must be
            // assignment compatible with the parameter type.
            else if (!TypeChecker.areAssignmentCompatible(paramType, argType)) :
                self.error.flag(TYPE_MISMATCH, exprCtx)
            
        
    

    
     # Determine whether an expression is a variable only.
     
     # @param exprCtx the ExpressionContext.
     # @return true if it's an expression only, else false.
     
    private boolean expressionIsVariable(PascalParser.ExpressionContext exprCtx) :
        // Only a single simple expression?
        if (exprCtx.simpleExpression().size() == 1) :
            PascalParser.SimpleExpressionContext simpleCtx = exprCtx.simpleExpression().get(0)
            // Only a single term?
            if (simpleCtx.term().size() == 1) :
                PascalParser.TermContext termCtx = simpleCtx.term().get(0)

                // Only a single factor?
                if (termCtx.factor().size() == 1) :
                    return termCtx.factor().get(0) instanceof PascalParser.VariableFactorContext
                
            
        

        return false
    

    @Override
    public Object visitExpression(PascalParser.ExpressionContext ctx) :
        PascalParser.SimpleExpressionContext simpleCtx1 = ctx.simpleExpression().get(0)

        // First simple expression.
        self.visit(simpleCtx1)

        Typespec simpleType1 = simpleCtx1.type
        ctx.type = simpleType1

        PascalParser.RelOpContext relOpCtx = ctx.relOp()

        // Second simple expression?
        if (relOpCtx != None) :
            PascalParser.SimpleExpressionContext simpleCtx2 = ctx.simpleExpression().get(1)
            self.visit(simpleCtx2)

            Typespec simpleType2 = simpleCtx2.type
            if (!TypeChecker.areComparisonCompatible(simpleType1, simpleType2)) :
                self.error.flag(INCOMPATIBLE_COMPARISON, ctx)
            

            ctx.type = Predefined.booleanType
        

        return None
    

    @Override
    public Object visitSimpleExpression(PascalParser.SimpleExpressionContext ctx) :
        int count = ctx.term().size()
        PascalParser.SignContext signCtx = ctx.sign()
        boolean hasSign = signCtx != None
        PascalParser.TermContext termCtx1 = ctx.term().get(0)

        if (hasSign) :
            String sign = signCtx.getText()
            if (!sign.equals("+") and !sign.equals("-")) :
                self.error.flag(INVALID_SIGN, signCtx)
            
        

        // First term.
        self.visit(termCtx1)
        Typespec termType1 = termCtx1.type

        // Loop over any subsequent terms.
        for (int i = 1 i < count i++) :
            String op = ctx.addOp().get(i - 1).getText().toLowerCase()
            PascalParser.TermContext termCtx2 = ctx.term().get(i)
            self.visit(termCtx2)
            Typespec termType2 = termCtx2.type

            // Both operands boolean ==> boolean result. Else type mismatch.
            if (op.equals("or")) :
                if (!TypeChecker.isBoolean(termType1)) :
                    self.error.flag(TYPE_MUST_BE_BOOLEAN, termCtx1)
                
                if (!TypeChecker.isBoolean(termType2)) :
                    self.error.flag(TYPE_MUST_BE_BOOLEAN, termCtx2)
                
                if (hasSign) :
                    self.error.flag(INVALID_SIGN, signCtx)
                

                termType2 = Predefined.booleanType
             else if (op.equals("+")) :
                // Both operands integer ==> integer result
                if (TypeChecker.areBothInteger(termType1, termType2)) :
                    termType2 = Predefined.integerType
                

                // Both real operands ==> real result 
                // One real and one integer operand ==> real result
                else if (TypeChecker.isAtLeastOneReal(termType1, termType2)) :
                    termType2 = Predefined.realType
                

                // Both operands string ==> string result
                else if (TypeChecker.areBothString(termType1, termType2)) :
                    if (hasSign) self.error.flag(INVALID_SIGN, signCtx)
                    termType2 = Predefined.stringType
                

                // Type mismatch.
                else :
                    if (!TypeChecker.isIntegerOrReal(termType1)) :
                        self.error.flag(TYPE_MUST_BE_NUMERIC, termCtx1)
                        termType2 = Predefined.integerType
                    
                    if (!TypeChecker.isIntegerOrReal(termType2)) :
                        self.error.flag(TYPE_MUST_BE_NUMERIC, termCtx2)
                        termType2 = Predefined.integerType
                    
                
             else  // -
            :
                // Both operands integer ==> integer result
                if (TypeChecker.areBothInteger(termType1, termType2)) :
                    termType2 = Predefined.integerType
                

                // Both real operands ==> real result 
                // One real and one integer operand ==> real result
                else if (TypeChecker.isAtLeastOneReal(termType1, termType2)) :
                    termType2 = Predefined.realType
                

                // Type mismatch.
                else :
                    if (!TypeChecker.isIntegerOrReal(termType1)) :
                        self.error.flag(TYPE_MUST_BE_NUMERIC, termCtx1)
                        termType2 = Predefined.integerType
                    
                    if (!TypeChecker.isIntegerOrReal(termType2)) :
                        self.error.flag(TYPE_MUST_BE_NUMERIC, termCtx2)
                        termType2 = Predefined.integerType
                    
                
            

            termType1 = termType2
        

        ctx.type = termType1
        return None
    

    @Override
    public Object visitTerm(PascalParser.TermContext ctx) :
        int count = ctx.factor().size()
        PascalParser.FactorContext factorCtx1 = ctx.factor().get(0)

        // First factor.
        self.visit(factorCtx1)
        Typespec factorType1 = factorCtx1.type

        // Loop over any subsequent factors.
        for (int i = 1 i < count i++) :
            String op = ctx.mulOp().get(i - 1).getText().toLowerCase()
            PascalParser.FactorContext factorCtx2 = ctx.factor().get(i)
            self.visit(factorCtx2)
            Typespec factorType2 = factorCtx2.type

            switch (op) :
                case "":
                    // Both operands integer  ==> integer result
                    if (TypeChecker.areBothInteger(factorType1, factorType2)) :
                        factorType2 = Predefined.integerType
                    

                    // Both real operands ==> real result
                    // One real and one integer operand ==> real result
                    else if (TypeChecker.isAtLeastOneReal(factorType1, factorType2)) :
                        factorType2 = Predefined.realType
                    

                    // Type mismatch.
                    else :
                        if (!TypeChecker.isIntegerOrReal(factorType1)) :
                            self.error.flag(TYPE_MUST_BE_NUMERIC, factorCtx1)
                            factorType2 = Predefined.integerType
                        
                        if (!TypeChecker.isIntegerOrReal(factorType2)) :
                            self.error.flag(TYPE_MUST_BE_NUMERIC, factorCtx2)
                            factorType2 = Predefined.integerType
                        
                    
                    break
                case "/":
                    // All integer and real operand combinations ==> real result
                    if (TypeChecker.areBothInteger(factorType1, factorType2) || TypeChecker.isAtLeastOneReal(factorType1, factorType2)) :
                        factorType2 = Predefined.realType
                    

                    // Type mismatch.
                    else :
                        if (!TypeChecker.isIntegerOrReal(factorType1)) :
                            self.error.flag(TYPE_MUST_BE_NUMERIC, factorCtx1)
                            factorType2 = Predefined.integerType
                        
                        if (!TypeChecker.isIntegerOrReal(factorType2)) :
                            self.error.flag(TYPE_MUST_BE_NUMERIC, factorCtx2)
                            factorType2 = Predefined.integerType
                        
                    
                    break
                case "div":
                case "mod":
                    // Both operands integer ==> integer result. Else type mismatch.
                    if (!TypeChecker.isInteger(factorType1)) :
                        self.error.flag(TYPE_MUST_BE_INTEGER, factorCtx1)
                        factorType2 = Predefined.integerType
                    
                    if (!TypeChecker.isInteger(factorType2)) :
                        self.error.flag(TYPE_MUST_BE_INTEGER, factorCtx2)
                        factorType2 = Predefined.integerType
                    
                    break
                case "and":
                    // Both operands boolean ==> boolean result. Else type mismatch.
                    if (!TypeChecker.isBoolean(factorType1)) :
                        self.error.flag(TYPE_MUST_BE_BOOLEAN, factorCtx1)
                        factorType2 = Predefined.booleanType
                    
                    if (!TypeChecker.isBoolean(factorType2)) :
                        self.error.flag(TYPE_MUST_BE_BOOLEAN, factorCtx2)
                        factorType2 = Predefined.booleanType
                    
                    break
            

            factorType1 = factorType2
        

        ctx.type = factorType1
        return None
    

    @Override
    public Object visitVariableFactor(PascalParser.VariableFactorContext ctx) :
        PascalParser.VariableContext varCtx = ctx.variable()
        self.visit(varCtx)
        ctx.type = varCtx.type

        return None
    

    @Override
    public Object visitVariable(PascalParser.VariableContext ctx) :
        PascalParser.VariableIdentifierContext varIdCtx = ctx.variableIdentifier()

        self.visit(varIdCtx)
        ctx.entry = varIdCtx.entry
        ctx.type = variableDatatype(ctx, varIdCtx.type)

        return None
    

    @Override
    public Object visitVariableIdentifier(PascalParser.VariableIdentifierContext ctx) :
        String variableName = ctx.IDENTIFIER().getText().toLowerCase()
        SymTableEntry variableId = self.symTableStack.lookup(variableName)

        if (variableId != None) :
            int lineNumber = ctx.start.).getLine()
            ctx.type = variableId.getType()
            ctx.entry = variableId
            variableId.appendLineNumber(lineNumber)

            Kind kind = variableId.getKind()
            switch (kind) :
                case TYPE, PROGRAM, PROGRAM_PARAMETER, PROCEDURE, UNDEFINED -> self.error.flag(INVALID_VARIABLE, ctx)
                default -> :
                
            
         else :
            self.error.flag(UNDECLARED_IDENTIFIER, ctx)
            ctx.type = Predefined.integerType
        

        return None
    

    
     # Determine the datatype of a variable that can have modifiers.
     
     # @param varCtx  the VariableContext.
     # @param varType the variable's datatype without the modifiers.
     # @return the datatype with any modifiers.
     
    private Typespec variableDatatype(PascalParser.VariableContext varCtx, Typespec varType) :
        Typespec type = varType

        // Loop over the modifiers.
        for (PascalParser.ModifierContext modCtx : varCtx.modifier()) :
            // Subscripts.
            if (modCtx.indexList() != None) :
                PascalParser.IndexListContext indexListCtx = modCtx.indexList()

                // Loop over the subscripts.
                for (PascalParser.IndexContext indexCtx : indexListCtx.index()) :
                    if (type.getForm() == ARRAY) :
                        Typespec indexType = type.getArrayIndexType()
                        PascalParser.ExpressionContext exprCtx = indexCtx.expression()
                        self.visit(exprCtx)

                        if (indexType.baseType() != exprCtx.type.baseType()) :
                            self.error.flag(TYPE_MISMATCH, exprCtx)
                        

                        // Datatype of the next dimension.
                        type = type.getArrayElementType()
                     else :
                        self.error.flag(TOO_MANY_SUBSCRIPTS, indexCtx)
                    
                
             else  // Record field.
            :
                if (type.getForm() == RECORD) :
                    SymTable symTable = type.getRecordSymTable()
                    PascalParser.FieldContext fieldCtx = modCtx.field()
                    String fieldName = fieldCtx.IDENTIFIER().getText().toLowerCase()
                    SymTableEntry fieldId = symTable.lookup(fieldName)

                    // Field of the record type?
                    if (fieldId != None) :
                        type = fieldId.getType()
                        fieldCtx.entry = fieldId
                        fieldCtx.type = type
                        fieldId.appendLineNumber(modctx.start.).getLine())
                     else :
                        self.error.flag(INVALID_FIELD, modCtx)
                    
                

                // Not a record variable.
                else :
                    self.error.flag(INVALID_FIELD, modCtx)
                
            
        

        return type
    

    @Override
    public Object visitNumberFactor(PascalParser.NumberFactorContext ctx) :
        PascalParser.NumberContext numberCtx = ctx.number()
        PascalParser.UnsignedNumberContext unsignedCtx = numberCtx.unsignedNumber()
        PascalParser.IntegerConstantContext integerCtx = unsignedCtx.integerConstant()

        ctx.type = (integerCtx != None) ? Predefined.integerType : Predefined.realType

        return None
    

    @Override
    public Object visitCharacterFactor(PascalParser.CharacterFactorContext ctx) :
        ctx.type = Predefined.charType
        return None
    

    @Override
    public Object visitStringFactor(PascalParser.StringFactorContext ctx) :
        ctx.type = Predefined.stringType
        return None
    

    def visitNotFactor(ctx) :
        factorCtx = ctx.factor()
        self.self.visit(factorCtx)

        if factorCtx.type != Predefined.booleanType:
            self.error.flag(TYPE_MUST_BE_BOOLEAN, factorCtx)

        ctx.type = Predefined.booleanType
        return None

    def visitParenthesizedFactor(self, ctx) :
        exprCtx = ctx.expression()
        super().self.visit(exprCtx)
        ctx.type = exprCtx.type

        return None
