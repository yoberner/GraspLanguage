from antlr4.error.ErrorListener import ErrorListener


class SyntaxErrorHandler(ErrorListener):
    count = 0
    first = True

    def get_count(self):
        return self.count

    def syntaxError(self, recognizer, offendingSymbol, line, charPositionInLine, msg, ex):
        if self.first:
            print("\n\n===== SYNTAX ERRORS =====\n")
            print("{:<4} {:<35}".format("Line", "Message"))
            print("{:<4} {:<35}".format("----", "-------"))
            self.first = False

        self.count += 1
        print("{:03d}  {:<35}".format(line, msg))

