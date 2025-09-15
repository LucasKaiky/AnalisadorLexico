import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from minicompiler.lexer import Lexer
from minicompiler.tokens import TokenType

class TestLexerBasic(unittest.TestCase):
    def collect(self, text):
        return [t.type for t in Lexer(text)]

    def test_ops_and_parens(self):
        text = "a=b+c*(d-e)/f"
        types = self.collect(text)
        self.assertEqual(types, [
            TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.IDENTIFIER,
            TokenType.PLUS, TokenType.IDENTIFIER, TokenType.STAR,
            TokenType.LPAREN, TokenType.IDENTIFIER, TokenType.MINUS,
            TokenType.IDENTIFIER, TokenType.RPAREN, TokenType.SLASH,
            TokenType.IDENTIFIER, TokenType.EOF
        ])

    def test_rel_ops(self):
        text = "x==y x!=y x<=y x>=y x<y x>y"
        types = [t.type for t in Lexer(text) if t.type != TokenType.EOF]
        self.assertIn(TokenType.EQUAL_EQUAL, types)
        self.assertIn(TokenType.BANG_EQUAL, types)
        self.assertIn(TokenType.LESS_EQUAL, types)
        self.assertIn(TokenType.GREATER_EQUAL, types)
        self.assertIn(TokenType.LESS, types)
        self.assertIn(TokenType.GREATER, types)

if __name__ == "__main__":
    unittest.main()
