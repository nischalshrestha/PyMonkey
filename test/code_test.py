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
            (OpConstant, [65534], [bytes(OpConstant), 255, 254]),
        ]
        for t in tests:
            instruction = Make(t[0], *t[1])
            self.assertEqual(len(instruction), len(t[2]), 
                msg=f'instruction has wrong length. want={len(t[2])}, got={len(instruction)}')
            for i, b in enumerate(t[2]):
                self.assertEqual(instruction[i], t[2][i],
                    msg=f'wrong byte at position {i}. want={t[2][i]}, got={instruction[i]}')
    
    def test_instructions_string(self):
        instructions = Instructions([Make(OpConstant, 1), Make(OpConstant, 2), Make(OpConstant, 65535)])
        expected = '''
        0000 OpConstant 1 
        0003 OpConstant 2 
        0006 OpConstant 65535
        '''
        concatted = Instructions()
        for ins in instructions.instructions:
            concatted.instructions.extend(ins)
        self.assertEqual(concatted.string(), expected,
            msg=f'instruction wrongly formatted.\nwant={expected}\ngot={concatted.string()}')

    def test_read_operands(self):
        test_struct = namedtuple('test_struct', 'op operands bytesread')
        tests = [test_struct(OpConstant, [65535], 2)]
        for t in tests:
            # print(t.op, t.operands, t.bytesread)
            instruction = Make(t.op, *t.operands)
            defn = lookup(bytes(t.op))
            self.assertIsNotNone(defn, msg=f'definition not found: {defn}\n')
            operands_read, n = read_operands(defn, instruction[1:])
            self.assertEqual(n, t.bytesread, msg=f'n wrong. want={t.bytesread}, got={n}')
            for i, want in enumerate(t.operands):
                self.assertEqual(operands_read[i], want,
                    msg=f'operand wrong. want={want}, got={operands_read[i]}')
   
if __name__ == '__main__':
    unittest.main()