"""
Monkey Compiler and Bytecode class definitions
"""

import sys
sys.path.append("../../")
from typing import NamedTuple
from typing import List

from monkey.ast import ast
from monkey.object import *
from monkey.code import code

class Bytecode(NamedTuple):
    instructions: code.Instructions
    constants: List[Object]

class EmittedInstruction(NamedTuple):
    opcode: bytes
    position: int

class Compiler:

    instructions: bytearray = None
    constants: List[Integer] = None
    last_instruction: EmittedInstruction = None
    previous_instruction: EmittedInstruction = None

    def __init__(self, instructions, constants, last_instruction, previous_instruction):
        self.instructions = instructions
        self.constants = constants
        self.last_instruction = last_instruction
        self.previous_instruction = previous_instruction

    def compile(self, node):
        """
        Walks the given AST and emits bytecode for the vm to execute
        """
        if isinstance(node, ast.Program):
            for s in node.statements:
                err = self.compile(s)
                if err != None:
                    return err
        elif isinstance(node, ast.ExpressionStatement):
            err = self.compile(node.expression)
            if err != None:
                return err
            self.emit(code.OpPop)
        elif isinstance(node, ast.PrefixExpression):
            err = self.compile(node.right)
            if err != None:
                return err
            if node.operator == '!':
                self.emit(code.OpBang)
            elif node.operator == '-':
                self.emit(code.OpMinus)
            else:
                return f'unknown operator {node.operator}'
        elif isinstance(node, ast.BlockStatement):
            for s in node.statements:
                err = self.compile(s)
                if err != None:
                    return err
        elif isinstance(node, ast.IfExpression):
            err = self.compile(node.condition)
            if err != None:
                return err
            # Emit an `OpJumpNotTruthy` with a bogus value
            jump_not_truthy_pos = self.emit(code.OpJumpNotTruthy, 9999)
            err = self.compile(node.consequence)
            if err != None:
                return  err
            if self.last_instruction_is_pop():
                self.remove_last_pop()
            after_conseq_pos = len(self.instructions)
            self.change_operand(jump_not_truthy_pos, after_conseq_pos)
        elif isinstance(node, ast.InfixExpression):
            # treat < as a special case by compiling right operand
            # before the left operand and simply work with OpGreaterThan
            # for e.g. for 3 > 5 one simply needs to flip operands to 5 > 3
            if node.operator == '<':
                err = self.compile(node.right)
                if err != None:
                    return err
                err = self.compile(node.left)
                if err != None:
                    return err
                self.emit(code.OpGreaterThan)
                return None
            err = self.compile(node.left)
            if err != None:
                return err
            err = self.compile(node.right)
            if err != None:
                return err
            if node.operator == '+':
                self.emit(code.OpAdd)
            elif node.operator == '-':
                self.emit(code.OpSub)
            elif node.operator == '*':
                self.emit(code.OpMul)
            elif node.operator == '/':
                self.emit(code.OpDiv)
            elif node.operator == '>':
                self.emit(code.OpGreaterThan)
            elif node.operator == '==':
                self.emit(code.OpEqual)
            elif node.operator == '!=':
                self.emit(code.OpNotEqual)
            else:
                return f'unknown operator {node.operator}'
        elif isinstance(node, ast.IntegerLiteral):
            integer = Integer(value=node.value)
            self.emit(code.OpConstant, self.add_constant(integer))
        elif isinstance(node, ast.Boolean):
            if node.value:
                self.emit(code.OpTrue)
            else:
                self.emit(code.OpFalse)
        return None

    def last_instruction_is_pop(self):
        return self.last_instruction.opcode == code.OpPop
    
    def remove_last_pop(self):
        self.instructions = self.instructions[:self.last_instruction.position]
        self.last_instruction = self.previous_instruction

    def add_constant(self, obj):
        """
        Add a given Object to the constant pool, currently just Integer(s)
        """
        self.constants.append(obj)
        return len(self.constants) - 1
    
    def emit(self, op, *operands):
        """
        Generate code for the given instruction based on opcode and operands
        and returnt the position
        """
        ins = code.Make(op, *operands)
        pos = self.add_instruction(ins)
        self.set_last_instruction(op, pos)
        return pos
    
    def set_last_instruction(self, op, pos):
        """
        Sets the last instruction given opcode and position
        """
        previous = self.last_instruction
        last = EmittedInstruction(op, pos)
        self.previous_instruction = previous
        self.last_instruction = last
    
    def change_operand(self, pos, operand):
        """
        Changes the old operand of an instruction to a new operand
        """
        op = self.instructions[pos]
        new_instruction = code.Make(op, operand)
        self.replace_instruction(pos, new_instruction)
    
    def replace_instruction(self, pos, new_instruction):
        """
        Replaces an instruction at some position in the instructions list.
        This is useful for setting the operand for OpJumpNotTruthy after compiling
        consequence. 
        Assumption: we only replace instructions of same type with same non-variable length
        """
        for i in range(len(new_instruction)):
            self.instructions[pos+i] = new_instruction[i]

    def add_instruction(self, ins):
        """
        Add an instruction and return its position in the instructions bytearray
        """
        pos_new_instruction = len(self.instructions)
        self.instructions += ins
        return pos_new_instruction
    
    def bytecode(self):
        """
        Return a bytecode representation of all instructions and the constant
        pool.
        """
        return Bytecode(self.instructions, self.constants)

def new():
    return Compiler(
        bytearray(), 
        [], 
        EmittedInstruction(None, 0), 
        EmittedInstruction(None, 0)
    )