import unittest
import sys
sys.path.append("../src/")
from monkey import ast
from monkey.ast import modify

class ModifyTest(unittest.TestCase):

    def test_modify(self):
        one = lambda : ast.ExpressionStatement(expression=ast.IntegerLiteral(value=1))
        two = lambda : ast.ExpressionStatement(expression=ast.IntegerLiteral(value=2))
        def turn_one_into_two(node):
            """ Modifier function to convert IntegerLiteral of value 1 to 2 """
            integer = node
            if not isinstance(integer, ast.IntegerLiteral):
                return node
            elif integer.value != 1:
                return node
            integer.value = 2
            return integer
        tests = [
            (one(), ast.ExpressionStatement(expression=ast.IntegerLiteral(value=2))),
            (two(), ast.ExpressionStatement(expression=ast.IntegerLiteral(value=2))),
            (ast.InfixExpression(operator = "+", left = one(), right = two()), 
                ast.InfixExpression(operator = "+", left = two(), right = two())),
            (ast.InfixExpression(operator = "+", left = two(), right = one()), 
                ast.InfixExpression(operator = "+", left = two(), right = two())),
            (ast.PrefixExpression(operator = "-", right = one()), 
                ast.PrefixExpression(operator = "-", right = two())),
            (ast.IndexExpression(left = one(), index = one()), 
                ast.IndexExpression(left = two(), index = two()))
        ]
        for t in tests:
            modified = modify.Modify(t[0], turn_one_into_two)
            deep_equals = (modified == t[1])
            self.assertTrue(deep_equals,
                'not equal. got={} want={}'.format(modified, t[1]))

if __name__ == '__main__':
    unittest.main()