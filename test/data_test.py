import sys
import unittest
import json

sys.path.append('../')

import data
import random

class TestJSON(unittest.TestCase):
    def test_built_in(self):
        '''Test the serialization and deserialization of Python built-in types
        with customized JSONEncoder and JSONDecoder'''
        entry = [1, 1.1, None, True, False, {'Year': 2018}]

        s = json.dumps(entry, cls = data.QQEncoder)
        copy = json.loads(s, cls = data.QQDecoder)

        self.assertEqual(entry, copy)

    def test_customized(self):
        '''Test the serialization and deserialization of two user-defined class,
        Ant and Boss, with customized JSONEncoder and JSONDecoder'''
        m = 10000000
        ants = []

        for _ in range(10):
            ants.append(data.Ant(str(random.randrange(m)), str(random.randrange(m))))

        s = json.dumps(ants, cls = data.QQEncoder)
        ants_copy = json.loads(s, cls = data.QQDecoder)

        self.assertEqual(ants, ants_copy)

class TestAnt(unittest.TestCase):
    '''Test built-in function support of Ant'''

    def test_str(self):
        ant = data.Ant('12345', '54321')
        s = "ant: name = '12345', password = '54321'"

        self.assertEqual(s, str(ant))

    def test_repr(self):
        ant = data.Ant('12345', '54321')
        r = "data.Ant('12345', '54321')"

        self.assertEqual(r, repr(ant))

    def test_eq(self):
        ant1 = data.Ant('12345', '54321')
        ant2 = data.Ant('12345', '54321')

        self.assertIsNot(ant1, ant2)
        self.assertEqual(ant1, ant2)

class TestBoss(unittest.TestCase):
    '''Test built-in function support of Boss'''

    def test_str(self):
        boss = data.Boss('12345')
        s = "boss: name = '12345'"

        self.assertEqual(s, str(boss))

    def test_repr(self):
        boss = data.Boss('12345')
        r = "data.Boss('12345')"

        self.assertEqual(r, repr(boss))

    def test_eq(self):
        boss1 = data.Boss('12345')
        boss2 = data.Boss('12345')

        self.assertIsNot(boss1, boss2)
        self.assertEqual(boss1, boss2)

if __name__ == '__main__':
    unittest.main()
