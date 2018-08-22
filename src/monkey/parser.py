from monkey import token
from monkey import lexer
from monkey import ast
from monkey import parser_tracing

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
    token.LPAREN: Precedence.CALL.value
}

# Uses Pratt Parsing
class Parser:

    lexer = None
    cur_token = None
    peek_token = None
    errors = []
    prefix_parse_fns = {}
    infix_parse_fns = {}

    def __init__(self, lexer, errors=None):
        self.lexer = lexer
        if errors == None:
            errors = []
        self.errors = errors
        # self.tracer = parser_tracing.ParserTracer()

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
        self.next_token()
        stmt.value = self.parse_expression(Precedence.LOWEST.value)
        if self.peek_token_is(token.SEMICOLON):
            self.next_token()
        return stmt

    def parse_return_statement(self):
        stmt = ast.ReturnStatement(self.cur_token)
        self.next_token()
        stmt.return_value = self.parse_expression(Precedence.LOWEST.value)
        if self.peek_token_is(token.SEMICOLON):
            self.next_token()
        return stmt
    
    def parse_expression_statement(self):
        # begin = self.tracer.trace('parse_expression_statement')
        stmt = ast.ExpressionStatement(self.cur_token)
        stmt.expression = self.parse_expression(Precedence.LOWEST.value)
        if self.peek_token_is(token.SEMICOLON):
            self.next_token()
        # self.tracer.untrace(begin)
        return stmt
    
    def parse_expression(self, precedence):
        # begin = self.tracer.trace('parse_expression')
        if self.cur_token.Type not in self.prefix_parse_fns:
            self.no_prefix_parse_fn_error(self.cur_token.Type)
            # self.tracer.untrace(begin)
            return None
        prefix = self.prefix_parse_fns[self.cur_token.Type]
        left_exp = prefix()
        while not self.peek_token_is(token.SEMICOLON) and precedence < self.peek_precendence():
            if self.peek_token.Type not in self.infix_parse_fns:
                print(self.peek_token.Type)
                # self.tracer.untrace(begin)
                return left_exp
            infix = self.infix_parse_fns[self.peek_token.Type]
            self.next_token()
            left_exp = infix(left_exp)
        # self.tracer.untrace(begin)
        return left_exp
    
    def parse_grouped_expression(self):
        self.next_token()
        exp = self.parse_expression(Precedence.LOWEST.value)
        if not self.expect_peek(token.RPAREN):
            return None
        return exp
    
    def parse_identifer(self):
        # self.tracer.untrace(self.tracer.trace('parse_identifer'))
        return ast.Identifier(self.cur_token, self.cur_token.Literal)
    
    def parse_integer_literal(self):
        # begin = self.tracer.trace('parse_integer_literal')
        lit = ast.IntegerLiteral(self.cur_token)
        try:
            value = int(self.cur_token.Literal)
            lit.value = value
            # self.tracer.untrace(begin)
            return lit
        except ValueError:
            msg = 'could not parse {} as integer'.format(self.cur_token)
            self.errors.append(msg)
            return None
    
    def parse_prefix_expression(self):
        # begin = self.tracer.trace('parse_prefix_expression')
        expression = ast.PrefixExpression(self.cur_token, self.cur_token.Literal)
        self.next_token()
        expression.right = self.parse_expression(Precedence.PREFIX.value)
        # self.tracer.untrace(begin)
        return expression
        
    def no_prefix_parse_fn_error(self, token_type):
        msg = "no prefix parse function for {} found".format(token_type)
        self.errors.append(msg)
    
    def parse_infix_expression(self, left):
        # begin = self.tracer.trace('parse_infix_expression')
        expression = ast.InfixExpression(
            self.cur_token, 
            self.cur_token.Literal, 
            left)
        precedence = self.cur_precendence()
        self.next_token()
        expression.right = self.parse_expression(precedence)
        # self.tracer.untrace(begin)
        return expression
    
    def parse_if_expression(self):
        expression = ast.IfExpression(self.cur_token)
        if not self.expect_peek(token.LPAREN):
            return None
        self.next_token()
        expression.condition = self.parse_expression(Precedence.LOWEST.value)
        if not self.expect_peek(token.RPAREN):
            return None
        if not self.expect_peek(token.LBRACE):
            return None
        expression.consequence = self.parse_block_statement()
        if self.peek_token_is(token.ELSE):
            self.next_token()
            if not self.expect_peek(token.LBRACE):
                return None
            expression.alternative = self.parse_block_statement()
        return expression
    
    def parse_block_statement(self):
        block = ast.BlockStatement(self.cur_token)
        self.next_token()
        while not self.current_token_is(token.RBRACE) and not self.current_token_is(token.EOF):
            stmt = self.parse_statement()
            if stmt != None:
                block.statements.append(stmt)
            self.next_token()
        return block
    
    def parse_function_literal(self):
        lit = ast.FunctionLiteral(self.cur_token)
        if not self.expect_peek(token.LPAREN):
            return None
        lit.parameters = self.parse_function_parameters()
        if not self.expect_peek(token.LBRACE):
            return None
        lit.body = self.parse_block_statement()
        return lit
    
    def parse_function_parameters(self):
        identifiers = []
        # empty case
        if self.peek_token_is(token.RPAREN):
            self.next_token()
            return identifiers
        self.next_token()
        ident = ast.Identifier(self.cur_token, self.cur_token.Literal)
        identifiers.append(ident)
        while self.peek_token_is(token.COMMA):
            self.next_token() # consume last ident
            self.next_token() # consume the comma
            ident = ast.Identifier(self.cur_token, self.cur_token.Literal)
            identifiers.append(ident)
        if not self.expect_peek(token.RPAREN):
            return None
        return identifiers

    def parse_call_expression(self, function):
        exp = ast.CallExpression(self.cur_token, function)
        exp.arguments = self.parse_call_arguments()
        return exp

    def parse_call_arguments(self):
        args = []
        if self.peek_token_is(token.RPAREN):
            self.next_token()
            return args
        self.next_token()
        args.append(self.parse_expression(Precedence.LOWEST.value))
        while self.peek_token_is(token.COMMA):
            self.next_token()
            self.next_token()
            args.append(self.parse_expression(Precedence.LOWEST.value))
        if not self.expect_peek(token.RPAREN):
            return None
        return args

    def parse_boolean(self):
        return ast.Boolean(self.cur_token, self.current_token_is(token.TRUE))

    def peek_error(self, t):
        msg = 'expected token to be {}, got {} instead'.format(t, self.peek_token.Type)
        self.errors.append(msg)
    
    def register_prefix(self, token_type, fn):
        self.prefix_parse_fns[token_type] = fn
    
    def register_infix(self, token_type, fn):
        self.infix_parse_fns[token_type] = fn

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
    p.register_prefix(token.TRUE, p.parse_boolean)
    p.register_prefix(token.FALSE, p.parse_boolean)
    p.register_prefix(token.LPAREN, p.parse_grouped_expression)
    p.register_prefix(token.IF, p.parse_if_expression)
    p.register_prefix(token.FUNCTION, p.parse_function_literal)
    # infix
    p.register_infix(token.PLUS, p.parse_infix_expression) 
    p.register_infix(token.MINUS, p.parse_infix_expression) 
    p.register_infix(token.SLASH, p.parse_infix_expression) 
    p.register_infix(token.ASTERISK, p.parse_infix_expression) 
    p.register_infix(token.EQ, p.parse_infix_expression) 
    p.register_infix(token.NOT_EQ, p.parse_infix_expression) 
    p.register_infix(token.LT, p.parse_infix_expression) 
    p.register_infix(token.GT, p.parse_infix_expression)
    p.register_infix(token.LPAREN, p.parse_call_expression)
    # this sets both cur_token and peek_token
    p.next_token()
    p.next_token()
    return p