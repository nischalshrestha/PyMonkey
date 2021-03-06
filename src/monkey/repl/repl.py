from monkey import lexer
from monkey.object import environment
from monkey import parser
from monkey import evaluator
from monkey import compiler
from monkey import vm
from monkey.compiler import symbol_table
from monkey.common import utilities
from monkey.evaluator import macro_expansion
import keyboard

prompt = ">> "
MONKEY_FACE = '''
            __,__
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \\
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"""""""-./, -' /
   ''-' /_   ^ ^   _\ '-''
       |  \._   _./  |
       \   \ '~' /   /
        '._ '-=-' _.'
           '-----'
'''

def start(interpreter=True):
    # need one instance since we are persisting values
    env = environment.new_environment()
    macro_env = environment.new_environment()
    # need to keep around constants, globals and symbol table for compiler
    constants = []
    global_vars = utilities.make_list(vm.GLOBAL_SIZE)
    sym_table = symbol_table.new_symbol_table()
    while True:
        line = input(prompt)
        if line == 'exit()':
            print('Goodbye!\n')
            break
        elif line == "":
            continue
        l = lexer.new(line)
        p = parser.new(l)
        program = p.parse_program()
        if len(p.errors) != 0:
            print_parse_errors(p.errors)
        else:
            if interpreter:
                macro_expansion.DefineMacros(program, macro_env)
                expanded = macro_expansion.ExpandMacros(program, macro_env)
                evaluated = evaluator.Eval(expanded, env)
                if evaluated != None:
                    print(evaluated.inspect(), '\n')
            else:
                # Note: Compiler is not yet completed
                comp = compiler.new_with_state(sym_table, constants)
                err = comp.compile(program)
                if err != None:
                    print(f'Woops! Compilation failed:\n{err}\n')
                    continue
                code = comp.bytecode()
                constants = code.constants
                machine = vm.new_with_global_store(code, global_vars)
                err = machine.run()
                if err != None:
                    print(f'Woops! Executing bytecode failed:\n{err}\n')
                    continue
                last_popped = machine.last_popped_stack_element()
                print(last_popped.inspect(), '\n')

def print_parse_errors(errors):
    print(MONKEY_FACE)
    print('Woops! We ran into some monkey business here!\n')
    print('parser errors:\n')
    for msg in errors:
        print("\t", msg, "\n")
