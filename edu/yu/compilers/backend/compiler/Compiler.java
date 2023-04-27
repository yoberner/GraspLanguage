package edu.yu.compilers.backend.compiler;

import antlr4.PascalBaseVisitor;
import antlr4.PascalParser;
import edu.yu.compilers.intermediate.symtable.Predefined;
import edu.yu.compilers.intermediate.symtable.SymTableEntry;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Optional;

/**
 * Compile Pascal to Jasmin assembly language.
 */
public class Compiler extends PascalBaseVisitor<Object> {
    private String programName;     // the program name
    private final CodeGenerator code;            // base code generator
    private final Optional<Path> outputPath;
    private ProgramGenerator programCode;     // program code generator
    private StatementGenerator statementCode;   // statement code generator
    private ExpressionGenerator expressionCode;  // expression code generator

    /**
     * Constructor for the base compiler.
     *
     * @param programName the program name.
     */
    public Compiler(String programName) throws IOException  {
        this(programName, null);
    }

    /**
     * Constructor for the base compiler.
     *
     * @param programName the program name.
     */
    public Compiler(String programName, Path outputPath) throws IOException {
        this.programName = programName;
        this.outputPath = Optional.ofNullable(outputPath);
        code = new CodeGenerator(programName, this);
    }

    /**
     * Constructor for child compilers of procedures and functions.
     *
     * @param parent the parent compiler.
     */
    public Compiler(Compiler parent) {
        this.outputPath = Optional.empty();
        this.code = parent.code;
        this.programCode = parent.programCode;
        this.programName = parent.programName;
    }

    /**
     * Constructor for child compilers of records.
     *
     * @param recordId the symbol table entry of the name of the record to compile.
     */
    protected Compiler(SymTableEntry recordId, Optional<Path> outputPath) throws IOException {
        this.outputPath = outputPath;
        String recordTypePath = recordId.getType().getRecordTypePath();
        code = new CodeGenerator(recordTypePath, this);
        createNewGenerators(code);

        programCode.emitRecord(recordId, recordTypePath);
    }

    /**
     * Create new child code generators.
     *
     * @param parentGenerator the parent code generator.
     */
    private void createNewGenerators(CodeGenerator parentGenerator) {
        programCode = new ProgramGenerator(parentGenerator, this);
        statementCode = new StatementGenerator(programCode, this);
        expressionCode = new ExpressionGenerator(programCode, this);
    }

    /**
     * Get the name of the object (Jasmin) file.
     *
     * @return the name.
     */
    public String getObjectFileName() {
        return code.getObjectFileName();
    }

    public Optional<Path> getOutputPath() {
        return outputPath;
    }

    @Override
    public Object visitProgram(PascalParser.ProgramContext ctx) {
        createNewGenerators(code);
        programCode.emitProgram(ctx);
        return null;
    }

    @Override
    public Object visitRoutineDefinition(
            PascalParser.RoutineDefinitionContext ctx) {
        createNewGenerators(programCode);
        programCode.emitRoutine(ctx);
        return null;
    }

    @Override
    public Object visitStatement(PascalParser.StatementContext ctx) {
        if ((ctx.compoundStatement() == null)
                && (ctx.emptyStatement() == null)) {
            statementCode.emitComment(ctx);
        }

        return visitChildren(ctx);
    }

    @Override
    public Object visitAssignmentStatement(
            PascalParser.AssignmentStatementContext ctx) {
        statementCode.emitAssignment(ctx);
        return null;
    }

    @Override
    public Object visitIfStatement(PascalParser.IfStatementContext ctx) {
        statementCode.emitIf(ctx);
        return null;
    }

    @Override
    public Object visitCaseStatement(PascalParser.CaseStatementContext ctx) {
        statementCode.emitCase(ctx);
        return null;
    }

    @Override
    public Object visitRepeatStatement(PascalParser.RepeatStatementContext ctx) {
        statementCode.emitRepeat(ctx);
        return null;
    }

    @Override
    public Object visitWhileStatement(PascalParser.WhileStatementContext ctx) {
        statementCode.emitWhile(ctx);
        return null;
    }

    @Override
    public Object visitForStatement(PascalParser.ForStatementContext ctx) {
        statementCode.emitFor(ctx);
        return null;
    }

    @Override
    public Object visitProcedureCallStatement(
            PascalParser.ProcedureCallStatementContext ctx) {
        statementCode.emitProcedureCall(ctx);
        return null;
    }

    @Override
    public Object visitExpression(PascalParser.ExpressionContext ctx) {
        expressionCode.emitExpression(ctx);
        return null;
    }

    @Override
    public Object visitVariableFactor(PascalParser.VariableFactorContext ctx) {
        expressionCode.emitLoadValue(ctx.variable());
        return null;
    }

    @Override
    public Object visitVariable(PascalParser.VariableContext ctx) {
        expressionCode.emitLoadVariable(ctx);
        return null;
    }

    @Override
    public Object visitNumberFactor(PascalParser.NumberFactorContext ctx) {
        if (ctx.type == Predefined.integerType) {
            expressionCode.emitLoadIntegerConstant(ctx.number());
        } else {
            expressionCode.emitLoadRealConstant(ctx.number());
        }

        return null;
    }

    @Override
    public Object visitCharacterFactor(PascalParser.CharacterFactorContext ctx) {
        char ch = ctx.getText().charAt(1);
        expressionCode.emitLoadConstant(ch);

        return null;
    }

    @Override
    public Object visitStringFactor(PascalParser.StringFactorContext ctx) {
        String jasminString = convertString(ctx.getText());
        expressionCode.emitLoadConstant(jasminString);

        return null;
    }

    /**
     * Convert a Pascal string to a Java string.
     *
     * @param pascalString the Pascal string.
     * @return the Java string.
     */
    String convertString(String pascalString) {
        String unquoted = pascalString.substring(1, pascalString.length() - 1);
        return unquoted.replace("''", "'").replace("\"", "\\\"");
    }

    @Override
    public Object visitFunctionCallFactor(
            PascalParser.FunctionCallFactorContext ctx) {
        statementCode.emitFunctionCall(ctx.functionCall());
        return null;
    }

    @Override
    public Object visitNotFactor(PascalParser.NotFactorContext ctx) {
        expressionCode.emitNotFactor(ctx);
        return null;
    }

    @Override
    public Object visitParenthesizedFactor(
            PascalParser.ParenthesizedFactorContext ctx) {
        return visit(ctx.expression());
    }

    @Override
    public Object visitWriteStatement(PascalParser.WriteStatementContext ctx) {
        statementCode.emitWrite(ctx);
        return null;
    }

    @Override
    public Object visitWritelnStatement(PascalParser.WritelnStatementContext ctx) {
        statementCode.emitWriteln(ctx);
        return null;
    }

    @Override
    public Object visitReadStatement(PascalParser.ReadStatementContext ctx) {
        statementCode.emitRead(ctx);
        return null;
    }

    @Override
    public Object visitReadlnStatement(PascalParser.ReadlnStatementContext ctx) {
        statementCode.emitReadln(ctx);
        return null;
    }
}
