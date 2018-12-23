import unittest
import sys
sys.path.append("../src/")
from monkey.object import *
from monkey import lexer
from monkey import parser
from monkey.evaluator import evaluator as e
from monkey.evaluator import macro_expansion

class TestMacros(unittest.TestCase):

    def test_define_macros(self):
        source = '''
            let number = 1;
            let function = fn(x, y) { x + y; };
            let mymacro = macro(x, y) { x + y; };
        '''
        env = e.new_environment()
        program = self.get_parse_program(source)
        macro_expansion.DefineMacros(program, env)
        self.assertEqual(len(program.statements), 2, 
            msg='Wrong number of statements. got={}'.format(len(program.statements)))
        self.assertIsNone(env.get("number"), msg='number should not be defined')
        self.assertIsNone(env.get("function"), msg='function should not be defined')
        obj = env.get("mymacro")
        self.assertIsNotNone(obj, msg='mymacro not in environment')
        macro = obj
        self.assertTrue(isinstance(macro, object.Macro),
            msg='object is not a macro. got={} {}'.format(macro, type(macro)))
        self.assertEqual(len(macro.parameters), 2, 
            msg='Wrong number of macro parameters. got={}'.format(len(macro.parameters)))
        self.assertEqual(macro.parameters[0].string(), 'x', 
            msg='parameter is not x. got={}'.format(macro.parameters[0].string()))   
        self.assertEqual(macro.parameters[1].string(), 'y', 
            msg='parameter is not y. got={}'.format(macro.parameters[1].string()))
        expected_body = '(x + y)'
        self.assertEqual(macro.body.string(), expected_body, 
            msg='body is not {}. got={}'.format(expected_body, macro.body.string()))

    def test_expand_macros(self):
        tests = [
            (
                '''
                let infixExpression = macro () { quote (1 + 2); };
                infixExpression()
                ''', 
                '(1 + 2)'
            ),
            (
                '''
                let reverse = macro (a, b) { quote(unquote(b) - unquote(a)); };
                reverse(2 + 2, 10 - 5)
                ''', 
                '(10 - 5) - (2 + 2)'
            ),
            (
                '''
                let unless = macro (condition, consequence, alternative) {
                    quote(if (!unquote(condition)) {
                        unquote(consequence);
                    } else {
                        unquote(alternative);
                    });
                };
                unless(10 < 5, puts("not greater"), puts("greater"))
                ''', 
                ''''
                if (!(10 < 5)) {
                    puts("not greater");
                } else {
                    puts("greater");
                };
                '''
            ),
        ]
        for t in tests:
            expected = self.get_parse_program(t[1])
            program = self.get_parse_program(t[0])
            env = e.new_environment()
            macro_expansion.DefineMacros(program, env)
            expanded = macro_expansion.ExpandMacros(program, env)
            self.assertEqual(expanded.string(), expected.string(),
                msg="not equal. want={}, got={}".format(expected.string(), expanded.string()))
        # Test this in REPL:
        # let unless = macro( condition, consequence, alternative) { quote( if (!( unquote( condition))) { unquote( consequence); } else { unquote( alternative); }); };

    def get_parse_program(self, source):
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        return program

if __name__ == '__main__':
    unittest.main()
    