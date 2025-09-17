import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from minicompiler.lexer import Lexer
from minicompiler.tokens import TokenType
from minicompiler.errors import LexicalError


class TestLexerBasic(unittest.TestCase):
    def collect(self, text):
        return [t.type for t in Lexer(text)]

    def collect_lexemes(self, text):
        return [t.lexeme for t in Lexer(text)]

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


    def test_valid_numbers(self):
        text = "123 123.456 .456"
        lexemes = self.collect_lexemes(text)
        self.assertIn("123", lexemes)
        self.assertIn("123.456", lexemes)
        self.assertIn(".456", lexemes)

    def test_invalid_numbers(self):
        for num in ["1.", "12.", "156."]:
            with self.assertRaises(LexicalError):
                list(Lexer(num))

    def test_keywords(self):
        text = "int float print if else"
        types = self.collect(text)
        self.assertIn(TokenType.INT, types)
        self.assertIn(TokenType.FLOAT, types)
        self.assertIn(TokenType.PRINT, types)
        self.assertIn(TokenType.IF, types)
        self.assertIn(TokenType.ELSE, types)


    def test_line_comment(self):
        text = "abc # this is a comment\n def"
        types = self.collect(text)
        self.assertEqual(types, [
            TokenType.IDENTIFIER, TokenType.IDENTIFIER, TokenType.EOF
        ])

    def test_block_comment(self):
        text = "abc /* a \n multiline comment */ def"
        types = self.collect(text)
        self.assertEqual(types, [
            TokenType.IDENTIFIER, TokenType.IDENTIFIER, TokenType.EOF
        ])

    def test_unterminated_block_comment(self):
        text = "abc /* no end"
        with self.assertRaises(LexicalError):
            list(Lexer(text))
    def test_invalid_characters(self):
        for char in ["@", "`", "´", "ç", "¨"]:
            with self.assertRaises(LexicalError):
                list(Lexer(char))


if __name__ == "__main__":
    unittest.main()
