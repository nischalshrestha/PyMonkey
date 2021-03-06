import unittest
import sys
sys.path.append("../src/")
from monkey.object import *
from monkey import lexer
from monkey import parser
from monkey.evaluator import evaluator as e

class TestQuote(unittest.TestCase):

    def check_eval(self, source):
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        env = e.new_environment()
        return e.Eval(program, env)

    def test_quote(self):
        tests = [
            ('quote(5)', '5'),
            ('quote(5 + 8)', '(5 + 8)'),
            ('quote(foobar)', 'foobar'),
            ('quote(foobar + barfoo)', '(foobar + barfoo)')
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            quote = evaluated
            self.assertTrue(isinstance(quote, Quote), 
                f'expected Quote. got={type(quote)} {quote}')
            self.assertIsNotNone(quote, 'quote.Node is None')
            self.assertEqual(quote.node.string(), t[1], 
                'not equal. got={} want={}'.format(quote.node.string(), t[1]))

    def test_quote_unquote(self):
        tests = [
            ('quote(unquote(4))', '4'),
            ('quote(unquote(4 + 4))', '8'),
            ('quote(8 + unquote(4 + 4))', '(8 + 8)'),
            ('quote(unquote(4 + 4) + 8)', '(8 + 8)'),
            ('let foobar = 8; quote(foobar)', 'foobar'),
            ('let foobar = 8; quote(unquote(foobar))', '8'),
            ('quote(unquote(true))', 'true'),
            ('quote(unquote(true == false))', 'false'),
            ('quote(unquote(quote(4 + 4)))', '(4 + 4)'),
            (
                '''let quotedInfixExpression = quote(4 + 4); 
                quote(unquote(4 + 4) + unquote(quotedInfixExpression))''', 
                '(8 + (4 + 4))'
            ),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            quote = evaluated
            self.assertTrue(isinstance(quote, Quote), 
                f'expected Quote. got={type(quote)} {quote}')
            self.assertIsNotNone(quote, 'quote.Node is None')
            self.assertEqual(quote.node.string(), t[1], 
                'not equal. got={} want={}'.format(quote.node.string(), t[1]))

if __name__ == '__main__':
    unittest.main()
    