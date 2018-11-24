from monkey.object import *
from monkey import evaluator

def _len(*args):
    arguments = args[0]
    arg = arguments[0]
    if len(arguments) != 1:
        return evaluator.new_error(f"wrong number of arguments. got={len(arguments)}, want=1")  
    elif isinstance(arg, Array):
        return Integer(len(arg.elements))
    elif isinstance(arg, String):
        return Integer(len(arg.value))
    return evaluator.new_error(f"argument to `len` not supported, got {arg.object_type()}")  

def _first(*args):
    arguments = args[0]
    arg = arguments[0]
    if len(arguments) != 1:
        return evaluator.new_error(f"wrong number of arguments. got={len(arguments)}, want=1")  
    elif not isinstance(arg, Array):
        return evaluator.new_error(f"argument to `first` must be ARRAY, got {arg.object_type()}") 
    if len(arg.elements) > 0:
        return arg.elements[0]
    return NULL

def _last(*args):
    arguments = args[0]
    arg = arguments[0]
    if len(arguments) != 1:
        return evaluator.new_error(f"wrong number of arguments. got={len(arguments)}, want=1")  
    elif not isinstance(arg, Array):
        return evaluator.new_error(f"argument to `last` must be ARRAY, got {arg.object_type()}") 
    length = len(arg.elements)
    if length > 0:
        return arg.elements[length-1]
    return NULL

def _rest(*args):
    arguments = args[0]
    arg = arguments[0]
    if len(arguments) != 1:
        return evaluator.new_error(f"wrong number of arguments. got={len(arguments)}, want=1")  
    elif not isinstance(arg, Array):
        return evaluator.new_error(f"argument to `rest` must be ARRAY, got {arg.object_type()}") 
    length = len(arg.elements)
    if length > 0:
        new_array = arg.elements[1:]
        return Array(new_array)
    return NULL

def _push(*args):
    arguments = args[0]
    arg = arguments[0]
    if len(arguments) != 2:
        return evaluator.new_error(f"wrong number of arguments. got={len(arguments)}, want=2")  
    elif not isinstance(arg, Array):
        return evaluator.new_error(f"argument to `push` must be ARRAY, got {arg.object_type()}")
    new_array = arg.elements[:]
    new_array.append(arguments[1])
    return Array(new_array)

def _puts(*args):
    for items in args:
        for a in items:
            print(a.inspect())
    return None

builtins = {
    'len': Builtin(_len),
    'first': Builtin(_first),
    'last': Builtin(_last),
    'push': Builtin(_push),
    'rest': Builtin(_rest),
    'puts': Builtin(_puts)
}