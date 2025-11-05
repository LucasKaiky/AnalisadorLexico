from .tokens import TokenType

KEYWORDS = {
    # Gramática (PT-BR)
    "DECLARACOES": TokenType.DECLARACOES,
    "ALGORITMO": TokenType.ALGORITMO,
    "LER": TokenType.LER,
    "IMPRIMIR": TokenType.IMPRIMIR,
    "SE": TokenType.SE,
    "ENTAO": TokenType.ENTAO,
    "SENAO": TokenType.SENAO,
    "ENQUANTO": TokenType.ENQUANTO,
    "INICIO": TokenType.INICIO,
    "FIM": TokenType.FIM,
    "E": TokenType.E,
    "OU": TokenType.OU,
    "INTEIRO": TokenType.INTEIRO_TIPO,
    "REAL": TokenType.REAL_TIPO,

    # Aliases já existentes (opcional)
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
}