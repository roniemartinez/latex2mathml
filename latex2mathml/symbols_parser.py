#!/usr/bin/python
import codecs
import os
import re

__author__ = 'Ronie Martinez'


def convert_symbol(symbol):
    symbols = parse_symbols()
    return symbols.get(symbol, None)


def parse_symbols():
    symbols = {}
    symbols_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'unimathsymbols.txt')
    with codecs.open(symbols_file, encoding='utf-8') as f:
        for line in f:
            if not line.startswith('#'):
                columns = line.strip().split('^')
                _unicode = columns[0]
                latex = columns[2]
                unicode_math = columns[3]
                if latex and latex not in symbols:
                    symbols[latex] = _unicode
                if unicode_math and unicode_math not in symbols:
                    symbols[unicode_math] = _unicode
                for equivalent in re.findall(r'=\s+(\\[^,^ ]+),?', columns[-1]):
                    if equivalent not in symbols:
                        symbols[equivalent] = _unicode
    return symbols
