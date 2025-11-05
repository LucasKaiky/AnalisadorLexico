"""
MiniCompiler - CLI (Lexer/Parser)

Como usar (exemplos):

  # 1) Somente análise léxica (padrão)
  python -m minicompiler.main ..examples/programa_checkpoint2.mc

  # 2) Análise sintática (requer parser.py com Parser.parse_programa)
  python -m minicompiler.main --parse ..examples/programa_checkpoint2.mc

Dica: execute os comandos a partir da RAIZ do projeto (onde ficam as pastas
`minicompiler/` e `examples/`) para que os imports relativos funcionem.
"""

from __future__ import annotations
import sys
import argparse

# Importa sempre o léxico (já existente)
from .lexer import Lexer
from .tokens import TokenType
from .errors import LexicalError
from .parser import Parser
from .errors import SyntacticError

# Classe de fallback apenas para tipagem e captura uniforme de erros.
class SyntacticError(Exception):
    pass

# Códigos de saída padronizados
EXIT_OK = 0
EXIT_NOT_FOUND = 2
EXIT_LEXICAL = 1
EXIT_SYNTACTIC = 1  # mesma convenção do léxico (1) para erro sintático

# Funções de execução (separadas para facilitar testes e manutenção)
def run_lex(path: str) -> None:
    """
    Executa SOMENTE a análise léxica e imprime os tokens em stdout.
    Útil para depuração do lexer (Checkpoint 1).
    """
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    lexer = Lexer(source)
    for tok in lexer:
        # Formato de saída padronizado: TIPO 'lexema' @ linha:coluna
        print(f"{tok.type.name} '{tok.lexeme}' @ {tok.line}:{tok.column}")
        if tok.type == TokenType.EOF:
            break


def run_parse(path: str):
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    parser = Parser(Lexer(source))
    # Ponto ÚNICO de entrada do parser (bom para explicar e testar)
    tree = parser.parse_programa()

    # Saída mínima e objetiva (pode trocar por um pretty-print da AST se quiser)
    print("OK: sintaxe válida.")
    return tree


# CLI - construção do argparse (coeso e limpo)
def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="minicompiler",
        description="MiniCompiler - Análise léxica e sintática",
    )

    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--lex",
        action="store_true",
        help="Executa somente a análise léxica (padrão).",
    )
    mode.add_argument(
        "--parse",
        action="store_true",
        help="Executa a análise sintática (requer parser.py).",
    )

    p.add_argument(
        "path",
        metavar="FILE",
        help="Caminho para o arquivo-fonte (.mc) a ser analisado.",
    )
    return p

# Função principal
def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    try:
        # Decisão do modo: se --parse foi usado, roda parser; senão, apenas léxico.
        if args.parse:
            run_parse(args.path)
        else:
            run_lex(args.path)

    # Tratamento de erros mais comuns, com mensagens explícitas e códigos padronizados
    except FileNotFoundError:
        print(f"file not found: {args.path}", file=sys.stderr)
        sys.exit(EXIT_NOT_FOUND)
    except UnicodeDecodeError as e:
        print(f"Encoding error ao ler o arquivo: {e}", file=sys.stderr)
        sys.exit(EXIT_NOT_FOUND)
    except LexicalError as e:
        print(f"LexicalError: {e}", file=sys.stderr)
        sys.exit(EXIT_LEXICAL)
    except SyntacticError as e:
        print(f"SyntacticError: {e}", file=sys.stderr)
        sys.exit(EXIT_SYNTACTIC)


if __name__ == "__main__":
    main()
