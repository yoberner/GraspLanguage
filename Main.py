# package edu.yu.compilers
#
import sys

import antlr4

from GraspLexer import GraspLexer
from GraspParser import GraspParser
from edu.yu.compilers.frontend.Semantics import Semantics
from edu.yu.compilers.frontend.SyntaxErrorHandler import SyntaxErrorHandler
from edu.yu.compilers.intermediate.util.BackendMode import BackendMode
from antlr4 import FileStream, InputStream, CommonTokenStream


# from antlr4 import CharStream
# from org.antlr.v4.runtime.CharStreams import CharStreams
# from org.antlr.v4.runtime.CommonTokenStream import CommonTokenStreams
# from org.antlr.v4.runtime.tree.ParseTree import ParseTree

# import antlr4.PascalLexer
# import antlr4.PascalParser
# import edu.yu.compilers.backend.compiler.Compiler
# import edu.yu.compilers.backend.converter.Converter
# import edu.yu.compilers.backend.interpreter.Executor
# import edu.yu.compilers.frontend.Semantics
# import edu.yu.compilers.frontend.SyntaxErrorHandler
# import edu.yu.compilers.intermediate.symtable.SymTableEntry
# import edu.yu.compilers.intermediate.util.BackendMode

def main(args):
    if len(args) != 3:
        print(args)
        print("USAGE: pascalCC {-execute|-convert|-compile} sourceFileName")
        return

    option = args[1]
    source_file_name = args[2]

    mode = BackendMode.EXECUTOR  # FIXME

    if option.lower() == "-convert":
        mode = BackendMode.CONVERTER
    elif option.lower() == "-execute":
        mode = BackendMode.EXECUTOR
    elif option.lower() == "-compile":
        mode = BackendMode.COMPILER
    else:
        print("ERROR: Invalid option.")
        print("   Valid options: -execute, -convert, or -compile")

    # Create the input stream.
    source = open(source_file_name, 'r').read()

    # Create the character stream from the input stream.
    cs = antlr4.InputStream(source)  # FIXME

    # Custom syntax error handler.
    syntax_error_handler = SyntaxErrorHandler()

    # Create a lexer which scans the character stream
    # to create a token stream.
    lexer = GraspLexer(cs)
    lexer.removeErrorListeners()
    lexer.addErrorListener(syntax_error_handler)
    tokens = CommonTokenStream(lexer)

    # Create a parser which parses the token stream.
    parser = GraspParser(tokens)

    # Pass 1: Check syntax and create the parse tree.
    parser.removeErrorListeners()
    parser.addErrorListener(syntax_error_handler)
    tree = parser.program()

    error_count = syntax_error_handler.get_count()
    if error_count > 0:
        print(f"\nThere were {error_count} syntax errors.")
        print("Object file not created or modified.")
        return

    # Pass 2: Semantic operations.
    pass2 = Semantics(mode)
    pass2.visit(tree)

    error_count = pass2.getErrorCount()
    if error_count > 0:
        print(f"\nThere were {error_count} semantic errors.")
        print("Object file not created or modified.")
        return

    # // Pass 3: Translation.
    # switch (mode) {
    #     case EXECUTOR -> {
    #         // Pass 3: Execute the Pascal program.
    #         SymTableEntry programId = pass2.getProgramId()
    #         Executor pass3 = new Executor(programId)
    #         pass3.visit(tree)
    #     }
    #     case CONVERTER -> {
    #         // Pass 3: Convert from Pascal to Java.
    #         Converter pass3 = new Converter()
    #         String objectCode = (String)pass3.visit(tree)
    #         System.out.println(objectCode)
    #     }
    #     case COMPILER -> {
    #         // Pass 3: Compile the Pascal program.
    #         SymTableEntry programId = pass2.getProgramId()
    #         Compiler pass3 = new Compiler(programId.getName())
    #         pass3.visit(tree)
    #         System.out.println(pass3.getObjectFileName())
    #     }
    # }


if __name__ == "__main__":
    main(sys.argv)
