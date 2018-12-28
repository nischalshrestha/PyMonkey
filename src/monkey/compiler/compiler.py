import sys
sys.path.append("../../")
from typing import NamedTuple
from typing import List

from monkey.ast import *
from monkey.object import *
from monkey.code import *

class Compiler:

    instructions = None
    constants = None

    def __init__(self, instructions, constants):
        self.instructions = instructions
        self.constants = constants

    def compile(self, node):
        if isinstance(node, Program):
            for s in node.statements:
                err = self.compile(s)
                if err != None:
                    return err
        elif isinstance(node, ExpressionStatement):
            err = self.compile(node.expression)
            if err != None:
                return err
        elif isinstance(node, InfixExpression):
            err = self.compile(node.left)
            if err != None:
                return err
            err = self.compile(node.right)
            if err != None:
                return err
        elif isinstance(node, IntegerLiteral):
            pass
        return None
    
    def bytecode(self):
        return Bytecode(self.instructions, self.constants)

class Bytecode(NamedTuple):
    instructions: Instructions
    constants: List[Object]

def new():
    return Compiler([], [])