import tokens

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
            if self.peek_char() == '=':
                lch = ch
                self.read_char()
                tok = new_token(tokens.EQ, lch+self.ch)
            else:
                tok = new_token(tokens.ASSIGN, ch)
        elif ch == '+':
            tok = new_token(tokens.PLUS, ch)
        elif ch == '-':
            tok = new_token(tokens.MINUS, ch)
        elif ch == '!':
            if self.peek_char() == '=':
                lch = ch
                self.read_char()
                tok = new_token(tokens.NOT_EQ, lch+self.ch)
            else:
                tok = new_token(tokens.BANG, ch)
        elif ch == '/':
            tok = new_token(tokens.SLASH, ch)
        elif ch == '*':
            tok = new_token(tokens.ASTERISK, ch)
        elif ch == '<':
            tok = new_token(tokens.LT, ch)
        elif ch == '>':
            tok = new_token(tokens.GT, ch)
        elif ch == ';':
            tok = new_token(tokens.SEMICOLON, ch)
        elif ch == ',':
            tok = new_token(tokens.COMMA, ch)
        elif ch == '{':
            tok = new_token(tokens.LBRACE, ch)
        elif ch == '}':
            tok = new_token(tokens.RBRACE, ch)
        elif ch == '(':
            tok = new_token(tokens.LPAREN, ch)
        elif ch == ')':
            tok = new_token(tokens.RPAREN, ch)
        elif ch == 0:
            tok = new_token(tokens.EOF, "")
        else:
            if is_letter(ch):
                literal = self.read_identifier()
                token_type = tokens.lookup_ident(literal)
                return new_token(token_type, literal)
            elif is_digit(ch):
                token_type = tokens.INT
                literal = self.read_number()
                return new_token(token_type, literal)
            else:
                tok = new_token(tokens.ILLEGAL, ch)
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
        while(self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r'):
            self.read_char()
    
    def read_char(self):
        if self.read_position >= len(self.source):
            self.ch = 0
        else:
            self.ch = self.source[self.read_position]
        self.position = self.read_position
        self.read_position = self.read_position + 1
    
    def peek_char(self):
        if self.read_position >= len(self.source):
            return 0
        else:
            return self.source[self.read_position]
    
    def print_fields(self):
        print(self.source, self.position, self.read_position, self.ch)

def is_letter(ch):
    return ('a' <= ch and ch <= 'z') or ('A' <= ch and ch <= 'Z') or ch == '_'

def is_digit(ch):
	return '0' <= ch and ch <= '9'

def new_token(token_type, ch):
	return tokens.Token(token_type, ch)

def new(source):
    l = Lexer(source)
    l.read_char()
    return l