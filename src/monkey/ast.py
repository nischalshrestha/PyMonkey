# from typing import NamedTuple
from monkey import token

class Node:
    # this method used only for debugging
    def token_literal(self):
        pass
    def string(self):
        pass

class Statement(Node):
    node = None
    # dummy method
    def statement_node(self):
        pass

class Expression(Node):
    node = None
    # dummy method
    def expression_node(self):
        pass

class Program(Node):
    statements = []

    def __init__(self, statements=[]):
        self.statements = statements

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].TokenLiteral()
        else:
            return ""
    
    def string(self):
        # for now just return string
        out = ""
        for s in self.statements:
            out = out + s
        return out

class Identifier(Expression):
    token = None # Token
    value = ""
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.Literal
        
class LetStatement(Statement):
    token = None # Token
    name = None # Identifier
    value = None # Expression

    def __init__(self, token, name=None, value=None):
        self.token = token
        self.name = name
        self.value = value

    def token_literal(self):
        return self.token.Literal

