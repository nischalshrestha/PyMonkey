import getpass
import sys
sys.path.append("../")
from monkey import repl

def main():
    user = getpass.getuser()
    print("Hello %s! This is the Monkey programming language!\n" % user)
    print("Feel free to type in commands. To quit, enter exit()\n")
    repl.start()

if __name__ == '__main__':
    main()