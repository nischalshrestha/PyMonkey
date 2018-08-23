from monkey import ast

"""
Object stuff
"""

NULL_OBJ = 'NULL'
INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'

# object "interface"
class Object:
    def object_type(self): pass # ObjectType (str)
    def inspect(self): pass # str
    
class Null(Object):
    def object_type(self):
        return NULL_OBJ
    def inspect(self):
        return "null"

class Integer(Object):
    value = 0
    def __init__(self, value=0):
        self.value = value
    def object_type(self):
        return INTEGER_OBJ
    def inspect(self):
        return str(self.value)

class Boolean(Object):
    value = False
    def __init__(self, value=False):
        self.value = value
    def object_type(self):
        return BOOLEAN_OBJ
    def inspect(self):
        return str(self.value)

NULL = Null()
TRUE  = Boolean(True) 
FALSE = Boolean(False)

"""
Evaluator stuff
"""

# takes in ast.Node
def Eval(node):
    if type(node) is ast.Program:
        return eval_statements(node.statements)
    if type(node) is ast.ExpressionStatement:
        return Eval(node.expression)
    if type(node) is ast.IntegerLiteral:
        return Integer(node.value)
    if type(node) is ast.Boolean:
        return native_boolean_object(node.value)
    if type(node) is ast.PrefixExpression:
        right = Eval(node.right)
        return eval_prefix_expression(node.operator, right)
    return None

def eval_statements(statements):
    result = Object()
    for s in statements:
        result = Eval(s)
    return result

def eval_prefix_expression(operator, right):
    if operator == "!":
        return eval_bang_operator_expression(right)
    if operator == "-":
        return eval_minus_prefix_operator(right)
    return None

def eval_bang_operator_expression(right):
    if right == TRUE:
        return FALSE
    if right == FALSE:
        return TRUE
    if right == NULL:
        return TRUE
    return FALSE

def eval_minus_prefix_operator(right):
    if right.object_type() != INTEGER_OBJ:
        return NULL
    value = right.value
    return Integer(-value)

def native_boolean_object(boolean):
    if boolean:
        return TRUE
    return FALSE

"""
Enviroment stuff
"""
