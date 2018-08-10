import lexer
import tokens

prompt = ">> "
def start():
    while True:
        line = input(prompt)
        l = lexer.new(line)
        tok = l.next_token()
        while tok.Type != tokens.EOF:
            print(tok)
            tok = l.next_token()
