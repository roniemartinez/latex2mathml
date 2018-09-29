#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2018, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
# __status__ = "Development"
from latex2mathml.aggregator import aggregate


def test_single_group():
    assert [['a']] == aggregate('{a}')


def test_multiple_groups():
    assert [['a'], ['b']] == aggregate('{a}{b}')


def test_inner_group():
    assert [['a', '+', ['b']]] == aggregate('{a+{b}}')


def test_subscript():
    assert ['_', 'a', 'b'] == aggregate('a_b')


def test_superscript():
    assert ['^', 'a', 'b'] == aggregate('a^b')


def test_subscript_and_superscript():
    assert ['_^', 'a', 'b', 'c'] == aggregate('a_b^c')


def test_root():
    assert [r'\root', ['2'], ['3']] == aggregate(r'\sqrt[3]{2}')


def test_matrix():
    assert [r'\matrix', [['a', 'b'], ['c', 'd']]] == list(aggregate(r'\begin{matrix}a & b \\ c & d \end{matrix}'))


def test_matrix_with_alignment():
    assert [r'\matrix*', 'r', [['a', 'b'], ['c', 'd']]] == \
           list(aggregate(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}'))


def test_matrix_with_negative_sign():
    assert [r'\matrix', [[['-', 'a'], 'b'], ['c', 'd']]] == \
           list(aggregate(r'\begin{matrix}-a & b \\ c & d \end{matrix}'))


def test_complex_matrix():
    assert ['\\matrix', [['_', 'a', ['1'], '_', 'b', ['2']], ['_', 'c', ['3'], '_', 'd', ['4']]]] == \
           list(aggregate(r'\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}'))


def test_simple_array():
    assert [r'\array', 'cc', [['1', '2'], ['3', '4']]] == \
           list(aggregate(r'\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}'''))


def test_frac():
    assert ['\\frac', ['1'], ['2']] == list(aggregate(r'\frac{1}{2}'))


def test_over():
    assert ['\\frac', ['1'], ['2']] == list(aggregate(r'1 \over 2'))
