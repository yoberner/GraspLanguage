/**
 * <h1>StatementGenerator</h1>
 * <p>Emit code for executable statements.</p>
 * <p>Adapted from</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 */

package edu.yu.compilers.backend.compiler;

import antlr4.PascalParser;
import edu.yu.compilers.backend.interpreter.Cell;
import edu.yu.compilers.intermediate.symtable.Predefined;
import edu.yu.compilers.intermediate.symtable.SymTableEntry;
import edu.yu.compilers.intermediate.type.Typespec;
import edu.yu.compilers.intermediate.type.Typespec.Form;
import org.antlr.v4.runtime.tree.ParseTree;

import java.util.ArrayList;
import java.util.List;

import static edu.yu.compilers.backend.compiler.Instruction.*;
import static edu.yu.compilers.intermediate.symtable.SymTableEntry.Kind.REFERENCE_PARAMETER;
import static edu.yu.compilers.intermediate.type.Typespec.Form.ENUMERATION;
import static edu.yu.compilers.intermediate.type.Typespec.Form.SCALAR;

public class StatementGenerator extends CodeGenerator {
    /**
     * Constructor.
     *
     * @param parent   the parent generator.
     * @param compiler the compiler to use.
     */
    public StatementGenerator(CodeGenerator parent, Compiler compiler) {
        super(parent, compiler);
    }

    /**
     * Emit code for an assignment statement.
     *
     * @param ctx the AssignmentStatementContext.
     */
    public void emitAssignment(PascalParser.AssignmentStatementContext ctx) {
        PascalParser.VariableContext varCtx = ctx.lhs().variable();
        PascalParser.ExpressionContext exprCtx = ctx.rhs().expression();
        SymTableEntry varId = varCtx.entry;
        Typespec varType = varCtx.type;
        Typespec exprType = exprCtx.type;

        // The last modifier, if any, is the variable's last subscript or field.
        int modifierCount = varCtx.modifier().size();
        PascalParser.ModifierContext lastModCtx = modifierCount == 0 ? null : varCtx.modifier().get(modifierCount - 1);

        // The target variable has subscripts and/or fields.
        if (modifierCount > 0) {
            lastModCtx = varCtx.modifier().get(modifierCount - 1);
            compiler.visit(varCtx);
        }

        // Emit code to evaluate the expression.
        compiler.visit(exprCtx);

        // float variable := integer constant
        if ((varType == Predefined.realType) && (exprType.baseType() == Predefined.integerType)) emit(I2F);

        // Emit code to store the expression value into the target variable.
        // The target variable has no subscripts or fields.
        if (lastModCtx == null) emitStoreValue(varId, varId.getType());

            // The target variable is a field.
        else if (lastModCtx.field() != null) {
            emitStoreValue(lastModCtx.field().entry, lastModCtx.field().type);
        }

        // The target variable is an array element.
        else {
            emitStoreValue(null, varType);
        }
    }

    /**
     * Emit code for an IF statement.
     *
     * @param ctx the IfStatementContext.
     */
    public void emitIf(PascalParser.IfStatementContext ctx) {
        /***** Complete this method. *****/
        Label elseLabel = new Label();
        Label afterElseLabel = new Label();
        compiler.visit(ctx.expression());//eval condition
        emit(IFEQ, elseLabel);
        compiler.visit(ctx.trueStatement().statement());
        emit(GOTO, afterElseLabel);
        emitLabel(elseLabel);
        if(ctx.falseStatement() != null) {
            compiler.visit(ctx.falseStatement().statement());
        }
        emitLabel(afterElseLabel);
    }

    /**
     * Emit code for a CASE statement.
     *
     * @param ctx the CaseStatementContext.
     */
    public void emitCase(PascalParser.CaseStatementContext ctx) {
        /***** Complete this method. *****/
        List<PascalParser.CaseBranchContext> branches = ctx.caseBranchList().caseBranch();
        List<Label> labels = new ArrayList<>();
//        for (int i = 0; i < labels.length; i++) {
//            labels[i] = new Label();
//        }
//        Label next_label = labels[branches.size() - 1];
        Label next_label = null;
        if(true){
            processSwitchStringStatement(ctx,labels, branches);
//            labels.add(new Label());
            next_label = new Label();
            emit(GOTO, next_label);
        }
        else {
//            compiler.visit(ctx.expression());
//            emit(LOOKUPSWITCH);
//            objectFile.print("\t");
//            for (int i = 0; i < branches.size() - 1; i++) {
//                PascalParser.CaseBranchContext branch = branches.get(i);
//                List<PascalParser.CaseConstantContext> constList = branch.caseConstantList().caseConstant();
//                for (PascalParser.CaseConstantContext constant : constList) {
//                    String constantStr = constant.value.toString();
//                    if (constant.type == Predefined.charType) {
//                        constantStr = String.valueOf(Character.getNumericValue(constantStr.charAt(0)));
//                    } else if (constant.type == Predefined.stringType) {
//                        emit(ALOAD, "\"" + constantStr + "\"");
//                        constantStr = "";
//
//                    }
//                    objectFile.print(constantStr + ":" + labels[i]);
//                    objectFile.println();
//                }
//            }
//            objectFile.print("default:" + next_label);
//            objectFile.println();
        }
        for (int i = 0; i < branches.size(); i++) {
            PascalParser.CaseBranchContext branch = branches.get(i);
            if(branch.children == null){
                break;
            }
            emitLabel(labels.get(i));
            compiler.visit(branch.statement());
            emit(GOTO, next_label);
        }
        emitLabel(next_label);

    }

    public void processSwitchStringStatement(PascalParser.CaseStatementContext ctx, List<Label> labels, List<PascalParser.CaseBranchContext> branches){
        //already on stack
        boolean neg = false;
        for (int i = 0; i < branches.size(); i++) {
            PascalParser.CaseBranchContext branch = branches.get(i);
            if(branch.children == null){return;}

            List<PascalParser.CaseConstantContext> constList = branch.caseConstantList().caseConstant();
            for (PascalParser.CaseConstantContext constant : constList) {
                String constantStr = constant.value.toString();
                Instruction cmd = constant.type == Predefined.stringType ? IF_ACMPEQ : IF_ICMPEQ;
                if (constant.type == Predefined.charType) {

                } else if (constant.type == Predefined.stringType) {
                    constantStr = "\"" + constant.value.toString() + "\"";
                }else if (Integer.parseInt(constant.value.toString()) < 0){
                    neg = true;
                    constantStr = constantStr.substring(1);
                }
                compiler.visit(ctx.expression());
//                emitLoadConstant(constantStr);
                if(constant.type == Predefined.charType){
                    emit(LDC, constantStr.charAt(0));
//                    emit(I2C);
                }else{
                    emit(LDC, constantStr);

                }
                if(neg){
//                  emit(LDC, constantStr);
                    emit(INEG);
                    neg = false;
                }
                labels.add(new Label());
                emit(cmd, labels.get(i));
//                objectFile.print(constantStr + ":" + );
//                objectFile.println();
            }

        }

    }
    /**
     * Emit code for a REPEAT statement.
     *
     * @param ctx the RepeatStatementContext.
     */
    public void emitRepeat(PascalParser.RepeatStatementContext ctx) {
        Label loopTopLabel = new Label();
        Label loopExitLabel = new Label();

        emitLabel(loopTopLabel);

        compiler.visit(ctx.statementList());
        compiler.visit(ctx.expression());
        emit(IFNE, loopExitLabel);
        emit(GOTO, loopTopLabel);

        emitLabel(loopExitLabel);
    }

    /**
     * Emit code for a WHILE statement.
     *
     * @param ctx the WhileStatementContext.
     */
    public void emitWhile(PascalParser.WhileStatementContext ctx) {
        /***** Complete this method. *****/
        Label loopTestLabel = new Label();
        Label loopExitLabel = new Label();
        emitLabel(loopTestLabel);
        compiler.visit(ctx.expression());//eval condition
        emit(IFEQ, loopExitLabel);
        compiler.visit(ctx.statement());
        emit(GOTO, loopTestLabel);
        emitLabel(loopExitLabel);
    }

    /**
     * Emit code for a FOR statement.
     *
     * @param ctx the ForStatementContext.
     */
    public void emitFor(PascalParser.ForStatementContext ctx) {
        /***** Complete this method. *****/
        boolean toLoop = ctx.TO() != null;
        Instruction limitCmd = toLoop ? IF_ICMPGT: IF_ICMPLT;
//        emit(ICONST_0);
//        int loopVarIndex = localVariables.reserve();
//        emit(ISTORE, loopVarIndex);
//        compiler.visit(ctx.variable());
        compiler.visit(ctx.expression(0));
        emitStoreValue(ctx.variable().entry, ctx.variable().entry.getType());
        //emitStoreValue(lastModCtx.field().entry, lastModCtx.field().type); Maybe?
        Label loopTestLabel = new Label();
        Label loopExitLabel = new Label();
        emitLabel(loopTestLabel);
        //
        compiler.visit(ctx.variable());
        compiler.visit(ctx.expression(1));//eval condition
        emit(limitCmd, loopExitLabel);
        compiler.visit(ctx.statement());

//        emit(IINC, 1, );
        if(toLoop) {
            compiler.visit(ctx.variable());
            emit(ICONST_1);
            emit(IADD);
        }else{
            compiler.visit(ctx.variable());
            emit(ICONST_1);
            emit(ISUB);
        }
        emitStoreValue(ctx.variable().entry, ctx.variable().entry.getType());
        emit(GOTO, loopTestLabel);
        emitLabel(loopExitLabel);
    }

    /**
     * Emit code for a procedure call statement.
     *
     * @param ctx the ProcedureCallStatementContext.
     */
    public void emitProcedureCall(PascalParser.ProcedureCallStatementContext ctx) {
        /***** Complete this method. *****/
        //put args on stack
        ParseTree node = ctx;
        while(!(node instanceof  PascalParser.ProgramContext)){
            node = node.getParent();
        }
        if(ctx.argumentList() == null){
            String methodArgStr = ((PascalParser.ProgramContext)node).programHeader().programIdentifier().IDENTIFIER() + "/" + ctx.procedureName().IDENTIFIER() + "()V";
            emit(INVOKESTATIC, methodArgStr);
            return;
        }
        List<PascalParser.ArgumentContext> args = ctx.argumentList().argument();
        StringBuilder argTypeStr = new StringBuilder();
        SymTableEntry ste = ctx.procedureName().entry;

        ArrayList<SymTableEntry> paramList = ste.getRoutineParameters();
        for (int i = 0; i < paramList.size(); i++) {
            SymTableEntry param = paramList.get(i);
            PascalParser.ArgumentContext arg = args.get(i);
            String type = arg.expression().type.getIdentifier().getName();

            if (param.getType().getIdentifier().getName().equals("integer")) {
                argTypeStr.append("I");
                compiler.visit(arg.expression());
                if(!type.equals("integer")) {
                    emit(F2I);
                }
            } else if (param.getType().getIdentifier().getName().equals("real")) {
                argTypeStr.append("F");
                compiler.visit(arg.expression());
                if(!type.equals("real")) {
                    emit(I2F);
                }
            } else if (param.getType().getIdentifier().getName().equals("boolean")) {
                argTypeStr.append("Z");
                compiler.visit(arg.expression());
            } else if (param.getType().getIdentifier().getName().equals("char")) {
                //char
                compiler.visit(arg.expression());
                argTypeStr.append("C");
            }

        }

//            for(PascalParser.ArgumentContext arg: args){
//                compiler.visit(arg.expression());
//            }


        String methodArgStr = ((PascalParser.ProgramContext)node).programHeader().programIdentifier().IDENTIFIER() + "/" + ctx.procedureName().IDENTIFIER() + "(" + argTypeStr + ")V";
        emit(INVOKESTATIC, methodArgStr);
    }

    /**
     * Emit code for a function call statement.
     *
     * @param ctx the FunctionCallContext.
     */
    public void emitFunctionCall(PascalParser.FunctionCallContext ctx) {
        /***** Complete this method. *****/
        ParseTree node = ctx;
        while(!(node instanceof  PascalParser.ProgramContext)){
            node = node.getParent();
        }
        if(ctx.argumentList() == null){
            String methodArgStr = ((PascalParser.ProgramContext)node).programHeader().programIdentifier().IDENTIFIER() + "/" + ctx.functionName().IDENTIFIER() + "()V";
            emit(INVOKESTATIC, methodArgStr);
            return;
        }
        List<PascalParser.ArgumentContext> args = ctx.argumentList().argument();
        StringBuilder argTypeStr = new StringBuilder();
        SymTableEntry ste = ctx.functionName().entry;

        ArrayList<SymTableEntry> paramList = ste.getRoutineParameters();
        for (int i = 0; i < paramList.size(); i++) {
            SymTableEntry param = paramList.get(i);
            PascalParser.ArgumentContext arg = args.get(i);
            String type = arg.expression().type.getIdentifier().getName();

            if (param.getType().getIdentifier().getName().equals("integer")) {
                argTypeStr.append("I");
                compiler.visit(arg.expression());
                if(!type.equals("integer")) {
                    emit(F2I);
                }
            } else if (param.getType().getIdentifier().getName().equals("real")) {
                argTypeStr.append("F");
                compiler.visit(arg.expression());
                if(!type.equals("real")) {
                    emit(I2F);
                }
            } else if (param.getType().getIdentifier().getName().equals("boolean")) {
                argTypeStr.append("Z");
                compiler.visit(arg.expression());
            } else if (param.getType().getIdentifier().getName().equals("char")) {
                //char
                compiler.visit(arg.expression());
                argTypeStr.append("C");
            }

        }

        String retType = "";
        if(ste.getType() == Predefined.integerType){
            retType = "I";
        }else if(ste.getType() == Predefined.realType){
            retType = "F";
        }else if(ste.getType() == Predefined.booleanType){
            retType = "Z";
        }else if(ste.getType() == Predefined.charType){
            retType = "C";
        }else if(ste.getType() == Predefined.stringType){
            retType = "A";
        }else {
            retType = "V";
        }

        String methodArgStr = ((PascalParser.ProgramContext)node).programHeader().programIdentifier().IDENTIFIER() + "/" + ctx.functionName().IDENTIFIER() + "(" + argTypeStr + ")" + retType;
        emit(INVOKESTATIC, methodArgStr);
//        emit(LDC, 1);
    }

    /**
     * Emit a call to a procedure or a function.
     *
     * @param routineId  the routine name's symbol table entry.
     * @param argListCtx the ArgumentListContext.
     */
    private void emitCall(SymTableEntry routineId, PascalParser.ArgumentListContext argListCtx) {
        /***** Complete this method. *****/
    }

    /**
     * Emit code for a WRITE statement.
     *
     * @param ctx the WriteStatementContext.
     */
    public void emitWrite(PascalParser.WriteStatementContext ctx) {
        emitWrite(ctx.writeArguments(), false);
    }

    /**
     * Emit code for a WRITELN statement.
     *
     * @param ctx the WritelnStatementContext.
     */
    public void emitWriteln(PascalParser.WritelnStatementContext ctx) {
        emitWrite(ctx.writeArguments(), true);
    }

    /**
     * Emit code for a call to WRITE or WRITELN.
     *
     * @param argsCtx the WriteArgumentsContext.
     * @param needLF  true if you need a line feed.
     */
    private void emitWrite(PascalParser.WriteArgumentsContext argsCtx, boolean needLF) {
        emit(GETSTATIC, "java/lang/System/out", "Ljava/io/PrintStream;");

        // WRITELN with no arguments.
        if (argsCtx == null) {
            emit(INVOKEVIRTUAL, "java/io/PrintStream.println()V");
            localStack.decrease(1);
        }

        // Generate code for the arguments.
        else {
            StringBuffer format = new StringBuffer();
            int exprCount = createWriteFormat(argsCtx, format, needLF);

            // Load the format string.
            emit(LDC, format.toString());

            // Emit the arguments array.
            if (exprCount > 0) {
                emitArgumentsArray(argsCtx, exprCount);

                emit(INVOKEVIRTUAL, "java/io/PrintStream/printf(Ljava/lang/String;[Ljava/lang/Object;)" + "Ljava/io/PrintStream;");
                localStack.decrease(2);
                emit(POP);
            } else {
                emit(INVOKEVIRTUAL, "java/io/PrintStream/print(Ljava/lang/String;)V");
                localStack.decrease(2);
            }
        }
    }

    /**
     * Create the printf format string.
     *
     * @param argsCtx the WriteArgumentsContext.
     * @param format  the format string to create.
     * @return the count of expression arguments.
     */
    private int createWriteFormat(PascalParser.WriteArgumentsContext argsCtx, StringBuffer format, boolean needLF) {
        int exprCount = 0;
        format.append("\"");

        // Loop over the arguments.
        for (PascalParser.WriteArgumentContext argCtx : argsCtx.writeArgument()) {
            Typespec type = argCtx.expression().type;
            String argText = argCtx.getText();

            // Append any literal strings.
            if (argText.charAt(0) == '\'') {
                format.append(convertString(argText));
            }

            // For any other expressions, append a field specifier.
            else {
                exprCount++;
                format.append("%");

                PascalParser.FieldWidthContext fwCtx = argCtx.fieldWidth();
                if (fwCtx != null) {
                    String sign = ((fwCtx.sign() != null) && (fwCtx.sign().getText().equals("-"))) ? "-" : "";
                    format.append(sign).append(fwCtx.integerConstant().getText());

                    PascalParser.DecimalPlacesContext dpCtx = fwCtx.decimalPlaces();
                    if (dpCtx != null) {
                        format.append(".").append(dpCtx.integerConstant().getText());
                    }
                }

                String typeFlag = type == Predefined.integerType ? "d" : type == Predefined.realType ? "f" : type == Predefined.booleanType ? "b" : type == Predefined.charType ? "c" : "s";
                format.append(typeFlag);
            }
        }

        format.append(needLF ? "\\n\"" : "\"");

        return exprCount;
    }

    /**
     * Emit the printf arguments array.
     *
     * @param argsCtx write argument context
     * @param exprCount expression count
     */
    private void emitArgumentsArray(PascalParser.WriteArgumentsContext argsCtx, int exprCount) {
        // Create the arguments array.
        emitLoadConstant(exprCount);
        emit(ANEWARRAY, "java/lang/Object");

        int index = 0;

        // Loop over the arguments to fill the arguments array.
        for (PascalParser.WriteArgumentContext argCtx : argsCtx.writeArgument()) {
            String argText = argCtx.getText();
            PascalParser.ExpressionContext exprCtx = argCtx.expression();
            Typespec type = exprCtx.type.baseType();

            // Skip string constants, which were made part of
            // the format string.
            if (argText.charAt(0) != '\'') {
                emit(DUP);
                emitLoadConstant(index++);

                compiler.visit(exprCtx);

                Form form = type.getForm();
                if (((form == SCALAR) || (form == ENUMERATION)) && (type != Predefined.stringType)) {
                    emit(INVOKESTATIC, valueOfSignature(type));
                }

                // Store the value into the array.
                emit(AASTORE);
            }
        }
    }

    /**
     * Emit code for a READ statement.
     *
     * @param ctx the ReadStatementContext.
     */
    public void emitRead(PascalParser.ReadStatementContext ctx) {
        emitRead(ctx.readArguments(), false);
    }

    /**
     * Emit code for a READLN statement.
     *
     * @param ctx the ReadlnStatementContext.
     */
    public void emitReadln(PascalParser.ReadlnStatementContext ctx) {
        emitRead(ctx.readArguments(), true);
    }

    /**
     * Generate code for a call to READ or READLN.
     *
     * @param argsCtx  the ReadArgumentsContext.
     * @param needSkip true if you need to skip the rest of the input line.
     */
    private void emitRead(PascalParser.ReadArgumentsContext argsCtx, boolean needSkip) {
        int size = argsCtx.variable().size();

        // Loop over read arguments.
        for (int i = 0; i < size; i++) {
            PascalParser.VariableContext varCtx = argsCtx.variable().get(i);
            Typespec varType = varCtx.type;

            if (varType == Predefined.integerType) {
                emit(GETSTATIC, programName + "/_sysin Ljava/util/Scanner;");
                emit(INVOKEVIRTUAL, "java/util/Scanner/nextInt()I");
                emitStoreValue(varCtx.entry, null);
            } else if (varType == Predefined.realType) {
                emit(GETSTATIC, programName + "/_sysin Ljava/util/Scanner;");
                emit(INVOKEVIRTUAL, "java/util/Scanner/nextFloat()F");
                emitStoreValue(varCtx.entry, null);
            } else if (varType == Predefined.booleanType) {
                emit(GETSTATIC, programName + "/_sysin Ljava/util/Scanner;");
                emit(INVOKEVIRTUAL, "java/util/Scanner/nextBoolean()Z");
                emitStoreValue(varCtx.entry, null);
            } else if (varType == Predefined.charType) {
                emit(GETSTATIC, programName + "/_sysin Ljava/util/Scanner;");
                emit(LDC, "\"\"");
                emit(INVOKEVIRTUAL, "java/util/Scanner/useDelimiter(Ljava/lang/String;)" + "Ljava/util/Scanner;");
                emit(POP);
                emit(GETSTATIC, programName + "/_sysin Ljava/util/Scanner;");
                emit(INVOKEVIRTUAL, "java/util/Scanner/next()Ljava/lang/String;");
                emit(ICONST_0);
                emit(INVOKEVIRTUAL, "java/lang/String/charAt(I)C");
                emitStoreValue(varCtx.entry, null);

                emit(GETSTATIC, programName + "/_sysin Ljava/util/Scanner;");
                emit(INVOKEVIRTUAL, "java/util/Scanner/reset()Ljava/util/Scanner;");

            } else  // string
            {
                emit(GETSTATIC, programName + "/_sysin Ljava/util/Scanner;");
                emit(INVOKEVIRTUAL, "java/util/Scanner/next()Ljava/lang/String;");
                emitStoreValue(varCtx.entry, null);
            }
        }

        // READLN: Skip the rest of the input line.
        if (needSkip) {
            emit(GETSTATIC, programName + "/_sysin Ljava/util/Scanner;");
            emit(INVOKEVIRTUAL, "java/util/Scanner/nextLine()Ljava/lang/String;");
            emit(POP);
        }
    }
}