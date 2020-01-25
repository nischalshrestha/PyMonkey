import unittest
from collections import namedtuple
from typing import Any
import sys
sys.path.append("../src/")
from monkey.lexer import lexer
from monkey.ast import ast
from monkey.parser import parser
from monkey.object import *
from monkey.code import *
from monkey.compiler import compiler as c
from monkey.vm import vm as v

VmTestCase = namedtuple('VmTestCase', 'input expected')

class VMTest(unittest.TestCase):

    def test_integer_arithmetic(self):
        tests = [
            VmTestCase("1", 1),
            VmTestCase("2", 2),
            VmTestCase("1 + 2", 3),
            VmTestCase("1 - 2", -1), 
            VmTestCase("1 * 2", 2), 
            VmTestCase("4 / 2", 2), 
            VmTestCase("50 / 2 * 2 + 10 - 5", 55), 
            VmTestCase("5 + 5 + 5 + 5 - 10", 10), 
            VmTestCase("2 * 2 * 2 * 2 * 2", 32), 
            VmTestCase("5 * 2 + 10", 20), 
            VmTestCase("5 + 2 * 10", 25), 
            VmTestCase("5 * (2 + 10)", 60),
            VmTestCase("-5", -5), 
            VmTestCase("-10", -10),
            VmTestCase("-50 + 100 + -50", 0), 
            VmTestCase("( 5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
        ]
        self.run_vm_tests(tests)
    
    def test_let_statements(self):
        tests = [
            VmTestCase("let one = 1; one", 1),
            VmTestCase("let one = 1; let two = 2; one + two", 3),
            VmTestCase("let one = 1; let two = one + one; one + two", 3),
        ]
        self.run_vm_tests(tests)
    
    def test_boolean_expressions(self):
        tests = [
            VmTestCase("1 < 2", True),
            VmTestCase("1 > 2", False),
            VmTestCase("1 < 1", False), 
            VmTestCase("1 > 1", False), 
            VmTestCase("1 == 1", True), 
            VmTestCase("1 != 1", False), 
            VmTestCase("1 == 2", False), 
            VmTestCase("1 != 2", True), 
            VmTestCase("true == true", True), 
            VmTestCase("false == false", True), 
            VmTestCase("true == false", False), 
            VmTestCase("true != false", True), 
            VmTestCase("false != true", True), 
            VmTestCase("(1 < 2) == true", True), 
            VmTestCase("(1 < 2) == false", False), 
            VmTestCase("(1 > 2) == true", False), 
            VmTestCase("(1 > 2) == false", True),
            VmTestCase("!true", False), 
            VmTestCase("!false", True), 
            VmTestCase("!5", False), 
            VmTestCase("!!true", True), 
            VmTestCase("!!false", False), 
            VmTestCase("!!5", True),
            VmTestCase("!(if (false) { 5; })", True),
        ]
        self.run_vm_tests(tests)
    
    def test_string_expressions(self):
        tests = [
            VmTestCase("\"monkey\"", "monkey"),
            VmTestCase("\"mon\" + \"key\"", "monkey"),
            VmTestCase("\"monkey\" + \"banana\"", "monkeybanana"),
        ]
        self.run_vm_tests(tests)

    def test_conditionals(self):
        tests = [
            VmTestCase("if (true) { 10 }", 10),
            VmTestCase("if (true) { 10 } else { 20 }", 10),
            VmTestCase("if (false) { 10 } else { 20 }", 20), 
            VmTestCase("if (1) { 10 }", 10), 
            VmTestCase("if (1 < 2) { 10 }", 10), 
            VmTestCase("if (1 < 2) { 10 } else { 20 }", 10), 
            VmTestCase("if (1 > 2) { 10 } else { 20 }", 20), 
            VmTestCase("if (1 > 2) { 10 }", Null), 
            VmTestCase("if (false) { 10 }", Null),
            VmTestCase("if ((if (false) { 10 })) { 10 } else { 20 }", 20),
        ]
        self.run_vm_tests(tests)
    
    def test_array_literals(self):
        tests = [
            VmTestCase("[]", []),
            VmTestCase("[1, 2, 3]", [1, 2, 3]),
            VmTestCase("[1 + 2, 3 * 4, 5 + 6]", [3, 12, 11]),
        ]
        self.run_vm_tests(tests)

    def run_vm_tests(self, tests):
        for t in tests:
            program = self.parse(t.input)
            comp = c.new()
            err = comp.compile(program)
            self.assertIsNone(err, msg=f'compiler error: {err}')
            vm = v.new(comp.bytecode())
            err = vm.run()
            self.assertIsNone(err, msg=f'vm error: {err}')
            stack_element = vm.last_popped_stack_element()
            self.check_expected_object(t.expected, stack_element)

    def check_expected_object(self, expected, actual):
        if type(expected) == int:
            err = self.check_integer_object(expected, actual)
            self.assertIsNone(err, msg=f'check_integer_object failed: {err}')
        elif type(expected) == bool:
            err = self.check_boolean_object(expected, actual)
            self.assertIsNone(err, msg=f'check_boolean_object failed: {err}')
        elif type(expected) == str:
            err = self.check_string_object(expected, actual)
            self.assertIsNone(err, msg=f'check_string_object failed: {err}')
        elif type(expected) == Null:
            self.assertEqual(actual, Null, msg=f'object is not Null: {type(actual)} {actual}')
        elif type(expected) == []:
            self.assertEqual(actual, Array, msg=f'object is not Array: {type(actual)} {actual}')
            self.assertEqual(len(actual.elements), len(expected), 
                msg=f'wrong num of elements. want={len(expected)} got={len(actual.elements)}')
            for i, e in enumerate(expected):
                err = self.check_integer_object(e, actual.elements[i])
                self.assertIsNone(err, None, msg=f'check_integer_object failed: {err}')


    def check_integer_object(self, expected, actual):
        if not isinstance(actual, Integer):
            return f'object is not Integer. got={type(actual)} {actual}'
        if actual.value != expected:
            return f'object has wrong value. got={actual.value} want={expected}'
        return None

    def check_string_object(self, expected, actual):
        if not isinstance(actual, String):
            return f'object is not String. got={type(actual)} {actual}'
        if actual.value != expected:
            return f'object has wrong value. got={actual.value}, want={expected}'
        return None
    
    def check_boolean_object(self, expected, actual):
        if not isinstance(actual, Boolean):
            return f'object is not Boolean. got={type(actual)} {actual}'
        if actual.value != expected:
            return f'object has wrong value. got={actual.value} want={expected}'
        return None

    def parse(self, source):
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        return program
   
if __name__ == '__main__':
    unittest.main()