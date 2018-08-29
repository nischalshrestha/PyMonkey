from monkey import ast

"""
Object stuff
"""

NULL_OBJ = 'NULL'
INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'
RETURN_VALUE_OBJ = 'RETURN_VALUE'
ERROR_OBJ = 'ERROR'
FUNCTION_OBJ = 'FUNCTION'

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

class ReturnValue(Object):
    value = None # Object
    def __init__(self, value=None):
        self.value = value
    def object_type(self):
        return RETURN_VALUE_OBJ
    def inspect(self):
        return self.value.inspect()

class Error(Object):
    message = None # Object
    def __init__(self, message=None):
        self.message = message
    def object_type(self):
        return ERROR_OBJ
    def inspect(self):
        return 'ERROR: '+ self.message

class Function(Object):
    parameters = [] # Identifier
    body = None # BlockStatement
    env = None # Environment
    
    def __init__(self, parameters=None, body=None, env=None):
        if parameters == None:
            parameters = []
        self.parameters = parameters
        self.body = body
        self.env = env

    def object_type(self):
        return FUNCTION_OBJ

    def inspect(self):
        params = []
        for p in self.parameters:
            params.append(p.string())
        out = ' fn('
        out = out + ','.join(params)
        out = out + ') {\n'
        out = out + self.body.string()
        out = out + '\n}'
        return out

NULL = Null()
TRUE  = Boolean(True) 
FALSE = Boolean(False)

"""
Evaluator stuff
"""

# takes in ast.Node
def Eval(node, env):
    if isinstance(node, ast.Program):
        return eval_program(node, env)
    elif isinstance(node, ast.ExpressionStatement):
        return Eval(node.expression, env)
    elif isinstance(node, ast.IntegerLiteral):
        return Integer(node.value)
    elif isinstance(node, ast.Boolean):
        return native_boolean_object(node.value)
    elif isinstance(node, ast.PrefixExpression):
        right = Eval(node.right, env)
        if is_error(right):
            return right
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, ast.InfixExpression):
        left = Eval(node.left, env)
        if is_error(left):
            return left
        right = Eval(node.right, env)
        if is_error(right):
            return right
        return eval_infix_expression(node.operator, left, right)
    elif isinstance(node, ast.BlockStatement):
        return eval_block_statement(node, env)
    elif isinstance(node, ast.IfExpression):
        return eval_if_expression(node, env)
    elif isinstance(node, ast.ReturnStatement):
        val = Eval(node.return_value, env)
        if is_error(val):
            return val
        return ReturnValue(val)
    elif isinstance(node, ast.LetStatement):
        val = Eval(node.value, env)
        if is_error(val):
            return val
        env.set_name(node.name.value, val)
    elif isinstance(node, ast.Identifier):
        return eval_identifier(node, env)
    return None

def is_error(obj):
    if obj != None:
        return obj.object_type() == ERROR_OBJ
    return False

def eval_program(program, env):
    result = Object()
    for s in program.statements:
        result = Eval(s, env)
        if isinstance(result, ReturnValue):
            return result.value
        if isinstance(result, Error):
            return result
    return result

def eval_block_statement(block, env):
    result = Object()
    for statement in block.statements:
        result = Eval(statement, env)
        rt = result.object_type()
        if rt == RETURN_VALUE_OBJ or rt == ERROR_OBJ:
            return result
    return result

def eval_prefix_expression(operator, right):
    if operator == "!":
        return eval_bang_operator_expression(right)
    if operator == "-":
        return eval_minus_prefix_operator(right)
    return new_error(f"unknown operator: {operator}{right.object_type()}")

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
        return new_error(f"unknown operator: -{right.object_type()}")
    value = right.value
    return Integer(-value)

def eval_infix_expression(operator, left, right):
    if left.object_type() == INTEGER_OBJ and right.object_type() == INTEGER_OBJ:
        return eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
        return native_boolean_object(left == right)
    elif operator == "!=":
        return native_boolean_object(left != right)
    elif left.object_type() != right.object_type():
        return new_error(f"type mismatch: {left.object_type()} {operator} {right.object_type()}")
    return new_error(f"unknown operator: {left.object_type()} {operator} {right.object_type()}")
    
def eval_integer_infix_expression(operator, left, right):
    left_val = left.value
    right_val = right.value
    if operator == "+":
        return Integer(left_val + right_val)
    elif operator == "-":
        return Integer(left_val - right_val)
    elif operator == "*":
        return Integer(left_val * right_val)
    elif operator == "/":
        return Integer(left_val / right_val)
    elif operator == "<":
        return native_boolean_object(left_val < right_val)
    elif operator == ">":
        return native_boolean_object(left_val > right_val)
    elif operator == "==":
        return native_boolean_object(left_val == right_val)
    elif operator == "!=":
        return native_boolean_object(left_val != right_val)
    return new_error(f"unknown operator: {left} {operator} {right.object_type()}")

def eval_if_expression(ie, env):
    condition = Eval(ie.condition, env)
    if is_truthy(condition):
        return Eval(ie.consequence, env)
    elif ie.alternative != None:
        return Eval(ie.alternative, env)
    return NULL

def is_truthy(obj):
    if obj == NULL:
        return False
    elif obj == TRUE:
        return True
    elif obj == FALSE:
        return False
    return True # number is truthy

def native_boolean_object(boolean):
    if boolean:
        return TRUE
    return FALSE

def new_error(string):
    return Error(string)

"""
Environment stuff
"""

def new_environment():
    return Environment({})

class Environment:
    store = {} # str

    def __init__(self, store):
        self.store = store
    
    def get(self, name):
        if name in self.store:
            return self.store[name]
        return None
    
    def set_name(self, name, value):
        self.store[name] = value
        return value

def eval_identifier(node, env):
    val = env.get(node.value)
    if val == None:
        return new_error("identifier not found: "+node.value)
    return val

