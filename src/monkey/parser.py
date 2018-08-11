from monkey import token
from monkey import lexer
from monkey import ast

class Parser:

    lexer = None
    cur_token = None
    peek_token = None

    def __init__(self, lexer):
        self.lexer = lexer
        self.next_token()
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        return None


def new(lexer):
    return Parser(lexer)
    