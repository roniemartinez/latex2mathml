#!/usr/bin/python
import unittest

import latex2mathml

__author__ = 'Ronie Martinez'


class SymbolParserTest(unittest.TestCase):
    def test_operator_plus(self):
        self.assertEqual('0002B', latex2mathml.convert_symbol('+'))

    def test_alias_command(self):
        self.assertEqual('02192', latex2mathml.convert_symbol(r'\to'))


if __name__ == '__main__':
    unittest.main()
