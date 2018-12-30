import unittest
from collections import namedtuple
import sys
sys.path.append("../src/")
from monkey.tokens import token
from monkey.lexer import lexer
from monkey.ast import ast
from monkey.parser import parser
from monkey.evaluator import evaluator as e
from monkey.object import *
from monkey.code import *

class CodeTest(unittest.TestCase):

    def test_eval_integer_expression(self):
        tests = [
            (
                OpConstant, 
                [65534], 
                [
                    OpConstant, 
                    255, 
                    254
                ]
            ),
        ]
        for t in tests:
            instruction = Make(t[0], *t[1])
            self.assertEqual(len(instruction), len(t[2]), 
                msg=f'instruction has wrong length. want={len(t[2])}, got={len(instruction)}')
            for i, b in enumerate(t[2]):
                self.assertEqual(instruction[i], t[2][i],
                    msg=f'wrong byte at position {i}. want={t[2][i]}, got={instruction[i]}')
    
    def test_instructions_string(self):
        ins = Instructions(Make(OpConstant, 1) + Make(OpConstant, 2) + Make(OpConstant, 65535))
        expected = '''0000 OpConstant 1\n0003 OpConstant 2\n0006 OpConstant 65535\n'''
        concatted = Instructions()
        concatted.instructions = ins.instructions
        self.assertEqual(str(concatted), expected,
            msg=f'instruction wrongly formatted.\nwant=\n{expected}\ngot=\n{str(concatted)}')

    def test_read_operands(self):
        test_struct = namedtuple('test_struct', ['op', 'operands', 'bytesread'])
        tests = [test_struct(OpConstant, [65535], 2)]
        for t in tests:
            instruction = Make(t.op, *t.operands)
            defn, err = lookup(t.op)
            self.assertIsNotNone(defn, msg=f'definition not found: {err}\n')
            operands_read, n = read_operands(defn, instruction[1:])
            self.assertEqual(n, t.bytesread, msg=f'n wrong. want={t.bytesread}, got={n}')
            for i, want in enumerate(t.operands):
                self.assertEqual(int.from_bytes(operands_read[i:], byteorder='big'), want,
                    msg=f'operand wrong. want={want}, got={operands_read}')
    
    def test_make(self):
        test_struct = namedtuple('test_struct', ['op', 'operands', 'expected'])
        tests = [
            test_struct(OpAdd, [], [OpAdd])
        ]
        for t in tests:
            instruction = Make(t.op, t.operands)
            self.assertEqual(len(instruction), len(t.expected), 
                msg=f'instruction has wrong length. want={len(t.expected)}, got={len(instruction)}')
            for i, b in enumerate(t.expected):
                self.assertEqual(instruction[i], t.expected[i],
                    msg=f'wrong byte at position {i}. want={t.expected[i]}, got={instruction[i]}')
   
if __name__ == '__main__':
    unittest.main()