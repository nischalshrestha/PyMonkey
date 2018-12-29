from typing import List

from monkey import code
from monkey import compiler
from monkey import object
from monkey.common import utilities

STACK_SIZE = 2048

class VM:

    constants: List[object.Object] = []
    instructions: code.Instructions = None
    stack: List[object.Object] = []
    sp: int = 0

    def __init__(self, instructions, constants, stack, sp):
        self.instructions = instructions
        self.constants = constants
        self.stack = stack
        self.sp = sp

    def stack_top(self):
        return None if self.sp == 0 else self.stack[self.sp - 1]
    
    def run(self):
        for ip in range(len(self.instructions)):
            op = self.instructions[ip]
            if op == code.OpConstant:
                const_index = code.bytes_to_int(self.instructions[ip+1:])
                ip += 2
                err = self.push(self.constants[const_index])
                if err != None:
                    return err
        return None
    
    def push(self, o):
        if self.sp >= STACK_SIZE:
            return "stack overflow"
        self.stack[self.sp] = o
        self.sp += 1
        return None

def new(bytecode):
    return VM(
        bytecode.instructions, 
        bytecode.constants, 
        utilities.make_list(STACK_SIZE), 
        0
    )
