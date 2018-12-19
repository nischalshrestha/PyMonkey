"""
This class has functions to modify AST Nodes for macros
"""
from monkey import ast

def Modify(node, modifier):
    """
    Modifies a given AST Node with the provided modifier function
    """
    if isinstance(node, ast.Program):
        for i, statement in enumerate(node.statements):
            node.statements[i] = Modify(statement, modifier)
    elif isinstance(node, ast.ExpressionStatement):
        node.expression = Modify(node.expression, modifier)
    elif isinstance(node, ast.InfixExpression): 
        node.left = Modify(node.left, modifier)
        node.right = Modify(node.right, modifier)
    elif isinstance(node, ast.PrefixExpression):
        node.right = Modify(node.right, modifier)
    elif isinstance(node, ast.IndexExpression):
        node.left = Modify(node.left, modifier)
        node.index = Modify(node.index, modifier)
    return modifier(node)