from monkey import ast
from fnvhash import fnv1_64

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
ARRAY_OBJ = 'ARRAY'

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
    def hash_key(self):
        return HashKey(self.object_type(), self.value)

class Boolean(Object):
    value = False
    def __init__(self, value=False):
        self.value = value
    def object_type(self):
        return BOOLEAN_OBJ
    def inspect(self):
        return str(self.value)
    def hash_key(self):
        value = 0
        if not self.value: value = 1
        return HashKey(self.object_type(), value)

class String(Object):
    value = ""
    def __init__(self, value=""):
        self.value = value
    def object_type(self):
        return STRING_OBJ
    def inspect(self):
        return self.value
    def hash_key(self):
        return HashKey(self.object_type(), fnv1_64(self.value.encode()))

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

class Array(Object):
    elements = [] # Object
    def __init__(self, elements):
        self.elements = elements
    def object_type(self):
        return ARRAY_OBJ
    def inspect(self):
        elements = []
        for e in self.elements:
            elements.append(e.inspect())
        out = '[' + ','.join(elements) + "]"
        return out

class HashKey(Object):
    key = None
    value = 0

    def __init__(self, key, value):
        self.key = key
        self.value = value

NULL = Null()
TRUE  = Boolean(True) 
FALSE = Boolean(False)