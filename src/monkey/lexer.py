import token

class Lexer:

    source = ""
    position = 0
    read_position = 0
    ch = ''

    def __init__(self, source, position=0, read_position=0, ch=''):
        self.source = source
        self.position = position
        self.read_position = read_position
        self.ch = ch

    def next_token(self):
        tok = None
        self.skip_whitespace()
        ch = self.ch
        if ch == '=':
            tok = new_token(token.ASSIGN, ch)
        elif ch == '+':
            tok = new_token(token.PLUS, ch)
        elif ch == '-':
            tok = new_token(token.MINUS, ch)
        elif ch == '!':
            tok = new_token(token.BANG, ch)
        elif ch == '/':
            tok = new_token(token.SLASH, ch)
        elif ch == '*':
            tok = new_token(token.ASTERISK, ch)
        elif ch == '<':
            tok = new_token(token.LT, ch)
        elif ch == '>':
            tok = new_token(token.GT, ch)
        elif ch == ';':
            tok = new_token(token.SEMICOLON, ch)
        elif ch == ',':
            tok = new_token(token.COMMA, ch)
        elif ch == '{':
            tok = new_token(token.LBRACE, ch)
        elif ch == '}':
            tok = new_token(token.RBRACE, ch)
        elif ch == '(':
            tok = new_token(token.LPAREN, ch)
        elif ch == ')':
            tok = new_token(token.RPAREN, ch)
        elif ch == 0:
            tok = new_token(token.EOF, "")
        else:
            if is_letter(ch):
                literal = self.read_identifier()
                token_type = token.lookup_ident(literal)
                return new_token(token_type, literal)
            elif is_digit(ch):
                token_type = token.INT
                literal = self.read_number()
                return new_token(token_type, literal)
            else:
                tok = new_token(token.ILLEGAL, ch)
        self.read_char()
        return tok

    def read_identifier(self):
        position = self.position
        while self.ch != 0 and is_letter(self.ch):
            self.read_char()
        return self.source[position:self.position]

    def read_number(self):
        position = self.position
        while self.ch != 0 and is_digit(self.ch):
            self.read_char()
        return self.source[position:self.position]
    
    def skip_whitespace(self):
        ch = self.ch
        while(ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r'):
            self.readch()
    
    def read_char(self):
        if self.read_position >= len(self.source):
            self.ch = 0
        else:
            self.ch = self.source[self.read_position]
        self.position = self.read_position
        self.read_position = self.read_position + 1
    
    def print_fields(self):
        print(self.source, self.position, self.read_position, self.ch)

def is_letter(ch):
    return ('a' <= ch and ch <= 'z') or ('A' <= ch and ch <= 'Z') or ch == '_'

def is_digit(ch):
	return '0' <= ch and ch <= '9'

def new_token(token_type, ch):
	return token.Token(token_type, ch)

def new(source):
    l = Lexer(source)
    l.read_char()
    return l