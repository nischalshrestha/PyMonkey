import unittest
import sys
sys.path.append("../src/")
from monkey.compiler import compiler as c
from monkey.compiler import symbol_table as s

class SymbolTableTest(unittest.TestCase):

    def test_define(self):
        expected = {
            'a': s.Symbol(name='a', scope=s.GLOBAL_SCOPE, index=0),
            'b': s.Symbol(name='b', scope=s.GLOBAL_SCOPE, index=1)
        }
        g = s.new_symbol_table()
        a = g.define('a')
        exp_a = str(expected['a'])
        self.assertEqual(a, expected['a'], msg=f'expected={exp_a} got={a}')
        b = g.define('b')
        exp_b = str(expected['b'])
        self.assertEqual(b, expected['b'], msg=f'expected={exp_b} got={b}')

    def test_resolve_global(self):
        g = s.new_symbol_table()
        g.define('a')
        g.define('b')
        expected = [
            s.Symbol(name='a', scope=s.GLOBAL_SCOPE, index=0),
            s.Symbol(name='b', scope=s.GLOBAL_SCOPE, index=1)
        ]
        for sym in expected:
            result = g.resolve(sym.name)
            self.assertIsNotNone(result, msg=f'name {sym.name} is not resolvable')
            self.assertEqual(result, sym, msg=f'expected {sym.name} to resolve to {sym}, got={result}')

if __name__ == '__main__':
    unittest.main()