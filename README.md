# PyMonkey

### Description

Python version of the [Monkey](https://interpreterbook.com/#the-monkey-programming-language) programming language:

![alt text](https://interpreterbook.com/img/monkey_logo-d5171d15.png "Official Logo")

The Monkey interpreter plus macros can be run with:

`python main.py`

The compiler isn't complete yet but can be run with a flag `--c`:

`python compile.py --c`

Ultimately, to compile a Monkey file, this command will be used instead:

`python compile.py [Program.mnk] [args]`

**NOTE:** This is a personal project created for the sole purpose of learning how to build interpreters / compilers and honing my Python skills. You may borrow code under the licence.

### Dependencies

- Python 3.6+

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
