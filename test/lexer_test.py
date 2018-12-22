import unittest
import sys
sys.path.append("../src/")
from monkey.tokens import token
from monkey.lexer import lexer

class LexerTest(unittest.TestCase):

    def setUp(self):
        self.source = '''let five = 5;
                    let ten = 10;

                    let add = fn(x, y) {
                    x + y;
                    };

                    let result = add(five, ten);
                    !-/*5;
                    5 < 10 > 5;

                    if (5 < 10) {
                        return true;
                    } else {
                        return false;
                    }

                    10 == 10;
                    10 != 9;
                    "foobar" 
                    "foo bar"
                    [1, 2];
                    macro(x, y) { 
                        x + y; 
                    };
                    '''
        self.lexer = lexer.new(self.source)
    
    def test_next_token(self):
        tests = [
            (token.LET, "let"),
            (token.IDENT, "five"),
            (token.ASSIGN, "="),
            (token.INT, "5"),
            (token.SEMICOLON, ";"),
            (token.LET, "let"),
            (token.IDENT, "ten"),
            (token.ASSIGN, "="),
            (token.INT, "10"),
            (token.SEMICOLON, ";"),
            (token.LET, "let"),
            (token.IDENT, "add"),
            (token.ASSIGN, "="),
            (token.FUNCTION, "fn"),
            (token.LPAREN, "("),
            (token.IDENT, "x"),
            (token.COMMA, ","),
            (token.IDENT, "y"),
            (token.RPAREN, ")"),
            (token.LBRACE, "{"),
            (token.IDENT, "x"),
            (token.PLUS, "+"),
            (token.IDENT, "y"),
            (token.SEMICOLON, ";"),
            (token.RBRACE, "}"),
            (token.SEMICOLON, ";"),
            (token.LET, "let"),
            (token.IDENT, "result"),
            (token.ASSIGN, "="),
            (token.IDENT, "add"),
            (token.LPAREN, "("),
            (token.IDENT, "five"),
            (token.COMMA, ","),
            (token.IDENT, "ten"),
            (token.RPAREN, ")"),
            (token.SEMICOLON, ";"),
            (token.BANG, "!"),
            (token.MINUS, "-"),
            (token.SLASH, "/"),
            (token.ASTERISK, "*"),
            (token.INT, "5"),
            (token.SEMICOLON, ";"),
            (token.INT, "5"),
            (token.LT, "<"),
            (token.INT, "10"),
            (token.GT, ">"),
            (token.INT, "5"),
            (token.SEMICOLON, ";"),
            (token.IF, "if"),
            (token.LPAREN, "("),
            (token.INT, "5"),
            (token.LT, "<"),
            (token.INT, "10"),
            (token.RPAREN, ")"),
            (token.LBRACE, "{"),
            (token.RETURN, "return"),
            (token.TRUE, "true"),
            (token.SEMICOLON, ";"),
            (token.RBRACE, "}"),
            (token.ELSE, "else"),
            (token.LBRACE, "{"),
            (token.RETURN, "return"),
            (token.FALSE, "false"),
            (token.SEMICOLON, ";"),
            (token.RBRACE, "}"),
            (token.INT, "10"),
            (token.EQ, "=="),
            (token.INT, "10"),
            (token.SEMICOLON, ";"),
            (token.INT, "10"),
            (token.NOT_EQ, "!="),
            (token.INT, "9"),
            (token.SEMICOLON, ";"),
            (token.STRING, "foobar"),
            (token.STRING, "foo bar"),
            (token.LBRACKET, "["),
            (token.INT, "1"),
            (token.COMMA, ","),
            (token.INT, "2"),
            (token.RBRACKET, "]"),
            (token.SEMICOLON, ";"),
            (token.MACRO, "macro"), 
            (token.LPAREN, "("), 
            (token.IDENT, "x"), 
            (token.COMMA, ","), 
            (token.IDENT, "y"), 
            (token.RPAREN, ")"), 
            (token.LBRACE, "{"), 
            (token.IDENT, "x"), 
            (token.PLUS, "+"),
            (token.IDENT, "y"), 
            (token.SEMICOLON, ";"), 
            (token.RBRACE, "}"), 
            (token.SEMICOLON, ";"),
            (token.EOF, ""),
        ]
        for t in tests:
            tok = self.lexer.next_token()
            self.assertEqual(tok.Type, t[0], 
                msg="{} - tokentype wrong. expected={}, got={}".format(t, t[0], tok.Type))
            self.assertEqual(tok.Literal, t[1], 
                msg="{} - literal wrong. expected={}, got={}".format(t, t[1], tok.Literal))

if __name__ == '__main__':
    unittest.main()