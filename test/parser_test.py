import unittest
import sys
sys.path.append("../src/")
from monkey import token
from monkey import lexer
from monkey import ast
from monkey import parser

class ParserTest(unittest.TestCase):

    def test_let_statements(self):
        tests = [
            ("let x = 5;", "x", 5),
            ("let y = true;", "y", True),
            ("let foobar = y;", "foobar", "y"),
        ]
        source = 'let x = 5; let y = 10; let foobar = 838383;'
        bad_source = 'let x 5; let = 10; let 838383;'
        tests = [
            ("let x = 5;", "x", 5),
            ("let y = 10;", "y", 10),
            ("let foobar = 838383;", "foobar", 838383),
        ]
        for t in tests:
            # l = lexer.new(bad_source)
            l = lexer.new(t[0])
            p = parser.new(l)
            program = p.parse_program()
            self.check_parse_errors(p)
            if len(program.statements) != 1:
                self.fail('program.statements does not contain 3 statements. got={}'.format(len(program.statements)))
            stmt = program.statements[0]
            if not self.is_let_statement(stmt, t[1]):
                return
            val = stmt.value
            if not self.check_literal_expression(val, t[2]):
                return

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
        if s.token_literal() != 'let':
            print("s.token_literal not 'let'. got={}".format(s.token_literal()))
            return False
        if not type(s) is ast.LetStatement:
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
        expected = (5, 10, 993322)
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        if len(program.statements) != 3:
            print('program.statements does not contain 3 statements. got={}'.format(len(program.statements)))
            return
        for i, s in enumerate(program.statements):
            if not type(s) is ast.ReturnStatement:
                self.fail("s is not a ast.ReturnStatement. got={}".format(type(s)))
            if s.token_literal() != "return":
                print("statement s token not 'return'. got={}".format(s.token_literal()))
            if not self.check_literal_expression(s.return_value, expected[i]):
                return
    
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

    def check_integer_literal(self, il, value):
        integ = il
        if not type(integ) is ast.IntegerLiteral:
            print('il not ast.IntegerLiteral. got={}'.format(type(integ)))
            return False
        if integ.value != value:
            print('integ.value not {}. got={}'.format(value, integ.value))
            return False
        if integ.token_literal() != str(value):
            print('integ.token_literal not {}. got={}'.format(value, integ.token_literal()))
            return False
        return True
    
    def check_identifier(self, exp, value):
        if not type(exp) is ast.Identifier:
            print('exp is not ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('exp.value is {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('exp.token_literal is not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True
    
    def check_literal_expression(self, exp, expected):
        v = type(expected)
        if v is int:
            return self.check_integer_literal(exp, expected)
        elif v is str:
            return self.check_identifier(exp, expected)
        print('type of exp not handled. got={}'.format(type(expected)))
        return False

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
            if not self.check_literal_expression(exp.right, t[2]):
                print(exp.right)
                return
    
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
            if not self.check_infix_expression(stmt.expression, t[1], t[2], t[3]):
                print(stmt.expression)
                return

    def check_infix_expression(self, exp, left, operator, right):
        if not type(exp) is ast.InfixExpression:
            print('exp is not ast.InfixExpression. got={}'.format(type(exp)))
            return False
        opExp = exp
        if not self.check_literal_expression(opExp.left, left):
            return False
        if opExp.operator != operator:
            print('exp.operator is not {}. got={}'.format(operator, opExp.operator))
            return False
        if not self.check_literal_expression(opExp.right, right):
            return False
        return True

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
            ("-1 * 2 + 3", "(((-1) * 2) + 3)"),
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