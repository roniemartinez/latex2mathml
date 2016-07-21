#!/usr/bin/python
import unittest
from latex2mathml import symbols_parser

__author__ = 'Ronie Martinez'


class SymbolParserTest(unittest.TestCase):
    def test_operator_plus(self):
        self.assertEqual('0002B', symbols_parser.convert_symbol('+'))

    def test_alias_command(self):
        self.assertEqual('02192', symbols_parser.convert_symbol(r'\to'))


if __name__ == '__main__':
    unittest.main()
