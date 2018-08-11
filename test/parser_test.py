import unittest
import sys
sys.path.append("../src/")
from monkey import token
from monkey import lexer
from monkey import ast
from monkey import parser

class ParserTest(unittest.TestCase):

    def test_let_statements(self):
        # tests = [
        #     ("let x = 5;", "x", 5),
        #     ("let y = true;", "y", True),
        #     ("let foobar = y;", "foobar", "y"),
        # ]
        source = 'let x = 5; let y = 10; let foobar = 838383;'
        tests = [
            ("let x = 5;", "x", 5),
            ("let y = 10;", "y", 10),
            ("let foobar = 838383;", "foobar", 838383),
        ]
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        if program == None:
            print('parse_program() returned None')
            return
        if len(program.statements) != 3:
            print('program.statements does not contain 3 statements. got={}'.format(len(program.statements)))
            return
        for i, t in enumerate(tests):
            s = program.statements[i]
            print(t[1])
            assertTrue(is_let_statement(s, t[1]))

    def is_let_statement(s, name):
        if s.token_literal() != 'let':
            print("s.token_literal not 'let'. got={}".format(s.token_literal()))
            return False
        if type(s) != type(ast.LetStatement):
            print("s is not a 'ast.LetStatement'. got={}".format(s))
            return False
        if s.name.value != name:
            print("statement s value is not {}. got={}".format(name, s.name.value))
            return False
        if s.name.token_literal() != name:
            print("statement s token is not {}. got={}".format(name, s.name.token_literal()))
            return False
        return True

    

if __name__ == '__main__':
    unittest.main()