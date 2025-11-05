from __future__ import annotations
import sys
import argparse

from .lexer import Lexer
from .tokens import TokenType
from .errors import LexicalError
from .parser import Parser
from .errors import SyntacticError

class SyntacticError(Exception):
    pass

EXIT_OK = 0
EXIT_NOT_FOUND = 2
EXIT_LEXICAL = 1
EXIT_SYNTACTIC = 1  

# Funções de execução 
def run_lex(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    lexer = Lexer(source)
    for tok in lexer:
        print(f"{tok.type.name} '{tok.lexeme}' @ {tok.line}:{tok.column}")
        if tok.type == TokenType.EOF:
            break


def run_parse(path: str):
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    parser = Parser(Lexer(source))
    tree = parser.parse_programa()

    print("OK: sintaxe válida.")
    return tree


# COnfiguração da linha de comando
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
        if args.parse:
            run_parse(args.path)
        else:
            run_lex(args.path)

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
