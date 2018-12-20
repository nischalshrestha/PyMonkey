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
            (
                ast.InfixExpression(operator = "+", left = one(), right = two()), 
                ast.InfixExpression(operator = "+", left = two(), right = two())
            ),
            (
                ast.InfixExpression(operator = "+", left = two(), right = one()), 
                ast.InfixExpression(operator = "+", left = two(), right = two())
            ),
            (
                ast.PrefixExpression(operator = "-", right = one()), 
                ast.PrefixExpression(operator = "-", right = two())
            ),
            (
                ast.IndexExpression(left = one(), index = one()), 
                ast.IndexExpression(left = two(), index = two())
            ),
            (
                ast.IfExpression(
                    condition = one(), 
                    consequence = ast.BlockStatement(statements=[
                        ast.ExpressionStatement(expression=one())
                    ]),
                    alternative = ast.BlockStatement(statements=[
                        ast.ExpressionStatement(expression=one())
                    ])
                ), 
                ast.IfExpression(
                    condition = two(), 
                    consequence = ast.BlockStatement(statements=[
                        ast.ExpressionStatement(expression=two())
                    ]),
                    alternative = ast.BlockStatement(statements=[
                        ast.ExpressionStatement(expression=two())
                    ])
                )
            ),
            (ast.ReturnStatement(return_value=one()), ast.ReturnStatement(return_value=two())),
            (ast.LetStatement(value=one()), ast.LetStatement(value=two())),
            (
                ast.FunctionLiteral(
                    parameters = [], 
                    body = ast.BlockStatement(statements=[
                        ast.ExpressionStatement(expression=one())
                    ])
                ),
                ast.FunctionLiteral(
                    parameters = [], 
                    body = ast.BlockStatement(statements=[
                        ast.ExpressionStatement(expression=two())
                    ])
                )
            ),
            (
                ast.ArrayLiteral(elements=[one(), one()]), 
                ast.ArrayLiteral(elements=[two(), two()])
            )
        ]
        for t in tests:
            modified = modify.Modify(t[0], turn_one_into_two)
            deep_equals = (modified == t[1])
            self.assertTrue(deep_equals,
                'not equal. got={} want={}'.format(modified, t[1]))
        # HashLiteral needs to be tested slightly different
        hash_literal = ast.HashLiteral(pairs={
            one(): one(),
            two(): two()
        })
        hash_literal = modify.Modify(hash_literal, turn_one_into_two)
        for key, value in hash_literal.pairs.items():
            self.assertTrue(key == two(),
                'value is not {}. got={}'.format(2, key))
            self.assertTrue(value == two(),
                'value is not {}. got={}'.format(2, value))

if __name__ == '__main__':
    unittest.main()