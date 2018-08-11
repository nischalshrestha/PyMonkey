from monkey import token
from monkey import lexer

prompt = ">> "
def start():
    while True:
        line = input(prompt)
        l = lexer.new(line)
        tok = l.next_token()
        while tok.Type != token.EOF:
            print(tok)
            tok = l.next_token()
