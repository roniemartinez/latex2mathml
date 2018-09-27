#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2018, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
# __status__ = "Development"
import string

from latex2mathml.tokenizer import tokenize


def test_alphabets():
    alphabets = string.ascii_letters
    assert list(alphabets) == list(tokenize(alphabets))


def test_numbers():
    numbers = '1234567890'
    assert [numbers] == list(tokenize(numbers))


def test_numbers_with_decimals():
    decimal = '12.56'
    assert [decimal] == list(tokenize(decimal))


def test_numbers_and_alphabets():
    s = '5x'
    assert list(s) == list(tokenize(s))


def test_decimals_and_alphabets():
    s = '5.8x'
    assert ['5.8', 'x'] == list(tokenize(s))


def test_string_with_spaces():
    s = '3 x'
    assert ['3', 'x'] == list(tokenize(s))


def test_operators():
    s = '+-*/=()[]_^{}'
    assert list(s) == list(tokenize(s))


def test_numbers_alphabets_and_operators():
    s = '3 + 5x - 5y = 7'
    assert ['3', '+', '5', 'x', '-', '5', 'y', '=', '7'] == list(tokenize(s))


def test_symbols():
    s = r'\alpha\beta'
    assert [r'\alpha', r'\beta'] == list(tokenize(s))


def test_symbols_appended_number():
    s = r'\frac2x'
    assert [r'\frac', '2', 'x'] == list(tokenize(s))


def test_matrix():
    assert [r'\matrix', '{', 'a', '&', 'b', r'\\', 'c', '&', 'd', '}'] == \
           list(tokenize(r'\begin{matrix}a & b \\ c & d \end{matrix}'))


def test_matrix_with_alignment():
    assert [r'\matrix*', 'r', '{', 'a', '&', 'b', r'\\', 'c', '&', 'd', '}'] == \
           list(tokenize(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}'))


def test_matrix_with_negative_sign():
    assert [r'\matrix', '{', '-', 'a', '&', 'b', r'\\', 'c', '&', 'd', '}'] == \
           list(tokenize(r'\begin{matrix}-a & b \\ c & d \end{matrix}'))


def test_simple_array():
    assert [r'\array', 'cc', '{', '1', '&', '2', r'\\', '3', '&', '4', '}'] == \
           list(tokenize(r'\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}'''))
