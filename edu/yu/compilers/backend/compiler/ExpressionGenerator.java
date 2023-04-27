/**
 * <h1>ExpressionGenerator</h1>
 * <p>Generate code for an expression.</p>
 * <p>Adapted from</p>
 * <p>Copyright (c) 2020 by Ronald Mak</p>
 */

package edu.yu.compilers.backend.compiler;

import antlr4.PascalParser;
import edu.yu.compilers.intermediate.symtable.Predefined;
import edu.yu.compilers.intermediate.symtable.SymTableEntry;
import edu.yu.compilers.intermediate.type.Typespec;
import edu.yu.compilers.intermediate.type.Typespec.Form;

import static edu.yu.compilers.backend.compiler.Instruction.*;
import static edu.yu.compilers.intermediate.type.Typespec.Form.*;

public class ExpressionGenerator extends CodeGenerator
{
    /**
     * Constructor.
     * @param parent the parent executor.
     * @param compiler the compiler to use.
     */
    public ExpressionGenerator(CodeGenerator parent, Compiler compiler)
    {
        super(parent, compiler);
    }
    
    /**
     * Emit code for an expression.
     * @param ctx the ExpressionContext.
     */
    public void emitExpression(PascalParser.ExpressionContext ctx)
    {
        PascalParser.SimpleExpressionContext simpleCtx1 = 
                                                ctx.simpleExpression().get(0);
        PascalParser.RelOpContext relOpCtx = ctx.relOp();
        Typespec type1 = simpleCtx1.type;
        emitSimpleExpression(simpleCtx1);
        
        // More than one simple expression?
        if (relOpCtx != null)
        {
            String op = relOpCtx.getText();
            PascalParser.SimpleExpressionContext simpleCtx2 = 
                                                ctx.simpleExpression().get(1);
            Typespec type2 = simpleCtx2.type;

            boolean integerMode   = false;
            boolean realMode      = false;
            boolean characterMode = false;

            if (   (type1 == Predefined.integerType)
                && (type2 == Predefined.integerType)) 
            {
                integerMode = true;
            }
            else if (   (type1 == Predefined.realType) 
                     || (type2 == Predefined.realType))
            {
                realMode = true;
            }
            else if (   (type1 == Predefined.charType) 
                     && (type2 == Predefined.charType))
            {
                characterMode = true;
            }

            Label trueLabel = new Label();
            Label exitLabel = new Label();

            if (integerMode || characterMode) 
            {
                emitSimpleExpression(simpleCtx2);

                switch (op) {
                    case "=" -> emit(IF_ICMPEQ, trueLabel);
                    case "<>" -> emit(IF_ICMPNE, trueLabel);
                    case "<" -> emit(IF_ICMPLT, trueLabel);
                    case "<=" -> emit(IF_ICMPLE, trueLabel);
                    case ">" -> emit(IF_ICMPGT, trueLabel);
                    case ">=" -> emit(IF_ICMPGE, trueLabel);
                }
            }
            else if (realMode)
            {
                if (type1 == Predefined.integerType) emit(I2F);
                emitSimpleExpression(simpleCtx2);
                if (type2 == Predefined.integerType) emit(I2F);
                
                emit(FCMPG);

                switch (op) {
                    case "=" -> emit(IFEQ, trueLabel);
                    case "<>" -> emit(IFNE, trueLabel);
                    case "<" -> emit(IFLT, trueLabel);
                    case "<=" -> emit(IFLE, trueLabel);
                    case ">" -> emit(IFGT, trueLabel);
                    case ">=" -> emit(IFGE, trueLabel);
                }
            }
            else  // stringMode
            {
                emitSimpleExpression(simpleCtx2);
                emit(INVOKEVIRTUAL,
                     "java/lang/String.compareTo(Ljava/lang/String;)I");
                localStack.decrease(1);

                switch (op) {
                    case "=" -> emit(IFEQ, trueLabel);
                    case "<>" -> emit(IFNE, trueLabel);
                    case "<" -> emit(IFLT, trueLabel);
                    case "<=" -> emit(IFLE, trueLabel);
                    case ">" -> emit(IFGT, trueLabel);
                    case ">=" -> emit(IFGE, trueLabel);
                }
            }

            emit(ICONST_0); // false
            emit(GOTO, exitLabel);
            emitLabel(trueLabel);
            emit(ICONST_1); // true
            emitLabel(exitLabel);
            
            localStack.decrease(1);  // only one branch will be taken
        }
    }
    
    /**
     * Emit code for a simple expression.
     * @param ctx the SimpleExpressionContext.
     */
    public void emitSimpleExpression(PascalParser.SimpleExpressionContext ctx)
    {
        int count = ctx.term().size();
        boolean negate =    (ctx.sign() != null)
                         && ctx.sign().getText().equals("-");
        
        // First term.
        PascalParser.TermContext termCtx1 = ctx.term().get(0);
        Typespec type1 = termCtx1.type;
        emitTerm(termCtx1);
        
        if (negate) emit(type1 == Predefined.integerType ? INEG : FNEG);
        
        // Loop over the subsequent terms.
        for (int i = 1; i < count; i++)
        {
            String op = ctx.addOp().get(i-1).getText().toLowerCase();
            PascalParser.TermContext termCtx2 = ctx.term().get(i);
            Typespec type2 = termCtx2.type;

            boolean integerMode = false;
            boolean realMode    = false;
            boolean booleanMode = false;

            if (   (type1 == Predefined.integerType)
                && (type2 == Predefined.integerType)) 
            {
                integerMode = true;
            }
            else if (   (type1 == Predefined.realType) 
                     || (type2 == Predefined.realType))
            {
                realMode = true;
            }
            else if (   (type1 == Predefined.booleanType) 
                     && (type2 == Predefined.booleanType))
            {
                booleanMode = true;
            }
                            
            if (integerMode)
            {
                emitTerm(termCtx2);
                
                if (op.equals("+")) emit(IADD);
                else                emit(ISUB);
            }
            else if (realMode)
            {
                if (type1 == Predefined.integerType) emit(I2F);
                emitTerm(termCtx2);
                if (type2 == Predefined.integerType) emit(I2F);
                
                if (op.equals("+")) emit(FADD);
                else                emit(FSUB);
            }
            else if (booleanMode)
            {
                emitTerm(termCtx2);
                emit(IOR);
            }
            else  // stringMode
            {
                emit(NEW, "java/lang/StringBuilder");
                emit(DUP_X1);             
                emit(SWAP);                  
                emit(INVOKESTATIC, "java/lang/String/valueOf(Ljava/lang/Object;)" +
                                   "Ljava/lang/String;");
                emit(INVOKESPECIAL, "java/lang/StringBuilder/<init>" +
                                    "(Ljava/lang/String;)V");
                localStack.decrease(1);
                
                emitTerm(termCtx2);
                emit(INVOKEVIRTUAL, "java/lang/StringBuilder/append(Ljava/lang/String;)" +
                                    "Ljava/lang/StringBuilder;");
                localStack.decrease(1);
                emit(INVOKEVIRTUAL, "java/lang/StringBuilder/toString()" +
                                    "Ljava/lang/String;");
                localStack.decrease(1);
            }
        }
    }
    
    /**
     * Emit code for a term.
     * @param ctx the TermContext.
     */
    public void emitTerm(PascalParser.TermContext ctx)
    {
        int count = ctx.factor().size();
        
        // First factor.
        PascalParser.FactorContext factorCtx1 = ctx.factor().get(0);
        Typespec type1 = factorCtx1.type;
        compiler.visit(factorCtx1);
        
        // Loop over the subsequent factors.
        for (int i = 1; i < count; i++)
        {
            String op = ctx.mulOp().get(i-1).getText().toLowerCase();
            PascalParser.FactorContext factorCtx2 = ctx.factor().get(i);
            Typespec type2 = factorCtx2.type;

            boolean integerMode = false;
            boolean realMode    = false;

            if (   (type1 == Predefined.integerType)
                && (type2 == Predefined.integerType)) 
            {
                integerMode = true;
            }
            else if (   (type1 == Predefined.realType) 
                     || (type2 == Predefined.realType))
            {
                realMode = true;
            }
                
            if (integerMode)
            {
                compiler.visit(factorCtx2);

                switch (op) {
                    case "*" -> emit(IMUL);
                    case "/" -> emit(FDIV);
                    case "div" -> emit(IDIV);
                    case "mod" -> emit(IREM);
                }
            }
            else if (realMode)
            {
                if (type1 == Predefined.integerType) emit(I2F);
                compiler.visit(factorCtx2); 
                if (type2 == Predefined.integerType) emit(I2F);
                
                if      (op.equals("*")) emit(FMUL);
                else if (op.equals("/")) emit(FDIV);
            }
            else  // booleanMode
            {
                compiler.visit(factorCtx2);                 
                emit(IAND);
            }
        }
    }
    
    /**
     * Emit code for NOT.
     * @param ctx the NotFactorContext.
     */
    public void emitNotFactor(PascalParser.NotFactorContext ctx)
    {
        compiler.visit(ctx.factor());
        emit(ICONST_1);
        emit(IXOR);
    }

    /**
     * Emit code to load a scalar variable's value 
     * or a structured variable's address.
     * @param varCtx the VariableContext.
     */
    public void emitLoadValue(PascalParser.VariableContext varCtx)
    {
        // Load the scalar value or structure address.
        Typespec variableType = emitLoadVariable(varCtx);
        
        // Load an array element's or record field's value.
        int modifierCount = varCtx.modifier().size();
        if (modifierCount > 0)
        {
            PascalParser.ModifierContext lastModCtx =
                                    varCtx.modifier().get(modifierCount - 1);
            
            if (lastModCtx.indexList() != null)
            {
                emitLoadArrayElementValue(variableType);
            }
            else
            {
                emitLoadRecordFieldValue(lastModCtx.field(), variableType);
            }
        }
    }

    /**
     * Emit code to load a scalar variable's value 
     * or a structured variable's address.
     * @param varCtx the variable node.
     * @return the datatype of the variable.
     */
    public Typespec emitLoadVariable(PascalParser.VariableContext varCtx)
    {
        SymTableEntry variableId = varCtx.entry;
        Typespec variableType = variableId.getType();
        int modifierCount = varCtx.modifier().size();
        
        // Scalar value or structure address.
        emitLoadValue(variableId);

        // Loop over subscript and field modifiers.
        for (int i = 0; i < modifierCount; ++i)
        {
            PascalParser.ModifierContext modCtx = varCtx.modifier().get(i);
            boolean lastModifier = i == modifierCount - 1;

            // Subscript
            if (modCtx.indexList() != null) 
            {
                variableType = emitLoadArrayElementAccess(
                                modCtx.indexList(), variableType, lastModifier);
            }
            
            // Field
            else if (!lastModifier)
            {
                variableType = emitLoadRecordField(modCtx.field(), variableType);
            }
        }

        return variableType;
    }

    /**
     * Emit code to access an array element by loading the array address
     * and the subscript value. This can subsequently be followed by code
     * to load the array element's value or to store into the array element. 
     * @param indexListCtx the SUBSCRIPTS node.
     * @param elmtType the array element type.
     * @param lastModifier true if this is the variable's last modifier.
     * @return the type of the element.
     */
    private Typespec emitLoadArrayElementAccess(
                                    PascalParser.IndexListContext indexListCtx,
                                    Typespec elmtType, boolean lastModifier)
    {
        int indexCount = indexListCtx.index().size();
        
        // Loop over the subscripts.
        for (int i = 0; i < indexCount; i++)
        {
            PascalParser.IndexContext indexCtx = indexListCtx.index().get(i);
            emitExpression(indexCtx.expression());

            Typespec indexType = elmtType.getArrayIndexType();

            if (indexType.getForm() == SUBRANGE) 
            {
                int min = indexType.getSubrangeMinValue();
                if (min != 0) 
                {
                    emitLoadConstant(min);
                    emit(ISUB);
                }
            }

            if (!lastModifier || (i < indexCount - 1)) emit(AALOAD);
            elmtType = elmtType.getArrayElementType();
        }

        return elmtType;
    }

    /**
     * Emit a load of an array element's value.
     * @param elmtType the element type if character, else null.
     */
    private void emitLoadArrayElementValue(Typespec elmtType)
    {
        Form form = SCALAR;

        if (elmtType != null) 
        {
            elmtType = elmtType.baseType();
            form = elmtType.getForm();
        }

        // Load a character from a string.
        if (elmtType == Predefined.charType) 
        {
            emit(INVOKEVIRTUAL, "java/lang/StringBuilder.charAt(I)C");
        }

        // Load an array element.
        else 
        {
            emit(  elmtType == Predefined.integerType ? IALOAD
                 : elmtType == Predefined.realType    ? FALOAD
                 : elmtType == Predefined.booleanType ? BALOAD
                 : form == ENUMERATION                ? IALOAD
                 :                                      AALOAD);
        }
    }
    
    private void emitLoadRecordFieldValue(
                        PascalParser.FieldContext fieldCtx, Typespec recordType)
    {
        emitLoadRecordField(fieldCtx, recordType);
    }

    /**
     * Emit code to load the address or value of a record field.
     * @param fieldCtx the FieldContext.
     * @param recordType the record type.
     * @return the type of the field.
     */
    private Typespec emitLoadRecordField(
                        PascalParser.FieldContext fieldCtx, Typespec recordType)
    {
        SymTableEntry fieldId = fieldCtx.entry;
        String fieldName = fieldId.getName();
        Typespec fieldType = fieldCtx.type;  
        
        String recordTypePath = recordType.getRecordTypePath();
        String fieldPath = recordTypePath + "/" + fieldName;        
        emit(GETFIELD, fieldPath, typeDescriptor(fieldType));

        return fieldType;
    }
    
    /**
     * Emit code to load an integer constant.
     * @param intCtx the IntegerConstantContext.
     */
    public void emitLoadIntegerConstant(PascalParser.NumberContext intCtx)
    {
        int value = Integer.parseInt(intCtx.getText());
        emitLoadConstant(value);
    }
    
    /**
     * Emit code to load real constant.
     * @param realCtx the realConstantContext.
     */
    public void emitLoadRealConstant(PascalParser.NumberContext realCtx)
    {
        float value = Float.parseFloat(realCtx.getText());
        emitLoadConstant(value);
    }
}
