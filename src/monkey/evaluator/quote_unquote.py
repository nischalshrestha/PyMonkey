"""
Functions to create Quote objects and evaluate unquotes
"""

from monkey import ast
from monkey import object
from monkey import evaluator
from monkey.tokens import token

def quote(node, env):
    node = eval_unquote_calls(node, env)
    return object.Quote(node)

def eval_unquote_calls(quoted, env):
    def modifier(node):
        # TODO make variables more explicit here
        if not is_unquote_call(node):
            return node
        if not isinstance(node, ast.CallExpression):
            return node
        if len(node.arguments) != 1:
            return node
        unquoted = evaluator.Eval(node.arguments[0], env)
        return convert_object_to_astnode(unquoted)
    return ast.Modify(quoted, modifier)

def is_unquote_call(node):
    if not isinstance(node, ast.CallExpression):
        return node
    return node.function.token_literal() == "unquote"

def convert_object_to_astnode(obj):
    if isinstance(obj, object.Integer):
        t = token.Token(Type=token.INT, Literal=str(obj.value))
        return ast.IntegerLiteral(t, obj.value)
    if isinstance(obj, object.Boolean):
        if obj.value:
            t = token.Token(Type=token.TRUE, Literal='true')
        else:
            t = token.Token(Type=token.FALSE, Literal='false')
        return ast.Boolean(t, obj.value)
    if isinstance(obj, object.Quote):
        # Quote already has the ASTNode object so just return it!
        return obj.node
    return None
        