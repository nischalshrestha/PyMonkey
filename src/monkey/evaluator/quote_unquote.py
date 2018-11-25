from monkey import ast
from monkey import object

def quote(node):
    return object.Quote(node)