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
        bad_source = 'let x 5; let = 10; let 838383;'
        tests = [
            ("let x = 5;", "x", 5),
            ("let y = 10;", "y", 10),
            ("let foobar = 838383;", "foobar", 838383),
        ]
        # l = lexer.new(bad_source)
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        if program == None:
            print('parse_program() returned None')
            return
        if len(program.statements) != 3:
            print('program.statements does not contain 3 statements. got={}'.format(len(program.statements)))
            return
        for i, t in enumerate(tests):
            s = program.statements[i]
            self.assertTrue(self.is_let_statement(s, t[1]))

    def check_parse_errors(self, p):
        errors = p.errors
        if len(errors) == 0:
            return
        print('parser has {} errors'.format(len(errors)))
        for e in errors:
            print('parser error: {}'.format(e))
        self.fail()

    # helper test function for test_let_statements
    def is_let_statement(self, s, name):
        # ignores values for now
        if s.token_literal() != 'let':
            print("s.token_literal not 'let'. got={}".format(s.token_literal()))
            return False
        if type(s) != ast.LetStatement:
            print("s is not a ast.LetStatement. got={}".format(type(s)))
            return False
        if s.name.value != name:
            print("statement s value is not {}. got={}".format(name, s.name.value))
            return False
        if s.name.token_literal() != name:
            print("statement s token is not {}. got={}".format(name, s.name.token_literal()))
            return False
        return True
    
    def test_return_statements(self):
        source = 'return 5; return 10; return 993322;'
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        if len(program.statements) != 3:
            print('program.statements does not contain 3 statements. got={}'.format(len(program.statements)))
            return
        for s in program.statements:
            if type(s) != ast.ReturnStatement:
                self.fail("s is not a ast.ReturnStatement. got={}".format(type(s)))
            if s.token_literal() != "return":
                print("statement s token not 'return'. got={}".format(s.token_literal()))
    
    def test_identifier_expression(self):
        source = 'foobar;'
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        self.assertEqual(len(program.statements), 1, 
            msg='program does not have enough statements. got={}'.format(len(program.statements)))
        stmt = program.statements[0]
        self.assertEqual(type(stmt), ast.ExpressionStatement,
            msg='program.statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        ident = stmt.expression
        self.assertEqual(type(ident), ast.Identifier,
            msg='exp not ast.Identifier. got={}'.format(type(ident)))
        self.assertEqual(ident.value, 'foobar',
            msg='ident.value not {}. got={}'.format('foobar', ident.value))
        self.assertEqual(ident.token_literal(), 'foobar',
            msg='ident.token_literal not {}. got={}'.format('foobar', ident.token_literal()))
    
    def test_integer_literal_expression(self):
        source = '5;'
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        self.assertEqual(len(program.statements), 1, 
            msg='program does not have enough statements. got={}'.format(len(program.statements)))
        stmt = program.statements[0]
        self.assertEqual(type(stmt), ast.ExpressionStatement,
            msg='program.statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        literal = stmt.expression
        self.assertEqual(type(literal), ast.IntegerLiteral,
            msg='exp not ast.IntegerLiteral. got={}'.format(type(literal)))
        self.assertEqual(literal.value, 5,
            msg='ident.value not {}. got={}'.format('5', literal.value))
        self.assertEqual(literal.token_literal(), '5',
            msg='ident.token_literal not {}. got={}'.format('5', literal.token_literal()))

    def is_integer_literal(self, il, value):
        integ = il
        if type(integ) != ast.IntegerLiteral:
            print('il not ast.IntegerLiteral. got={}'.format(type(integ)))
            return False
        if integ.value != value:
            print('integ.value not {}. got={}'.format(value, integ.value))
            return False
        if integ.token_literal() != str(value):
            print('integ.token_literal not {}. got={}'.format(value, integ.token_literal()))
            return False
        return True
    
    def test_parsing_prefix_expressions(self):
        prefix_tests = [
            ("!5;", "!", 5),
            ("-15;", "-", 15)
        ]
        for t in prefix_tests:
            l = lexer.new(t[0])
            p = parser.new(l)
            program = p.parse_program()
            self.check_parse_errors(p)
            self.assertEqual(len(program.statements), 1, 
                msg='program does not have enough statements. got={}'.format(len(program.statements)))
            stmt = program.statements[0]
            self.assertEqual(type(stmt), ast.ExpressionStatement,
                msg='program.statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
            exp = stmt.expression
            self.assertEqual(type(exp), ast.PrefixExpression,
                msg='exp not ast.PrefixExpression. got={}'.format(type(exp)))
            self.assertEqual(exp.operator, t[1],
                msg='exp.operator not {}. got={}'.format(t[1], exp.operator))
            self.assertTrue(self.is_integer_literal(exp.right, t[2]))
    
    def test_parsing_infix_expressions(self):
        infix_tests = [
            ("5 + 5;", 5, "+", 5),
            ("5 - 5;", 5, "-", 5),         
            ("5 * 5;", 5, "*", 5),         
            ("5 / 5;", 5, "/", 5),         
            ("5 > 5;", 5, ">", 5),         
            ("5 < 5;", 5, "<", 5),         
            ("5 == 5;", 5, "==", 5),         
            ("5 != 5;", 5, "!=", 5),
        ]
        for t in infix_tests:
            l = lexer.new(t[0])
            p = parser.new(l)
            program = p.parse_program()
            self.check_parse_errors(p)
            self.assertEqual(len(program.statements), 1, 
                msg='program does not have enough statements. got={}'.format(len(program.statements)))
            stmt = program.statements[0]
            self.assertEqual(type(stmt), ast.ExpressionStatement,
                msg='program.statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
            exp = stmt.expression
            self.assertEqual(type(exp), ast.InfixExpression,
                msg='exp not ast.InfixExpression. got={}'.format(type(exp)))
            self.assertTrue(self.is_integer_literal(exp.left, t[1]))
            self.assertEqual(exp.operator, t[2],
                msg='exp.operator not {}. got={}'.format(t[2], exp.operator))
            self.assertTrue(self.is_integer_literal(exp.right, t[1]))

    def test_operator_precedence_parsing(self):
        tests = [
            ("-a * b", "((-a) * b)"), 
            ( "!-a", "(!(-a))"), 
            ("a + b + c", "((a + b) + c)"),
            ("a + b - c", "((a + b) - c)"), 
            ("a * b * c", "((a * b) * c)"), 
            ("a * b / c", "((a * b) / c)"), 
            ("a + b / c", "(a + (b / c))"),
            ("a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"), 
            ("3 + 4; -5 * 5", "(3 + 4)((-5) * 5)"), 
            ("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),
            ("5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"), 
            ("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
        ]
        for t in tests:
            l = lexer.new(t[0])
            p = parser.new(l)
            program = p.parse_program()
            self.check_parse_errors(p)
            actual = program.string()
            self.assertEqual(actual, t[1],
                msg='expected={}, got={}'.format(t[1], actual))

if __name__ == '__main__':
    unittest.main()