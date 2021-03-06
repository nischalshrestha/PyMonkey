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

    def test_string_expressions(self):
        tests = [
            CompilerTestCase("\"monkey\"", ["monkey"], 
                Make(OpConstant, 0) +
                Make(OpPop)
            ),
            CompilerTestCase("\"mon\" + \"key\"", ["mon", "key"], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) + 
                Make(OpAdd) +
                Make(OpPop)
            )
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
                [1],
                Make(OpConstant, 0) +
                Make(OpSetGlobal, 0) +
                Make(OpGetGlobal, 0) +
                Make(OpSetGlobal, 1) +
                Make(OpGetGlobal, 1) + 
                Make(OpPop))
        ]
        self.run_compiler_tests(tests)

    def test_array_literals(self):
        tests = [
            CompilerTestCase(
                "[]", 
                [], 
                Make(OpArray, 0) + 
                Make(OpPop)),
            CompilerTestCase(
                "[1, 2, 3]", 
                [1, 2, 3], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpConstant, 2) +
                Make(OpArray, 3) + 
                Make(OpPop)),
            CompilerTestCase(
                "[1 + 2, 3 - 4, 5 * 6]", 
                [1, 2, 3, 4, 5, 6], 
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpAdd) +
                Make(OpConstant, 2) +
                Make(OpConstant, 3) +
                Make(OpSub) +
                Make(OpConstant, 4) +
                Make(OpConstant, 5) +
                Make(OpMul) +
                Make(OpArray, 3) + 
                Make(OpPop)),
        ]
        self.run_compiler_tests(tests)

    def test_hash_literals(self):
        tests = [
            CompilerTestCase(
                "{}",
                {},
                Make(OpHash, 0) +
                Make(OpPop)
            ),
            CompilerTestCase(
                "{1: 2, 3: 4, 5: 6}",
                [1, 2, 3, 4, 5, 6],
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpConstant, 2) +
                Make(OpConstant, 3) +
                Make(OpConstant, 4) +
                Make(OpConstant, 5) +
                Make(OpHash, 6) +
                Make(OpPop)
            ),
            CompilerTestCase(
                "{1: 2 + 3, 4: 5 * 6}",
                [1, 2, 3, 4, 5, 6],
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpConstant, 2) +
                Make(OpAdd) +
                Make(OpConstant, 3) +
                Make(OpConstant, 4) +
                Make(OpConstant, 5) +
                Make(OpMul) +
                Make(OpHash, 4) +
                Make(OpPop)
            ),
        ]
        self.run_compiler_tests(tests)
    
    def test_index_expressions(self):
        tests = [
            CompilerTestCase(
                "[1, 2, 3][1 + 1]",
                [1, 2, 3, 1, 1],
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpConstant, 2) +
                Make(OpArray, 3) +
                Make(OpConstant, 3) +
                Make(OpConstant, 4) +
                Make(OpAdd) +
                Make(OpIndex) +
                Make(OpPop)
            ),
            CompilerTestCase(
                "{1: 2}[2 - 1]",
                [1, 2, 2, 1],
                Make(OpConstant, 0) +
                Make(OpConstant, 1) +
                Make(OpHash, 2) +
                Make(OpConstant, 2) +
                Make(OpConstant, 3) +
                Make(OpSub) +
                Make(OpIndex) +
                Make(OpPop)
            )
        ]
        self.run_compiler_tests(tests)
    
    def test_functions(self):
        tests = [
            CompilerTestCase(
                "fn() { return 5 + 10 }",
                [
                    5,
                    10,
                    Instructions(
                        Make(OpConstant, 0) +
                        Make(OpConstant, 1) +
                        Make(OpAdd) +
                        Make(OpReturnValue)
                    )
                ],
                Make(OpConstant, 2) + Make(OpPop)
            ),
            CompilerTestCase(
                "fn() { 5 + 10 }",
                [
                    5,
                    10,
                    Instructions(
                        Make(OpConstant, 0) + 
                        Make(OpConstant, 1) + 
                        Make(OpAdd) +
                        Make(OpReturnValue)
                    )
                ],
                Make(OpConstant, 2) + Make(OpPop)
            ),
            CompilerTestCase(
                "fn() { 1; 2 }",
                [
                    1,
                    2,
                    Instructions(
                        Make(OpConstant, 0) + 
                        Make(OpPop) + 
                        Make(OpConstant, 1) +
                        Make(OpReturnValue)
                    )
                ],
                Make(OpConstant, 2) + Make(OpPop)
            ),
            CompilerTestCase(
                "fn() {  }",
                [
                    Instructions(
                        Make(OpReturn)
                    )
                ],
                Make(OpConstant, 0) + Make(OpPop)
            ),
        ]
        self.run_compiler_tests(tests)
    
    def test_function_calls(self):
        tests = [
            CompilerTestCase(
                "fn() { 24 }();",
                [
                    24,
                    Instructions(
                        Make(OpConstant, 0) +
                        Make(OpReturnValue)
                    )
                ],
                Make(OpConstant, 1) +
                Make(OpCall) +
                Make(OpPop)
            ),
            CompilerTestCase(
                """
                let noArg = fn() { 24 };
                noArg();
                """,
                [
                    24,
                    Instructions(
                        Make(OpConstant, 0) +
                        Make(OpReturnValue)
                    )
                ],
                Make(OpConstant, 1) +
                Make(OpSetGlobal, 0) +
                Make(OpGetGlobal, 0) +
                Make(OpCall) +
                Make(OpPop)
            )
        ]
        self.run_compiler_tests(tests)
    
    def test_compiler_scopes(self):
        compiler = c.new()
        self.assertEqual(compiler.scope_index, 0, 
            msg=f'scope_index wrong. got={compiler.scope_index}, want=0')
        compiler.emit(OpMul)
        # in a new scope, scope_index should increase, but only have 1 instruction
        # if we emit 1 Opcode inside that scope
        compiler.enter_scope()
        self.assertEqual(compiler.scope_index, 1,
            msg=f'scope_index wrong. got={compiler.scope_index}, want=1')
        compiler.emit(OpSub)
        self.assertEqual(len(compiler.scopes[compiler.scope_index].instructions), 
            1,
            msg=f'instructions length wrong. got={len(compiler.scopes[compiler.scope_index].instructions)}')
        last = compiler.scopes[compiler.scope_index].last_instruction
        self.assertEqual(last.opcode, OpSub,
            msg=f'last_instruction.opcode wrong. got={last.opcode}, want={OpSub}')
        compiler.leave_scope()
        # when we leave the scope, scope_index should go back to what it was in
        # previous scope
        self.assertEqual(compiler.scope_index, 0,
            msg=f'scope_index wrong. got={compiler.scope_index}, want=0')
        # when we add another OpCode should reflect 2 instructions and not > 2
        compiler.emit(OpAdd)
        self.assertEqual(len(compiler.scopes[compiler.scope_index].instructions), 
            2,
            msg=f'instructions length wrong. got={len(compiler.scopes[compiler.scope_index].instructions)}')
        last = compiler.scopes[compiler.scope_index].last_instruction
        self.assertEqual(last.opcode, OpAdd,
            msg=f'last_instruction.opcode wrong. got={last.opcode}, want={OpAdd}')
        previous = compiler.scopes[compiler.scope_index].previous_instruction
        self.assertEqual(previous.opcode, OpMul,
            msg=f'previous_instruction.opcode wrong. got={previous.opcode}, want={OpMul}')
            
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
        # print(actual, expected)
        return None
    
    def check_constants(self, expected, actual):
        self.assertEqual(len(expected), len(actual),
            msg=f'wrong number of constants.\nwant=\n{len(actual)}\ngot=\n{len(expected)}')
        for i, constant in enumerate(expected):
            if isinstance(constant, int):
                err = self.check_integer_object(constant, actual[i])
                self.assertIsNone(err, 
                    msg=f'constant {i} - check_integer_object failed: {err}')
            elif isinstance(constant, str):
                err = self.check_string_object(constant, actual[i])
                self.assertIsNone(err,
                    msg=f'constant {i} - check_string_object failed: {err}')
            elif isinstance(constant, Instructions):
                self.assertTrue(isinstance(actual[i], CompiledFunction),
                    msg=f'constant {i} - not a function: {actual[i]}')
                err = self.check_instructions(constant, expected[i])
                self.assertIsNone(err, 
                    msg=f'constant {i} - check_instructions failed: {err}')
        return None
    
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
            return f'object has wrong value. got={actual.value} want={expected}'
    
    def parse(self, source):
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        return program
   
if __name__ == '__main__':
    unittest.main()