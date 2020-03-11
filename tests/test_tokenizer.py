#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2018-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import string

import pytest

from latex2mathml.tokenizer import tokenize


@pytest.mark.parametrize(
    'latex, expected',
    ids=[
        'single backslash',
        'alphabets',
        'numbers',
        'backslash after number',
        'double backslash after number',
        'decimal',
        'incomplete decimal',
        'numbers and alphabets',
        'decimals and alphabets',
        'string with spaces',
        'operators',
        'numbers, alphabets and operators',
        'symbols',
        'symbols appended with number',
        'matrix',
        'matrix with alignment',
        'matrix with negative sign',
        'simple array',
        'subscript',
        'superscript with curly braces',
        'issue #33',
        'issue #51',
        'issue #55',
        'issue #60',
        'issue #61',
        'issue #63',
    ],
    argvalues=[
        ('\\', ['\\']),
        (string.ascii_letters, list(string.ascii_letters)),
        (string.digits, [string.digits]),
        ('123\\', ['123', '\\']),
        (r'123\\', ['123', r'\\']),
        ('12.56', ['12.56']),
        (r'12.\\', ['12', '.', r'\\']),
        ('5x', list('5x')),
        ('5.8x', ['5.8', 'x']),
        ('3 x', ['3', 'x']),
        ('+-*/=()[]_^{}', list('+-*/=()[]_^{}')),
        ('3 + 5x - 5y = 7', ['3', '+', '5', 'x', '-', '5', 'y', '=', '7']),
        (r'\alpha\beta', [r'\alpha', r'\beta']),
        (r'\frac2x', [r'\frac', '2', 'x']),
        (r'\begin{matrix}a & b \\ c & d \end{matrix}',
         [r'\begin{matrix}', 'a', '&', 'b', r'\\', 'c', '&', 'd', r'\end{matrix}']),
        (r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}',
         [r'\begin{matrix*}', '[', 'r', ']', 'a', '&', 'b', r'\\', 'c', '&', 'd', r'\end{matrix*}']),
        (r'\begin{matrix}-a & b \\ c & d \end{matrix}',
         [r'\begin{matrix}', '-', 'a', '&', 'b', r'\\', 'c', '&', 'd', r'\end{matrix}']),
        (r'\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}',
         [r'\begin{array}', '{', 'c', 'c', '}', '1', '&', '2', r'\\', '3', '&', '4', r'\end{array}']),
        ('a_{2,n}', ['a', '_', '{', '2', ',', 'n', '}']),
        ('a^{i+1}_3', ['a', '^', '{', 'i', '+', '1', '}', '_', '3']),
        (r'''\begin{bmatrix}
         a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
         a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
         \vdots  & \vdots  & \ddots & \vdots  \\
         a_{m,1} & a_{m,2} & \cdots & a_{m,n}
        \end{bmatrix}''',
         [r'\begin{bmatrix}', 'a', '_', '{', '1', ',', '1', '}', '&', 'a', '_', '{', '1', ',', '2', '}', '&', r'\cdots',
          '&', 'a', '_', '{', '1', ',', 'n', '}', r'\\', 'a', '_', '{', '2', ',', '1', '}', '&', 'a', '_', '{', '2',
          ',', '2', '}', '&', r'\cdots', '&', 'a', '_', '{', '2', ',', 'n', '}', r'\\', r'\vdots', '&', r'\vdots', '&',
          r'\ddots', '&', r'\vdots', r'\\', 'a', '_', '{', 'm', ',', '1', '}', '&', 'a', '_', '{', 'm', ',', '2', '}',
          '&', r'\cdots', '&', 'a', '_', '{', 'm', ',', 'n', '}', r'\end{bmatrix}']),
        (r'\mathbb{R}', ['&#x0211D;']),
        (r'\begin{array}{rcl}ABC&=&a\\A&=&abc\end{array}',
         [r'\begin{array}', '{', 'r', 'c', 'l', '}', 'A', 'B', 'C', '&', '=', '&', 'a', r'\\', 'A', '&', '=', '&', 'a',
          'b', 'c', r'\end{array}']),
        (r'\mathrm{...}', [r'\mathrm', '{', '.', '.', '.', '}']),
        (r'\frac{x + 4}{x + \frac{123 \left(\sqrt{x} + 5\right)}{x + 4} - 8}',
         [r'\frac', '{', 'x', '+', '4', '}', '{', 'x', '+', r'\frac', '{', '123', r'\left', '(', r'\sqrt', '{', 'x',
          '}', '+', '5', r'\right', ')', '}', '{', 'x', '+', '4', '}', '-', '8', '}']),
        (r'\sqrt {\sqrt {\left( x^{3}\right) + v}}',
         [r'\sqrt', '{', r'\sqrt', '{', r'\left', '(', 'x', '^', '{', '3', '}', r'\right', ')', '+', 'v', '}', '}'],),
    ],
)
def test_tokenize(latex: str, expected: list):
    assert list(tokenize(latex)) == expected
