class LexicalError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at {line}:{column}")
        self.line = line
        self.column = column
        self.message = message
