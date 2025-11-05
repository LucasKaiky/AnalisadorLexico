# parser.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Iterable
from .tokens import TokenType, Token
from .errors import SyntacticError


# AST simples e didática
@dataclass
class ASTNode:
    kind: str
    value: Optional[str] = None
    children: List["ASTNode"] = field(default_factory=list)

    def add(self, *nodes: "ASTNode") -> "ASTNode":
        self.children.extend(nodes)
        return self

    def __repr__(self) -> str:
        v = f":{self.value}" if self.value is not None else ""
        return f"<{self.kind}{v} {len(self.children)} filhos>"


def pretty_print(node: ASTNode, indent: int = 0) -> None:
    """Imprime a AST com indentação."""
    pad = "  " * indent
    header = node.kind if node.value is None else f"{node.kind}: {node.value}"
    print(f"{pad}{header}")
    for c in node.children:
        pretty_print(c, indent + 1)


class Parser:
    """Parser recursivo-descendente para a gramática do checkpoint."""

    def __init__(self, lexer: Iterable[Token]):
        self.tokens: List[Token] = list(lexer)
        self.i: int = 0

    # Helpers de token
    def _peek(self) -> Token:
        return self.tokens[self.i]

    def _previous(self) -> Token:
        return self.tokens[self.i - 1]

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.i += 1
        return self.tokens[self.i - 1]

    def _check(self, *types: TokenType) -> bool:
        """True se o token atual for de um dos tipos (inclui EOF)."""
        return self._peek().type in types

    def _match(self, *types: TokenType) -> bool:
        """Consome se for um dos tipos; nunca consome EOF."""
        if (not self._is_at_end()) and self._peek().type in types:
            self._advance()
            return True
        return False

    def _consume(self, ttype: TokenType, msg: str) -> Token:
        if self._check(ttype):
            return self._advance()
        tk = self._peek()
        raise SyntacticError(f"{msg}. Encontrado {tk.type.name} '{tk.lexeme}'", tk.line, tk.column)


    # programa : ':' DECLARACOES listaDeclaracoes ':' ALGORITMO listaComandos EOF
    def parse_programa(self) -> ASTNode:
        root = ASTNode("programa")
        self._consume(TokenType.COLON, "Esperava ':' antes de DECLARACOES")
        self._consume(TokenType.DECLARACOES, "Esperava 'DECLARACOES'")
        root.add(self.lista_declaracoes())
        self._consume(TokenType.COLON, "Esperava ':' antes de ALGORITMO")
        self._consume(TokenType.ALGORITMO, "Esperava 'ALGORITMO'")
        root.add(self.lista_comandos())
        self._consume(TokenType.EOF, "Esperava fim do arquivo")
        return root

    # listaDeclaracoes : declaracao+
    def lista_declaracoes(self) -> ASTNode:
        node = ASTNode("listaDeclaracoes")
        while self._check(TokenType.IDENTIFIER):
            node.add(self.declaracao())
        return node

    # declaracao : IDENTIFIER ':' tipoVar
    def declaracao(self) -> ASTNode:
        node = ASTNode("declaracao")
        ident = self._consume(TokenType.IDENTIFIER, "Esperava nome de variável na declaração")
        self._consume(TokenType.COLON, "Esperava ':' depois do nome da variável")
        tipo = self.tipo_var()
        return node.add(ASTNode("id", ident.lexeme), tipo)

    # tipoVar : INTEIRO | REAL
    def tipo_var(self) -> ASTNode:
        if self._match(TokenType.INTEIRO_TIPO): return ASTNode("tipo", "INTEIRO")
        if self._match(TokenType.REAL_TIPO):    return ASTNode("tipo", "REAL")
        t = self._peek(); raise SyntacticError("Esperava tipo 'INTEIRO' ou 'REAL'", t.line, t.column)

    # expressaoAritmetica : termo (('+'|'-') termo)*
    def expressao_aritmetica(self) -> ASTNode:
        node = self.termo_aritmetico()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous()
            rhs = self.termo_aritmetico()
            node = ASTNode("binop", op.lexeme, [node, rhs])
        return node

    # termo : fator (('*'|'/') fator)*
    def termo_aritmetico(self) -> ASTNode:
        node = self.fator_aritmetico()
        while self._match(TokenType.STAR, TokenType.SLASH):
            op = self._previous()
            rhs = self.fator_aritmetico()
            node = ASTNode("binop", op.lexeme, [node, rhs])
        return node

    # fator : INT_LIT | FLOAT_LIT | IDENTIFIER | '(' expressaoAritmetica ')'
    def fator_aritmetico(self) -> ASTNode:
        t = self._peek()
        if self._match(TokenType.INT_LIT):   return ASTNode("int", self._previous().lexeme)
        if self._match(TokenType.FLOAT_LIT): return ASTNode("float", self._previous().lexeme)
        if self._match(TokenType.IDENTIFIER):return ASTNode("var", self._previous().lexeme)
        if self._match(TokenType.LPAREN):
            expr = self.expressao_aritmetica()
            self._consume(TokenType.RPAREN, "Esperava ')' após expressão")
            return expr
        raise SyntacticError("Esperava número, variável ou '('", t.line, t.column)

    # termoRel : expressaoAritmetica OP_REL expressaoAritmetica | '(' expressaoRelacional ')'
    def termo_relacional(self) -> ASTNode:
        if self._match(TokenType.LPAREN):
            inner = self.expressao_relacional()
            self._consume(TokenType.RPAREN, "Esperava ')' após expressão relacional")
            return inner
        left = self.expressao_aritmetica()
        if self._match(
            TokenType.GREATER, TokenType.GREATER_EQUAL,
            TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL
        ):
            op = self._previous()
        else:
            t = self._peek(); raise SyntacticError("Esperava operador relacional", t.line, t.column)
        right = self.expressao_aritmetica()
        return ASTNode("relop", op.lexeme, [left, right])

    # expressaoRelacional : termoRel ((E|OU) termoRel)*
    def expressao_relacional(self) -> ASTNode:
        node = self.termo_relacional()
        while self._match(TokenType.E, TokenType.OU):
            op = self._previous()
            rhs = self.termo_relacional()
            node = ASTNode("boolop", op.lexeme, [node, rhs])
        return node

    # listaComandos : comando+      (pára em FIM, SENAO ou EOF)
    def lista_comandos(self) -> ASTNode:
        node = ASTNode("listaComandos")
        while not self._is_at_end() and self._peek().type not in (TokenType.FIM, TokenType.SENAO):
            node.add(self.comando())
        return node

    # comando : atribuicao | entrada | saida | condicao | repeticao | subAlgoritmo
    def comando(self) -> ASTNode:
        t = self._peek().type
        if t == TokenType.IDENTIFIER:                 return self.comando_atribuicao()
        if t == TokenType.LER:                        return self.comando_entrada()
        if t in (TokenType.IMPRIMIR, TokenType.PRINT):return self.comando_saida()
        if t == TokenType.SE:                         return self.comando_condicao()
        if t == TokenType.ENQUANTO:                   return self.comando_repeticao()
        if t == TokenType.INICIO:                     return self.sub_algoritmo()
        tk = self._peek(); raise SyntacticError("Comando inválido", tk.line, tk.column)

    # comandoAtribuicao : IDENTIFIER '=' expressaoAritmetica
    def comando_atribuicao(self) -> ASTNode:
        ident = self._consume(TokenType.IDENTIFIER, "Esperava identificador no comando de atribuição")
        self._consume(TokenType.ASSIGN, "Esperava '='")
        expr = self.expressao_aritmetica()
        return ASTNode("atribuicao").add(ASTNode("var", ident.lexeme), expr)

    # comandoEntrada : LER IDENTIFIER
    def comando_entrada(self) -> ASTNode:
        self._consume(TokenType.LER, "Esperava 'LER'")
        ident = self._consume(TokenType.IDENTIFIER, "Esperava identificador após LER")
        return ASTNode("ler", ident.lexeme)

    # comandoSaida : (IMPRIMIR|print) '(' (IDENTIFIER|STRING) ')'
    def comando_saida(self) -> ASTNode:
        if not (self._match(TokenType.IMPRIMIR) or self._match(TokenType.PRINT)):
            t = self._peek(); raise SyntacticError("Esperava IMPRIMIR/print", t.line, t.column)
        self._consume(TokenType.LPAREN, "Esperava '(' após IMPRIMIR/print")
        if self._match(TokenType.IDENTIFIER):
            arg = ASTNode("var", self._previous().lexeme)
        elif self._match(TokenType.STRING):
            arg = ASTNode("string", self._previous().lexeme)
        else:
            t = self._peek(); raise SyntacticError("Esperava variável ou string em IMPRIMIR/print", t.line, t.column)
        self._consume(TokenType.RPAREN, "Esperava ')' após argumento")
        return ASTNode("imprimir", None, [arg])

    # comandoCondicao : SE expressaoRelacional ENTAO comando (SENAO comando)?
    def comando_condicao(self) -> ASTNode:
        self._consume(TokenType.SE, "Esperava 'SE'")
        cond = self.expressao_relacional()
        self._consume(TokenType.ENTAO, "Esperava 'ENTAO'")
        then_cmd = self.comando()
        if self._match(TokenType.SENAO):
            else_cmd = self.comando()
            return ASTNode("if", None, [cond, then_cmd, else_cmd])
        return ASTNode("if", None, [cond, then_cmd])

    # comandoRepeticao : ENQUANTO expressaoRelacional comando
    def comando_repeticao(self) -> ASTNode:
        self._consume(TokenType.ENQUANTO, "Esperava 'ENQUANTO'")
        cond = self.expressao_relacional()
        body = self.comando()
        return ASTNode("enquanto", None, [cond, body])

    # subAlgoritmo : INICIO listaComandos FIM
    def sub_algoritmo(self) -> ASTNode:
        self._consume(TokenType.INICIO, "Esperava 'INICIO'")
        body = self.lista_comandos()
        self._consume(TokenType.FIM, "Esperava 'FIM'")
        return ASTNode("bloco", None, [body])
