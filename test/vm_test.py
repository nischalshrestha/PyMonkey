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
            stack_element = vm.stack_top()
            self.check_expected_object(t.expected, stack_element)

    def check_expected_object(self, expected, actual):
        if isinstance(expected, int):
            err = self.check_integer_object(expected, actual)
            self.assertIsNone(err, msg=f'check_integer_object failed: {err}')

    def check_integer_object(self, expected, actual):
        if not isinstance(actual, Integer):
            return (f'object is not Integer. got={type(actual)} {actual}')
        if actual.value != expected:
            return (f'object has wrong value. got={actual.value} want={expected}')
        return None
    
    def parse(self, source):
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        return program
   
if __name__ == '__main__':
    unittest.main()