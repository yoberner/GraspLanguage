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


# This class defines a complete generic visitor for a parse tree produced by GraspParser.

class GraspVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GraspParser#program.
    def visitProgram(self, ctx:GraspParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#programHeader.
    def visitProgramHeader(self, ctx:GraspParser.ProgramHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#programParameters.
    def visitProgramParameters(self, ctx:GraspParser.ProgramParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#programIdentifier.
    def visitProgramIdentifier(self, ctx:GraspParser.ProgramIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#block.
    def visitBlock(self, ctx:GraspParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#declarations.
    def visitDeclarations(self, ctx:GraspParser.DeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#constantsPart.
    def visitConstantsPart(self, ctx:GraspParser.ConstantsPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#constantDefinitionsList.
    def visitConstantDefinitionsList(self, ctx:GraspParser.ConstantDefinitionsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#constantDefinition.
    def visitConstantDefinition(self, ctx:GraspParser.ConstantDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#constantIdentifier.
    def visitConstantIdentifier(self, ctx:GraspParser.ConstantIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#constant.
    def visitConstant(self, ctx:GraspParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#sign.
    def visitSign(self, ctx:GraspParser.SignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#typesPart.
    def visitTypesPart(self, ctx:GraspParser.TypesPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#typeDefinitionsList.
    def visitTypeDefinitionsList(self, ctx:GraspParser.TypeDefinitionsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#typeDefinition.
    def visitTypeDefinition(self, ctx:GraspParser.TypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#typeIdentifier.
    def visitTypeIdentifier(self, ctx:GraspParser.TypeIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#simpleTypespec.
    def visitSimpleTypespec(self, ctx:GraspParser.SimpleTypespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#arrayTypespec.
    def visitArrayTypespec(self, ctx:GraspParser.ArrayTypespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#recordTypespec.
    def visitRecordTypespec(self, ctx:GraspParser.RecordTypespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#typeIdentifierTypespec.
    def visitTypeIdentifierTypespec(self, ctx:GraspParser.TypeIdentifierTypespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#arrayType.
    def visitArrayType(self, ctx:GraspParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#recordType.
    def visitRecordType(self, ctx:GraspParser.RecordTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#recordFields.
    def visitRecordFields(self, ctx:GraspParser.RecordFieldsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#variablesPart.
    def visitVariablesPart(self, ctx:GraspParser.VariablesPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#variableDeclarationsList.
    def visitVariableDeclarationsList(self, ctx:GraspParser.VariableDeclarationsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#variableDeclarations.
    def visitVariableDeclarations(self, ctx:GraspParser.VariableDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#variableIdentifierList.
    def visitVariableIdentifierList(self, ctx:GraspParser.VariableIdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#variableIdentifier.
    def visitVariableIdentifier(self, ctx:GraspParser.VariableIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#routinesPart.
    def visitRoutinesPart(self, ctx:GraspParser.RoutinesPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#routineDefinition.
    def visitRoutineDefinition(self, ctx:GraspParser.RoutineDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#functionHead.
    def visitFunctionHead(self, ctx:GraspParser.FunctionHeadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#routineIdentifier.
    def visitRoutineIdentifier(self, ctx:GraspParser.RoutineIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#parameters.
    def visitParameters(self, ctx:GraspParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#parameterDeclarationsList.
    def visitParameterDeclarationsList(self, ctx:GraspParser.ParameterDeclarationsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#parameterDeclarations.
    def visitParameterDeclarations(self, ctx:GraspParser.ParameterDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#parameterIdentifier.
    def visitParameterIdentifier(self, ctx:GraspParser.ParameterIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#statement.
    def visitStatement(self, ctx:GraspParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#compoundStatement.
    def visitCompoundStatement(self, ctx:GraspParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#emptyStatement.
    def visitEmptyStatement(self, ctx:GraspParser.EmptyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#statementList.
    def visitStatementList(self, ctx:GraspParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#declareAndAssignStatement.
    def visitDeclareAndAssignStatement(self, ctx:GraspParser.DeclareAndAssignStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:GraspParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#returnStatement.
    def visitReturnStatement(self, ctx:GraspParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#lhs.
    def visitLhs(self, ctx:GraspParser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#rhs.
    def visitRhs(self, ctx:GraspParser.RhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#ifStatement.
    def visitIfStatement(self, ctx:GraspParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#trueStatement.
    def visitTrueStatement(self, ctx:GraspParser.TrueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#falseStatement.
    def visitFalseStatement(self, ctx:GraspParser.FalseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#caseStatement.
    def visitCaseStatement(self, ctx:GraspParser.CaseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#caseBranchList.
    def visitCaseBranchList(self, ctx:GraspParser.CaseBranchListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#caseBranch.
    def visitCaseBranch(self, ctx:GraspParser.CaseBranchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#caseConstantList.
    def visitCaseConstantList(self, ctx:GraspParser.CaseConstantListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#caseConstant.
    def visitCaseConstant(self, ctx:GraspParser.CaseConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#whileStatement.
    def visitWhileStatement(self, ctx:GraspParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#forStatement.
    def visitForStatement(self, ctx:GraspParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#doStatement.
    def visitDoStatement(self, ctx:GraspParser.DoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#argumentList.
    def visitArgumentList(self, ctx:GraspParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#argument.
    def visitArgument(self, ctx:GraspParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#printStatement.
    def visitPrintStatement(self, ctx:GraspParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#printlnStatement.
    def visitPrintlnStatement(self, ctx:GraspParser.PrintlnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#writeArguments.
    def visitWriteArguments(self, ctx:GraspParser.WriteArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#writeArgument.
    def visitWriteArgument(self, ctx:GraspParser.WriteArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#fieldWidth.
    def visitFieldWidth(self, ctx:GraspParser.FieldWidthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#decimalPlaces.
    def visitDecimalPlaces(self, ctx:GraspParser.DecimalPlacesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#readStatement.
    def visitReadStatement(self, ctx:GraspParser.ReadStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#readlnStatement.
    def visitReadlnStatement(self, ctx:GraspParser.ReadlnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#readArguments.
    def visitReadArguments(self, ctx:GraspParser.ReadArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#expression.
    def visitExpression(self, ctx:GraspParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#simpleExpression.
    def visitSimpleExpression(self, ctx:GraspParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#term.
    def visitTerm(self, ctx:GraspParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#variableFactor.
    def visitVariableFactor(self, ctx:GraspParser.VariableFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#numberFactor.
    def visitNumberFactor(self, ctx:GraspParser.NumberFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#characterFactor.
    def visitCharacterFactor(self, ctx:GraspParser.CharacterFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#stringFactor.
    def visitStringFactor(self, ctx:GraspParser.StringFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#functionCallFactor.
    def visitFunctionCallFactor(self, ctx:GraspParser.FunctionCallFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#notFactor.
    def visitNotFactor(self, ctx:GraspParser.NotFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#parenthesizedFactor.
    def visitParenthesizedFactor(self, ctx:GraspParser.ParenthesizedFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#variable.
    def visitVariable(self, ctx:GraspParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#modifier.
    def visitModifier(self, ctx:GraspParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#indexList.
    def visitIndexList(self, ctx:GraspParser.IndexListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#index.
    def visitIndex(self, ctx:GraspParser.IndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#field.
    def visitField(self, ctx:GraspParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#functionCall.
    def visitFunctionCall(self, ctx:GraspParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#functionName.
    def visitFunctionName(self, ctx:GraspParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#number.
    def visitNumber(self, ctx:GraspParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#unsignedNumber.
    def visitUnsignedNumber(self, ctx:GraspParser.UnsignedNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#integerConstant.
    def visitIntegerConstant(self, ctx:GraspParser.IntegerConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#decConstant.
    def visitDecConstant(self, ctx:GraspParser.DecConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#characterConstant.
    def visitCharacterConstant(self, ctx:GraspParser.CharacterConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#stringConstant.
    def visitStringConstant(self, ctx:GraspParser.StringConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#booleanConstant.
    def visitBooleanConstant(self, ctx:GraspParser.BooleanConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#relOp.
    def visitRelOp(self, ctx:GraspParser.RelOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#addOp.
    def visitAddOp(self, ctx:GraspParser.AddOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GraspParser#mulOp.
    def visitMulOp(self, ctx:GraspParser.MulOpContext):
        return self.visitChildren(ctx)



del GraspParser