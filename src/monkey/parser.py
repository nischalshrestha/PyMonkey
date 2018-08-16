from monkey import token
from monkey import lexer
from monkey import ast

class Parser:

    lexer = None
    cur_token = None
    peek_token = None
    errors = []

    def __init__(self, lexer, errors=[]):
        self.lexer = lexer
        self.errors = errors
        self.next_token()
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()
    
    def current_token_is(self, t):
        return self.cur_token.Type == t

    def peek_token_is(self, t):
        return self.peek_token.Type == t

    def expect_peek(self, t):
        if self.peek_token_is(t):
            self.next_token()
            return True
        self.peek_error(t)
        return False

    def parse_program(self):
        program = ast.Program()
        while self.cur_token.Type != token.EOF:
            stmt = self.parse_statement()
            if stmt != None:
                program.statements.append(stmt)
            self.next_token()
        return program

    def parse_statement(self):
        if self.cur_token.Type == token.LET:
            return self.parse_let_statement()
        if self.cur_token.Type == token.RETURN:
            return self.parse_return_statement()
        return None
    
    def parse_let_statement(self):
        statement = ast.LetStatement(self.cur_token)
        if not self.expect_peek(token.IDENT):
            return None
        statement.name = ast.Identifier(self.cur_token, self.cur_token.Literal)
        if not self.expect_peek(token.ASSIGN):
            return None
        while not self.current_token_is(token.SEMICOLON):
            self.next_token()
        return statement

    def parse_return_statement(self):
        statement = ast.ReturnStatement(self.cur_token)
        self.next_token()
        while not self.current_token_is(token.SEMICOLON):
            self.next_token()
        return statement

    def peek_error(self, t):
        msg = "expected token to be {}, got {} instead".format(t, self.peek_token.Type)
        self.errors.append(msg)
        

def new(lexer):
    return Parser(lexer)
    