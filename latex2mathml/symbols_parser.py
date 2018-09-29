#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2018, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
# __status__ = "Production"
import codecs
import os
import re

symbols_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'unimathsymbols.txt')
symbols = None


def convert_symbol(symbol):
    global symbols
    if not symbols:
        symbols = parse_symbols()
    return symbols.get(symbol, None)


def parse_symbols():
    _symbols = {}
    with codecs.open(symbols_file, encoding='utf-8') as f:
        for line in f:
            if not line.startswith('#'):
                columns = line.strip().split('^')
                _unicode = columns[0]
                latex = columns[2]
                unicode_math = columns[3]
                if latex and latex not in _symbols:
                    _symbols[latex] = _unicode
                if unicode_math and unicode_math not in _symbols:
                    _symbols[unicode_math] = _unicode
                for equivalent in re.findall(r'=\s+(\\[^,^ ]+),?', columns[-1]):
                    if equivalent not in _symbols:
                        _symbols[equivalent] = _unicode
    return _symbols
