"""
This module defines OpCodes and the Instructions class representing a bytecode
instruction for Monkey.

For the sake of being explicit we define expected types with typing module
"""

from typing import NamedTuple
from typing import List
from enum import Enum, auto
from ctypes import c_uint16
import math

from monkey.common import utilities

class Instructions:

    # instructions are represented as bytearray as they behave like lists
    # and are amenable to most string operations like indexing
    instructions: bytearray = None

    def __init__(self, instructions=None):
        if instructions != None:
            self.instructions = instructions

    def __str__(self):
        """
        Prints a nicely-formatted string version of the instruction like so:

        <offset> <OpCode> <Operand>

        where offset is which index the instruction starts in the total bytecode,
        OpCode is the name of the instruciton and the operand is the bytecode for
        the operands.
        """
        out = ''
        i = 0
        ins = self.instructions
        while i < len(ins):
            defn, err = lookup(ins[i])
            if err != None:
                out += (f'ERROR: {err}\n')
                continue
            operands, read = read_operands(defn, ins[i+1:])
            out += ('{0:04d} {1}\n'.format(i, self.string_instruction(defn, operands)))     
            i += 1 + read
        return out
    
    def string_instruction(self, defn, operands):
        """
        Returns a formatted string representing the <OpCode> <Operand> or an 
        error message.
        """
        operand_count = len(defn.operand_widths)
        operand = c_uint16(int.from_bytes(operands, byteorder='big')).value
        if operand_count > 0:
            # For now, this is a hack to check operand length since len() works
            # differently for bytearray compared to lists
            length = len([int.from_bytes(operands, byteorder='big')])
        else:
            # in the case of 0 operands, we can just take len of operands
            length = len(operands)

        if length != operand_count:
            print('err', defn.name, length, operand_count)
            return f'ERROR: operand len {length} does not match defined {operand_count}\n'

        if operand_count == 0:
            return defn.name
        elif operand_count == 1:
            return f'{defn.name} {operand}'

        return f'ERROR: unhandled operand_count for {operand_count}\n'

class ByteEnum(Enum):
    """
    This class is the same as Enum except it stores the OpCodes
    in the global space so it's easy to reference.
    """
    def _generate_next_value_(name, start, count, last_values):
        """
        Stores <OpCode, Integer> into the global space such that each OpCode
        has a corresponding unique int value.
        """
        for last_value in reversed(last_values):
            try:
                globals()[name] = last_value + 1
                return last_value + 1
            except TypeError:
                pass
        else:
            globals()[name] = start
            return start

class OpCodes(ByteEnum):
    OpConstant = auto()
    OpAdd = auto()
    OpPop = auto()
    OpSub = auto()
    OpMul = auto()
    OpDiv = auto()
    OpTrue = auto()
    OpFalse = auto()
    OpEqual = auto()
    OpNotEqual = auto()
    OpGreaterThan = auto()
    OpMinus = auto()
    OpBang = auto()
    OpJumpNotTruthy = auto()
    OpJump = auto()

class Definition(NamedTuple):
    name: str
    # this represents a list of operands defined by an int indicating how many
    # bytes each one should be; for e.g. [2] means 1 operand that is 2 bytes
    operand_widths: List[int]

# Holds the Definitions for all the OpCodes in Monkey
definitions = {
    OpConstant : Definition("OpConstant", [2]),
    OpAdd : Definition("OpAdd", []),
    OpPop : Definition("OpPop", []),
    OpSub : Definition("OpSub", []),
    OpMul : Definition("OpMul", []),
    OpDiv : Definition("OpDiv", []),
    OpTrue : Definition("OpTrue", []),
    OpFalse : Definition("OpFalse", []),
    OpEqual : Definition("OpEqual", []),
    OpNotEqual : Definition("OpNotEqual", []),
    OpGreaterThan : Definition("OpGreaterThan", []),
    OpMinus : Definition("OpMinus", []),
    OpBang : Definition("OpBang", []),
    OpJumpNotTruthy : Definition("OpJumpNotTruthy", [2]),
    OpJump : Definition("OpJump", [2]),
}

def lookup(op):
    """
    Looks up the OpCode represented as an int in the definitions dictionary.
    If found, returns the Definition and a None
    Else, it returns a None and an error message
    """
    if op not in definitions:
        return None, f'opcode {op} undefined'
    return definitions[op], None

def Make(op, *operands):
    """
    Creates and returns a bytecode instruction as a bytearray (OpCode + Operand...)
    """
    if op not in definitions:
        return [bytes()]
    defn = definitions[op]
    instruction_len = 1 # opcode counts
    for w in defn.operand_widths:
        instruction_len += w
    # instruction byte size is opcode plus operand_widths (if any operands)
    instruction = bytearray(instruction_len)
    instruction[0] = op
    if instruction_len >= 1:
        offset = 1
        # We can do almost all string operators with bytes w. exceptions:
        # https://docs.python.org/3.3/library/stdtypes.html#bytes-methods
        for i, o in enumerate(operands):
            width = defn.operand_widths[i]
            if width == 2:
                instruction[offset:] = put_int_16(instruction[offset:], c_uint16(o).value)
            offset += width
    return instruction

def put_int_16(array, unint16):
    """
    Constructs and returns a bytearray with the appropriate bytes 
    representing an usigned int
    """
    return bytearray((unint16).to_bytes(byte_size(unint16), byteorder='big'))

def byte_size(integer):
    """
    Returns the number of bytes required to represent the integer based on the
    bit length of the integer (if only 1 byte needed, make default 2 bytes)
    """
    byte_s = math.ceil(integer.bit_length() / 8)
    return 2 if byte_s < 2 else byte_s

def bytes_to_int(ins):
    """
    Converts bytes representing an integer to an integer
    """
    concatted = ins[0]
    i = 1
    while i < len(ins):
        concatted += ins[i]
        i += 1
    return concatted

def read_operands(defn, ins):
    """
    Given the Definition of the instruction, and the instruction itself,
    this function reads operands portion of the instruction bytecode and 
    returns them along with the updated offset into the instruction.
    """
    operands = bytearray(len(defn.operand_widths))
    offset = 0
    for i, width in enumerate(defn.operand_widths):
        if width == 2:
            operands[i:i+width] = ins[offset:offset+width]
        offset += width
    return operands, offset
