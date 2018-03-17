import unittest
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..', 'calc'))
from calc.core import units
from calc import ohm_law


class OhmLawTestCase(unittest.TestCase):
    def test1_simple_cases(self):
        p = units.Parser.instance

        r = p.normalize('1kR')
        i = p.normalize('1A')
        v = ohm_law.play(r, i)
        self.assertEqual(1000.0, v[0])
        self.assertEqual('V', v[1])

        r = p.normalize('3.3V')
        i = p.normalize('560R')
        v = ohm_law.play(r, i)
        self.assertAlmostEqual(0.005892857142857142, v[0])
        self.assertEqual('A', v[1])


if __name__ == '__main__':
    unittest.main()
