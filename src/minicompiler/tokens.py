from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    BANG_EQUAL = auto()
    EQUAL_EQUAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    NUMBER = auto()
    EOF = auto()
    INT = auto()
    FLOAT = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()

@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
