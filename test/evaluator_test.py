import unittest
import sys
sys.path.append("../src/")
from monkey import token
from monkey import lexer
from monkey import ast
from monkey import parser
from monkey import evaluator as e

class EvaluatorTest(unittest.TestCase):

    def test_eval_integer_expression(self):
        tests = [
            ("5", 5),
            ("10", 10),
            ("5", 5),         
            ("10", 10),         
            ("-5", -5),         
            ("-10", -10),
            ("5 + 5 + 5 + 5 - 10", 10),         
            ("2 * 2 * 2 * 2 * 2", 32),         
            ("-50 + 100 + -50", 0),         
            ("5 * 2 + 10", 20),         
            ("5 + 2 * 10", 25),         
            ("20 + 2 * -10", 0),         
            ("50 / 2 * 2 + 10", 60),         
            ("2 * (5 + 10)", 30),         
            ("3 * 3 * 3 + 10", 37),         
            ("3 * (3 * 3) + 10", 37),         
            ("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            self.assertTrue(self.check_integer_object(evaluated, t[1]))
    
    def check_eval(self, source):
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        return e.Eval(program)

    def check_integer_object(self, obj, expected):
        if not type(obj) is e.Integer:
            print('object is not Integer. got={}'.format(type(obj)))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}'.format(obj.value))
            return False
        return True

    def test_eval_boolean_expression(self):
        tests = [
            ("true", True),
            ("false", False),
            ("1 < 2", True),         
            ("1 > 2", False),
            ("1 < 1", False),         
            ("1 > 1", False),         
            ("1 == 1", True),         
            ("1 != 1", False),         
            ("1 == 2", False),         
            ("1 != 2", True),
            ("true == true", True),
            ("false == false", True), 
            ("true == false", False),  
            ("true != false", True),
            ("false != true", True),
            ("(1 < 2) == true", True),
            ("(1 < 2) == false", False),    
            ("(1 > 2) == true", False),  
            ("(1 > 2) == false", True),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            self.assertTrue(self.check_boolean_object(evaluated, t[1]))
    
    def check_boolean_object(self, obj, expected):
        if not type(obj) is e.Boolean:
            print('object is not Boolean. got={}'.format(type(obj)))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}'.format(obj.value))
            return False
        return True

    def test_bang_operator(self):
        tests = [
            ("!true", False),
            ("!false", True),         
            ("!5", False),         
            ("!!true", True),         
            ("!!false", False),         
            ("!!5", True),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            self.assertTrue(self.check_boolean_object(evaluated, t[1]))
    
    def test_if_else_expressions(self):
        tests = [
            ("if (true) { 10 }", 10),
            ("if (false) { 10 }", None),
            ("if (1) { 10 }", 10),
            ("if (1 < 2) { 10 }", 10),
            ("if (1 > 2) { 10 }", None),
            ("if (1 > 2) { 10 } else { 20 }", 20),
            ("if (1 < 2) { 10 } else { 20 }", 10),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            if type(t[1]) is int:
                self.assertTrue(self.check_integer_object(evaluated, t[1]))
            else:
                self.assertTrue(self.check_null_object(evaluated))
    
    def check_null_object(self, obj):
        if obj != e.NULL:
            print('object is not NULL. got={}({})'.format(type(obj), obj))
            return False
        return True

    def test_return_statements(self):
        tests = [
            ("return 10;", 10),
            ("return 10; 9;", 10),
            ("return 2 * 5; 9;", 10),
            ("9; return 2 * 5; 9;", 10),
            ("if (10 > 1) { if (10 > 1) { return 10; } return 1; }", 10),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            self.assertTrue(self.check_integer_object(evaluated, t[1]))
        
    def test_error_handling(self):
        tests = [
            ("5 + true;", "type mismatch: INTEGER + BOOLEAN"),
            ("5 + true; 5;", "type mismatch: INTEGER + BOOLEAN"),
            ("-true", "unknown operator: -BOOLEAN"),
            ("true + false;", "unknown operator: BOOLEAN + BOOLEAN"),
            ("5; true + false; 5;", "unknown operator: BOOLEAN + BOOLEAN"),
            ("if (10 > 1) { true + false; }", "unknown operator: BOOLEAN + BOOLEAN"),
            ("if (10 > 1) { if (10 > 1) { return true + false; } return 1; }", "unknown operator: BOOLEAN + BOOLEAN"),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            if not type(evaluated) is e.Error:
                print("no error object returned. got={}({})".format(type(evaluated), evaluated))
                continue
            self.assertEqual(evaluated.message, t[1], 
                msg="wrong error message. expected={}, got={}".format(t[1], evaluated.message))
            

if __name__ == '__main__':
    unittest.main()