import unittest
import sys
sys.path.append("../src/monkey")
import tokens
import lexer

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
                    '''
        self.lexer = lexer.new(self.source)
    
    def test_next_token(self):
        tests = [
            (tokens.LET, "let"),
            (tokens.IDENT, "five"),
            (tokens.ASSIGN, "="),
            (tokens.INT, "5"),
            (tokens.SEMICOLON, ";"),
            (tokens.LET, "let"),
            (tokens.IDENT, "ten"),
            (tokens.ASSIGN, "="),
            (tokens.INT, "10"),
            (tokens.SEMICOLON, ";"),
            (tokens.LET, "let"),
            (tokens.IDENT, "add"),
            (tokens.ASSIGN, "="),
            (tokens.FUNCTION, "fn"),
            (tokens.LPAREN, "("),
            (tokens.IDENT, "x"),
            (tokens.COMMA, ","),
            (tokens.IDENT, "y"),
            (tokens.RPAREN, ")"),
            (tokens.LBRACE, "{"),
            (tokens.IDENT, "x"),
            (tokens.PLUS, "+"),
            (tokens.IDENT, "y"),
            (tokens.SEMICOLON, ";"),
            (tokens.RBRACE, "}"),
            (tokens.SEMICOLON, ";"),
            (tokens.LET, "let"),
            (tokens.IDENT, "result"),
            (tokens.ASSIGN, "="),
            (tokens.IDENT, "add"),
            (tokens.LPAREN, "("),
            (tokens.IDENT, "five"),
            (tokens.COMMA, ","),
            (tokens.IDENT, "ten"),
            (tokens.RPAREN, ")"),
            (tokens.SEMICOLON, ";"),
            (tokens.BANG, "!"),
            (tokens.MINUS, "-"),
            (tokens.SLASH, "/"),
            (tokens.ASTERISK, "*"),
            (tokens.INT, "5"),
            (tokens.SEMICOLON, ";"),
            (tokens.INT, "5"),
            (tokens.LT, "<"),
            (tokens.INT, "10"),
            (tokens.GT, ">"),
            (tokens.INT, "5"),
            (tokens.SEMICOLON, ";"),
            (tokens.IF, "if"),
            (tokens.LPAREN, "("),
            (tokens.INT, "5"),
            (tokens.LT, "<"),
            (tokens.INT, "10"),
            (tokens.RPAREN, ")"),
            (tokens.LBRACE, "{"),
            (tokens.RETURN, "return"),
            (tokens.TRUE, "true"),
            (tokens.SEMICOLON, ";"),
            (tokens.RBRACE, "}"),
            (tokens.ELSE, "else"),
            (tokens.LBRACE, "{"),
            (tokens.RETURN, "return"),
            (tokens.FALSE, "false"),
            (tokens.SEMICOLON, ";"),
            (tokens.RBRACE, "}"),
            (tokens.INT, "10"),
            (tokens.EQ, "=="),
            (tokens.INT, "10"),
            (tokens.SEMICOLON, ";"),
            (tokens.INT, "10"),
            (tokens.NOT_EQ, "!="),
            (tokens.INT, "9"),
            (tokens.SEMICOLON, ";"),
            (tokens.EOF, "")
        ]
        for t in tests:
            tok = self.lexer.next_token()
            self.assertEqual(tok.Type, t[0], 
                msg="{} - tokentype wrong. expected={}, got={}".format(t, t[0], tok.Type))
            self.assertEqual(tok.Literal, t[1], 
                msg="{} - literal wrong. expected={}, got={}".format(t, t[1], tok.Literal))

if __name__ == '__main__':
    unittest.main()