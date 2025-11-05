from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Identificadores e literais
    IDENTIFIER = auto()
    INT_LIT = auto()
    FLOAT_LIT = auto()
    STRING = auto()

    # Operadores e símbolos
    PLUS = auto(); 
    MINUS = auto(); 
    STAR = auto(); 
    SLASH = auto()
    ASSIGN = auto()
    GREATER = auto(); 
    GREATER_EQUAL = auto()
    LESS = auto(); 
    LESS_EQUAL = auto()
    BANG_EQUAL = auto();
    EQUAL_EQUAL = auto()
    LPAREN = auto();
    RPAREN = auto()
    COLON = auto()
    EOF = auto()

    # Palavras-chave em PT-BR (gramática)
    DECLARACOES = auto(); 
    ALGORITMO = auto()
    LER = auto();
    IMPRIMIR = auto()
    SE = auto(); 
    ENTAO = auto(); 
    SENAO = auto()
    ENQUANTO = auto()
    INICIO = auto(); 
    FIM = auto()
    E = auto(); 
    OU = auto()
    INTEIRO_TIPO = auto(); 
    REAL_TIPO = auto()

    # Palavras-chave já existentes (mantidas como alias)
    PRINT = auto();
    IF = auto(); 
    ELSE = auto()

@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
