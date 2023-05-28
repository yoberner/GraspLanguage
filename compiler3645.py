import os
import sys

import antlr4

from gen.GraspLexer import GraspLexer
from gen.GraspParser import GraspParser
from edu.yu.compilers.frontend.Semantics import Semantics
from edu.yu.compilers.frontend.SyntaxErrorHandler import SyntaxErrorHandler
from edu.yu.compilers.intermediate.util.BackendMode import BackendMode
from edu.yu.compilers.backend.converter.Converter import Converter
from antlr4 import CommonTokenStream


def main(args):
    if len(args) != 2:
        print(args)
        print("python3 compiler3645.py <sourceFileName>")
        return

    source_file_name = args[1]

    mode = BackendMode.CONVERTER
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
    #
    # error_count = syntax_error_handler.get_count()
    # if error_count > 0:
    #     print(f"\nThere were {error_count} syntax errors.")
    #     print("Object file not created or modified.")
    #     return

    # Pass 2: Semantic operations.
    pass2 = Semantics(mode)
    pass2.visit(tree)

    error_count = pass2.getErrorCount()
    if error_count > 0:
        print(f"\nThere were {error_count} semantic errors.")
        print("Object file not created or modified.")
        return

    if mode == BackendMode.CONVERTER:
        # Pass 3: Convert from Grasp to Java.
        pass3 = Converter()
        objectCode = str(pass3.visit(tree))
        print(objectCode)
        java_file_name = (source_file_name[source_file_name.rfind(os.sep) + 1:source_file_name.index('.')] + '.java').capitalize()
        open(java_file_name, "x")
        javaFile = open(java_file_name, "a")
        javaFile.write(objectCode)
        javaFile.close()


if __name__ == "__main__":
    main(sys.argv)
