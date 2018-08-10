from typing import NamedTuple

# Constants
ILLEGAL = "ILLEGAL"
EOF     = "EOF"
# Identifiers + literals
IDENT = "IDENT" # add, foobar, x, y, ...
INT   = "INT"   # 1343456

# Operators
ASSIGN   = "="
PLUS     = "+"
MINUS    = "-"
BANG     = "!"
ASTERISK = "*"
SLASH    = "/"

LT = "<"
GT = ">"

EQ     = "=="
NOT_EQ = "!="

# Delimiters
COMMA     = ","
SEMICOLON = ";"

LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"

# Keywords
FUNCTION = "FUNCTION"
LET      = "LET"
TRUE     = "TRUE"
FALSE    = "FALSE"
IF       = "IF"
ELSE     = "ELSE"
RETURN   = "RETURN"

# immutable 'struct'
class Token(NamedTuple):
    Type: str
    Literal: str

keywords = {
    'fn': FUNCTION,
    'let': LET,
    'true': TRUE,
    'false': FALSE,
    'if': IF,
    'else': ELSE,
    'return': RETURN,
}

def lookup_ident(ident):
    return keywords[ident] if ident in keywords else IDENT