import unittest
import sys
sys.path.append("../src/")
from monkey import token
from monkey import lexer
from monkey import ast
from monkey import parser

# TODO use isinstance() instead of type()
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
            if not self.check_let_statement(stmt, t[1]):
                return
            val = stmt.value
            if not self.check_literal_expression(val, t[2]):
                return

    # helper test function for test_let_statements
    def check_let_statement(self, s, name):
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
    
    def check_boolean_literal(self, exp, value):
        if not type(exp) is ast.Boolean:
            print('exp is not ast.Boolean. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('exp.value is {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != str(value).lower(): # this is bc bools in Python are caps
            print('exp.token_literal is not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True
    
    def test_string_literal_expression(self):
        source = '\"hello world\";'
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        stmt = program.statements[0]
        literal = stmt.expression
        self.assertEqual(type(literal), ast.StringLiteral,
            msg='exp not ast.StringLiteral. got={}'.format(type(literal)))
        self.assertEqual(literal.value, "hello world",
            msg='ident.value not {}. got={}'.format('hello world', literal.value))
    
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
        elif v is bool:
            return self.check_boolean_literal(exp, expected)
        print('type of exp not handled. got={}'.format(type(expected)))
        return False

    def test_parsing_prefix_expressions(self):
        prefix_tests = [
            ("!5;", "!", 5),
            ("-15;", "-", 15),
            ("!true;", "!", True),    
            ("!false;", "!", False),
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
            ("true == true", True, "==", True),
            ("true != false", True, "!=", False),         
            ("false == false", False, "==", False),
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
            ("true", "true"),
            ("false", "false"),
            ("3 > 5 == false", "((3 > 5) == false)"),
            ("3 < 5 == true", "((3 < 5) == true)"),
            ("1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"), 
            ("(5 + 5) * 2", "((5 + 5) * 2)"), 
            ("2 / (5 + 5)", "(2 / (5 + 5))"), 
            ("-(5 + 5)", "(-(5 + 5))"), 
            ("!(true == true)", "(!(true == true))"),
            ("a + add(b * c) + d", "((a + add((b * c))) + d)"), 
            ("add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))", "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))"), 
            ("add(a + b + c * d / f + g)", "add((((a + b) + ((c * d) / f)) + g))")
        ]
        for t in tests:
            l = lexer.new(t[0])
            p = parser.new(l)
            program = p.parse_program()
            self.check_parse_errors(p)
            actual = program.string()
            self.assertEqual(actual, t[1],
                msg='expected={}, got={}'.format(t[1], actual))
    
    def test_boolean_expression(self):
        tests = [
            ("true;", True),
            ("false;", False)
        ]
        for t in tests:
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
            if not type(exp) is ast.Boolean:
                print('exp is not ast.Boolean. got={}'.format(type(exp)))
            boolean = exp.value
            self.assertEqual(boolean, t[1],
                msg='boolean.value not {}. got={}'.format(t[1], boolean))

    def test_if_expression(self):
        # tests = [
        #     ("true;", True),
        #     ("false;", False)
        # ]
        source = 'if (x < y) { x }'
        # for t in tests:
        # l = lexer.new(t[0])
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        self.assertEqual(len(program.statements), 1, 
            msg='program does not have enough statements. got={}'.format(len(program.statements)))
        stmt = program.statements[0]
        self.assertEqual(type(stmt), ast.ExpressionStatement,
            msg='program.statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        exp = stmt.expression
        if not type(exp) is ast.IfExpression:
            print('exp is not ast.IfExpression. got={}'.format(type(exp)))
        if not self.check_infix_expression(exp.condition, 'x', '<', 'y'):
            return
        self.assertEqual(len(exp.consequence.statements), 1, 
            msg='consequences does not have enough statements. got={}'.format(len(exp.consequence.statements)))
        consequence = exp.consequence.statements[0]
        if not type(consequence) is ast.ExpressionStatement:
            print('statements[0] is not ast.ExpressionStatement. got={}'.format(type(consequence)))
        if not self.check_identifier(consequence.expression, 'x'):
            return
        self.assertEqual(exp.alternative, None,
            msg='exp.alternative.statements is not None. got={}'.format(exp.alternative))

    def test_if_else_expression(self):
        # tests = [
        #     ("true;", True),
        #     ("false;", False)
        # ]
        source = 'if (x < y) { x } else { y }'
        # for t in tests:
        # l = lexer.new(t[0])
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        self.assertEqual(len(program.statements), 1, 
            msg='program does not have enough statements. got={}'.format(len(program.statements)))
        stmt = program.statements[0]
        self.assertEqual(type(stmt), ast.ExpressionStatement,
            msg='program.statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        exp = stmt.expression
        if not type(exp) is ast.IfExpression:
            print('exp is not ast.IfExpression. got={}'.format(type(exp)))
        if not self.check_infix_expression(exp.condition, 'x', '<', 'y'):
            return
        self.assertEqual(len(exp.consequence.statements), 1, 
            msg='consequences does not have enough statements. got={}'.format(len(exp.consequence.statements)))
        consequence = exp.consequence.statements[0]
        if not type(consequence) is ast.ExpressionStatement:
            print('statements[0] is not ast.ExpressionStatement. got={}'.format(type(consequence)))
        if not self.check_identifier(consequence.expression, 'x'):
            return
        if len(exp.alternative.statements) != 1:
            print("exp.alternative.statements does not contain 1 statements. got={}",
                len(exp.alternative.statements))
        alternative = exp.alternative.statements[0]
        if not type(alternative) is ast.ExpressionStatement:
            print('statements[0] is not ast.ExpressionStatement. got={}'.format(type(alternative)))
        if not self.check_identifier(alternative.expression, "y"):
            return
    
    def test_function_literal_parsing(self):
        source = 'fn(x, y) { x + y; }'
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        self.assertEqual(len(program.statements), 1, 
            msg='program does not have enough statements. got={}'.format(len(program.statements)))
        stmt = program.statements[0]
        self.assertEqual(type(stmt), ast.ExpressionStatement,
            msg='program.statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        function = stmt.expression
        if not type(function) is ast.FunctionLiteral:
            print('function is not ast.FunctionLiteral. got={}'.format(type(function)))
        self.assertEqual(len(function.parameters), 2, 
            msg='function literal parameters wrong. want 2, got={}'.format(len(function.parameters)))
        self.check_literal_expression(function.parameters[0], 'x')
        self.check_literal_expression(function.parameters[1], 'y')
        self.assertEqual(len(function.body.statements), 1, 
            msg='function.body.statements does not have 1 statement, got={}'.format(len(function.body.statements)))
        body_stmt = function.body.statements[0]
        if not type(body_stmt) is ast.ExpressionStatement:
            print('function body statement is not ast.ExpressionStatement. got={}'.format(type(body_stmt)))
        self.check_infix_expression(body_stmt.expression, 'x', '+', 'y')
    
    def test_function_parameter_parsing(self):
        tests = [
            ("fn() {};", []),
            ("fn(x) {};", ['x']),
            ("fn(x, y, z) {};", ['x', 'y', 'z'])
        ]
        for t in tests:
            l = lexer.new(t[0])
            p = parser.new(l)
            program = p.parse_program()
            self.check_parse_errors(p)
            stmt = program.statements[0]
            function = stmt.expression
            self.assertEqual(len(function.parameters), len(t[1]),
                msg='function literal parameters wrong. want {}, got={}'.format(len(t[1]), len(function.parameters)))
            for i, ident in enumerate(t[1]):
                self.check_literal_expression(function.parameters[i], ident)
    
    def test_call_expression_parsing(self):
        source = 'add(1, 2 * 3, 4 + 5);'
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parse_errors(p)
        self.assertEqual(len(program.statements), 1, 
            msg='program does not have enough statements. got={}'.format(len(program.statements)))
        stmt = program.statements[0]
        self.assertEqual(type(stmt), ast.ExpressionStatement,
            msg='program.statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        exp = stmt.expression
        if not type(exp) is ast.CallExpression:
            print('exp is not ast.CallExpression. got={}'.format(type(exp)))
        if not self.check_identifier(exp.function, "add"):
            return
        self.assertEqual(len(exp.arguments), 3, 
            msg='wrong lenght of arguments. want 3, got={}'.format(len(exp.arguments)))
        self.check_literal_expression(exp.arguments[0], 1)
        self.check_infix_expression(exp.arguments[1], 2, '*', 3)
        self.check_infix_expression(exp.arguments[2], 4, '+', 5)
    
    def test_call_expression_parameter_parsing(self):
        tests = [
			("add();", "add", []),
		    ("add(1);", "add", ["1"]),
            ("add(1, 2 * 3, 4 + 5);", "add", ["1", "(2 * 3)", "(4 + 5)"])
        ]
        for t in tests:
            l = lexer.new(t[0])
            p = parser.new(l)
            program = p.parse_program()
            self.check_parse_errors(p)
            stmt = program.statements[0]
            exp = stmt.expression
            if not type(exp) is ast.CallExpression:
                print('stmt.Expression is not ast.CallExpression. got={}'.format(type(exp)))
            if not self.check_identifier(exp.function, t[1]):
                return
            self.assertEqual(len(exp.arguments), len(t[2]), 
                msg='wrong lenght of arguments. want={}, got={}'.format(len(t[2]), len(exp.arguments)))
            for i, arg in enumerate(t[2]):
                if exp.arguments[i].string() != arg:
                    print("argument {} wrong. want={}, got={}".format(i, arg, exp.arguments[i].string()))

    def check_parse_errors(self, p):
        errors = p.errors
        if len(errors) == 0:
            return
        print('parser has {} errors'.format(len(errors)))
        for e in errors:
            print('parser error: {}'.format(e))
        self.fail()

if __name__ == '__main__':
    unittest.main()