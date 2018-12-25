from typing import NamedTuple
from typing import NewType
from typing import List
from enum import Enum, auto
from ctypes import c_uint16
import math

# For the sake of being explicit we definite expected types
Instructions = NewType('Instructions', bytearray)
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
                globals()[name] = bytes([last_value + 1])
                return last_value + 1
            except TypeError:
                pass
        else:
            globals()[name] = bytes([start])
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
        print('opcode {} undefined'.format(op))
        return None
    return definitions[op]

def Make(op, operands):
    """
    Creates and returns a bytecode instruction as a list [OpCode, Operand...]
    """
    if op not in definitions:
        return [bytes()]
    defn = definitions[op]
    instruction_len = 1 # opcode counts
    for w in defn.operand_widths:
        instruction_len += w
    instruction = [None for x in range(instruction_len)]
    instruction[0] = bytes(op)
    offset = 1
    for i, o in enumerate(operands):
        width = defn.operand_widths[i]
        if width == 2:
            instruction[offset:] = put_int_16(instruction[offset:], c_uint16(o).value)
        offset += width
    return instruction

def put_int_16(array, unint16):
    """
    Constructs and returns an array with the appropriate number of bytes 
    representing an usigned int
    """
    new_array = []
    byte_array = (unint16).to_bytes(byte_size(unint16), byteorder='big')
    for i in range(len(array)):
        new_array.append(byte_array[i])
    return new_array

def byte_size(integer):
    """
    Returns the number of bytes required to represent the integer based on the
    bit liength of the integer
    """
    return math.ceil(integer.bit_length() / 8)

# print(lookup(OpConstant))