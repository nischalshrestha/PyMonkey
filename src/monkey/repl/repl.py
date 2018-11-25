from monkey import lexer
from monkey.object import environment
from monkey import parser
from monkey import evaluator
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

def start():
    # need one instance since we are persisting values
    env = environment.new_environment()
    while True:
        line = input(prompt)
        if line == 'exit()':
            print('Goodbye!\n')
            break
        l = lexer.new(line)
        p = parser.new(l)
        program = p.parse_program()
        if len(p.errors) != 0:
            print_parse_errors(p.errors)
        else:
            evaluated = evaluator.Eval(program, env)
            if evaluated != None:
                print(evaluated.inspect(), '\n')

def print_parse_errors(errors):
    print(MONKEY_FACE)
    print('Woops! We ran into some monkey business here!\n')
    print('parser errors:\n')
    for msg in errors:
        print("\t", msg, "\n")

