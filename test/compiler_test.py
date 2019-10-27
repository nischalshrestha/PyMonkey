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

CompilerTestCase = namedtuple('CompilerTestCase', 'source expected_constants expected_instructions')

class CompilerTest(unittest.TestCase):

    def test_integer_arithmetic(self):
        tests = [
            CompilerTestCase("1 + 2", [1, 2], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpAdd) +
                Make(OpPop)),
            CompilerTestCase("1; 2;", [1, 2], 
                Make(OpConstant, 0) + 
                Make(OpPop) +
                Make(OpConstant, 1) +
                Make(OpPop)),
            CompilerTestCase("1 - 2", [1, 2], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpSub) +
                Make(OpPop)),
            CompilerTestCase("1 * 2", [1, 2], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpMul) +
                Make(OpPop)),
            CompilerTestCase("2 / 1", [2, 1], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpDiv) +
                Make(OpPop)),
            CompilerTestCase("1 > 2", [1, 2], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpGreaterThan) +
                Make(OpPop)),
            CompilerTestCase("1 < 2", [2, 1], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpGreaterThan) +
                Make(OpPop)),
            CompilerTestCase("1 == 2", [1, 2], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpEqual) +
                Make(OpPop)),
            CompilerTestCase("1 != 2", [1, 2], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpNotEqual) +
                Make(OpPop)),
            CompilerTestCase("true == false", [], 
                Make(OpTrue) +
                Make(OpFalse) +
                Make(OpEqual) +
                Make(OpPop)),
            CompilerTestCase("true != false", [], 
                Make(OpTrue) +
                Make(OpFalse) +
                Make(OpNotEqual) +
                Make(OpPop)),
            CompilerTestCase("-1", [1], 
                Make(OpConstant, 0) +
                Make(OpMinus) +
                Make(OpPop)),
        ]
        self.run_compiler_tests(tests)
    
    def test_boolean_expressions(self):
        tests = [
            CompilerTestCase("true", [], 
                Make(OpTrue) +
                Make(OpPop)),
            CompilerTestCase("false", [], 
                Make(OpFalse) +
                Make(OpPop)),
            CompilerTestCase("!true", [], 
                Make(OpTrue) +
                Make(OpBang) +
                Make(OpPop)),
        ]
        self.run_compiler_tests(tests)
    
    def test_conditionals(self):
        tests = [
            CompilerTestCase("if (true) { 10 }; 3333;", [10, 3333],
                # 0000
                Make(OpTrue) +
                # 0001
                Make(OpJumpNotTruthy, 10) +
                # 0004
                Make(OpConstant, 0) +
                # 0007
                Make(OpJump, 11) +
                # 0010
                Make(OpNull) +
                # 0011; this pop is bc ifs are expressions with an added pop at end
                Make(OpPop) +
                # 0012
                Make(OpConstant, 1) +
                # 0015
                Make(OpPop)),
            CompilerTestCase("if (true) { 10 } else { 20 }; 3333;", [10, 20, 3333],
                # 0000
                Make(OpTrue) +
                # 0001
                Make(OpJumpNotTruthy, 10) +
                # 0004
                Make(OpConstant, 0) +
                # 0007
                Make(OpJump, 13) +
                # 0010
                Make(OpConstant, 1) +
                # 0013
                Make(OpPop) +
                # 0014
                Make(OpConstant, 2) + 
                # 0017
                Make(OpPop)),
        ]
        self.run_compiler_tests(tests)
    
    def test_global_let_statements(self):
        tests = [
            CompilerTestCase(
                """
                let one = 1;
                let two = 2;
                """, 
                [1, 2],
                Make(OpConstant, 0) +
                Make(OpSetGlobal, 0) +
                Make(OpConstant, 1) +
                Make(OpSetGlobal, 1)),
            CompilerTestCase(
                """
                let one = 1;
                one;
                """, 
                [1],
                Make(OpConstant, 0) +
                Make(OpSetGlobal, 0) +
                Make(OpGetGlobal, 0) +
                Make(OpPop)),
            CompilerTestCase(
                """
                let one = 1;
                let two = one;
                two;
                """, 
                [1, 2],
                Make(OpConstant, 0) +
                Make(OpSetGlobal, 0) +
                Make(OpGetGlobal, 0) +
                Make(OpSetGlobal, 1) +
                Make(OpGetGlobal, 1) + 
                Make(OpPop))
        ]
        self.run_compiler_tests(tests)

    def run_compiler_tests(self, tests):
        for t in tests:
            program = self.parse(t.source)
            compiler = c.new()
            err = compiler.compile(program)
            self.assertIsNone(err, msg=f'compiler error: {err}')
            bytecode = compiler.bytecode()
            err = self.check_instructions(Instructions(t.expected_instructions), Instructions(bytecode.instructions))
            self.assertIsNone(err, msg=f'check_instructions failed: {err}')
            err = self.check_constants(t.expected_constants, bytecode.constants)
            self.assertIsNone(err, msg=f'check_constants failed: {err}')

    def check_instructions(self, expected, actual):
        self.assertEqual(len(actual.instructions), len(expected.instructions), 
            msg=f'wrong instruction length.\nwant=\n{str(expected)}\ngot=\n{str(actual)}')
        self.assertEqual(actual.instructions, expected.instructions, 
                msg=f'wrong instruction \nwant=\n{str(expected)}\ngot=\n{str(actual)}')
        return None
    
    def check_constants(self, expected, actual):
        self.assertEqual(len(expected), len(actual),
            msg=f'wrong number of constants.\nwant=\n{len(actual)}\ngot=\n{len(expected)}')
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