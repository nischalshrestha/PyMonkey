import unittest
import sys
sys.path.append("../src/")
from monkey.object import *

class ObjectTest(unittest.TestCase):

    def test_string_hash_key(self):
        hello1 = String("Hello World")
        hello2 = String("Hello World")
        diff1 = String("My name is johnny")
        diff2 = String("My name is johnny")

        if hello1.hash_key().value != hello2.hash_key().value:
            self.fail("strings with same content have different hash keys")
        if diff1.hash_key().value != diff2.hash_key().value:
            self.fail("strings with same content have different hash keys")
        if hello1.hash_key().value == diff1.hash_key().value:
            self.fail("strings with different content have different hash keys")

    def test_boolean_hash_key(self):
        true1 = Boolean(True)
        true2 = Boolean(True)
        false1 = Boolean(False)
        false2 = Boolean(False)

        if true1.hash_key().value != true2.hash_key().value:
            self.fail("trues do not have same hash key")

        if false1.hash_key().value != false2.hash_key().value:
            self.fail("falses do not have same hash key")

        if true1.hash_key().value == false1.hash_key().value:
            self.fail("true has same hash key as false")

    def test_integer_hash_key(self):
        one1 = Integer(1)
        one2 = Integer(1)
        two1 = Integer(2)
        two2 = Integer(2)

        if one1.hash_key().value != one2.hash_key().value:
            self.fail("integers with same content have different hash keys")

        if two1.hash_key().value != two2.hash_key().value:
            self.fail("integers with same content have different hash keys")

        if one1.hash_key().value == two1.hash_key().value:
            self.fail("integers with different content have same hash keys")

if __name__ == "__main__":
    unittest.main()