#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import string

import pytest

from latex2mathml.aggregator import aggregate
from latex2mathml.exceptions import ExtraLeftOrMissingRight


@pytest.mark.parametrize(
    'latex, expected',
    ids=[
        'alphabets',
        'empty group',
        'numbers',
        'numbers with decimal',
        'numbers and alphabets',
        'decimals and alphabets',
        'string with spaces',
        'operators',
        'numbers, alphabets and operators',
        'symbols',
        'symbols appended with number',
        'single group',
        'multiple groups',
        'inner group',
        'subscript #1',
        'subscript #2',
        'subscript #3',
        'subscript #4',
        'superscript #1',
        'superscript #2',
        'superscript #3',
        'subscript and superscript #1',
        'subscript and superscript #2',
        'root',
        'matrix #1',
        'matrix #2',
        'fraction #1',
        'fraction #2',
        'fraction #3',
        'null delimiter #1',
        'null delimiter #2',
        'matrix with alignment',
        'matrix with negative sign',
        'complex matrix',
        'simple array',
        'issue #33',
        'issue #55',
        'array with horizontal lines',
        'issue #60',
        'issue #61',
        'issue #63',
        'group after \\right',
        'issue #44'
    ],
    argvalues=[
        (string.ascii_letters, list(string.ascii_letters)),
        ('{{}}', [['{', '}']]),
        (string.digits, [string.digits]),
        ('12.56', ['12.56']),
        ('5x', list('5x')),
        ('5.8x', ['5.8', 'x']),
        ('3 x', ['3', 'x']),
        ('+-*/=()[]_^{}', list('+-*/=()[]_^{}')),
        ('3 + 5x - 5y = 7', ['3', '+', '5', 'x', '-', '5', 'y', '=', '7']),
        (r'\alpha\beta', [r'\alpha', r'\beta']),
        (r'\frac2x', [r'\frac', '2', 'x']),
        ('{a}', [['a']]),
        ('{a}{b}', [['a'], ['b']]),
        ('{a+{b}}', [['a', '+', ['b']]]),
        ('a_b', ['_', 'a', 'b']),
        ('{a_b}', [['_', 'a', 'b']]),
        ('1_2', ['_', '1', '2']),
        ('1.2_2', ['_', '1.2', '2']),
        ('a^b', ['^', 'a', 'b']),
        ('{a^b}', [['^', 'a', 'b']]),
        ('a^{i+1}_3', ['_^', 'a', '3', ['i', '+', '1']]),
        ('a_b^c', ['_^', 'a', 'b', 'c']),
        ('a^b_c', ['_^', 'a', 'c', 'b']),
        (r'\sqrt[3]{2}', [r'\root', ['2'], ['3']]),
        (r'\matrix{a & b \\ c & d}', [r'\matrix', [['a', 'b'], ['c', 'd']]]),
        (r'\begin{matrix}a & b \\ c & d \end{matrix}', [r'\matrix', [['a', 'b'], ['c', 'd']]]),
        (r'\frac{1}{2}', [r'\frac', ['1'], ['2']]),
        (r'1 \over 2', [r'\frac', ['1'], ['2']]),
        (r'{1 \over 2}', [[r'\frac', ['1'], ['2']]]),
        (r'\left\{\right.', [[r'\left', r'\{', r'\right', '.']]),
        (r'\left\{ \begin{array} { l } { 3x - 5y + 4z = 0} \\ { x - y + 8z = 0} \\ { 2x - 6y + z = 0} '
         r'\end{array}\right.',
         [[r'\left', r'\{',
           [r'\array', 'l',
            [
                [['3', 'x', '-', '5', 'y', '+', '4', 'z', '=', '0']],
                [['x', '-', 'y', '+', '8', 'z', '=', '0']],
                [['2', 'x', '-', '6', 'y', '+', 'z', '=', '0']]
            ]
            ], r'\right', '.']
          ]),
        (r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}', [r'\matrix*', 'r', [['a', 'b'], ['c', 'd']]]),
        (r'\begin{matrix}-a & b \\ c & d \end{matrix}', [r'\matrix', [[['-', 'a'], 'b'], ['c', 'd']]]),
        (r'\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}',
         [r'\matrix', [[['_', 'a', ['1']], ['_', 'b', ['2']]], [['_', 'c', ['3']], ['_', 'd', ['4']]]]]),
        (r'\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}', [r'\array', 'cc', [['1', '2'], ['3', '4']]]),
        (r'''\begin{bmatrix}
     a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
     a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
     \vdots  & \vdots  & \ddots & \vdots  \\
     a_{m,1} & a_{m,2} & \cdots & a_{m,n}
    \end{bmatrix}''',
         [r'\bmatrix',
          [[['_', 'a', ['1', ',', '1']], ['_', 'a', ['1', ',', '2']], r'\cdots', ['_', 'a', ['1', ',', 'n']]],
           [['_', 'a', ['2', ',', '1']], ['_', 'a', ['2', ',', '2']], r'\cdots', ['_', 'a', ['2', ',', 'n']]],
           [r'\vdots', r'\vdots', r'\ddots', r'\vdots'],
           [['_', 'a', ['m', ',', '1']], ['_', 'a', ['m', ',', '2']], r'\cdots', ['_', 'a', ['m', ',', 'n']]]]
          ]),
        (r"\begin{array}{rcl}ABC&=&a\\A&=&abc\end{array}",
         [r'\array', 'rcl', [[['A', 'B', 'C'], '=', 'a'], ['A', '=', ['a', 'b', 'c']]]]),
        (r'\begin{array}{cr} 1 & 2 \\ 3 & 4 \\ \hline 5 & 6 \end{array}',
         [r'\array', 'cr', [['1', '2'], ['3', '4'], [r'\hline', '5', '6']]],),
        (r'\mathrm{...}', [r'\mathrm', ['.', '.', '.']]),
        (r'\frac{x + 4}{x + \frac{123 \left(\sqrt{x} + 5\right)}{x + 4} - 8}',
         [r'\frac',
          ['x', '+', '4'],
          ['x', '+', r'\frac', [
              '123',
              [r'\left', '(', [r'\sqrt', ['x'], '+', '5'], r'\right', ')']
          ], ['x', '+', '4'], '-', '8']
          ]),
        (r'\sqrt {\sqrt {\left( x^{3}\right) + v}}',
         [r'\sqrt', [r'\sqrt', [[r'\left', '(', ['^', 'x', ['3']], r'\right', ')', '+', 'v', ]]]]),
        (r'\left(x\right){5}', [[r'\left', '(', ['x'], r'\right', ')', ['5']]]),
        (r'\left(- x^{3} + 5\right)^{5}',
         [['^', ['\\left', '(', ['-', '^', 'x', ['3'], '+', '5'], '\\right', ')'], ['5']]])
    ],
)
def test_aggregator(latex: str, expected: list):
    assert aggregate(latex) == expected


def test_missing_right():
    latex = r'\left(x'
    with pytest.raises(ExtraLeftOrMissingRight):
        aggregate(latex)
