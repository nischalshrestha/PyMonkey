import getpass
import repl

def main():
    user = getpass.getuser()
    print("Hello %s! This is the Monkey programming language!\n" % user)
    print("Feel free to type in commands\n")
    repl.start()

if __name__ == '__main__':
    main()