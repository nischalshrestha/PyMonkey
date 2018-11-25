# from typing import NamedTuple
from monkey.tokens import token

class Node:
    # this method used only for debugging
    def token_literal(self): pass
    def string(self): pass

class Statement(Node):
    node = None
    # dummy method
    def statement_node(self): pass

class Expression(Node):
    node = None
    # dummy method
    def expression_node(self): pass

class Program(Node):
    statements = []

    def __init__(self, statements=None):
        if statements == None:
            statements = []
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
            out = out + s.string()
        return out

class Identifier(Expression):
    token = None # Token
    value = "" 

    def __init__(self, token, value):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        return self.value
        
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

    def string(self):
        out = self.token_literal() + " "
        out = out + self.name.string()
        out = out + " = "
        if self.value != None:
            out = out + self.value.string()
        out = out + ";"
        return out

class ReturnStatement(Statement):
    token = None # Token
    return_value = None # Expression

    def __init__(self, token, value=None):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.Literal

    def string(self):
        out = self.token_literal() + " "
        if self.return_value != None:
            out = out + self.return_value.string()
        out = out + ";"
        return out

class ExpressionStatement(Statement):
    token = None 
    expression = None # Expression

    def __init__(self, token=None, expression=None):
        self.token = token
        self.expression = expression
    
    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        if self.expression != None:
            return self.expression.string()
        return ""
    
    def __eq__(self, other):
        return isinstance(other, ExpressionStatement) and self.__dict__ == other.__dict__

class IntegerLiteral(Expression):
    token = None # Token
    value = 0 # integer

    def __init__(self, token=None, value=0):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, IntegerLiteral) and self.__dict__ == other.__dict__

class StringLiteral(Expression):
    token = None # Token
    value = "" # str

    def __init__(self, token, value=""):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        return self.token.Literal

class PrefixExpression(Expression):
    token = None # Token
    operator = ""
    right = None # Expression

    def __init__(self, token, operator="", right=None):
        self.token = token
        self.operator = operator
        self.right = right

    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        out = "(" + self.operator + self.right.string() + ")" 
        return out

class InfixExpression(Expression):
    token = None # Token
    left = None # Expression
    operator = ""
    right = None # Expression

    def __init__(self, token, operator="", left=None, right=None):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        out = "(" + self.left.string() + " " + self.operator + " " + self.right.string() + ")"
        return out

class Boolean(Expression):
    token = None
    value = False

    def __init__(self, token, value):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        return self.token.Literal

class IfExpression(Expression):
    token = None # 'if' token
    condition = None # Expression
    consequence = None # BlockStatement
    alternative = None # BlockStatement

    def __init__(self, token, condition=None, consequence=None, alternative=None):
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        out = "if" + self.condition.string() + " " + self.consequence.string()
        if self.alternative != None:
            out = out + "else " + self.alternative.string()
        return out

class BlockStatement(Statement):
    token = None 
    statements = [] # Statement(s)

    def __init__(self, token, statements=None):
        self.token = token
        if statements == None:
            statements = []
        self.statements = statements
    
    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        out = ""
        for s in self.statements:
            out = out + s.string()
        return out

class CallExpression(Expression):

    token = None
    function = None # Identifier or FunctionLiteral
    arguments = [] # Expression

    def __init__(self, token, function=None, arguments=None):
        self.token = token
        self.function = function
        if arguments == None:
            arguments = []
        self.arguments = arguments

    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        args  = []
        for a in self.arguments:
            args.append(a.string())
        out = "" + self.function.string()
        out = out + "(" + ", ".join(args) + ")"
        return out

class FunctionLiteral(Expression):
    token = None # fn
    parameters = [] # Identifier
    body = None # BlockStatement

    def __init__(self, token, parameters=None, body=None):
        self.token = token
        if parameters == None:
            parameters = []
        self.parameters = parameters
        self.body = body

    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        args  = []
        for a in self.arguments:
            args.append(a.string())
        out = "" + self.function.string()
        out = out + "(" + ", ".join(args) + ")"
        return out

class ArrayLiteral(Expression):
    token = None
    elements = [] # Expression

    def __init__(self, token, elements=None):
        self.token = token
        if elements == None:
            elements = []
        self.elements = elements
    
    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        elements  = []
        for e in self.elements:
            elements.append(e.string())
        out = "[" + ", ".join(elements) + "]"
        return out

class IndexExpression(Expression):
    token = None
    left = None # Expression
    index = None # Expression

    def __init__(self, token, left=None, index=None):
        self.token = token
        self.left = left
        self.index = index
    
    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        out = "(" + self.left.string() + "[" +  self.index.string() + "])"
        return out

class HashLiteral(Expression):
    token = None # { token
    pairs = {} # Expression

    def __init__(self, token, pairs=None):
        self.token = token
        self.pairs = pairs
    
    def token_literal(self):
        return self.token.Literal
    
    def string(self):
        pairs = []
        for key, value in self.pairs.items():
            pairs.append(key.string() + ":" + value.string())
        out = "{" + ", ".join(pairs) + "}"
        return out