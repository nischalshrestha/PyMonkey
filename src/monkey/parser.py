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

precedences = {
    token.EQ: Precedence.EQUALS.value,
    token.NOT_EQ: Precedence.EQUALS.value,
    token.LT: Precedence.LESSGREATER.value,
    token.GT: Precedence.LESSGREATER.value,
    token.PLUS: Precedence.SUM.value,
    token.MINUS: Precedence.SUM.value,
    token.SLASH: Precedence.PRODUCT.value,
    token.ASTERISK: Precedence.PRODUCT.value,
}

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
            self.no_prefix_parse_fn_error(self.cur_token.Type)
            return None
        prefix = self.prefix_parse_fns[self.cur_token.Type]
        left_exp = prefix()
        while not self.peek_token_is(token.SEMICOLON) and precedence < self.peek_precendence():
            if self.peek_token.Type not in self.infix_parse_fns:
                return left_exp
            infix = self.infix_parse_fns[self.peek_token.Type]
            self.next_token()
            left_exp = infix(left_exp)
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
    
    def parse_prefix_expression(self):
        expression = ast.PrefixExpression(self.cur_token, self.cur_token.Literal)
        self.next_token()
        expression.right = self.parse_expression(Precedence.PREFIX.value)
        return expression
        
    def no_prefix_parse_fn_error(self, token_type):
        msg = "no prefix parse function for {} found".format(token_type)
        self.errors.append(msg)
    
    def parse_infix_expression(self, left):
        expression = ast.InfixExpression(
            self.cur_token, 
            self.cur_token.Literal, 
            left)
        precedence = self.cur_precendence()
        self.next_token()
        expression.right = self.parse_expression(precedence)
        return expression

    def peek_error(self, t):
        msg = 'expected token to be {}, got {} instead'.format(t, self.peek_token.Type)
        self.errors.append(msg)
    
    def register_prefix(self, token_type, fn):
        self.prefix_parse_fns[token_type] = fn
    
    def register_infix(self, token_type, fn):
        self.infix_parse_fns[token_type] = fn
        
    # def prefix_parse_fn(self):
    #     pass
    
    # def infix_parse_fn(self, expression):
    #     pass

    def peek_precendence(self):
        if self.peek_token.Type in precedences:
            return precedences[self.peek_token.Type]
        return Precedence.LOWEST.value
    
    def cur_precendence(self):
        if self.cur_token.Type in precedences:
            return precedences[self.cur_token.Type]
        return Precedence.LOWEST.value

def new(lexer):
    p = Parser(lexer)
    # create maps for prefix and infix operators to parse functions
    p.prefix_parse_fns = {}
    p.register_prefix(token.IDENT, p.parse_identifer)
    p.register_prefix(token.INT, p.parse_integer_literal)
    p.register_prefix(token.BANG, p.parse_prefix_expression)
    p.register_prefix(token.MINUS, p.parse_prefix_expression)
    # infix
    p.register_infix(token.PLUS, p.parse_infix_expression) 
    p.register_infix(token.MINUS, p.parse_infix_expression) 
    p.register_infix(token.SLASH, p.parse_infix_expression) 
    p.register_infix(token.ASTERISK, p.parse_infix_expression) 
    p.register_infix(token.EQ, p.parse_infix_expression) 
    p.register_infix(token.NOT_EQ, p.parse_infix_expression) 
    p.register_infix(token.LT, p.parse_infix_expression) 
    p.register_infix(token.GT, p.parse_infix_expression)
    # this sets both cur_token and peek_token
    p.next_token()
    p.next_token()
    return p
    