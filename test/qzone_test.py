import unittest
import sys

sys.path.append('..')

import qzone
import data

class TestConfig(unittest.TestCase):
    def test_check_config(self):
        invalid_path = 'config/invalid.json'
        valid_path = 'test_ants.json'

        self.assertRaises(AssertionError, qzone.check_config, invalid_path)
        self.assertIs(qzone.check_config(valid_path), None)

    def test_get_ants(self):
        ants = []

        for i in range(1, 6):
            name = str(i) * 5
            ants.append(data.Ant(name, name))

        path = 'test_ants.json'
        ants_copy = qzone.get_ants(path)

        self.assertIsNot(ants, ants_copy)
        self.assertEqual(ants, ants_copy)

    def test_get_bosses(self):
        bosses = []

        for i in range(1, 6):
            name = str(i) * 5
            bosses.append(data.Boss(name))

        path = 'test_bosses.json'
        bosses_copy = qzone.get_bosses(path)

        self.assertIsNot(bosses, bosses_copy)
        self.assertEqual(bosses, bosses_copy)
