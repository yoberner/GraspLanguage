# Generated from C:/Users/mitch/CS_CLASSES_AND_PROJECTS/LanguageProject/GraspLanguage/antlr\Grasp.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GraspParser import GraspParser
else:
    from GraspParser import GraspParser

    # package antlr4
    # import java.util.HashMap
    # import edu.yu.compilers.intermediate.symtable.SymTableEntry
    # import edu.yu.compilers.intermediate.type.Typespec


# This class defines a complete listener for a parse tree produced by GraspParser.
class GraspListener(ParseTreeListener):

    # Enter a parse tree produced by GraspParser#program.
    def enterProgram(self, ctx:GraspParser.ProgramContext):
        pass

    # Exit a parse tree produced by GraspParser#program.
    def exitProgram(self, ctx:GraspParser.ProgramContext):
        pass


    # Enter a parse tree produced by GraspParser#programHeader.
    def enterProgramHeader(self, ctx:GraspParser.ProgramHeaderContext):
        pass

    # Exit a parse tree produced by GraspParser#programHeader.
    def exitProgramHeader(self, ctx:GraspParser.ProgramHeaderContext):
        pass


    # Enter a parse tree produced by GraspParser#programParameters.
    def enterProgramParameters(self, ctx:GraspParser.ProgramParametersContext):
        pass

    # Exit a parse tree produced by GraspParser#programParameters.
    def exitProgramParameters(self, ctx:GraspParser.ProgramParametersContext):
        pass


    # Enter a parse tree produced by GraspParser#programIdentifier.
    def enterProgramIdentifier(self, ctx:GraspParser.ProgramIdentifierContext):
        pass

    # Exit a parse tree produced by GraspParser#programIdentifier.
    def exitProgramIdentifier(self, ctx:GraspParser.ProgramIdentifierContext):
        pass


    # Enter a parse tree produced by GraspParser#block.
    def enterBlock(self, ctx:GraspParser.BlockContext):
        pass

    # Exit a parse tree produced by GraspParser#block.
    def exitBlock(self, ctx:GraspParser.BlockContext):
        pass


    # Enter a parse tree produced by GraspParser#declarations.
    def enterDeclarations(self, ctx:GraspParser.DeclarationsContext):
        pass

    # Exit a parse tree produced by GraspParser#declarations.
    def exitDeclarations(self, ctx:GraspParser.DeclarationsContext):
        pass


    # Enter a parse tree produced by GraspParser#constantsPart.
    def enterConstantsPart(self, ctx:GraspParser.ConstantsPartContext):
        pass

    # Exit a parse tree produced by GraspParser#constantsPart.
    def exitConstantsPart(self, ctx:GraspParser.ConstantsPartContext):
        pass


    # Enter a parse tree produced by GraspParser#constantDefinitionsList.
    def enterConstantDefinitionsList(self, ctx:GraspParser.ConstantDefinitionsListContext):
        pass

    # Exit a parse tree produced by GraspParser#constantDefinitionsList.
    def exitConstantDefinitionsList(self, ctx:GraspParser.ConstantDefinitionsListContext):
        pass


    # Enter a parse tree produced by GraspParser#constantDefinition.
    def enterConstantDefinition(self, ctx:GraspParser.ConstantDefinitionContext):
        pass

    # Exit a parse tree produced by GraspParser#constantDefinition.
    def exitConstantDefinition(self, ctx:GraspParser.ConstantDefinitionContext):
        pass


    # Enter a parse tree produced by GraspParser#constantIdentifier.
    def enterConstantIdentifier(self, ctx:GraspParser.ConstantIdentifierContext):
        pass

    # Exit a parse tree produced by GraspParser#constantIdentifier.
    def exitConstantIdentifier(self, ctx:GraspParser.ConstantIdentifierContext):
        pass


    # Enter a parse tree produced by GraspParser#constant.
    def enterConstant(self, ctx:GraspParser.ConstantContext):
        pass

    # Exit a parse tree produced by GraspParser#constant.
    def exitConstant(self, ctx:GraspParser.ConstantContext):
        pass


    # Enter a parse tree produced by GraspParser#sign.
    def enterSign(self, ctx:GraspParser.SignContext):
        pass

    # Exit a parse tree produced by GraspParser#sign.
    def exitSign(self, ctx:GraspParser.SignContext):
        pass


    # Enter a parse tree produced by GraspParser#typesPart.
    def enterTypesPart(self, ctx:GraspParser.TypesPartContext):
        pass

    # Exit a parse tree produced by GraspParser#typesPart.
    def exitTypesPart(self, ctx:GraspParser.TypesPartContext):
        pass


    # Enter a parse tree produced by GraspParser#typeDefinitionsList.
    def enterTypeDefinitionsList(self, ctx:GraspParser.TypeDefinitionsListContext):
        pass

    # Exit a parse tree produced by GraspParser#typeDefinitionsList.
    def exitTypeDefinitionsList(self, ctx:GraspParser.TypeDefinitionsListContext):
        pass


    # Enter a parse tree produced by GraspParser#typeDefinition.
    def enterTypeDefinition(self, ctx:GraspParser.TypeDefinitionContext):
        pass

    # Exit a parse tree produced by GraspParser#typeDefinition.
    def exitTypeDefinition(self, ctx:GraspParser.TypeDefinitionContext):
        pass


    # Enter a parse tree produced by GraspParser#typeIdentifier.
    def enterTypeIdentifier(self, ctx:GraspParser.TypeIdentifierContext):
        pass

    # Exit a parse tree produced by GraspParser#typeIdentifier.
    def exitTypeIdentifier(self, ctx:GraspParser.TypeIdentifierContext):
        pass


    # Enter a parse tree produced by GraspParser#simpleTypespec.
    def enterSimpleTypespec(self, ctx:GraspParser.SimpleTypespecContext):
        pass

    # Exit a parse tree produced by GraspParser#simpleTypespec.
    def exitSimpleTypespec(self, ctx:GraspParser.SimpleTypespecContext):
        pass


    # Enter a parse tree produced by GraspParser#arrayTypespec.
    def enterArrayTypespec(self, ctx:GraspParser.ArrayTypespecContext):
        pass

    # Exit a parse tree produced by GraspParser#arrayTypespec.
    def exitArrayTypespec(self, ctx:GraspParser.ArrayTypespecContext):
        pass


    # Enter a parse tree produced by GraspParser#recordTypespec.
    def enterRecordTypespec(self, ctx:GraspParser.RecordTypespecContext):
        pass

    # Exit a parse tree produced by GraspParser#recordTypespec.
    def exitRecordTypespec(self, ctx:GraspParser.RecordTypespecContext):
        pass


    # Enter a parse tree produced by GraspParser#typeIdentifierTypespec.
    def enterTypeIdentifierTypespec(self, ctx:GraspParser.TypeIdentifierTypespecContext):
        pass

    # Exit a parse tree produced by GraspParser#typeIdentifierTypespec.
    def exitTypeIdentifierTypespec(self, ctx:GraspParser.TypeIdentifierTypespecContext):
        pass


    # Enter a parse tree produced by GraspParser#enumerationTypespec.
    def enterEnumerationTypespec(self, ctx:GraspParser.EnumerationTypespecContext):
        pass

    # Exit a parse tree produced by GraspParser#enumerationTypespec.
    def exitEnumerationTypespec(self, ctx:GraspParser.EnumerationTypespecContext):
        pass


    # Enter a parse tree produced by GraspParser#enumerationType.
    def enterEnumerationType(self, ctx:GraspParser.EnumerationTypeContext):
        pass

    # Exit a parse tree produced by GraspParser#enumerationType.
    def exitEnumerationType(self, ctx:GraspParser.EnumerationTypeContext):
        pass


    # Enter a parse tree produced by GraspParser#enumerationConstant.
    def enterEnumerationConstant(self, ctx:GraspParser.EnumerationConstantContext):
        pass

    # Exit a parse tree produced by GraspParser#enumerationConstant.
    def exitEnumerationConstant(self, ctx:GraspParser.EnumerationConstantContext):
        pass


    # Enter a parse tree produced by GraspParser#arrayType.
    def enterArrayType(self, ctx:GraspParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by GraspParser#arrayType.
    def exitArrayType(self, ctx:GraspParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by GraspParser#arrayElemType.
    def enterArrayElemType(self, ctx:GraspParser.ArrayElemTypeContext):
        pass

    # Exit a parse tree produced by GraspParser#arrayElemType.
    def exitArrayElemType(self, ctx:GraspParser.ArrayElemTypeContext):
        pass


    # Enter a parse tree produced by GraspParser#arrayDimensionList.
    def enterArrayDimensionList(self, ctx:GraspParser.ArrayDimensionListContext):
        pass

    # Exit a parse tree produced by GraspParser#arrayDimensionList.
    def exitArrayDimensionList(self, ctx:GraspParser.ArrayDimensionListContext):
        pass


    # Enter a parse tree produced by GraspParser#recordType.
    def enterRecordType(self, ctx:GraspParser.RecordTypeContext):
        pass

    # Exit a parse tree produced by GraspParser#recordType.
    def exitRecordType(self, ctx:GraspParser.RecordTypeContext):
        pass


    # Enter a parse tree produced by GraspParser#recordFields.
    def enterRecordFields(self, ctx:GraspParser.RecordFieldsContext):
        pass

    # Exit a parse tree produced by GraspParser#recordFields.
    def exitRecordFields(self, ctx:GraspParser.RecordFieldsContext):
        pass


    # Enter a parse tree produced by GraspParser#variablesPart.
    def enterVariablesPart(self, ctx:GraspParser.VariablesPartContext):
        pass

    # Exit a parse tree produced by GraspParser#variablesPart.
    def exitVariablesPart(self, ctx:GraspParser.VariablesPartContext):
        pass


    # Enter a parse tree produced by GraspParser#variableDeclarationsList.
    def enterVariableDeclarationsList(self, ctx:GraspParser.VariableDeclarationsListContext):
        pass

    # Exit a parse tree produced by GraspParser#variableDeclarationsList.
    def exitVariableDeclarationsList(self, ctx:GraspParser.VariableDeclarationsListContext):
        pass


    # Enter a parse tree produced by GraspParser#variableDeclarations.
    def enterVariableDeclarations(self, ctx:GraspParser.VariableDeclarationsContext):
        pass

    # Exit a parse tree produced by GraspParser#variableDeclarations.
    def exitVariableDeclarations(self, ctx:GraspParser.VariableDeclarationsContext):
        pass


    # Enter a parse tree produced by GraspParser#variableIdentifierList.
    def enterVariableIdentifierList(self, ctx:GraspParser.VariableIdentifierListContext):
        pass

    # Exit a parse tree produced by GraspParser#variableIdentifierList.
    def exitVariableIdentifierList(self, ctx:GraspParser.VariableIdentifierListContext):
        pass


    # Enter a parse tree produced by GraspParser#variableIdentifier.
    def enterVariableIdentifier(self, ctx:GraspParser.VariableIdentifierContext):
        pass

    # Exit a parse tree produced by GraspParser#variableIdentifier.
    def exitVariableIdentifier(self, ctx:GraspParser.VariableIdentifierContext):
        pass


    # Enter a parse tree produced by GraspParser#routinesPart.
    def enterRoutinesPart(self, ctx:GraspParser.RoutinesPartContext):
        pass

    # Exit a parse tree produced by GraspParser#routinesPart.
    def exitRoutinesPart(self, ctx:GraspParser.RoutinesPartContext):
        pass


    # Enter a parse tree produced by GraspParser#routineDefinition.
    def enterRoutineDefinition(self, ctx:GraspParser.RoutineDefinitionContext):
        pass

    # Exit a parse tree produced by GraspParser#routineDefinition.
    def exitRoutineDefinition(self, ctx:GraspParser.RoutineDefinitionContext):
        pass


    # Enter a parse tree produced by GraspParser#functionHead.
    def enterFunctionHead(self, ctx:GraspParser.FunctionHeadContext):
        pass

    # Exit a parse tree produced by GraspParser#functionHead.
    def exitFunctionHead(self, ctx:GraspParser.FunctionHeadContext):
        pass


    # Enter a parse tree produced by GraspParser#routineIdentifier.
    def enterRoutineIdentifier(self, ctx:GraspParser.RoutineIdentifierContext):
        pass

    # Exit a parse tree produced by GraspParser#routineIdentifier.
    def exitRoutineIdentifier(self, ctx:GraspParser.RoutineIdentifierContext):
        pass


    # Enter a parse tree produced by GraspParser#parameters.
    def enterParameters(self, ctx:GraspParser.ParametersContext):
        pass

    # Exit a parse tree produced by GraspParser#parameters.
    def exitParameters(self, ctx:GraspParser.ParametersContext):
        pass


    # Enter a parse tree produced by GraspParser#parameterDeclarationsList.
    def enterParameterDeclarationsList(self, ctx:GraspParser.ParameterDeclarationsListContext):
        pass

    # Exit a parse tree produced by GraspParser#parameterDeclarationsList.
    def exitParameterDeclarationsList(self, ctx:GraspParser.ParameterDeclarationsListContext):
        pass


    # Enter a parse tree produced by GraspParser#parameterDeclaration.
    def enterParameterDeclaration(self, ctx:GraspParser.ParameterDeclarationContext):
        pass

    # Exit a parse tree produced by GraspParser#parameterDeclaration.
    def exitParameterDeclaration(self, ctx:GraspParser.ParameterDeclarationContext):
        pass


    # Enter a parse tree produced by GraspParser#paramTypeMod.
    def enterParamTypeMod(self, ctx:GraspParser.ParamTypeModContext):
        pass

    # Exit a parse tree produced by GraspParser#paramTypeMod.
    def exitParamTypeMod(self, ctx:GraspParser.ParamTypeModContext):
        pass


    # Enter a parse tree produced by GraspParser#parameterIdentifier.
    def enterParameterIdentifier(self, ctx:GraspParser.ParameterIdentifierContext):
        pass

    # Exit a parse tree produced by GraspParser#parameterIdentifier.
    def exitParameterIdentifier(self, ctx:GraspParser.ParameterIdentifierContext):
        pass


    # Enter a parse tree produced by GraspParser#statement.
    def enterStatement(self, ctx:GraspParser.StatementContext):
        pass

    # Exit a parse tree produced by GraspParser#statement.
    def exitStatement(self, ctx:GraspParser.StatementContext):
        pass


    # Enter a parse tree produced by GraspParser#compoundStatement.
    def enterCompoundStatement(self, ctx:GraspParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#compoundStatement.
    def exitCompoundStatement(self, ctx:GraspParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#emptyStatement.
    def enterEmptyStatement(self, ctx:GraspParser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#emptyStatement.
    def exitEmptyStatement(self, ctx:GraspParser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#statementList.
    def enterStatementList(self, ctx:GraspParser.StatementListContext):
        pass

    # Exit a parse tree produced by GraspParser#statementList.
    def exitStatementList(self, ctx:GraspParser.StatementListContext):
        pass


    # Enter a parse tree produced by GraspParser#declareAndAssignStatement.
    def enterDeclareAndAssignStatement(self, ctx:GraspParser.DeclareAndAssignStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#declareAndAssignStatement.
    def exitDeclareAndAssignStatement(self, ctx:GraspParser.DeclareAndAssignStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:GraspParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:GraspParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#returnStatement.
    def enterReturnStatement(self, ctx:GraspParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#returnStatement.
    def exitReturnStatement(self, ctx:GraspParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#lhs.
    def enterLhs(self, ctx:GraspParser.LhsContext):
        pass

    # Exit a parse tree produced by GraspParser#lhs.
    def exitLhs(self, ctx:GraspParser.LhsContext):
        pass


    # Enter a parse tree produced by GraspParser#rhs.
    def enterRhs(self, ctx:GraspParser.RhsContext):
        pass

    # Exit a parse tree produced by GraspParser#rhs.
    def exitRhs(self, ctx:GraspParser.RhsContext):
        pass


    # Enter a parse tree produced by GraspParser#ifStatement.
    def enterIfStatement(self, ctx:GraspParser.IfStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#ifStatement.
    def exitIfStatement(self, ctx:GraspParser.IfStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#trueStatement.
    def enterTrueStatement(self, ctx:GraspParser.TrueStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#trueStatement.
    def exitTrueStatement(self, ctx:GraspParser.TrueStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#falseStatement.
    def enterFalseStatement(self, ctx:GraspParser.FalseStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#falseStatement.
    def exitFalseStatement(self, ctx:GraspParser.FalseStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#caseStatement.
    def enterCaseStatement(self, ctx:GraspParser.CaseStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#caseStatement.
    def exitCaseStatement(self, ctx:GraspParser.CaseStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#caseBranchList.
    def enterCaseBranchList(self, ctx:GraspParser.CaseBranchListContext):
        pass

    # Exit a parse tree produced by GraspParser#caseBranchList.
    def exitCaseBranchList(self, ctx:GraspParser.CaseBranchListContext):
        pass


    # Enter a parse tree produced by GraspParser#caseBranch.
    def enterCaseBranch(self, ctx:GraspParser.CaseBranchContext):
        pass

    # Exit a parse tree produced by GraspParser#caseBranch.
    def exitCaseBranch(self, ctx:GraspParser.CaseBranchContext):
        pass


    # Enter a parse tree produced by GraspParser#caseConstantList.
    def enterCaseConstantList(self, ctx:GraspParser.CaseConstantListContext):
        pass

    # Exit a parse tree produced by GraspParser#caseConstantList.
    def exitCaseConstantList(self, ctx:GraspParser.CaseConstantListContext):
        pass


    # Enter a parse tree produced by GraspParser#caseConstant.
    def enterCaseConstant(self, ctx:GraspParser.CaseConstantContext):
        pass

    # Exit a parse tree produced by GraspParser#caseConstant.
    def exitCaseConstant(self, ctx:GraspParser.CaseConstantContext):
        pass


    # Enter a parse tree produced by GraspParser#whileStatement.
    def enterWhileStatement(self, ctx:GraspParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#whileStatement.
    def exitWhileStatement(self, ctx:GraspParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#forStatement.
    def enterForStatement(self, ctx:GraspParser.ForStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#forStatement.
    def exitForStatement(self, ctx:GraspParser.ForStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#doStatement.
    def enterDoStatement(self, ctx:GraspParser.DoStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#doStatement.
    def exitDoStatement(self, ctx:GraspParser.DoStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#argumentList.
    def enterArgumentList(self, ctx:GraspParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by GraspParser#argumentList.
    def exitArgumentList(self, ctx:GraspParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by GraspParser#argument.
    def enterArgument(self, ctx:GraspParser.ArgumentContext):
        pass

    # Exit a parse tree produced by GraspParser#argument.
    def exitArgument(self, ctx:GraspParser.ArgumentContext):
        pass


    # Enter a parse tree produced by GraspParser#printStatement.
    def enterPrintStatement(self, ctx:GraspParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#printStatement.
    def exitPrintStatement(self, ctx:GraspParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#printlnStatement.
    def enterPrintlnStatement(self, ctx:GraspParser.PrintlnStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#printlnStatement.
    def exitPrintlnStatement(self, ctx:GraspParser.PrintlnStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#writeArguments.
    def enterWriteArguments(self, ctx:GraspParser.WriteArgumentsContext):
        pass

    # Exit a parse tree produced by GraspParser#writeArguments.
    def exitWriteArguments(self, ctx:GraspParser.WriteArgumentsContext):
        pass


    # Enter a parse tree produced by GraspParser#writeArgument.
    def enterWriteArgument(self, ctx:GraspParser.WriteArgumentContext):
        pass

    # Exit a parse tree produced by GraspParser#writeArgument.
    def exitWriteArgument(self, ctx:GraspParser.WriteArgumentContext):
        pass


    # Enter a parse tree produced by GraspParser#fieldWidth.
    def enterFieldWidth(self, ctx:GraspParser.FieldWidthContext):
        pass

    # Exit a parse tree produced by GraspParser#fieldWidth.
    def exitFieldWidth(self, ctx:GraspParser.FieldWidthContext):
        pass


    # Enter a parse tree produced by GraspParser#decimalPlaces.
    def enterDecimalPlaces(self, ctx:GraspParser.DecimalPlacesContext):
        pass

    # Exit a parse tree produced by GraspParser#decimalPlaces.
    def exitDecimalPlaces(self, ctx:GraspParser.DecimalPlacesContext):
        pass


    # Enter a parse tree produced by GraspParser#readStatement.
    def enterReadStatement(self, ctx:GraspParser.ReadStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#readStatement.
    def exitReadStatement(self, ctx:GraspParser.ReadStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#readlnStatement.
    def enterReadlnStatement(self, ctx:GraspParser.ReadlnStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#readlnStatement.
    def exitReadlnStatement(self, ctx:GraspParser.ReadlnStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#readArguments.
    def enterReadArguments(self, ctx:GraspParser.ReadArgumentsContext):
        pass

    # Exit a parse tree produced by GraspParser#readArguments.
    def exitReadArguments(self, ctx:GraspParser.ReadArgumentsContext):
        pass


    # Enter a parse tree produced by GraspParser#expression.
    def enterExpression(self, ctx:GraspParser.ExpressionContext):
        pass

    # Exit a parse tree produced by GraspParser#expression.
    def exitExpression(self, ctx:GraspParser.ExpressionContext):
        pass


    # Enter a parse tree produced by GraspParser#simpleExpression.
    def enterSimpleExpression(self, ctx:GraspParser.SimpleExpressionContext):
        pass

    # Exit a parse tree produced by GraspParser#simpleExpression.
    def exitSimpleExpression(self, ctx:GraspParser.SimpleExpressionContext):
        pass


    # Enter a parse tree produced by GraspParser#term.
    def enterTerm(self, ctx:GraspParser.TermContext):
        pass

    # Exit a parse tree produced by GraspParser#term.
    def exitTerm(self, ctx:GraspParser.TermContext):
        pass


    # Enter a parse tree produced by GraspParser#variableFactor.
    def enterVariableFactor(self, ctx:GraspParser.VariableFactorContext):
        pass

    # Exit a parse tree produced by GraspParser#variableFactor.
    def exitVariableFactor(self, ctx:GraspParser.VariableFactorContext):
        pass


    # Enter a parse tree produced by GraspParser#numberFactor.
    def enterNumberFactor(self, ctx:GraspParser.NumberFactorContext):
        pass

    # Exit a parse tree produced by GraspParser#numberFactor.
    def exitNumberFactor(self, ctx:GraspParser.NumberFactorContext):
        pass


    # Enter a parse tree produced by GraspParser#characterFactor.
    def enterCharacterFactor(self, ctx:GraspParser.CharacterFactorContext):
        pass

    # Exit a parse tree produced by GraspParser#characterFactor.
    def exitCharacterFactor(self, ctx:GraspParser.CharacterFactorContext):
        pass


    # Enter a parse tree produced by GraspParser#stringFactor.
    def enterStringFactor(self, ctx:GraspParser.StringFactorContext):
        pass

    # Exit a parse tree produced by GraspParser#stringFactor.
    def exitStringFactor(self, ctx:GraspParser.StringFactorContext):
        pass


    # Enter a parse tree produced by GraspParser#functionCallFactor.
    def enterFunctionCallFactor(self, ctx:GraspParser.FunctionCallFactorContext):
        pass

    # Exit a parse tree produced by GraspParser#functionCallFactor.
    def exitFunctionCallFactor(self, ctx:GraspParser.FunctionCallFactorContext):
        pass


    # Enter a parse tree produced by GraspParser#notFactor.
    def enterNotFactor(self, ctx:GraspParser.NotFactorContext):
        pass

    # Exit a parse tree produced by GraspParser#notFactor.
    def exitNotFactor(self, ctx:GraspParser.NotFactorContext):
        pass


    # Enter a parse tree produced by GraspParser#parenthesizedFactor.
    def enterParenthesizedFactor(self, ctx:GraspParser.ParenthesizedFactorContext):
        pass

    # Exit a parse tree produced by GraspParser#parenthesizedFactor.
    def exitParenthesizedFactor(self, ctx:GraspParser.ParenthesizedFactorContext):
        pass


    # Enter a parse tree produced by GraspParser#variable.
    def enterVariable(self, ctx:GraspParser.VariableContext):
        pass

    # Exit a parse tree produced by GraspParser#variable.
    def exitVariable(self, ctx:GraspParser.VariableContext):
        pass


    # Enter a parse tree produced by GraspParser#modifier.
    def enterModifier(self, ctx:GraspParser.ModifierContext):
        pass

    # Exit a parse tree produced by GraspParser#modifier.
    def exitModifier(self, ctx:GraspParser.ModifierContext):
        pass


    # Enter a parse tree produced by GraspParser#indexList.
    def enterIndexList(self, ctx:GraspParser.IndexListContext):
        pass

    # Exit a parse tree produced by GraspParser#indexList.
    def exitIndexList(self, ctx:GraspParser.IndexListContext):
        pass


    # Enter a parse tree produced by GraspParser#index.
    def enterIndex(self, ctx:GraspParser.IndexContext):
        pass

    # Exit a parse tree produced by GraspParser#index.
    def exitIndex(self, ctx:GraspParser.IndexContext):
        pass


    # Enter a parse tree produced by GraspParser#field.
    def enterField(self, ctx:GraspParser.FieldContext):
        pass

    # Exit a parse tree produced by GraspParser#field.
    def exitField(self, ctx:GraspParser.FieldContext):
        pass


    # Enter a parse tree produced by GraspParser#functionCallStatement.
    def enterFunctionCallStatement(self, ctx:GraspParser.FunctionCallStatementContext):
        pass

    # Exit a parse tree produced by GraspParser#functionCallStatement.
    def exitFunctionCallStatement(self, ctx:GraspParser.FunctionCallStatementContext):
        pass


    # Enter a parse tree produced by GraspParser#functionName.
    def enterFunctionName(self, ctx:GraspParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by GraspParser#functionName.
    def exitFunctionName(self, ctx:GraspParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by GraspParser#number.
    def enterNumber(self, ctx:GraspParser.NumberContext):
        pass

    # Exit a parse tree produced by GraspParser#number.
    def exitNumber(self, ctx:GraspParser.NumberContext):
        pass


    # Enter a parse tree produced by GraspParser#unsignedNumber.
    def enterUnsignedNumber(self, ctx:GraspParser.UnsignedNumberContext):
        pass

    # Exit a parse tree produced by GraspParser#unsignedNumber.
    def exitUnsignedNumber(self, ctx:GraspParser.UnsignedNumberContext):
        pass


    # Enter a parse tree produced by GraspParser#integerConstant.
    def enterIntegerConstant(self, ctx:GraspParser.IntegerConstantContext):
        pass

    # Exit a parse tree produced by GraspParser#integerConstant.
    def exitIntegerConstant(self, ctx:GraspParser.IntegerConstantContext):
        pass


    # Enter a parse tree produced by GraspParser#decConstant.
    def enterDecConstant(self, ctx:GraspParser.DecConstantContext):
        pass

    # Exit a parse tree produced by GraspParser#decConstant.
    def exitDecConstant(self, ctx:GraspParser.DecConstantContext):
        pass


    # Enter a parse tree produced by GraspParser#characterConstant.
    def enterCharacterConstant(self, ctx:GraspParser.CharacterConstantContext):
        pass

    # Exit a parse tree produced by GraspParser#characterConstant.
    def exitCharacterConstant(self, ctx:GraspParser.CharacterConstantContext):
        pass


    # Enter a parse tree produced by GraspParser#stringConstant.
    def enterStringConstant(self, ctx:GraspParser.StringConstantContext):
        pass

    # Exit a parse tree produced by GraspParser#stringConstant.
    def exitStringConstant(self, ctx:GraspParser.StringConstantContext):
        pass


    # Enter a parse tree produced by GraspParser#relOp.
    def enterRelOp(self, ctx:GraspParser.RelOpContext):
        pass

    # Exit a parse tree produced by GraspParser#relOp.
    def exitRelOp(self, ctx:GraspParser.RelOpContext):
        pass


    # Enter a parse tree produced by GraspParser#addOp.
    def enterAddOp(self, ctx:GraspParser.AddOpContext):
        pass

    # Exit a parse tree produced by GraspParser#addOp.
    def exitAddOp(self, ctx:GraspParser.AddOpContext):
        pass


    # Enter a parse tree produced by GraspParser#mulOp.
    def enterMulOp(self, ctx:GraspParser.MulOpContext):
        pass

    # Exit a parse tree produced by GraspParser#mulOp.
    def exitMulOp(self, ctx:GraspParser.MulOpContext):
        pass



del GraspParser