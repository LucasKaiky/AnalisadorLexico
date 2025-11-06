from .tokens import TokenType, Token
from .errors import LexicalError
from .keywords import KEYWORDS


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
        # Caso \r\n
        if c == "\r" and self.peek_next() == "\n":
            self.i += 2
            self.line += 1
            self.col = 1
            return True
        # Caso \n ou \r
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


# Analisador léxico

class Lexer:
    """Responsável por transformar o código-fonte (string) em uma sequência de Tokens."""

    def __init__(self, source: str):
        self.r = Reader(source)
        self.single_char = {
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            ":": TokenType.COLON,
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

        line, col = self.r.line, self.r.col
        c = self.r.peek()

        if c == '#':
            self.r.advance()
            self._skip_line_comment()
            return self.next_token()

        if c == '/':
            if self.r.peek_next() == '*':
                self.r.advance()
                self.r.advance()
                self._skip_block_comment()
                return self.next_token()
            else:
                self.r.advance()
                return Token(TokenType.SLASH, "/", line, col)

        if self._is_identifier_start(c):
            return self._scan_identifier(line, col)

        if c.isdigit() or (c == '.' and self.r.peek_next().isdigit()):
            return self._scan_number(line, col)

        if c == "=":
            self.r.advance()
            if self.r.match("="):
                return Token(TokenType.EQUAL_EQUAL, "==", line, col)
            return Token(TokenType.ASSIGN, "=", line, col)

        if c == "!":
            self.r.advance()
            if self.r.match("="):
                return Token(TokenType.BANG_EQUAL, "!=", line, col)
            raise LexicalError("expected '=' after '!'", line, col)

        if c == ">":
            self.r.advance()
            if self.r.match("="):
                return Token(TokenType.GREATER_EQUAL, ">=", line, col)
            return Token(TokenType.GREATER, ">", line, col)

        if c == "<":
            self.r.advance()
            if self.r.match("="):
                return Token(TokenType.LESS_EQUAL, "<=", line, col)
            return Token(TokenType.LESS, "<", line, col)

        if c == '"':
            return self._scan_string(line, col)

        if c in self.single_char:
            self.r.advance()
            return Token(self.single_char[c], c, line, col)

        self.r.advance()
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

    def _scan_identifier(self, line: int, col: int) -> Token:
        buf = []
        while self._is_identifier_part(self.r.peek()):
            buf.append(self.r.advance())

        text = "".join(buf)
        if text in KEYWORDS:
            return Token(KEYWORDS[text], text, line, col)
        return Token(TokenType.IDENTIFIER, text, line, col)

    def _is_identifier_start(self, c: str) -> bool:
        return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_"

    def _is_identifier_part(self, c: str) -> bool:
        return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_" or c.isdigit()

    def _scan_number(self, line: int, col: int) -> Token:
        seen_dot = False
        has_digit = False
        buf: list[str] = []

        while True:
            c = self.r.peek()

            if c.isdigit():
                has_digit = True
                buf.append(self.r.advance())
                continue

            if c == '.':
                if seen_dot:
                    if self.r.peek_next().isdigit():
                        raise LexicalError("invalid numeric literal with multiple dots", line, col)
                    raise LexicalError("invalid numeric literal ending with a dot", line, col)

                if not self.r.peek_next().isdigit():
                    if has_digit:
                        raise LexicalError("invalid numeric literal ending with a dot", line, col)
                    raise LexicalError("invalid numeric literal starting with a dot without a number after", line, col)

                seen_dot = True
                buf.append(self.r.advance())
                continue

            break

        if not has_digit:
            raise LexicalError("invalid numeric literal", line, col)

        tok_type = TokenType.FLOAT_LIT if seen_dot else TokenType.INT_LIT
        return Token(tok_type, "".join(buf), line, col)

    def _scan_string(self, line: int, col: int) -> Token:
        self.r.advance()
        buf = []
        while not self.r.is_at_end():
            c = self.r.peek()
            if c == '"':
                self.r.advance()
                return Token(TokenType.STRING, "".join(buf), line, col)
            if c == "\\":
                self.r.advance()
                esc = self.r.peek()
                mapping = {'"': '"', 'n': '\n', 'r': '\r', 't': '\t', '\\': '\\'}
                buf.append(mapping.get(esc, esc))
                self.r.advance()
            else:
                if not self.r.consume_newline():
                    buf.append(self.r.advance())
        raise LexicalError("unterminated string literal", line, col)

    def _skip_line_comment(self):
        while not self.r.is_at_end() and self.r.peek() not in "\n\r":
            self.r.advance()

    def _skip_block_comment(self):
        start_line, start_col = self.r.line, self.r.col
        while not self.r.is_at_end():
            if self.r.peek() == "*" and self.r.peek_next() == "/":
                self.r.advance()
                self.r.advance()
                return

            self.r.consume_newline() or self.r.advance()

        raise LexicalError("Unterminated block comment", start_line, start_col)
