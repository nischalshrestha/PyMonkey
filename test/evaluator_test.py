import unittest
import sys
sys.path.append("../src/")
from monkey import token
from monkey import lexer
from monkey import ast
from monkey import parser
from monkey import evaluator as e
from monkey.object import *

# TODO use isinstance() instead of type()
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
        env = e.new_environment()
        return e.Eval(program, env)

    def check_integer_object(self, obj, expected):
        if not isinstance(obj, Integer):
            print('object is not Integer. got={} {}'.format(type(obj), obj.message))
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
        if not type(obj) is Boolean:
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
        # Note: the reason we use 'is' is bc NULL is an instance not a type
        if not obj is NULL:
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
            (
                '''
                if (10 > 1) {
                    if (10 > 1) {
                        return 10;
                    }
                    return 1;
                }
                ''', 10,
            ),
		    (
                '''
                let f = fn(x) {
                    return x;
                    x + 10;
                };
                f(10);''', 10
            ),
		    (
                '''
                let f = fn(x) {
                    let result = x + 10;
                    return result;
                    return 10;
                };
                f(10);''', 20
            )
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
            ("foobar", "identifier not found: foobar"),
            ("\"Hello\" - \"World!\"", "unknown operator: STRING - STRING"),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            if not type(evaluated) is Error:
                print(f"no error object returned. got={type(evaluated)}({evaluated})")
                continue
            self.assertEqual(evaluated.message, t[1], 
                msg=f"wrong error message. expected={t[1]}, got={evaluated.message}")

    def test_let_statements(self):
        tests = [
            ("let a = 5; a;", 5),
            ("let a = 5 * 5; a;", 25),
            ("let a = 5; let b = a; b;", 5),
            ("let a = 5; let b = a; let c = a + b + 5; c;", 15),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            self.assertTrue(self.check_integer_object(evaluated, t[1]))
    
    def test_function_object(self):
        source = "fn(x) { x + 2; };"
        fn = self.check_eval(source)
        self.assertTrue(isinstance(fn, Function), 
            msg=f"object is not Function. got={type(fn)} ({fn})")
        self.assertEqual(len(fn.parameters), 1,
            msg=f"function has wrong parameters. Parameters={fn.parameters}")
        self.assertEqual(fn.parameters[0].string(), "x",
            msg=f"parameter is not 'x'. got={fn.parameters[0].string()}")
        expected_body = "(x + 2)"
        self.assertEqual(fn.body.string(), expected_body,
            msg=f"parameter is not {expected_body}. got={fn.body.string()}")
    
    def test_function_application(self):
        tests = [
            ("let identity = fn(x) { x; }; identity(5);", 5),         
            ("let identity = fn(x) { return x; }; identity(5);", 5),
            ("let double = fn(x) { x * 2; }; double(5);", 10),    
            ("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
            ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
            ("fn(x) { x; }(5)", 5),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            self.assertTrue(self.check_integer_object(evaluated, t[1]))
    
    def test_closures(self):
        source = '''
            let newAdder = fn(x) { 
                fn(y) { 
                    x + y 
                }; 
            }; 
            let addTwo = newAdder(2); 
            addTwo(2);
        '''
        evaluated = self.check_eval(source)
        self.assertTrue(self.check_integer_object(evaluated, 4))
    
    def test_string_literal(self):
        source = '\"Hello World!\";'
        evaluated = self.check_eval(source)
        self.assertTrue(isinstance(evaluated, String),
            msg=f"object is not String. got={type(evaluated)}")
        self.assertEqual(evaluated.value, "Hello World!", 
            msg=f"String has wrong value. got={evaluated.value}")
    
    def test_string_concatenation(self):
        source = '"Hello" + " " + "World!";'
        evaluated = self.check_eval(source)
        self.assertTrue(isinstance(evaluated, String),
            msg=f"object is not String. got={type(evaluated)} ({evaluated})")
        self.assertEqual(evaluated.value, "Hello World!", 
            msg=f"String has wrong value. got={evaluated.value}")
    
    def test_array_literals(self):
        source = '[1, 2 * 2, 3 + 3]'
        evaluated = self.check_eval(source)
        self.assertTrue(isinstance(evaluated, Array),
            msg=f"object is not Array. got={type(evaluated)} ({evaluated})")
        self.assertEqual(len(evaluated.elements), 3, 
            msg=f"array has wrong num of elements. got={len(evaluated.elements)}")
        self.check_integer_object(evaluated.elements[0], 1)
        self.check_integer_object(evaluated.elements[1], 4)
        self.check_integer_object(evaluated.elements[2], 6)

    def test_array_index_expressions(self):
        tests = [
            ("[1, 2, 3][0]", 1),
            ("[1, 2, 3][1]", 2),
            ("[1, 2, 3][2]", 3),
            ("let i = 0; [1][i]", 1),
            ("[1, 2, 3][1 + 1]", 3),
            ("let myArray = [1, 2, 3]; myArray[2]", 3),
            ("let myArray = [1, 2, 3]; myArray[0] + myArray[1] + myArray[2];", 6),
            ("let myArray = [1, 2, 3]; let i = myArray[0]; myArray[i];", 2),
            ("[1, 2, 3][3]", None),
            ("[1, 2, 3][-1]", None),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            if isinstance(t[1], int):
                self.check_integer_object(evaluated, t[1])
            else:
                self.check_null_object(evaluated)
    
    def test_builtin_functions(self):
        tests = [
            ('len("")', 0),     
            ('len("four")', 4), 
            ('len("hello world")', 11),
            ('len(1)', "argument to `len` not supported, got INTEGER"),
            ('len("one", "two")', "wrong number of arguments. got=2, want=1"),
            ('len([1, 2, 3])', 3),
            ('len([])', 0),
            # ('puts("hello", "world!")', None),
            ('first([1, 2, 3])', 1),
            ('first([])', None),
            ('first(1)', "argument to `first` must be ARRAY, got INTEGER"),
            ('last([1, 2, 3])', 3),
            ('last([])', None),
            ('last(1)', "argument to `last` must be ARRAY, got INTEGER"),
            ('rest([1, 2, 3])', [2, 3]),
            ('rest([])', None),
            ('push([], 1)', [1]),
            ('push(1, 1)', "argument to `push` must be ARRAY, got INTEGER"),
        ]
        for t in tests:
            evaluated = self.check_eval(t[0])
            if isinstance(t[1], int):
                self.assertTrue(self.check_integer_object(evaluated, t[1]))
            elif isinstance(t[1], str):
                if not isinstance(evaluated, Error):
                    print(f"{t[0]} object is not Error. got={type(evaluated)} ({evaluated.value})")
                    continue
                self.assertEqual(evaluated.message, t[1],
                    msg=f"wrong error message. expected={t[1]}, got={evaluated.message}")

        # e.g. of using builtin functions: map
        # let map = fn(arr, f) { let iter = fn(arr, accumulated) {     if (len(arr) == 0) { accumulated     } else {       iter(rest(arr), push(accumulated, f(first(arr))));     }   };   iter(arr, []); };
        # let a = [1,2,3,4]
        # let double = fn(x) { x * 2 }
        # map(a, double)
        # [2,4,6,8]

        # e.g. of using builtin functions: reduce
        # let reduce = fn(arr, initial, f) {   let iter = fn(arr, result) {     if (len(arr) == 0) { result     } else {       iter(rest(arr), f(result, first(arr)));     }   };   iter(arr, initial);};
        # let sum = fn(arr) {   reduce(arr, 0, fn(initial, el) { initial + el }); };
        # sum([1, 2, 3, 4, 5]);

if __name__ == '__main__':
    unittest.main()