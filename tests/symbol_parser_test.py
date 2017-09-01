#!/usr/bin/env python
import unittest
from latex2mathml import symbols_parser

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2016-2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Development"


class SymbolParserTest(unittest.TestCase):
    def test_operator_plus(self):
        self.assertEqual('0002B', symbols_parser.convert_symbol('+'))

    def test_alias_command(self):
        self.assertEqual('02192', symbols_parser.convert_symbol(r'\to'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
