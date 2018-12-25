from typing import NamedTuple
from typing import NewType
from typing import List
from enum import Enum, auto
from ctypes import c_uint16
import math

# For the sake of being explicit we definite expected types
class Instructions:
    instructions = []

    def __init__(self, instructions=None):
        if instructions == None:
            self.instructions = []
        else:
            self.instructions = instructions

    def string(self):
        return ''

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
    # print('instruction len ', instruction_len)
    instruction = [None for x in range(instruction_len)]
    instruction[0] = bytes(op)
    offset = 1
    for i, o in enumerate(operands):
        width = defn.operand_widths[i]
        if width == 2:
            instruction[offset:] = put_int_16(instruction[offset:], c_uint16(o).value)
        offset += width
    # print('instruction:', instruction)
    return instruction

def put_int_16(array, unint16):
    """
    Constructs and returns an array with the appropriate number of bytes 
    representing an usigned int
    """
    new_array = []
    byte_array = (unint16).to_bytes(byte_size(unint16), byteorder='big')
    for i in byte_array:
        new_array.append(bytes([i]))
    return new_array

def byte_size(integer):
    """
    Returns the number of bytes required to represent the integer based on the
    bit liength of the integer
    """
    byte_s = math.ceil(integer.bit_length() / 8)
    return 1 if not byte_s else byte_s

def read_operands(defn, ins):
    operands = [None for x in range(len(defn.operand_widths))]
    offset = 0
    for i, width in enumerate(defn.operand_widths):
        if width == 2:
            operands[i] = bytes_to_int(ins[offset:])
            offset += width
    return operands, offset

def bytes_to_int(ins):
    concatted = ins[0]
    for i in range(1, len(ins)):
        concatted += ins[i]
    return int.from_bytes(concatted, byteorder='big')


# print(lookup(OpConstant))