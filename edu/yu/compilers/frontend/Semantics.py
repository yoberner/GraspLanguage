#  Semantic operations.
#  Perform type checking and create symbol tables.
import re

from gen.GraspParser import GraspParser
from gen.GraspVisitor import GraspVisitor
from edu.yu.compilers.frontend.SemanticErrorHandler import SemanticErrorHandler
from edu.yu.compilers.intermediate.symtable.Kind import Kind
from edu.yu.compilers.intermediate.symtable.Predefined import Predefined
from edu.yu.compilers.intermediate.symtable.Routine import Routine
from edu.yu.compilers.intermediate.symtable.SymTable import SymTable
from edu.yu.compilers.intermediate.symtable.SymTableStack import SymTableStack
from edu.yu.compilers.intermediate.type.Form import Form
from edu.yu.compilers.intermediate.type.TypeChecker import TypeChecker
from edu.yu.compilers.intermediate.type.Typespec import Typespec
from edu.yu.compilers.intermediate.util.BackendMode import BackendMode
from edu.yu.compilers.intermediate.util.CrossReferencer import CrossReferencer


class Semantics(GraspVisitor):

    def __init__(self, mode):
        # Create and initialize the symbol table stack.
        self.symTableStack = SymTableStack()
        Predefined.initialize(self.symTableStack)

        self.mode = mode
        self.error = SemanticErrorHandler()
        self.programId = None

    # Return the default value for a data type.
    #
    # @param type the data type.
    # @return the default value.

    # @staticmethod
    # def defaultValue(_type: Typespec):
    #     _type = _type.baseType()
    #
    #     if _type == Predefined.integerType:
    #         return 0
    #     elif _type == Predefined.realType:
    #         return 0.0
    #     elif _type == Predefined.booleanType:
    #         return False
    #     elif _type == Predefined.charType:
    #         return '#'
    #     else:
    #         return "#"

    def getProgramId(self):
        return self.programId

    def getErrorCount(self):
        return self.error.get_count()

    # def printSymbolTableStack(self):
    #     # Print the cross-reference table.
    #     crossReferencer = CrossReferencer()
    #     crossReferencer.printCrossRefTable(self.symTableStack)

    def visitProgram(self, ctx):
        self.visit(ctx.programHeader())
        self.visit(ctx.block().declarations())
        self.visit(ctx.block().compoundStatement())

        return None

    def visitProgramHeader(self, ctx):
        idCtx = ctx.programIdentifier()
        programName = idCtx.IDENTIFIER().getText()  # don't shift case

        self.programId = self.symTableStack.enterLocal(programName, Kind.PROGRAM)
        self.programId.setRoutineSymTable(self.symTableStack.push())

        self.symTableStack.setProgramId(self.programId)
        self.symTableStack.getLocalSymTable().setOwner(self.programId)

        idCtx.entry = self.programId
        return None

    def visitConstantDefinition(self, ctx):
        idCtx = ctx.constantIdentifier()
        constantName = idCtx.IDENTIFIER().getText().lower()
        constantId = self.symTableStack.lookupLocal(constantName)

        if constantId is None:
            constCtx = ctx.constant()
            constValue = self.visit(constCtx)

            constantId = self.symTableStack.enterLocal(constantName, Kind.CONSTANT)
            constantId.setValue(constValue)
            constantId.setType(constCtx.type_)

            idCtx.entry = constantId
            idCtx.type_ = constCtx.type_
        else:
            self.error.flag(SemanticErrorHandler.Code.REDECLARED_IDENTIFIER, ctx)  # TODO change this enum format

            idCtx.entry = constantId
            idCtx.type_ = Predefined.integerType

        constantId.appendLineNumber(ctx.start.line)
        return None

    def visitConstant(self, ctx):
        if ctx.IDENTIFIER() is not None:
            constantName = ctx.IDENTIFIER().getText().lower()
            constantId = self.symTableStack.lookup(constantName)

            if constantId is not None:
                kind = constantId.getKind()
                if (kind != Kind.CONSTANT) and (kind != Kind.ENUMERATION_CONSTANT):
                    self.error.flag(SemanticErrorHandler.Code.INVALID_CONSTANT, ctx)

                ctx.type_ = constantId.getType()
                ctx.value = constantId.getValue()

                constantId.appendLineNumber(ctx.start.line)
            else:
                self.error.flag(SemanticErrorHandler.Code.UNDECLARED_IDENTIFIER, ctx)

                ctx.type_ = Predefined.integerType
                ctx.value = 0

        elif ctx.characterConstant() is not None:
            ctx.type_ = Predefined.charType
            ctx.value = ctx.getText().charAt(1)
        elif ctx.stringConstant() is not None:
            graspString = ctx.stringConstant().STRING().getText()
            unquoted = graspString[1, graspString.length() - 1]
            ctx.type_ = Predefined.stringType
            ctx.value = unquoted.replace("''", "'").replace("\"", "\\\"")
        else:
            if ctx is not None:
                ctx.type_ = Predefined.integerType
                ctx.value = int(ctx.getText())
            else:
                ctx.type_ = Predefined.realType
                ctx.value = float(ctx.getText())

        return ctx.value

    def visitTypeDefinition(self, ctx: GraspParser.TypeDefinitionContext):
        idCtx = ctx.typeIdentifier()
        typeName = idCtx.IDENTIFIER().getText().lower()
        typeId = self.symTableStack.lookupLocal(typeName)

        typespecCtx = ctx.typeSpecification()

        # If it's a record type, create a named record type.
        if isinstance(typespecCtx, GraspParser.RecordTypespecContext):
            if self.symTableStack.lookupLocal(typeName) is None:
                typeId = self.createRecordType(typespecCtx, typeName)  # TODO ??? highilighted portion?
            else:
                self.error.flag(SemanticErrorHandler.Code.REDECLARED_IDENTIFIER, idCtx)

        # Enter the type name of any other type into the symbol table.
        elif typeId is None:
            self.visit(typespecCtx)

            typeId = self.symTableStack.enterLocal(typeName, Kind.TYPE)
            typeId.setType(typespecCtx.type_)
            typespecCtx.type_.setIdentifier(typeId.getName(), typeId.getSymTable())  # setIdentifier(typeId)
        # Redeclared identifier.
        else:
            self.error.flag(SemanticErrorHandler.Code.REDECLARED_IDENTIFIER, ctx)

        idCtx.entry = typeId
        idCtx.type_ = typespecCtx.type_

        typeId.appendLineNumber(ctx.start.line)
        return None

    def visitRecordTypespec(self, ctx: GraspParser.RecordTypespecContext):
        # Create an unnamed record type.
        recordTypeName = SymTable.generateUnnamedName()
        self.createRecordType(ctx, recordTypeName)  # FIXME ?

        return None

    # Create a new record type.

    # @param recordTypeSpecCtx the RecordTypespecContext.
    # @param recordTypeName    the name of the record type.
    # @return the symbol table entry of the record type identifier.

    def createRecordType(self, recordTypeSpecCtx, recordTypeName):
        recordTypeCtx = recordTypeSpecCtx.recordType()
        recordType = Typespec(Form.RECORD)

        recordTypeId = self.symTableStack.enterLocal(recordTypeName, Kind.TYPE)
        recordTypeId.setType(recordType)
        recordType.setIdentifier(recordTypeId.getName(), recordTypeId.getSymTable())

        recordTypePath = self.createRecordTypePath(recordType)
        recordType.setRecordTypePath(recordTypePath)

        # Enter the record fields into the record type's symbol table.
        recordSymTable = self.createRecordSymTable(recordTypeCtx.recordFields(), recordTypeId)
        recordType.setRecordSymTable(recordSymTable)

        recordTypeCtx.entry = recordTypeId
        recordTypeSpecCtx.type_ = recordType

        return recordTypeId

    # Create the fully qualified type pathname of a record type.

    # @param recordType the record type.
    # @return the pathname.

    def createRecordTypePath(self, recordType):
        parentId = recordType.getSymTab().getOwner()
        path = recordType.getName()

        while (parentId.getKind() == Kind.TYPE) and (parentId.getType().getForm() == Form.RECORD):
            path = parentId.getName() + "$" + path
            parentId = parentId.getSymTable().getOwner()

        path = parentId.getName() + "$" + path
        return path

    # Create the symbol table for a record type.

    # @param ctx     the RecordFieldsContext,
    # @param ownerId the symbol table entry of the owner's identifier.
    # @return the symbol table.

    def createRecordSymTable(self, ctx, ownerId):
        recordSymTable = self.symTableStack.push()

        recordSymTable.setOwner(ownerId)
        self.visit(ctx.variableDeclarationsList())
        recordSymTable.resetVariables(Kind.RECORD_FIELD)
        self.symTableStack._pop()

        return recordSymTable

    def visitSimpleTypespec(self, ctx):
        self.visit(ctx.simpleType())
        ctx.type_ = ctx.simpleType().type_

        return None

    def visitArrayElemType(self, ctx:GraspParser.ArrayElemTypeContext):
        self.visit(ctx.simpleType())
        ctx.type_ = ctx.simpleType().type_

        return None

    def visitTypeIdentifierTypespec(self, ctx):
        self.visit(ctx.typeIdentifier())
        ctx.type_ = ctx.typeIdentifier().type_

        return None

    def visitTypeIdentifier(self, ctx):
        typeName = ctx.IDENTIFIER().getText().lower()
        typeId = self.symTableStack.lookup(typeName)

        if typeId is not None:
            if typeId.getKind() != Kind.TYPE:
                self.error.flag(SemanticErrorHandler.Code.INVALID_TYPE, ctx)
                ctx.type_ = Predefined.integerType
            else:
                ctx.type_ = typeId.getType()

            typeId.appendLineNumber(ctx.start.line)
        else:
            self.error.flag(SemanticErrorHandler.Code.INVALID_TYPE, ctx)
            ctx.type_ = Predefined.integerType

        ctx.entry = typeId
        return None

    def visitEnumerationTypespec(self, ctx):
        enumType = Typespec(Form.ENUMERATION)
        constants = []
        value = -1

        # Loop over the enumeration constants.
        for constCtx in ctx.enumerationType().enumerationConstant():
            constIdCtx = constCtx.constantIdentifier()
            constantName = constIdCtx.IDENTIFIER().getText().lower()
            constantId = self.symTableStack.lookupLocal(constantName)

            if constantId is None:
                constantId = self.symTableStack.enterLocal(constantName, Kind.ENUMERATION_CONSTANT)
                constantId.setType(enumType)
                constantId.setValue(++value)

                constants.append(constantId)
            else:
                self.error.flag(SemanticErrorHandler.Code.REDECLARED_IDENTIFIER, constCtx)

            constIdCtx.entry = constantId
            constIdCtx.type_ = enumType

            constantId.appendLineNumber(ctx.start.line)

        enumType.setEnumerationConstants(constants)
        ctx.type_ = enumType

        return None

    def visitSubrangeTypespec(self, ctx):
        type = Typespec(Form.SUBRANGE)
        subCtx = ctx.subrangeType()
        minCtx = subCtx.constant()[0]
        maxCtx = subCtx.constant()[1]

        minObj = self.visit(minCtx)
        maxObj = self.visit(maxCtx)

        minType = minCtx.type_
        maxType = maxCtx.type_

        if ((minType.getForm() != Form.SCALAR) and (minType.getForm() != Form.ENUMERATION)) or (
                minType == Predefined.realType) or (minType == Predefined.stringType):
            self.error.flag(SemanticErrorHandler.Code.INVALID_CONSTANT, minCtx)
            minType = Predefined.integerType
            minObj = 0

        minValue = None
        maxValue = None

        if minType == Predefined.integerType:
            minValue = minObj
            maxValue = maxObj
        elif minType == Predefined.charType:
            minValue = minObj
            maxValue = maxObj
        else:  # enumeration constants
            minValue = minCtx.value
            maxValue = maxCtx.value

        if (maxType != minType) or (minValue > maxValue):
            self.error.flag(SemanticErrorHandler.Code.INVALID_CONSTANT, maxCtx)
            maxValue = minValue

        type.setSubrangeBaseType(minType)
        type.setSubrangeMinValue(minValue)
        type.setSubrangeMaxValue(maxValue)

        ctx.type_ = type
        return None

    def visitArrayTypespec(self, ctx):
        arrayType = Typespec(Form.ARRAY)
        arrayCtx = ctx.arrayType()
        listCtx = arrayCtx.arrayDimensionList()

        ctx.type_ = arrayType # arrayTypespec.type_

        # FIXME THIS CODE PORTION IS UNNECCESARY FOR OUR LANGUAGE - NO VARYING INDEX TYPES OR RANGES OF INDEX TYPE.
        # Loop over the array dimensions.
        count = len(listCtx.expression())  # simpleType().size()
        for i in range(0, count):
            exprCtx = listCtx.expression()[i]
            self.visit(exprCtx)
            arrayType.setArrayIndexType(Predefined.integerType)
            arrayType.setArrayElementCount(5) # TODO UNNACEPTABLE

            if i < count - 1:
                elementType = Typespec(Form.ARRAY)
                arrayType.setArrayElementType(elementType)
                arrayType = elementType
        #  ---------------------------------------------------------------------------------

        self.visit(arrayCtx.arrayElemType())
        elementType = arrayCtx.arrayElemType().type_  # arrayTypeSpec -> arrayType -> arrayElemType.type_
        arrayType.setArrayElementType(elementType)

        return None

    # Return the number of values in a datatype.

    # @param type the datatype.
    # @return the number of values.

    def typeCount(self, data_type):
        count = None

        if data_type.getForm() == Form.ENUMERATION:
            constants = data_type.getEnumerationConstants()
            count = constants.size()
        else:  # subrange
            minValue = data_type.getSubrangeMinValue()
            maxValue = data_type.getSubrangeMaxValue()
            count = maxValue - minValue + 1

        return count

    def visitVariableDeclarations(self, ctx):
        typeCtx = ctx.typeSpecification()
        self.visit(typeCtx)

        listCtx = ctx.variableIdentifierList()

        # Loop over the variables being declared.
        for idCtx in listCtx.variableIdentifier():
            lineNumber = idCtx.start.line
            variableName = idCtx.IDENTIFIER().getText().lower()
            pat = re.compile("[a-zA-Z][a-zA-Z0-9]*")
            if not pat.match(variableName):
                self.error.flag(SemanticErrorHandler.Code.INVALID_VARIABLE, ctx)
            variableId = self.symTableStack.lookupLocal(variableName)

            if variableId is None:
                variableId = self.symTableStack.enterLocal(variableName, Kind.VARIABLE)
                variableId.setType(typeCtx.type_)

                # Assign slot numbers to local variables.
                symTable = variableId.getSymTable()
                if symTable.getNestingLevel() > 1:
                    variableId.setSlotNumber(symTable.nextSlotNumber())

                idCtx.entry = variableId
            else:
                self.error.flag(SemanticErrorHandler.Code.REDECLARED_IDENTIFIER, ctx)

            variableId.appendLineNumber(lineNumber)

        return None

    def visitRoutineDefinition(self, ctx):
        funcCtx = ctx.functionHead()
        # procCtx = ctx.procedureHead() # we do not have procedures
        idCtx = None
        parameters = None
        functionDefinition = funcCtx is not None
        returnType = None

        if functionDefinition:
            idCtx = funcCtx.routineIdentifier()
            parameters = funcCtx.parameters()
        # else :
        #     idCtx = procCtx.routineIdentifier()
        #     parameters = procCtx.parameters()

        routineName = idCtx.IDENTIFIER().getText().lower()
        routineId = self.symTableStack.lookupLocal(routineName)

        if routineId is not None:
            self.error.flag(SemanticErrorHandler.Code.REDECLARED_IDENTIFIER, ctx.start.line, routineName)
            return None

        # this is an in line conditional in python - cool
        routineId = self.symTableStack.enterLocal(routineName, Kind.FUNCTION if functionDefinition else Kind.PROCEDURE)
        routineId.setRoutineCode(Routine.DECLARED)
        if funcCtx.FINAL() is not None:
            routineId.setImmutable(True)
        if self.symTableStack.getCurrentNestingLevel() > 1:
            routineId.setNested(True)
        idCtx.entry = routineId

        # Append to the parent routine's list of subroutines.
        parentId = self.symTableStack.getLocalSymTable().getOwner()
        parentId.appendSubroutine(routineId)

        routineId.setRoutineSymTable(self.symTableStack.push())
        idCtx.entry = routineId

        symTable = self.symTableStack.getLocalSymTable()
        symTable.setOwner(routineId)

        if parameters is not None:
            parameterIds = self.visit(parameters.parameterDeclarationsList())
            routineId.setRoutineParameters(parameterIds)

            for paramId in parameterIds:
                paramId.setSlotNumber(symTable.nextSlotNumber())

        if functionDefinition:
            typeIdCtx = funcCtx.typeIdentifier()
            self.visit(typeIdCtx)
            returnType = typeIdCtx.type_

            if returnType.getForm() != Form.SCALAR and returnType.getForm() != Form.ENUMERATION: #  TODO VOID?
                self.error.flag(SemanticErrorHandler.Code.INVALID_RETURN_TYPE, typeIdCtx)
                returnType = Predefined.integerType
            routineId.setType(returnType)
            idCtx.type_ = returnType
        else:
            idCtx.type_ = None

        self.visit(ctx.block().declarations())

        # Enter the function's associated variable into its symbol table.
        if functionDefinition:
            assocVarId = self.symTableStack.enterLocal(routineName, Kind.VARIABLE)
            assocVarId.setSlotNumber(symTable.nextSlotNumber())
            assocVarId.setType(returnType)
        functionStatements = ctx.block().compoundStatement().statementList().statement()
        if len(functionStatements) < 3:
            routineId.setInline(True)

        for stmt in functionStatements:
            if stmt.returnStatement() is not None:
                self.visit(stmt.returnStatement().expression())
                if stmt.returnStatement().expression().type_ != returnType:
                    self.error.flag(SemanticErrorHandler.Code.INVALID_RETURN_TYPE, funcCtx.typeIdentifier())
        self.visit(ctx.block().compoundStatement())
        routineId.setExecutable(ctx.block().compoundStatement())
        self.symTableStack._pop()
        return None

    def visitParameterDeclarationsList(self, ctx):
        parameterList = []

        # Loop over the parameter declarations.
        for dclCtx in ctx.parameterDeclaration():
            # parameterSublist = self.visit(dclCtx)
            # parameterList.extend(parameterSublist)
            parameter = self.visit(dclCtx)
            parameterList.append(parameter)

        return parameterList

    def visitParameterDeclaration(self, ctx):
        kind = Kind.REFERENCE_PARAMETER if (ctx.VAR() is not None) else Kind.VALUE_PARAMETER  # kind #already see a prob here
        typeCtx = ctx.typeIdentifier()

        self.visit(typeCtx)
        paramType = typeCtx.type_
        # we have type now we just need the id
        # parameterSublist = []
        param = ctx.parameterIdentifier()
        lineNumber = param.start.line
        paramName = param.IDENTIFIER().getText().lower()
        paramId = self.symTableStack.lookupLocal(paramName)

        if paramId is None:
            paramId = self.symTableStack.enterLocal(paramName, kind)
            paramId.setType(paramType)

            if (kind == Kind.REFERENCE_PARAMETER) and (self.mode != BackendMode.EXECUTOR) and (
                    paramType.getForm() == Form.SCALAR):
                self.error.flag(SemanticErrorHandler.Code.INVALID_REFERENCE_PARAMETER, param)

        else:
            self.error.flag(SemanticErrorHandler.Code.REDECLARED_IDENTIFIER, param)

        param.entry = paramId
        param.type_ = paramType

        paramId.appendLineNumber(lineNumber)

        return paramId

    # ? type checker converted?
    def visitAssignmentStatement(self, ctx: GraspParser.AssignmentStatementContext):
        lhsCtx = ctx.lhs()
        rhsCtx = ctx.rhs()

        self.visit(lhsCtx)  # TODO why not self.visitChildren()?
        self.visit(rhsCtx)

        lhsType = lhsCtx.type_
        rhsType = rhsCtx.expression().type_

        if not TypeChecker.areAssignmentCompatible(lhsType, rhsType):
            self.error.flag(SemanticErrorHandler.Code.INCOMPATIBLE_ASSIGNMENT, rhsCtx)

        return None

    # ? assuming visit defined
    def visitLhs(self, ctx):

        # if symTable.getNestingLevel() > 1:
        varCtx = ctx.variable()
        varST = self.symTableStack.lookup(varCtx.variableIdentifier().IDENTIFIER().getText().lower()).getSymTable()
        currentScope = self.symTableStack.getLocalSymTable().getOwner()
        if varST.getNestingLevel() <= 1 and currentScope.getKind() == Kind.FUNCTION and currentScope.isImmutable():
            self.error.flag(SemanticErrorHandler.Code.IMMUTABLE_FUNCTION, ctx)
        self.visit(varCtx)
        ctx.type_ = varCtx.type_

        return None

    def visitIfStatement(self, ctx):
        exprCtx = ctx.expression()
        trueCtx = ctx.trueStatement()
        falseCtx = ctx.falseStatement()

        self.visit(exprCtx)
        exprType = exprCtx.type_

        if not TypeChecker.isBoolean(exprType):
            self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_BOOLEAN, exprCtx)

        self.visit(trueCtx)
        if falseCtx is not None:
            self.visit(falseCtx)

        return None

    def visitCaseStatement(self, ctx):
        exprCtx = ctx.expression()
        self.visit(exprCtx)
        exprType = exprCtx.type_
        exprTypeForm = exprType.getForm()

        if (((exprTypeForm != Form.SCALAR) and (exprTypeForm != Form.ENUMERATION) and (
                exprTypeForm != Form.SUBRANGE)) or (exprType == Predefined.realType)):
            self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, exprCtx)
            exprType = Predefined.integerType

        constants = set()
        branchListCtx = ctx.caseBranchList()

        # Loop over the CASE branches.
        for branchCtx in branchListCtx.caseBranch():
            constListCtx = branchCtx.caseConstantList()
            stmtCtx = branchCtx.statement()

            if constListCtx is not None:
                # Loop over the CASE constants in each branch.
                for caseConstCtx in constListCtx.caseConstant():
                    constCtx = caseConstCtx.constant()
                    constValue = self.visit(constCtx)

                    caseConstCtx.type_ = constCtx.type_
                    caseConstCtx.value = None

                    if constCtx.type_ != exprType:
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, constCtx)

                    elif (constCtx.type_ == Predefined.integerType) or (
                            constCtx.type.getForm() == Form.ENUMERATION):  # TODO == same thing for enums in python? I think its good
                        caseConstCtx.value = int(constValue)
                    elif constCtx.type_ == Predefined.charType:
                        caseConstCtx.value = chr(constValue)
                    elif constCtx.type_ == Predefined.stringType:
                        caseConstCtx.value = str(constValue)

                    if caseConstCtx.value in constants:
                        self.error.flag(SemanticErrorHandler.Code.DUPLICATE_CASE_CONSTANT, constCtx)
                    else:
                        constants.append(caseConstCtx.value)  # TODO is it not append()?

            if stmtCtx is not None:
                self.visit(stmtCtx)

        return None

    def visitRepeatStatement(self, ctx):
        exprCtx = ctx.expression()
        self.visit(exprCtx)
        exprType = exprCtx.type_

        if not TypeChecker.isBoolean(exprType):
            self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_BOOLEAN, exprCtx)

        self.visit(ctx.statementList())
        return None

    def visitWhileStatement(self, ctx):
        exprCtx = ctx.expression()
        self.visit(exprCtx)
        exprType = exprCtx.type_

        if not TypeChecker.isBoolean(exprType):
            self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_BOOLEAN, exprCtx)

        self.visit(ctx.statement())
        return None

    def visitForStatement(self, ctx):
        varCtx = ctx.variable()
        self.visit(varCtx)

        controlName = varCtx.variableIdentifier().getText().lower()
        controlType = Predefined.integerType

        if varCtx.entry is not None:
            controlType = varCtx.type_

            if (controlType.getForm() != Form.SCALAR) or (controlType == Predefined.realType) or (
                    controlType == Predefined.stringType) or (len(varCtx.modifier()) != 0):
                self.error.flag(SemanticErrorHandler.Code.INVALID_CONTROL_VARIABLE, varCtx)
        else:
            self.error.flag(SemanticErrorHandler.Code.UNDECLARED_IDENTIFIER, ctx.start.line,
                            controlName)  # TODO getStart() or just start?

        startCtx = ctx.expression()[0]
        endCtx = ctx.expression()[1]

        self.visit(startCtx)
        self.visit(endCtx)

        if startCtx.type_ != controlType:
            self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, startCtx)
        if startCtx.type_ != endCtx.type_:
            pass
            # self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, endCtx)

        self.visit(ctx.statement())
        return None

    def visitProcedureCallStatement(self, ctx):
        nameCtx = ctx.procedureName()
        listCtx = ctx.argumentList()
        name = ctx.procedureName().getText().lower()
        procedureId = self.symTableStack.lookup(name)
        badName = False
        if procedureId is None:

            self.error.flag(SemanticErrorHandler.Code.UNDECLARED_IDENTIFIER, nameCtx)
            badName = True
        elif procedureId.getKind() != Kind.PROCEDURE:
            self.error.flag(SemanticErrorHandler.Code.NAME_MUST_BE_PROCEDURE, nameCtx)
            badName = True

        # Bad procedure name. Do a simple arguments check and then leave.

        if badName:
            for exprCtx in listCtx.argument():
                self.visit(exprCtx)

        # Good procedure name.

        else:
            params = procedureId.getRoutineParameters()
            self.checkCallArguments(listCtx, params)

        nameCtx.entry = procedureId
        return None

    def visitFunctionCallFactor(self, ctx):
        callCtx = ctx.functionCallStatement()
        nameCtx = callCtx.functionName()
        listCtx = callCtx.argumentList()
        name = callCtx.functionName().getText().lower()
        functionId = self.symTableStack.lookup(name)
        badName = False
        ctx.type_ = Predefined.integerType
        if functionId is None:
            self.error.flag(SemanticErrorHandler.Code.UNDECLARED_IDENTIFIER, nameCtx)
            badName = True
        elif functionId.getKind() != Kind.FUNCTION:
            self.error.flag(SemanticErrorHandler.Code.NAME_MUST_BE_FUNCTION, nameCtx)
            badName = True

        # Bad function name. Do a simple arguments check and then leave.

        if badName:
            for exprCtx in listCtx.argument():
                self.visit(exprCtx)

        # Good function name.

        else:
            parameters = functionId.getRoutineParameters()
            self.checkCallArguments(listCtx, parameters)

            ctx.type_ = functionId.getType()

        nameCtx.entry = functionId
        nameCtx.type_ = ctx.type_

        return None

    def checkCallArguments(self, listCtx, parameters):
        paramsCount = len(parameters)
        argsCount = len(listCtx.argument()) if listCtx is not None else 0

        if paramsCount != argsCount:
            self.error.flag(SemanticErrorHandler.Code.ARGUMENT_COUNT_MISMATCH, listCtx)
            return
        # Check each argument against the corresponding parameter.

        for i in range(paramsCount):
            argCtx = listCtx.argument()[i]

            exprCtx = argCtx.expression()
            self.visit(exprCtx)

            paramId = parameters[i]
            paramType = paramId.getType()
            argType = exprCtx.type_

            # For a VAR parameter, the argument must be a variable
            # with the same datatype.

            if paramId.getKind() == Kind.REFERENCE_PARAMETER:
                if self.expression_is_variable(exprCtx):
                    if paramType != argType:
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, exprCtx)
                else:
                    self.error.flag(SemanticErrorHandler.Code.ARGUMENT_MUST_BE_VARIABLE, exprCtx)

            # For a value parameter, the argument type must be
            # assignment compatible with the parameter type.

            elif not TypeChecker.areAssignmentCompatible(paramType, argType):
                if paramType == Predefined.realType:
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_NUMERIC, exprCtx)
                elif paramType == Predefined.integerType:
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_INTEGER, exprCtx)
                elif paramType == Predefined.booleanType:
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_BOOLEAN, exprCtx)
                elif paramType == Predefined.stringType:
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_STRING, exprCtx)
                else:
                    pass
                    # self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, exprCtx)

    def expression_is_variable(self, expr_ctx):
        # Only a single simple expression?
        if len(expr_ctx.simpleExpression()) == 1:
            simple_ctx = expr_ctx.simpleExpression(0)
            # Only a single term?
            if len(simple_ctx.term()) == 1:
                term_ctx = simple_ctx.term(0)

                # Only a single factor?
                if len(term_ctx.factor()) == 1:
                    return isinstance(term_ctx.factor(0), GraspParser.VariableFactorContext)

        return False

    def visitExpression(self, ctx):
        simpleCtx1 = ctx.simpleExpression()[0]

        # First simple expression.
        self.visit(simpleCtx1)

        simpleType1 = simpleCtx1.type_
        ctx.type_ = simpleType1

        relOpCtx = ctx.relOp()

        # Second simple expression?

        if relOpCtx is not None:
            simpleCtx2 = ctx.simpleExpression()[1]

            self.visit(simpleCtx2)
            simpleType2 = simpleCtx2.type_
            # # char int and dec operations are all possible
            # if simpleType1 == Predefined.booleanType and simpleType2 != Predefined.booleanType:
            #     self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH)
            # if simpleType2 == Predefined.booleanType and simpleType1 != Predefined.booleanType:
            #     self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH)
            # if simpleType1 == Predefined.stringType and simpleType2 != Predefined.stringType:
            #     self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH)
            # if simpleType2 == Predefined.stringType and simpleType1 != Predefined.stringType:
            #     self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH)

            if relOpCtx.getText() == '+' or relOpCtx.getText == '-' or relOpCtx.getText == '*' or relOpCtx.getText == '/':
                if not (simpleType1 == Predefined.integerType or simpleType1 == Predefined.realType or simpleType1 == Predefined.charType) :
                    self.error.flag(SemanticErrorHandler.Code.INVALID_OPERATOR, ctx)
                if not (simpleType2 == Predefined.integerType or simpleType2 == Predefined.realType or simpleType2 == Predefined.charType) :
                    self.error.flag(SemanticErrorHandler.Code.INVALID_OPERATOR, ctx)
            elif relOpCtx.getText() == 'AND'.lower() or relOpCtx.getText == 'OR'.lower():
                if simpleType1 != Predefined.booleanType:
                    self.error.flag(SemanticErrorHandler.Code.INVALID_OPERATOR, ctx)
                if simpleType2 != Predefined.booleanType:
                    self.error.flag(SemanticErrorHandler.Code.INVALID_OPERATOR, ctx)

            if not TypeChecker.areComparisonCompatible(simpleType1, simpleType2):
                self.error.flag(SemanticErrorHandler.Code.INCOMPATIBLE_COMPARISON, ctx)

            ctx.type_ = Predefined.booleanType

        return None

    def visitSimpleExpression(self, ctx):
        count = len(ctx.term())
        signCtx = ctx.sign()
        hasSign = signCtx is not None
        termCtx1 = ctx.term()[0]  # TODO Is this correct? is it not [0]

        if hasSign:
            sign = signCtx.getText()
            if (sign != "+") and (sign != "-"):
                self.error.flag(SemanticErrorHandler.Code.INVALID_SIGN, signCtx)

        # First term.
        self.visit(termCtx1)
        termType1 = termCtx1.type_

        # Loop over any subsequent terms.
        for i in range(1, count):
            op = ctx.addOp()[i - 1].getText().lower()  # TODO get?
            termCtx2 = ctx.term()[i]  # TODO get?
            self.visit(termCtx2)
            termType2 = termCtx2.type_

            # Both operands boolean ==> boolean result. Else type mismatch.
            if op == "or":
                if not TypeChecker.isBoolean(termType1):
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, termCtx1)

                if not TypeChecker.isBoolean(termType2):
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, termCtx2)

                if hasSign:
                    self.error.flag(SemanticErrorHandler.Code.INVALID_SIGN, signCtx)

                termType2 = Predefined.booleanType
            elif op == "+":
                # Both operands integer ==> integer result
                if TypeChecker.areBothInteger(termType1, termType2):
                    termType2 = Predefined.integerType


                # Both real operands ==> real result
                # One real and one integer operand ==> real result
                elif TypeChecker.isAtLeastOneReal(termType1, termType2):
                    termType2 = Predefined.realType


                # Both operands string ==> string result
                elif TypeChecker.areBothString(termType1, termType2):
                    if hasSign:
                        self.error.flag(SemanticErrorHandler.Code.INVALID_SIGN, signCtx)
                    termType2 = Predefined.stringType


                # Type mismatch.
                else:
                    if not TypeChecker.isIntegerOrReal(termType1):
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, termCtx1)
                        termType2 = Predefined.integerType

                    if not TypeChecker.isIntegerOrReal(termType2):
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, termCtx2)
                        termType2 = Predefined.integerType

            else:
                # Both operands integer ==> integer result
                if TypeChecker.areBothInteger(termType1, termType2):
                    termType2 = Predefined.integerType
                # Both real operands ==> real result
                # One real and one integer operand ==> real result
                elif TypeChecker.isAtLeastOneReal(termType1, termType2):
                    termType2 = Predefined.realType
                # Type mismatch.
                else:
                    if not TypeChecker.isIntegerOrReal(termType1):
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_NUMERIC, termCtx1)
                        termType2 = Predefined.integerType
                    if not TypeChecker.isIntegerOrReal(termType2):
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_NUMERIC, termCtx2)
                        termType2 = Predefined.integerType
            termType1 = termType2

        ctx.type_ = termType1
        return None

    def visitTerm(self, ctx):
        count = len(ctx.factor())
        factorCtx1 = ctx.factor()[0]

        # First factor.
        self.visit(factorCtx1)
        factorType1 = factorCtx1.type_

        # Loop over any subsequent factors.
        for i in range(1, count):
            op = ctx.mulOp()[i - 1].getText().lower()
            factorCtx2 = ctx.factor()[i]
            self.visit(factorCtx2)
            factorType2 = factorCtx2.type_

            if op == "*":
                # Both operands integer  ==> integer result
                if TypeChecker.areBothInteger(factorType1, factorType2):
                    factorType2 = Predefined.integerType
                    # Both real operands ==> real result
                # One real and one integer operand ==> real result
                elif TypeChecker.isAtLeastOneReal(factorType1, factorType2):
                    factorType2 = Predefined.realType
                    # Type mismatch.
                else:
                    if not TypeChecker.isIntegerOrReal(factorType1):
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, factorCtx1)
                        factorType2 = Predefined.integerType

                    if not TypeChecker.isIntegerOrReal(factorType2):
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, factorCtx2)
                        factorType2 = Predefined.integerType
            elif op == "/":
                # All integer and real operand combinations ==> real result
                if TypeChecker.areBothInteger(factorType1, factorType2) or TypeChecker.isAtLeastOneReal(factorType1,
                                                                                                        factorType2):
                    factorType2 = Predefined.realType
                    # Type mismatch.
                else:
                    if not TypeChecker.isIntegerOrReal(factorType1):
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, factorCtx1)
                        factorType2 = Predefined.integerType

                    if not TypeChecker.isIntegerOrReal(factorType2):
                        self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, factorCtx2)
                        factorType2 = Predefined.integerType
            elif op == "div" or op == "mod":
                # Both operands integer ==> integer result. Else type mismatch.
                if not TypeChecker.isInteger(factorType1):
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, factorCtx1)
                    factorType2 = Predefined.integerType

                if not TypeChecker.isInteger(factorType2):
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, factorCtx2)
                    factorType2 = Predefined.integerType
            elif op == "and":
                # Both operands boolean ==> boolean result. Else type mismatch.
                if not TypeChecker.isBoolean(factorType1):
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, factorCtx1)
                    factorType2 = Predefined.booleanType

                if not TypeChecker.isBoolean(factorType2):
                    self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, factorCtx2)
                    factorType2 = Predefined.booleanType

            factorType1 = factorType2

        ctx.type_ = factorType1
        return None

    def visitVariableFactor(self, ctx):
        varCtx = ctx.variable()

        self.visit(varCtx)
        ctx.type_ = varCtx.type_

        return None

    def visitVariable(self, ctx):

        varIdCtx = ctx.variableIdentifier()

        self.visit(varIdCtx)
        ctx.entry = varIdCtx.entry
        ctx.type_ = self.variableDatatype(ctx, varIdCtx.type_)

        return None

    def visitVariableIdentifier(self, ctx):
        variableName = ctx.IDENTIFIER().getText().lower()
        variableId = self.symTableStack.lookup(variableName)

        if variableId is not None:
            lineNumber = ctx.start.line

            ctx.type_ = variableId.getType()
            ctx.entry = variableId
            variableId.appendLineNumber(lineNumber)

            kind = variableId.getKind()
            if kind in [Kind.TYPE, Kind.PROGRAM, Kind.PROGRAM_PARAMETER, Kind.PROCEDURE, Kind.UNDEFINED]:
                self.error.flag(SemanticErrorHandler.Code.INVALID_VARIABLE, ctx)
        else:
            self.error.flag(SemanticErrorHandler.Code.UNDECLARED_IDENTIFIER, ctx)
            ctx.type_ = Predefined.integerType

        return None

    def variableDatatype(self, varCtx, varType):
        dataType = varType

        # Loop over the modifiers.
        for modCtx in varCtx.modifier():
            # Subscripts.
            if modCtx.indexList() is not None:
                indexListCtx = modCtx.indexList()

                # Loop over the subscripts.
                for indexCtx in indexListCtx.index():
                    if dataType.getForm() == Form.ARRAY:
                        indexType = dataType.getArrayIndexType()
                        exprCtx = indexCtx.expression()
                        self.visit(exprCtx)

                        if indexType.baseType() != exprCtx.type_.baseType():
                            self.error.flag(SemanticErrorHandler.Code.TYPE_MISMATCH, exprCtx)

                        # Datatype of the next dimension.
                        dataType = dataType.getArrayElementType()
                    else:
                        self.error.flag(SemanticErrorHandler.Code.TOO_MANY_SUBSCRIPTS, indexCtx)
            else:  # Record field.
                if dataType.getForm() == Form.RECORD:
                    symTable = dataType.getRecordSymTable()
                    fieldCtx = modCtx.field()
                    fieldName = fieldCtx.IDENTIFIER().getText().lower()
                    fieldId = symTable.lookup(fieldName)

                    # Field of the record type?
                    if fieldId is not None:

                        dataType = fieldId.getType()
                        fieldCtx.entry = fieldId
                        fieldCtx.type_ = dataType
                        fieldId.appendLineNumber(modCtx.start.line)
                    else:
                        self.error.flag(SemanticErrorHandler.Code.INVALID_FIELD, modCtx)

                # Not a record variable.

                else:
                    self.error.flag(SemanticErrorHandler.Code.INVALID_FIELD, modCtx)

        return dataType

    def visitNumberFactor(self, ctx):

        numberCtx = ctx.number()
        unsignedCtx = numberCtx.unsignedNumber()
        integerCtx = unsignedCtx.integerConstant()

        ctx.type_ = Predefined.integerType if integerCtx is not None else Predefined.realType

        return None

    def visitCharacterFactor(self, ctx):

        ctx.type_ = Predefined.charType
        return None

    def visitStringFactor(self, ctx):

        ctx.type_ = Predefined.stringType
        return None

    def visitNotFactor(self, ctx):
        factorCtx = ctx.factor()
        self.visit(factorCtx)

        if factorCtx.type_ != Predefined.booleanType:
            self.error.flag(SemanticErrorHandler.Code.TYPE_MUST_BE_BOOLEAN, factorCtx)

        ctx.type_ = Predefined.booleanType
        return None

    def visitParenthesizedFactor(self, ctx):
        exprCtx = ctx.expression()
        self.visit(exprCtx)
        ctx.type_ = exprCtx.type_

        return None
