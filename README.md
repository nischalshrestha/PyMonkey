# PyMonkey

### Description

Python version of the [Monkey](https://interpreterbook.com/#the-monkey-programming-language) programming language:

![alt text](https://interpreterbook.com/img/monkey_logo-d5171d15.png "Official Logo")

**NOTE:** This is a personal project created for the sole purpose of learning how to build interpreters / compilers and honing my Python skills. You may borrow code under the licence.

### Dependencies

- Python 3.6+

### Execution

Inside the [src/monkey](https://github.com/nischalshrestha/PyMonkey/tree/master/src/monkey):

The Monkey interpreter plus macros can be run with:

`python main.py`

The compiler isn't complete yet but can be run with a flag `--c`:

`python main.py --c`

Ultimately, to compile a Monkey file, this command will be used instead:

`python main.py [Program.mnk] [args]`

### Testing

Inside the [test](https://github.com/nischalshrestha/PyMonkey/tree/master/test):

`python [test_file].py`

### Progress

#### Interpreter

- [x] Interpreter
- [x] Built-in types and functions

#### Extras
- [x] Macros

#### Compiler

- [x] Compile expressions
- [x] Conditionals
- [ ] Data structures
- [ ] Functions
- [ ] Closures

#### Possible Future extensions
- Better error handling (stack trace)
- More operators like postfix (e.g. ++, --) or ternary
- Default arguments to functions 
- Macros hygiene 
- Debugging Macros
- Continuations
- Time travel debugging
