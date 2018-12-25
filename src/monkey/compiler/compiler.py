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
        return None
    
    def bytecode(self):
        return Bytecode(self.instructions, self.constants)

class Bytecode(NamedTuple):
    instructions: Instructions
    constants: List[Object]

def new():
    return Compiler([], [])