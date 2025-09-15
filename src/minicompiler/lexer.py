from .tokens import TokenType, Token
from .errors import LexicalError

class Reader:
    def __init__(self, text: str):
        self.text = text
        self.n = len(text)
        self.i = 0
        self.line = 1
        self.col = 1

    def is_at_end(self) -> bool:
        return self.i >= self.n

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.text[self.i]

    def peek_next(self) -> str:
        if self.i + 1 >= self.n:
            return "\0"
        return self.text[self.i + 1]

    def advance(self) -> str:
        if self.is_at_end():
            return "\0"
        ch = self.text[self.i]
        self.i += 1
        self.col += 1
        return ch

    def consume_newline(self) -> bool:
        if self.is_at_end():
            return False
        c = self.peek()
        if c == "\r" and self.peek_next() == "\n":
            self.i += 2
            self.line += 1
            self.col = 1
            return True
        if c == "\n" or c == "\r":
            self.i += 1
            self.line += 1
            self.col = 1
            return True
        return False

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.text[self.i] != expected:
            return False
        self.i += 1
        self.col += 1
        return True


class Lexer:
    def __init__(self, source: str):
        self.r = Reader(source)
        self.single_char = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "/": TokenType.SLASH,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
        }

    def __iter__(self):
        while True:
            tok = self.next_token()
            yield tok
            if tok.type == TokenType.EOF:
                break

    def next_token(self) -> Token:
        self._skip_whitespace()
        if self.r.is_at_end():
            return Token(TokenType.EOF, "", self.r.line, self.r.col)
        line = self.r.line
        col = self.r.col
        c = self.r.advance()
        if self._is_identifier_start(c):
            return self._scan_identifier(c, line, col)
        if c in self.single_char:
            return Token(self.single_char[c], c, line, col)
        if c == "=":
            if self.r.match("="):
                return Token(TokenType.EQUAL_EQUAL, "==", line, col)
            return Token(TokenType.ASSIGN, "=", line, col)
        if c == "!":
            if self.r.match("="):
                return Token(TokenType.BANG_EQUAL, "!=", line, col)
            raise LexicalError("unexpected '!'", line, col)
        if c == ">":
            if self.r.match("="):
                return Token(TokenType.GREATER_EQUAL, ">=", line, col)
            return Token(TokenType.GREATER, ">", line, col)
        if c == "<":
            if self.r.match("="):
                return Token(TokenType.LESS_EQUAL, "<=", line, col)
            return Token(TokenType.LESS, "<", line, col)
        if c.isdigit() or c == ".":
            raise LexicalError("numeric literal not supported yet", line, col)
        raise LexicalError(f"invalid character '{c}'", line, col)

    def _skip_whitespace(self):
        while True:
            c = self.r.peek()
            if c in " \t":
                self.r.advance()
                continue
            if self.r.consume_newline():
                continue
            break

    def _scan_identifier(self, first: str, line: int, col: int) -> Token:
        buf = [first]
        while self._is_identifier_part(self.r.peek()):
            buf.append(self.r.advance())
        return Token(TokenType.IDENTIFIER, "".join(buf), line, col)

    def _is_identifier_start(self, c: str) -> bool:
        return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_"

    def _is_identifier_part(self, c: str) -> bool:
        return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_" or c.isdigit()

    def _scan_number(self, first: str, line: int, col: int) -> Token:
        raise LexicalError("numeric literal not supported yet", line, col)

    def _skip_line_comment(self):
        pass

    def _skip_block_comment(self):
        pass
