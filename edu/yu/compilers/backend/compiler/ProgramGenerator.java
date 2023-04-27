package edu.yu.compilers.backend.compiler;

import antlr4.PascalParser;
import edu.yu.compilers.intermediate.symtable.SymTable;
import edu.yu.compilers.intermediate.symtable.SymTableEntry;
import edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind;
import edu.yu.compilers.intermediate.type.Typespec;

import java.io.IOException;
import java.util.ArrayList;

import static edu.yu.compilers.backend.compiler.Directive.*;
import static edu.yu.compilers.backend.compiler.Instruction.*;
import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind.*;
import static edu.yu.compilers.intermediate.type.Typespec.Form.RECORD;


public class ProgramGenerator extends CodeGenerator {
    private final int programLocalsCount;  // count of program local variables
    private SymTableEntry programId;   // symbol table entry of the program name

    /**
     * Constructor.
     *
     * @param parent   the parent generator.
     * @param compiler the compiler to use.
     */
    public ProgramGenerator(CodeGenerator parent, Compiler compiler) {
        super(parent, compiler);

        localStack = new LocalStack();
        programLocalsCount = 0;
    }

    /**
     * Emit code for a program.
     *
     * @param ctx the ProgramContext.
     */
    public void emitProgram(PascalParser.ProgramContext ctx) {
        programId = ctx.programHeader().programIdentifier().entry;
        SymTable programSymTable = programId.getRoutineSymTable();

        localVariables = new LocalVariables(programLocalsCount);

        emitRecords(programSymTable);

        emitDirective(CLASS_PUBLIC, programName);
        emitDirective(SUPER, "java/lang/Object");

        emitProgramVariables();
        emitInputScanner();
        emitConstructor();
        emitSubroutines(ctx.block().declarations().routinesPart());

        emitMainMethod(ctx);
    }

    /**
     * Create a new compiler instance for a record.
     *
     * @param SymTable the record type's symbol table.
     */
    public void emitRecords(SymTable SymTable) {
        for (SymTableEntry id : SymTable.sortedEntries()) {
            if ((id.getKind() == TYPE) && (id.getType().getForm() == RECORD)) {
                try {
                    new Compiler(id, this.compiler.getOutputPath());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        }
    }

    /**
     * Emit code for a record.
     */
    public void emitRecord(SymTableEntry recordId, String namePath) {
        SymTable recordSymTable = recordId.getType().getRecordSymTable();

        emitDirective(CLASS_PUBLIC, namePath);
        emitDirective(SUPER, "java/lang/Object");
        emitLine();

        // Emit code for any nested records.
        emitRecords(recordSymTable);

        // Emit record fields.
        for (SymTableEntry id : recordSymTable.sortedEntries()) {
            if (id.getKind() == RECORD_FIELD) {
                emitDirective(FIELD, id.getName(), typeDescriptor(id));
            }
        }

        emitConstructor();
        close();  // the object file
    }

    /**
     * Emit field directives for the program variables.
     */
    private void emitProgramVariables() {
        // Runtime timer and standard in.

        SymTable SymTable = programId.getRoutineSymTable();
        ArrayList<SymTableEntry> ids = SymTable.sortedEntries();

        emitLine();
        emitDirective(FIELD_PRIVATE_STATIC, "_sysin", "Ljava/util/Scanner;");

        // Loop over all the program's identifiers and
        // emit a .field directive for each variable.
        for (SymTableEntry id : ids) {
            if (id.getKind() == VARIABLE) {
                emitDirective(FIELD_PRIVATE_STATIC, id.getName(), typeDescriptor(id));
            }
        }
    }

    /**
     * Emit code for the runtime input scanner.
     */
    private void emitInputScanner() {
        emitLine();
        emitComment("Runtime input scanner");
        emitDirective(METHOD_STATIC, "<clinit>()V");
        emitLine();

        emit(NEW, "java/util/Scanner");
        emit(DUP);
        emit(GETSTATIC, "java/lang/System/in Ljava/io/InputStream;");
        emit(INVOKESPECIAL, "java/util/Scanner/<init>(Ljava/io/InputStream;)V");
        emit(PUTSTATIC, programName + "/_sysin Ljava/util/Scanner;");
        emit(RETURN);

        emitLine();
        emitDirective(LIMIT_LOCALS, 0);
        emitDirective(LIMIT_STACK, 3);
        emitDirective(END_METHOD);

        localStack.reset();
    }

    /**
     * Emit code for the main program constructor.
     */
    private void emitConstructor() {
        emitLine();
        emitComment("Main class constructor");
        emitDirective(METHOD_PUBLIC, "<init>()V");
        emitDirective(VAR, "0 is this L" + programName + ";");
        emitLine();

        emit(ALOAD_0);
        emit(INVOKESPECIAL, "java/lang/Object/<init>()V");
        emit(RETURN);

        emitLine();
        emitDirective(LIMIT_LOCALS, 1);
        emitDirective(LIMIT_STACK, 1);
        emitDirective(END_METHOD);

        localStack.reset();
    }

    /**
     * Emit code for any nested procedures and functions.
     */
    private void emitSubroutines(PascalParser.RoutinesPartContext ctx) {
        if (ctx != null) {
            for (PascalParser.RoutineDefinitionContext defnCtx : ctx.routineDefinition()) {
                new Compiler(compiler).visit(defnCtx);
            }
        }
    }

    /**
     * Emit code for the program body as the main method.
     *
     * @param ctx the ProgramContext.
     */
    private void emitMainMethod(PascalParser.ProgramContext ctx) {
        emitLine();
        emitComment("MAIN");
        emitDirective(METHOD_PUBLIC_STATIC, "main([Ljava/lang/String;)V");

        emitMainPrologue(programId);

        // Emit code to allocate any arrays, records, and strings.
        StructuredDataGenerator structureCode = new StructuredDataGenerator(this, compiler);
        structureCode.emitData(programId);

        // Emit code for the compound statement.
        emitLine();
        compiler.visit(ctx.block().compoundStatement());

        emitMainEpilogue();
    }

    /**
     * Emit the main method prologue.
     *
     * @param programId the symbol table entry for the program name.
     */
    private void emitMainPrologue(SymTableEntry programId) {
        emitDirective(VAR, "0 is args [Ljava/lang/String;");
    }

    /**
     * Emit the main method epilogue.
     */
    private void emitMainEpilogue() {
        emitLine();
        emit(RETURN);
        emitLine();

        emitDirective(LIMIT_LOCALS, localVariables.count());
        emitDirective(LIMIT_STACK, localStack.capacity());
        emitDirective(END_METHOD);

        close();  // the object file
    }

    /**
     * Emit code for a declared procedure or function
     *
     * @param ctx the symbol table entry of the routine's name.
     */
    public void emitRoutine(PascalParser.RoutineDefinitionContext ctx) {
        SymTableEntry routineId = ctx.procedureHead() != null ? ctx.procedureHead().routineIdentifier().entry : ctx.functionHead().routineIdentifier().entry;
        SymTable routineSymTable = routineId.getRoutineSymTable();

        emitRoutineHeader(routineId);
        emitRoutineLocals(routineId);

        // Generate code to allocate any arrays, records, and strings.
        StructuredDataGenerator structuredCode = new StructuredDataGenerator(this, compiler);
        structuredCode.emitData(routineId);

        localVariables = new LocalVariables(routineSymTable.getMaxSlotNumber());

        // Emit code for the compound statement.
        PascalParser.CompoundStatementContext stmtCtx = (PascalParser.CompoundStatementContext) routineId.getExecutable();
        compiler.visit(stmtCtx);

        emitRoutineReturn(routineId);
        emitRoutineEpilogue();
    }

    /**
     * Emit the routine header.
     *
     * @param routineId the symbol table entry of the routine's name.
     */
    private void emitRoutineHeader(SymTableEntry routineId) {
        String routineName = routineId.getName();
        ArrayList<SymTableEntry> parmIds = routineId.getRoutineParameters();
        StringBuilder buffer = new StringBuilder();

        // Procedure or function name.
        buffer.append(routineName);
        buffer.append("(");

        // Parameter and return type descriptors.
        if (parmIds != null) {
            for (SymTableEntry parmId : parmIds) {
                buffer.append(typeDescriptor(parmId));
            }
        }
        buffer.append(")");
        buffer.append(typeDescriptor(routineId));

        emitLine();
        if (routineId.getKind() == PROCEDURE) {
            emitComment("PROCEDURE " + routineName);
        } else {
            emitComment("FUNCTION " + routineName);
        }

        emitDirective(METHOD_PRIVATE_STATIC, buffer.toString());
    }

    /**
     * Emit directives for the local variables.
     *
     * @param routineId the symbol table entry of the routine's name.
     */
    private void emitRoutineLocals(SymTableEntry routineId) {
        SymTable SymTable = routineId.getRoutineSymTable();
        ArrayList<SymTableEntry> ids = SymTable.sortedEntries();

        emitLine();

        // Loop over all the routine's identifiers and
        // emit a .var directive for each variable and formal parameter.
        for (SymTableEntry id : ids) {
            Kind kind = id.getKind();

            if ((kind == VARIABLE) || (kind == VALUE_PARAMETER) || (kind == REFERENCE_PARAMETER)) {
                int slot = id.getSlotNumber();
                emitDirective(VAR, slot + " is " + id.getName(), typeDescriptor(id));
            }
        }
    }

    /**
     * Emit the routine's return code.
     *
     * @param routineId the symbol table entry of the routine's name.
     */
    private void emitRoutineReturn(SymTableEntry routineId) {
        emitLine();

        // Function: Return the value in the implied function variable.
        if (routineId.getKind() == FUNCTION) {
            Typespec type = routineId.getType();

            // Get the slot number of the function variable.
            String varName = routineId.getName();
            SymTableEntry varId = routineId.getRoutineSymTable().lookup(varName);
            emitLoadLocal(type, varId.getSlotNumber());
            emitReturnValue(type);
        }

        // Procedure: Just return.
        else emit(RETURN);
    }

    /**
     * Emit the routine's epilogue.
     */
    private void emitRoutineEpilogue() {
        emitLine();
        emitDirective(LIMIT_LOCALS, localVariables.count());
        emitDirective(LIMIT_STACK, localStack.capacity());
        emitDirective(END_METHOD);
    }
}
