import unittest
import sys
sys.path.append("../src/")
from monkey import ast
from monkey.ast import modify

class ModifyTest(unittest.TestCase):

    def test_modify(self):
        one = ast.ExpressionStatement(expression=ast.IntegerLiteral(value=1))
        two = ast.ExpressionStatement(expression=ast.IntegerLiteral(value=2))
        def turn_one_into_two(node):
            integer = node
            if not isinstance(integer, ast.IntegerLiteral):
                return node
            elif integer.value != 1:
                return node
            integer.value = 2
            return integer
        tests = [
            (one, ast.ExpressionStatement(expression=ast.IntegerLiteral(value=2))),
            (two, ast.ExpressionStatement(expression=ast.IntegerLiteral(value=2)))
        ]
        for t in tests:
            modified = modify.Modify(t[0], turn_one_into_two)
            deep_equals = modified == t[1]
            self.assertTrue(deep_equals,
                'not equal. got={} want={}'.format(modified, t[1]))

if __name__ == '__main__':
    unittest.main()