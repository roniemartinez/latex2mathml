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

from latex2mathml.aggregator import aggregate


def test_alphabets():
    alphabets = string.ascii_letters
    assert list(alphabets) == aggregate(alphabets)


def test_numbers():
    numbers = string.digits
    assert [numbers] == aggregate(numbers)


def test_numbers_with_decimals():
    decimal = '12.56'
    assert [decimal] == aggregate(decimal)


def test_numbers_and_alphabets():
    s = '5x'
    assert list(s) == aggregate(s)


def test_decimals_and_alphabets():
    s = '5.8x'
    assert ['5.8', 'x'] == aggregate(s)


def test_string_with_spaces():
    s = '3 x'
    assert ['3', 'x'] == aggregate(s)


def test_operators():
    s = '+-*/=()[]_^{}'
    assert list(s) == aggregate(s)


def test_numbers_alphabets_and_operators():
    s = '3 + 5x - 5y = 7'
    assert ['3', '+', '5', 'x', '-', '5', 'y', '=', '7'] == aggregate(s)


def test_symbols():
    s = r'\alpha\beta'
    assert [r'\alpha', r'\beta'] == aggregate(s)


def test_symbols_appended_number():
    s = r'\frac2x'
    assert [r'\frac', '2', 'x'] == aggregate(s)


def test_single_group():
    assert [['a']] == aggregate('{a}')


def test_multiple_groups():
    assert [['a'], ['b']] == aggregate('{a}{b}')


def test_inner_group():
    assert [['a', '+', ['b']]] == aggregate('{a+{b}}')


def test_subscript():
    assert ['_', 'a', 'b'] == aggregate('a_b')
    assert [['_', 'a', 'b']] == aggregate('{a_b}')
    assert ['_', '1', '2'] == aggregate('1_2')
    assert ['_', '1.2', '2'] == aggregate('1.2_2')


def test_superscript():
    assert ['^', 'a', 'b'] == aggregate('a^b')
    assert [['^', 'a', 'b']] == aggregate('{a^b}')


def test_subscript_and_superscript():
    assert ['_^', 'a', 'b', 'c'] == aggregate('a_b^c')
    assert ['_^', 'a', 'c', 'b'] == aggregate('a^b_c')


def test_root():
    assert [r'\root', ['2'], ['3']] == aggregate(r'\sqrt[3]{2}')


def test_matrix():
    assert [r'\matrix', [['a', 'b'], ['c', 'd']]] == list(aggregate(r'\matrix{a & b \\ c & d}'))
    assert [r'\matrix', [['a', 'b'], ['c', 'd']]] == list(aggregate(r'\begin{matrix}a & b \\ c & d \end{matrix}'))


def test_matrix_with_alignment():
    assert [r'\matrix*', 'r', [['a', 'b'], ['c', 'd']]] == \
           list(aggregate(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}'))


def test_matrix_with_negative_sign():
    assert [r'\matrix', [[['-', 'a'], 'b'], ['c', 'd']]] == \
           list(aggregate(r'\begin{matrix}-a & b \\ c & d \end{matrix}'))


def test_complex_matrix():
    # assert ['\\matrix', [['_', 'a', ['1']], ['_', 'b', ['2']], ['_', 'c', ['3']], ['_', 'd', ['4']]]]
    assert [r'\matrix', [['_', 'a', ['1'], '_', 'b', ['2']], ['_', 'c', ['3'], '_', 'd', ['4']]]] == \
           list(aggregate(r'\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}'))


def test_simple_array():
    assert [r'\array', 'cc', [['1', '2'], ['3', '4']]] == \
           list(aggregate(r'\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}'))


def test_frac():
    assert [r'\frac', ['1'], ['2']] == list(aggregate(r'\frac{1}{2}'))


def test_over():
    assert [r'\frac', ['1'], ['2']] == list(aggregate(r'1 \over 2'))
    assert [[r'\frac', ['1'], ['2']]] == list(aggregate(r'{1 \over 2}'))


def test_null_delimiter():
    assert [r'\left', r'\{', r'\right', '.'] == list(aggregate(r'\left\{\right.'))
    latex = r'\left\{ \begin{array} { l } { 3x - 5y + 4z = 0} \\ { x - y + 8z = 0} \\ { 2x - 6y + z = 0} \end{array}' \
            r' \right.'
    assert [r'\left', r'\{', r'\array', 'l',
            [[['3', 'x', '-', '5', 'y', '+', '4', 'z', '=', '0']],
             [['x', '-', 'y', '+', '8', 'z', '=', '0']],
             [['2', 'x', '-', '6', 'y', '+', 'z', '=', '0']]],
            r'\right', '.'] == list(aggregate(latex))


def test_superscript_with_curly_braces():
    assert ['_^', 'a', '3', ['i', '+', '1']] == list(aggregate('a^{i+1}_3'))


def test_issue_33():
    latex = r"""\begin{bmatrix}
     a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
     a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
     \vdots  & \vdots  & \ddots & \vdots  \\
     a_{m,1} & a_{m,2} & \cdots & a_{m,n} 
    \end{bmatrix}"""
    expected = ['\\bmatrix',
                [['_', 'a', ['1', ',', '1'], '_', 'a', ['1', ',', '2'], '\\cdots', '_', 'a', ['1', ',', 'n']],
                 ['_', 'a', ['2', ',', '1'], '_', 'a', ['2', ',', '2'], '\\cdots', '_', 'a', ['2', ',', 'n']],
                 ['\\vdots', '\\vdots', '\\ddots', '\\vdots'],
                 ['_', 'a', ['m', ',', '1'], '_', 'a', ['m', ',', '2'], '\\cdots', '_', 'a', ['m', ',', 'n']]]]
    assert expected == list(aggregate(latex))

