"""
This module defines OpCodes and the Instructions class representing a bytecode
instruction for Monkey.

For the sake of being explicit we define expected types with typing module
"""

from typing import NamedTuple
from typing import NewType
from typing import List
from enum import Enum, auto
from ctypes import c_uint16
import math

from monkey.common import utilities

class Instructions:

    instructions: bytearray = None

    def __init__(self, instructions=None):
        if instructions != None:
            self.instructions = instructions

    def __str__(self):
        out = ''
        i = 0
        ins = self.instructions
        while i < len(ins):
            defn, err = lookup(ins[i])
            if err != None:
                out += (f'ERROR: {err}\n')
                i += 1
                continue
            operands, read = read_operands(defn, ins[i+1:])
            out += ('{0:04d} {1}\n'.format(i, self.string_instruction(defn, operands)))     
            i += 1 + read
        return out
    
    def string_instruction(self, defn, operands):
        operand_count = len(defn.operand_widths)
        operand = c_uint16(int.from_bytes(operands, byteorder='big')).value
        # For now, this is a hack to check operand length since len() works
        # differently for bytearray compared to lists
        length = len([int.from_bytes(operands, byteorder='big')])
        if length != operand_count:
            return (f'ERROR: operand len {len(operands)} does not match defined {operand_count}\n')
        if operand_count == 1:
            return (f'{defn.name} {operand}')
        return (f'ERROR: unhandled operand_count for {operand_count}\n')

OpCode = NewType('OpCode', bytes)

class ByteEnum(Enum):
    """
    This class is the same as Enum except it stores the OpCodes
    in the global space so it's easy to reference.
    """
    def _generate_next_value_(name, start, count, last_values):
        """
        Stores <OpCode, Byte> into the global space such that each OpCode
        has a corresponding unique bytes value.
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

class Definition(NamedTuple):
    name: str
    operand_widths: List[bytes]

# This is just to be transparent about what the OpCodes do and for debugging or
# testing purposes
definitions = {
    OpConstant : Definition("OpConstant", [2]), # operand_widths is two bytes
}

def lookup(op):
    if op not in definitions:
        return None, f'opcode {op} undefined'
    return definitions[op], None

def Make(op, *operands):
    """
    Creates and returns a bytecode instruction as a list [OpCode, Operand...]
    """
    if op not in definitions:
        return [bytes()]
    defn = definitions[op]
    instruction_len = 1 # opcode counts
    for w in defn.operand_widths:
        instruction_len += w
    # instruction byte size is opcode plus operand_widths
    instruction = bytearray(1 + defn.operand_widths[0])
    instruction[0] = op
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

def read_operands(defn, ins):
    total_width = len(defn.operand_widths)
    operands = bytearray(len(defn.operand_widths))
    offset = 0
    for i, width in enumerate(defn.operand_widths):
        if width == 2:
            operands[i:i+width] = ins[offset:offset+width]
        offset += width
    return operands, offset
