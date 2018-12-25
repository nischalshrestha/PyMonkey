import unittest
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
            instruction = Make(t[0], t[1])
            self.assertEqual(len(instruction), len(t[2]), 
                msg=f'instruction has wrong length. want={len(t[2])}, got={len(instruction)}')
            for i, b in enumerate(t[2]):
                self.assertEqual(instruction[i], t[2][i],
                    msg=f'wrong byte at position {i}. want={t[2][i]}, got={instruction[i]}')
   
if __name__ == '__main__':
    unittest.main()