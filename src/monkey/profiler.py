"""
Use this script to do profiling of tree-based interpreter and the vm-based compiler
"""

import sys
sys.path.append("../")
import time

from monkey import evaluator
from monkey import environment
from monkey import lexer
from monkey import parser

line = '''let fibonacci = fn(x) { if (x == 0) { return 0; } else { if (x == 1) { return 1; } else { fibonacci( x - 1) + fibonacci( x - 2); } } }; 
    fibonacci(25);'''
env = environment.new_environment()
l = lexer.new(line)
p = parser.new(l)
program = p.parse_program()
time0 = time.time()
evaluated = evaluator.Eval(program, env)
time1 = time.time()
print("time taken: ", time1-time0)