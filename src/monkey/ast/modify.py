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
    elif isinstance(node, ast.IfExpression):
        node.condition = Modify(node.condition, modifier)
        node.consequence = Modify(node.consequence, modifier)
        if node.alternative != None:
            node.alternative = Modify(node.alternative, modifier)
    elif isinstance(node, ast.BlockStatement):
        for statement in node.statements:
            statement = Modify(statement, modifier)
    elif isinstance(node, ast.ReturnStatement):
        node.return_value = Modify(node.return_value, modifier)
    elif isinstance(node, ast.LetStatement):
        node.value = Modify(node.value, modifier)
    elif isinstance(node, ast.FunctionLiteral):
        for parameter in node.parameters:
            parameter = Modify(parameter, modifier)
        node.body = Modify(node.body, modifier)
    elif isinstance(node, ast.ArrayLiteral):
        for element in node.elements:
            element = Modify(element, modifier)
    elif isinstance(node, ast.HashLiteral):            
        new_pairs = {}
        for key, value in node.pairs.items():
            new_key = Modify(key, modifier)
            new_value = Modify(value, modifier)
            new_pairs[new_key] = new_value
        node.pairs = new_pairs
    return modifier(node)