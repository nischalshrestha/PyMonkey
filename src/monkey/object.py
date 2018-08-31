from monkey import ast

"""
Object stuff
"""

NULL_OBJ = 'NULL'
INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'
STRING_OBJ = 'STRING'
RETURN_VALUE_OBJ = 'RETURN_VALUE'
ERROR_OBJ = 'ERROR'
FUNCTION_OBJ = 'FUNCTION'
BUILTIN_OBJ = 'BUILTIN'

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

class String(Object):
    value = ""
    def __init__(self, value=""):
        self.value = value
    def object_type(self):
        return STRING_OBJ
    def inspect(self):
        return self.value

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

    def __init__(self, parameters=None, env=None, body=None):
        if parameters == None:
            parameters = []
        self.parameters = parameters
        self.env = env
        self.body = body

    def object_type(self):
        return FUNCTION_OBJ

    def inspect(self):
        params = []
        for p in self.parameters:
            params.append(p.string())
        out = 'fn('
        out = out + ','.join(params)
        out = out + ') {\n'
        out = out + self.body.string()
        out = out + '\n}'
        return out
    
class Builtin(Object):
    fn = None # function
    def __init__(self, fn):
        self.fn = fn
    def object_type(self):
        return BUILTIN_OBJ
    def inspect(self):
        return 'builtin function'

NULL = Null()
TRUE  = Boolean(True) 
FALSE = Boolean(False)