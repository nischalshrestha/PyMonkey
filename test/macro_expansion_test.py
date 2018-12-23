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

    def get_parse_program(self, source):
        l = lexer.new(source)
        p = parser.new(l)
        program = p.parse_program()
        return program

if __name__ == '__main__':
    unittest.main()
    