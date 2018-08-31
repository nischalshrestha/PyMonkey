from monkey.object import *
from monkey import evaluator

def _len(*args):
    arg = args[0]
    if len(arg) != 1:
        return evaluator.new_error(f"wrong number of arguments. got={len(arg)}, want=1")  
    elif isinstance(arg[0], String):
        return Integer(len(arg[0].value))
    return evaluator.new_error(f"argument to `len` not supported, got {arg[0].object_type()}")  

builtins = {
    'len': Builtin(_len)
}