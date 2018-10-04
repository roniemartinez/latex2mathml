#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2018, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
# __status__ = "Production"
from latex2mathml.aggregator import aggregate
import string

import TexSoup

from latex2mathml.aggregator import aggregate


def test_alphabets():
    alphabets = string.ascii_letters
    assert list(alphabets) == aggregate(TexSoup.TexSoup(alphabets))


def test_numbers():
    numbers = string.digits
    assert [numbers] == aggregate(TexSoup.TexSoup(numbers))


# noinspection PyTypeChecker
def test_numbers_with_decimals():
    decimal = '12.56'
    assert [decimal] == aggregate(TexSoup.TexSoup(decimal))


# noinspection PyTypeChecker
def test_numbers_and_alphabets():
    s = '5x'
    assert list(s) == aggregate(TexSoup.TexSoup(s))


# noinspection PyTypeChecker
def test_decimals_and_alphabets():
    s = '5.8x'
    assert ['5.8', 'x'] == aggregate(TexSoup.TexSoup(s))


# noinspection PyTypeChecker
def test_string_with_spaces():
    s = '3 x'
    assert ['3', 'x'] == aggregate(TexSoup.TexSoup(s))


# noinspection PyTypeChecker
def test_operators():
    s = '+-*/=()[]_^{}'
    assert list(s) == aggregate(TexSoup.TexSoup(s))


# noinspection PyTypeChecker
def test_numbers_alphabets_and_operators():
    s = '3 + 5x - 5y = 7'
    assert ['3', '+', '5', 'x', '-', '5', 'y', '=', '7'] == aggregate(TexSoup.TexSoup(s))


# noinspection PyTypeChecker
def test_symbols():
    s = r'\alpha\beta'
    assert [r'\alpha', r'\beta'] == aggregate(TexSoup.TexSoup(s))


# noinspection PyTypeChecker
def test_symbols_appended_number():
    s = r'\frac2x'
    assert [r'\frac', '2', 'x'] == aggregate(TexSoup.TexSoup(s))


# noinspection PyTypeChecker
def test_single_group():
    assert [['a']] == aggregate(TexSoup.TexSoup('{a}'))


# noinspection PyTypeChecker
def test_multiple_groups():
    assert [['a'], ['b']] == aggregate(TexSoup.TexSoup('{a}{b}'))


# noinspection PyTypeChecker
def test_inner_group():
    assert [['a', '+', ['b']]] == aggregate(TexSoup.TexSoup('{a+{b}}'))


# noinspection PyTypeChecker
def test_subscript():
    assert ['_', 'a', 'b'] == aggregate(TexSoup.TexSoup('a_b'))


# noinspection PyTypeChecker
def test_superscript():
    assert ['^', 'a', 'b'] == aggregate(TexSoup.TexSoup('a^b'))


# noinspection PyTypeChecker
def test_subscript_and_superscript():
    assert ['_^', 'a', 'b', 'c'] == aggregate(TexSoup.TexSoup('a_b^c'))


# noinspection PyTypeChecker
def test_root():
    assert [r'\root', ['2'], ['3']] == aggregate(TexSoup.TexSoup(r'\sqrt[3]{2}'))


# noinspection PyTypeChecker
def test_matrix():
    assert [r'\matrix', [['a', 'b'], ['c', 'd']]] == \
           list(aggregate(TexSoup.TexSoup(r'\begin{matrix}a & b \\ c & d \end{matrix}')))


# noinspection PyTypeChecker
def test_matrix_with_alignment():
    assert [r'\matrix*', 'r', [['a', 'b'], ['c', 'd']]] == \
           list(aggregate(TexSoup.TexSoup(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}')))


# noinspection PyTypeChecker
def test_matrix_with_negative_sign():
    assert [r'\matrix', [[['-', 'a'], 'b'], ['c', 'd']]] == \
           list(aggregate(TexSoup.TexSoup(r'\begin{matrix}-a & b \\ c & d \end{matrix}')))


# noinspection PyTypeChecker
def test_complex_matrix():
    # assert ['\\matrix', [['_', 'a', ['1']], ['_', 'b', ['2']], ['_', 'c', ['3']], ['_', 'd', ['4']]]]
    assert [r'\matrix', [['_', 'a', ['1'], '_', 'b', ['2']], ['_', 'c', ['3'], '_', 'd', ['4']]]] == \
           list(aggregate(TexSoup.TexSoup(r'\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}')))


# noinspection PyTypeChecker
def test_simple_array():
    assert [r'\array', 'cc', [['1', '2'], ['3', '4']]] == \
           list(aggregate(TexSoup.TexSoup(r'\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}')))


# noinspection PyTypeChecker
def test_frac():
    assert [r'\frac', ['1'], ['2']] == list(aggregate(TexSoup.TexSoup(r'\frac{1}{2}')))


# noinspection PyTypeChecker
def test_over():
    assert [r'\frac', ['1'], ['2']] == list(aggregate(TexSoup.TexSoup(r'1 \over 2')))


# noinspection PyTypeChecker
def test_null_delimiter():
    assert [r'\left\{', r'\right.'] == list(aggregate(TexSoup.TexSoup(r'\left\{\right.')))
    latex = r'\left\{ \begin{array} { l } { 3x - 5y + 4z = 0} \\ { x - y + 8z = 0} \\ { 2x - 6y + z = 0} \end{array}' \
            r' \right.'
    assert [r'\left\{', r'\array', ['l'],
            [[['3', 'x', '-', '5', 'y', '+', '4', 'z', '=', '0']],
             [['x', '-', 'y', '+', '8', 'z', '=', '0']],
             [['2', 'x', '-', '6', 'y', '+', 'z', '=', '0']]],
            r'\right.'] == list(aggregate(TexSoup.TexSoup(latex)))
