class CodeGenerator:
    
    blanks = ' ' * 80  # 80 blanks

    # ? how to do PrintWriter here ?
    def __init__(self, object_file):
        self.object_file = object_file
        self.length = 0  # length of the code line
        self.position = 0  # position in the code line
        self.indentation = ''  # indentation of the code line
        self.need_lf = False  # true if a line feed is needed, else false

    def close(self):
        self.object_file.close()

    def lf_if_needed(self):
        if self.need_lf:
            self.object_file.write('\n')
            self.object_file.flush()
            self.length = 0
            self.need_lf = False

    def emit(self, code):
        self.object_file.write(code)
        self.object_file.flush()
        self.length += len(code)
        self.need_lf = True

    def emit_start(self):
        self.lf_if_needed()
        self.emit(self.indentation)
        self.position = 0

    # ? can you method overload here ?
    def emit_start_with_code(self, code):
        self.lf_if_needed()
        self.emit(self.indentation + code)
        self.position = 0

    def emit_line(self):
        self.lf_if_needed()
        self.object_file.write('\n')
        self.object_file.flush()
        self.length = 0
        self.position = 0
        self.need_lf = False

    def emit_line_with_code(self, code):
        self.lf_if_needed()
        self.object_file.write(self.indentation + code + '\n')
        self.object_file.flush()
        self.length = 0
        self.position = 0
        self.need_lf = False

    def emit_end(self, code):
        self.object_file.write(code + '\n')
        self.object_file.flush()
        self.length = 0
        self.position = 0
        self.need_lf = False

    def emit_comment_line(self, text):
        self.emit_line_with_code('// ' + text)
        self.need_lf = False

    def indent(self):
        self.indentation += '    '

    def dedent(self):
        self.indentation = self.indentation[:-4]

    def dedent(self):
        self.indentation = self.indentation[:-4]

    def split(self, limit):
        if self.length > limit:
            self.object_file.write('\n')
            self.object_file.write(self.blanks[:self.position])
            self.object_file.flush()
            self.length = self.position
            self.position = 0
            self.need_lf = False
