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
    return modifier(node)