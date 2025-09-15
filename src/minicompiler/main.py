import sys
from .lexer import Lexer
from .tokens import TokenType
from .errors import LexicalError

def run_source(source: str):
    lexer = Lexer(source)
    for tok in lexer:
        print(f"{tok.type.name} '{tok.lexeme}' @ {tok.line}:{tok.column}")
        if tok.type == TokenType.EOF:
            break

def main():
    if len(sys.argv) < 2:
        print("usage: python -m minicompiler.main <file.mc>")
        sys.exit(2)
    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            run_source(f.read())
    except FileNotFoundError:
        print(f"file not found: {path}")
        sys.exit(2)
    except LexicalError as e:
        print(f"LexicalError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
