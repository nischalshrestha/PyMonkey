import getpass
import sys
sys.path.append("../")
from monkey import repl

def main(interpreter=True):
    user = getpass.getuser()
    print("Hello %s! This is the Monkey programming language!\n" % user)
    print("Feel free to type in commands. To quit, enter exit()\n")
    repl.start(interpreter)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--c': # for using compiler
        main(False)
    else:                                           # otherwise, interpreter
        main()