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

class Compiler:

    instructions = None
    constants = None

    def __init__(self, instructions, constants):
        self.instructions = instructions
        self.constants = constants

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
            self.emit(code.OpJumpNotTruthy, 9999)
            err = self.compile(node.consequence)
            if err != None:
                return  err
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

    def add_constant(self, obj):
        """
        Add a given Object to the constant pool, currently just Integer(s)
        """
        self.constants.append(obj)
        return len(self.constants) - 1
    
    def emit(self, op, *operands):
        """
        Generate code for the given instruction based on opcode and operands
        """
        ins = code.Make(op, *operands)
        pos = self.add_instruction(ins)
        return pos

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

class Bytecode(NamedTuple):
    instructions: code.Instructions
    constants: List[Object]

def new():
    return Compiler(bytearray(), [])