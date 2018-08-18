from monkey import token
from monkey import lexer
from monkey import ast

from enum import Enum, auto

class Precedence(Enum):
    LOWEST = auto()
    EQUALS = auto()     
    LESSGREATER = auto()
    SUM = auto()         
    PRODUCT = auto()     
    PREFIX = auto()      
    CALL = auto()

class Parser:

    lexer = None
    cur_token = None
    peek_token = None
    errors = []
    prefix_parse_fns = {}
    infix_parse_fns = {}

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
        return self.parse_expression_statement()
    
    def parse_let_statement(self):
        stmt = ast.LetStatement(self.cur_token)
        if not self.expect_peek(token.IDENT):
            return None
        stmt.name = ast.Identifier(self.cur_token, self.cur_token.Literal)
        if not self.expect_peek(token.ASSIGN):
            return None
        while not self.current_token_is(token.SEMICOLON):
            self.next_token()
        return stmt

    def parse_return_statement(self):
        stmt = ast.ReturnStatement(self.cur_token)
        self.next_token()
        while not self.current_token_is(token.SEMICOLON):
            self.next_token()
        return stmt
    
    def parse_expression_statement(self):
        stmt = ast.ExpressionStatement(self.cur_token)
        stmt.expression = self.parse_expression(Precedence.LOWEST.value)
        if self.peek_token_is(token.SEMICOLON):
            self.next_token()
        return stmt
    
    def parse_expression(self, precedence):
        if self.cur_token.Type not in self.prefix_parse_fns:
            return None
        prefix = self.prefix_parse_fns[self.cur_token.Type]
        left_exp = prefix()
        return left_exp
    
    def parse_identifer(self):
        return ast.Identifier(self.cur_token, self.cur_token.Literal)
    
    def parse_integer_literal(self):
        lit = ast.IntegerLiteral(self.cur_token)
        try:
            value = int(self.cur_token.Literal)
            lit.value = value
            return lit
        except ValueError:
            msg = 'could not parse {} as integer'.format(self.cur_token)
            self.errors.append(msg)
            return None

    def peek_error(self, t):
        msg = 'expected token to be {}, got {} instead'.format(t, self.peek_token.Type)
        self.errors.append(msg)
    
    def register_prefix(self, token_type, fn):
        self.prefix_parse_fns[token_type] = fn
    
    def register_infix(self, token_type, fn):
        self.infix_parse_fns[token_type] = fn
        
    def prefix_parse_fn(self):
        pass
    
    def infix_parse_fn(self, expression):
        pass

def new(lexer):
    p = Parser(lexer)
    p.prefix_parse_fns = {}
    p.register_prefix(token.IDENT, p.parse_identifer)
    p.register_prefix(token.INT, p.parse_integer_literal)
    return p
    