import unittest
import sys
sys.path.append("../src/")
from monkey import token
from monkey import ast

class AstTest(unittest.TestCase):

    def test_string(self):
        program = ast.Program([
            ast.LetStatement(
                token.Token(token.LET, "let"), # token
                ast.Identifier( # name
                    token.Token(token.IDENT, "myVar"), 
                    "myVar"
                ),
                ast.Identifier( # value
                    token.Token(token.IDENT, "anotherVar"),
                    "anotherVar"
                )
            )
        ])
        self.assertEqual(program.string(), "let myVar = anotherVar;",
            msg = "program.string() wrong. got={}".format(program.string()))

if __name__ == "__main__":
    unittest.main()