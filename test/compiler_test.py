import unittest
from collections import namedtuple
from typing import Any
import sys
sys.path.append("../src/")
from monkey.tokens import token
from monkey.lexer import lexer
from monkey.ast import ast
from monkey.parser import parser
from monkey.evaluator import evaluator as e
from monkey.object import *
from monkey.code import *
from monkey.compiler import compiler as c

CompilerTestCase = namedtuple('CompilerTestCase', 'source expected_constants expected_instructions')

class CompilerTest(unittest.TestCase):

    def test_integer_arithmetic(self):
        tests = [
            CompilerTestCase("1 + 2", [1, 2], [Make(OpConstant, 0), Make(OpConstant, 1)])
        ]
        self.run_compiler_tests(tests)

    def run_compiler_tests(self, tests):
        for t in tests:
            program = self.parse(t.source)
            compiler = c.new()
            err = compiler.compile(program)
            self.assertIsNone(err, msg=f'compiler error: {err}')
            bytecode = compiler.bytecode()
            err = self.check_instructions(t.expected_instructions, bytecode.instructions)
            self.assertIsNone(err, msg=f'check_instructions failed: {err}')
            err = self.check_constants(t.expected_constants, bytecode.constants)
            self.assertIsNone(err, msg=f'check_constants failed: {err}')

    def check_instructions(self, expected, actual):
        concatted = self.concat_instructions(expected)
        self.assertEqual(len(actual), len(concatted.instructions), 
            msg=f'wrong instruction length.\nwant=\n{str(concatted)}\ngot=\n{str(actual)}')
        for i, ins in enumerate(concatted.instructions):
            self.assertEqual(actual[i], concatted.instructions[i], 
                msg=f'wrong instruction at {i}\nwant=\n{concatted.instructions[i]}\ngot={actual[i]}')
        return None
    
    def concat_instructions(self, instructions):
        out = Instructions()
        for ins in instructions:
            out.instructions.extend(ins)
        return out
    
    def check_constants(self, expected, actual):
        self.assertEqual(len(expected), len(actual),
            msg=f'wrong number of constatnts.\nwant=\n{len(actual)}\ngot={len(expected)}')
        for i, constant in enumerate(expected):
            if isinstance(constant, int):
                err = self.check_integer_object(constant, actual[i])
                self.assertIsNone(err, 
                    msg=f'constant {i} - check_integer_object failed: {err}')
        return None
    
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