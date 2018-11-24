from monkey import ast
from monkey.object import *
from monkey.environment import *
from monkey.builtins import *

# takes in ast.Node
def Eval(node, env):
    if isinstance(node, ast.Program):
        return eval_program(node, env)
    elif isinstance(node, ast.ExpressionStatement):
        return Eval(node.expression, env)
    elif isinstance(node, ast.IntegerLiteral):
        return Integer(node.value)
    elif isinstance(node, ast.StringLiteral):
        return String(node.value)
    elif isinstance(node, ast.Boolean):
        return native_boolean_object(node.value)
    elif isinstance(node, ast.HashLiteral):
        return eval_hash_literal(node, env)
    elif isinstance(node, ast.ArrayLiteral):
        elements = eval_expressions(node.elements, env)
        if len(elements) == 1 and is_error(elements[0]):
            return elements[0]
        return Array(elements)
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
    elif isinstance(node, ast.IndexExpression):
        left = Eval(node.left, env)
        if is_error(left):
            return left
        index = Eval(node.index, env)
        if is_error(index):
            return index
        return eval_index_expression(left, index)
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
    elif isinstance(node, ast.FunctionLiteral):
        params = node.parameters
        body = node.body
        return Function(params, env, body)
    elif isinstance(node, ast.CallExpression):
        function = Eval(node.function, env)
        if is_error(function):
            return function
        args = eval_expressions(node.arguments, env)
        if len(args) == 1 and is_error(args[0]):
            return args[0]
        return apply_function(function, args)
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

def eval_expressions(exps, env):
    result = []
    for e in exps:
        evaluated = Eval(e, env)
        if is_error(evaluated):
            return [evaluated]
        result.append(evaluated)
    return result

def apply_function(fn, args):
    if isinstance(fn, Function):
        extended_env = extend_function_env(fn, args)
        evaluated = Eval(fn.body, extended_env)
        return unwrapped_return_value(evaluated)
    elif isinstance(fn, Builtin):
        return fn.fn(args)
    return new_error(f"not a function: {fn.object_type()}")

def extend_function_env(fn, args):
    env = new_enclosed_environment(fn.env)
    # set all params for this enclosed env
    for i, param in enumerate(fn.parameters):
        env.set_name(param.value, args[i])
    return env

def unwrapped_return_value(obj):
    if isinstance(obj, ReturnValue):
        return obj.value
    return obj

def eval_block_statement(block, env):
    result = Object()
    for statement in block.statements:
        result = Eval(statement, env)
        if result != None:
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
    elif left.object_type() == STRING_OBJ and right.object_type() == STRING_OBJ:
        return eval_string_infix_expression(operator, left, right)
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
    return new_error(f"unknown operator: {left.object_type()} {operator} {right.object_type()}")

def eval_string_infix_expression(operator, left, right):
    if operator != "+":
        return new_error(f"unknown operator: {left.object_type()} {operator} {right.object_type()}")
    left_val = left.value
    right_val = right.value
    return String(left_val + right_val)

def eval_index_expression(left, index):
    if left.object_type() == ARRAY_OBJ and index.object_type() == INTEGER_OBJ:
        return eval_array_index_expression(left, index)
    elif left.object_type() == HASH_OBJ:
        return eval_hash_index_expression(left, index)
    return new_error(f"index operator not supported: {left.object_type()}")

def eval_hash_literal(node, env):
    pairs = {}
    for key_node, value_node in node.pairs.items():
        key = Eval(key_node, env)
        if is_error(key):
            return key
        if not callable(getattr(key, 'hash_key', None)):
            return new_error(f"unusable as hash key: {key.object_type()}")
        value = Eval(value_node, env)
        if is_error(value):
            return value
        hashed = key.hash_key()
        pairs[hashed] = HashPair(key, value)
    return Hash(pairs)

def eval_hash_index_expression(hash, index):
    hash_object = hash
    if not callable(getattr(index, 'hash_key', None)):
        return new_error(f"unusable as hash key: {index.object_type()}")
    pair = NULL
    key = index.hash_key()
    if key in hash_object.pairs:
        pair = hash_object.pairs[key]
    return pair.value if pair != NULL else pair

def eval_array_index_expression(array, index):
    array_object = array
    idx = index.value
    max_size = len(array_object.elements) - 1
    if idx < 0 or idx > max_size:
        return NULL
    return array_object.elements[idx]
    
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

def new_enclosed_environment(outer):
    env = new_environment()
    env.outer = outer
    return env

def eval_identifier(node, env):
    val = env.get(node.value)
    if val != None:
        return val
    elif node.value in builtins:
        return builtins[node.value]
    return new_error("identifier not found: "+node.value)