from typing import List

from monkey import code
from monkey import compiler
from monkey import object
from monkey.common import utilities

STACK_SIZE = 2048
TRUE = object.Boolean(True)
FALSE = object.Boolean(False)

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
        while ip < len(self.instructions):
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
            elif op == code.OpAdd or op == code.OpSub or op == code.OpMul or op == code.OpDiv:
                err = self.execute_binary_operation(op)
                if err != None:
                    return err
                ip += 1
            elif op == code.OpTrue:
                err = self.push(TRUE)
                if err != None:
                    return err
                ip += 1
            elif op == code.OpFalse:
                err = self.push(FALSE)
                if err != None:
                    return err
                ip += 1
            elif op == code.OpPop:
                self.pop()
                ip += 1
        return None

    def execute_binary_operation(self, op):
        right = self.pop()
        left = self.pop()
        left_type = left.object_type()
        right_type = right.object_type()
        if left_type == object.INTEGER_OBJ and right_type == object.INTEGER_OBJ:
            return self.execute_binary_integer_operation(op, left, right)
        return f'unsupported types for binary operation: {left_type} {right_type}'

    def execute_binary_integer_operation(self, op, left, right):
        left_value = left.value
        right_value = right.value
        result = 0
        if op == code.OpAdd:
            result = left_value + right_value
        elif op == code.OpSub:
            result = left_value - right_value
        elif op == code.OpMul:
            result = left_value * right_value
        elif op == code.OpDiv:
            result = left_value / right_value
        else:
            return f'unknown integer operator {op}'
        self.push(object.Integer(value=result))
    
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
    
    def last_popped_stack_element(self):
        return self.stack[self.sp]

def new(bytecode):
    return VM(
        bytecode.instructions, 
        bytecode.constants, 
        utilities.make_list(STACK_SIZE), 
        0
    )
