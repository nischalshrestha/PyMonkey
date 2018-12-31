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
        ip = 0
        while ip <= code.bytes_to_int(self.instructions):
            op = self.instructions[ip]
            if op == code.OpConstant:
                # because we are using bytearray we will need to specify
                # the end range of the instructions bytearray so we don't
                # overshoot the operand and accidentally read next opcode
                const_index = code.bytes_to_int(self.instructions[ip+1:ip+3])
                # move ip up to next OpCode
                ip += 3
                err = self.push(self.constants[const_index])
                if err != None:
                    return err
            if op == code.OpAdd:
                right = self.pop()
                left = self.pop()
                left_value = left.value
                right_value = right.value
                result = left_value + right_value
                self.push(object.Integer(value=result))
                ip += 1
        return None
    
    def push(self, o):
        if self.sp >= STACK_SIZE:
            return "stack overflow"
        self.stack[self.sp] = o
        self.sp += 1
        return None

    def pop(self):
        o = self.stack[self.sp-1]
        self.sp -= 1
        return o

def new(bytecode):
    return VM(
        bytecode.instructions, 
        bytecode.constants, 
        utilities.make_list(STACK_SIZE), 
        0
    )
