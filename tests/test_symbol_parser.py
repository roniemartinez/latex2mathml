#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from latex2mathml.symbols_parser import convert_symbol


def test_operator_plus():
    assert '0002B' == convert_symbol('+')


def test_alias_command():
    assert '02192' == convert_symbol(r'\to')
