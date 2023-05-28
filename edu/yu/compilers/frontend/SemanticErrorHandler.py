from enum import Enum
from multipledispatch import dispatch
from antlr4 import ParserRuleContext


class SemanticErrorHandler:
    class Code(Enum):
        UNDECLARED_IDENTIFIER = "Undeclared identifier"
        REDECLARED_IDENTIFIER = "Redeclared identifier"
        IMMUTABLE_FUNCTION = "Function is Immutable - can not write to global variable"
        INVALID_CONSTANT = "Invalid constant"
        INVALID_SIGN = "Invalid sign"
        INVALID_TYPE = "Invalid type"
        INVALID_VARIABLE = "Invalid variable"
        INVALID_OPERATOR = "Invalid operator"
        TYPE_MISMATCH = "Type mismatch"
        TYPE_MUST_BE_INTEGER = "Datatype must be integer"
        TYPE_MUST_BE_NUMERIC = "Datatype must be integer or real"
        TYPE_MUST_BE_BOOLEAN = "Datatype must be boolean"
        TYPE_MUST_BE_STRING = "Datatype must be string"
        INCOMPATIBLE_ASSIGNMENT = "Incompatible assignment"
        INCOMPATIBLE_COMPARISON = "Incompatible comparison"
        DUPLICATE_CASE_CONSTANT = "Duplicate CASE constant"
        INVALID_CONTROL_VARIABLE = "Invalid control variable datatype"
        NAME_MUST_BE_PROCEDURE = "Must be a procedure name"
        NAME_MUST_BE_FUNCTION = "Must be a procedure name"
        ARGUMENT_COUNT_MISMATCH = "Invalid number of arguments"
        ARGUMENT_MUST_BE_VARIABLE = "Argument must be a variable"
        INVALID_REFERENCE_PARAMETER = "Reference parameter cannot be scalar"
        INVALID_RETURN_TYPE = "Invalid function return type"
        TOO_MANY_SUBSCRIPTS = "Too many subscripts"
        INVALID_FIELD = "Invalid field"

        def __init__(self, message):
            self.message = message

    def __init__(self):
        self.count = 0

    def get_count(self):
        return self.count

    @dispatch(Code, int, str)
    def flag(self, code, lineNumber, text):
        if self.count == 0:
            print("\n===== SEMANTIC ERRORS =====\n")
            print("{:<4} {:<40} {}".format("Line", "Message", "Found near"))
            print("{:<4} {:<40} {}".format("----", "-------", "----------"))

        self.count += 1

        print("{:03d}  {:<40} \"{}\"".format(lineNumber, code.message, text))

    @dispatch(Code, ParserRuleContext)
    def flag(self, code, ctx):
        self.flag(code, ctx.start.line, ctx.getText())
