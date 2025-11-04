from .tokens import TokenType, Token
from .errors import LexicalError
from .keywords import KEYWORDS


class Reader:
    """
    Responsável por ler o código-fonte caractere por caractere,
    mantendo o controle de linha e coluna para relatório de erros.
    """

    def __init__(self, text: str):
        self.text = text
        self.n = len(text)
        self.i = 0
        self.line = 1
        self.col = 1

    def is_at_end(self) -> bool:
        """Verifica se o fim do arquivo foi atingido."""
        return self.i >= self.n

    def peek(self) -> str:
        """Retorna o caractere atual sem avançar."""
        if self.is_at_end():
            return "\0"
        return self.text[self.i]

    def peek_next(self) -> str:
        """Retorna o próximo caractere sem avançar."""
        if self.i + 1 >= self.n:
            return "\0"
        return self.text[self.i + 1]

    def advance(self) -> str:
        """Consome o caractere atual e avança para o próximo, atualizando a coluna."""
        if self.is_at_end():
            return "\0"
        ch = self.text[self.i]
        self.i += 1
        self.col += 1
        return ch

    def consume_newline(self) -> bool:
        """
        Consome uma quebra de linha (\n, \r ou \r\n) e atualiza a linha/coluna.
        Crucial para o Requisito 8 (comentários) e _skip_whitespace.
        """
        if self.is_at_end():
            return False
        c = self.peek()
        # Caso \r\n (Windows)
        if c == "\r" and self.peek_next() == "\n":
            self.i += 2
            self.line += 1
            self.col = 1
            return True
        # Caso \n ou \r (Unix/Mac/legacy)
        if c == "\n" or c == "\r":
            self.i += 1
            self.line += 1
            self.col = 1
            return True
        return False

    def match(self, expected: str) -> bool:
        """
        Consome o caractere atual *somente* se for igual a 'expected'.
        Usado para operadores duplos (==, >=, etc.).
        """
        if self.is_at_end():
            return False
        if self.text[self.i] != expected:
            return False
        self.i += 1
        self.col += 1
        return True


# --- Classe Lexer (Analisador Léxico) ---

class Lexer:
    """
    Responsável por transformar o código-fonte (string) em uma sequência de Tokens.
    """

    def __init__(self, source: str):
        self.r = Reader(source)
        # Requisitos 2, 5: Tabela para tokens de um único caractere
        self.single_char = {
            "+": TokenType.PLUS,  # Requisito 2a
            "-": TokenType.MINUS,  # Requisito 2b
            "*": TokenType.STAR,  # Requisito 2c
            "(": TokenType.LPAREN,  # Requisito 5a
            ")": TokenType.RPAREN,  # Requisito 5b
        }

    def __iter__(self):
        """Permite iterar sobre o lexer para obter todos os tokens."""
        while True:
            tok = self.next_token()
            yield tok
            if tok.type == TokenType.EOF:
                break

    def next_token(self) -> Token:
        """
        Função principal que determina o próximo token no fluxo.
        """
        self._skip_whitespace()  # Ignora espaços em branco

        if self.r.is_at_end():
            return Token(TokenType.EOF, "", self.r.line, self.r.col)

        line, col = self.r.line, self.r.col
        c = self.r.peek()

        # Requisito 8: Comentário de Linha Única (#)
        if c == '#':
            self.r.advance()
            self._skip_line_comment()
            return self.next_token()  # Recomeça para ignorar o comentário

        # Requisito 2d (Divisão) e Requisito 8 (Comentário de Bloco /* */)
        if c == '/':
            if self.r.peek_next() == '*':
                self.r.advance()
                self.r.advance()
                self._skip_block_comment()
                return self.next_token()  # Recomeça para ignorar o comentário
            else:
                self.r.advance()
                return Token(TokenType.SLASH, "/", line, col)

        # Requisitos 1 e 7: Identificadores e Palavras Reservadas
        if self._is_identifier_start(c):
            return self._scan_identifier(line, col)

        # Requisito 6: Constantes Numéricas
        # Reconhece se começa com dígito (123, 123.456) OU ponto seguido de dígito (.456)
        if c.isdigit() or (c == '.' and self.r.peek_next().isdigit()):
            return self._scan_number(line, col)

        # Requisito 3 e 4f: Atribuição (=) e Igualdade (==)
        if c == "=":
            self.r.advance()
            if self.r.match("="):
                return Token(TokenType.EQUAL_EQUAL, "==", line, col)
            return Token(TokenType.ASSIGN, "=", line, col)

        # Requisito 4e: Diferente (!=) - Requisito 9 (Erro Léxico) se for só '!'
        if c == "!":
            self.r.advance()
            if self.r.match("="):
                return Token(TokenType.BANG_EQUAL, "!=", line, col)
            raise LexicalError("expected '=' after '!'", line, col)  # Requisito 9

        # Requisitos 4a e 4b: Maior (>) e Maior ou Igual (>=)
        if c == ">":
            self.r.advance()
            if self.r.match("="):
                return Token(TokenType.GREATER_EQUAL, ">=", line, col)
            return Token(TokenType.GREATER, ">", line, col)

        # Requisitos 4c e 4d: Menor (<) e Menor ou Igual (<=)
        if c == "<":
            self.r.advance()
            if self.r.match("="):
                return Token(TokenType.LESS_EQUAL, "<=", line, col)
            return Token(TokenType.LESS, "<", line, col)

        # Requisitos 2 e 5: Tokens de um único caractere
        if c in self.single_char:
            self.r.advance()
            return Token(self.single_char[c], c, line, col)

        # Requisito 9: Caractere Inválido
        self.r.advance()
        raise LexicalError(f"invalid character '{c}'", line, col)

    def _skip_whitespace(self):
        """Ignora espaços e tabulações, e lida com quebras de linha."""
        while True:
            c = self.r.peek()
            if c in " \t":
                self.r.advance()
                continue
            if self.r.consume_newline():
                continue
            break

    # Requisitos 1 e 7: Scanner de Identificador/Palavra Reservada
    def _scan_identifier(self, line: int, col: int) -> Token:
        """
        Consome caracteres que formam um identificador e verifica se é uma
        palavra reservada (Requisito 7).
        """
        buf = []
        while self._is_identifier_part(self.r.peek()):
            buf.append(self.r.advance())

        text = "".join(buf)
        if text in KEYWORDS:
            return Token(KEYWORDS[text], text, line, col)
        return Token(TokenType.IDENTIFIER, text, line, col)

    # Requisito 1: Lógica para início e continuação do identificador
    def _is_identifier_start(self, c: str) -> bool:
        """Verifica se o caractere pode iniciar um identificador (a-z, A-Z, _)."""
        return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_"

    def _is_identifier_part(self, c: str) -> bool:
        """Verifica se o caractere pode continuar um identificador (a-z, A-Z, _, 0-9)."""
        return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_" or c.isdigit()

    # Requisitos 6 e 9: Scanner de Números com Ponto Decimal
    def _scan_number(self, line: int, col: int) -> Token:
        """
        Reconhece constantes numéricas, incluindo decimais, e aplica as
        restrições de formato (Requisito 6).
        """
        buf = []

        # 1. Consome dígitos da parte inteira
        while self.r.peek().isdigit():
            buf.append(self.r.advance())

        # 2. Verifica o ponto decimal
        if self.r.peek() == '.':

            # Checa os casos inválidos: '1.' (parte inteira existe, mas sem decimal)
            if not self.r.peek_next().isdigit():
                if len(buf) > 0:
                    # Inválido: 1., 12., 156. (termina com ponto) - Requisito 6
                    raise LexicalError(f"invalid numeric literal ending with a dot", line, col)
                else:
                    # Inválido: '.' (ponto sem nada antes ou depois) - Requisito 9
                    raise LexicalError(f"invalid numeric literal starting with a dot without a number after", line, col)

            # Consome o ponto (válido se for: 1.23 ou .456)
            buf.append(self.r.advance())

            # 3. Consome dígitos da parte fracionária
            while self.r.peek().isdigit():
                buf.append(self.r.advance())

        text = "".join(buf)
        if not text:
            # Caso de erro que não foi pego no 'next_token'
            raise LexicalError(f"invalid numeric literal", line, col)

        return Token(TokenType.NUMBER, text, line, col)

    # Requisito 8: Comentário de Linha Única
    def _skip_line_comment(self):
        """Ignora todos os caracteres até o final da linha."""
        while not self.r.is_at_end() and self.r.peek() not in "\n\r":
            self.r.advance()

    # Requisitos 8 e 9: Comentário de Múltiplas Linhas
    def _skip_block_comment(self):
        """
        Ignora todos os caracteres até encontrar '*/'. Lança erro se não for fechado (Requisito 9).
        """
        start_line, start_col = self.r.line, self.r.col
        while not self.r.is_at_end():
            if self.r.peek() == "*" and self.r.peek_next() == "/":
                self.r.advance()  # Consome '*'
                self.r.advance()  # Consome '/'
                return
            # Se não é o fim do comentário, consome o próximo caractere.
            # consume_newline lida com quebras de linha e atualiza linha/col.
            self.r.consume_newline() or self.r.advance()

        # Requisito 9: Erro de Comentário Não Terminado
        raise LexicalError("Unterminated block comment", start_line, start_col)