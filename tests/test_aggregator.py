#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import string

import pytest

from latex2mathml.aggregator import aggregate
from latex2mathml.exceptions import (
    DenominatorNotFoundError,
    ExtraLeftOrMissingRight,
    MissingSuperScriptOrSubscript,
    NumeratorNotFoundError,
)

PARAMS = [
    ("alphabets", string.ascii_letters, list(string.ascii_letters)),
    ("empty group", "{{}}", [[[]]]),
    ("numbers", string.digits, [string.digits]),
    ("numbers with decimal", "12.56", ["12.56"]),
    ("numbers and alphabets", "5x", list("5x")),
    ("decimals and alphabets", "5.8x", ["5.8", "x"]),
    ("string with spaces", "3 x", ["3", "x"]),
    ("operators", "+-*/=()[]_^{}", list("+-*/=()[]_^{}")),
    (
        "numbers, alphabets and operators",
        "3 + 5x - 5y = 7",
        ["3", "+", "5", "x", "-", "5", "y", "=", "7"],
    ),
    ("symbols", r"\alpha\beta", [r"\alpha", r"\beta"]),
    ("symbols appended with number", r"\frac2x", [r"\frac", "2", "x"]),
    ("single group", "{a}", [["a"]]),
    ("multiple groups", "{a}{b}", [["a"], ["b"]]),
    ("inner group", "{a+{b}}", [["a", "+", ["b"]]]),
    ("subscript #1", "a_b", ["_", "a", "b"]),
    ("subscript #2", "{a_b}", [["_", "a", "b"]]),
    ("subscript #3", "1_2", ["_", "1", "2"]),
    ("subscript #4", "1.2_2", ["_", "1.2", "2"]),
    ("superscript #1", "a^b", ["^", "a", "b"]),
    ("superscript #2", "{a^b}", [["^", "a", "b"]]),
    ("superscript #3", "a^{i+1}_3", ["_^", "a", "3", ["i", "+", "1"]]),
    ("subscript and superscript #1", "a_b^c", ["_^", "a", "b", "c"]),
    ("subscript and superscript #2", "a^b_c", ["_^", "a", "c", "b"]),
    ("root", r"\sqrt[3]{2}", [r"\root", ["2"], ["3"]]),
    ("matrix #1", r"\matrix{a & b \\ c & d}", [r"\matrix", [["a", "b"], ["c", "d"]]],),
    (
        "matrix #2",
        r"\begin{matrix}a & b \\ c & d \end{matrix}",
        [r"\matrix", [["a", "b"], ["c", "d"]]],
    ),
    ("fraction #1", r"\frac{1}{2}", [r"\frac", ["1"], ["2"]]),
    ("fraction #2", r"1 \over 2", [r"\frac", ["1"], ["2"]]),
    ("fraction #3", r"{1 \over 2}", [[r"\frac", ["1"], ["2"]]]),
    ("null delimiter #1", r"\left\{\right.", [[r"\left", r"\{", r"\right", "."]]),
    (
        "null delimiter #2",
        r"\left\{ \begin{array} { l } { 3x - 5y + 4z = 0} \\ { x - y + 8z = 0} \\ { 2x - 6y + z = 0} "
        r"\end{array}\right.",
        [
            [
                r"\left",
                r"\{",
                [
                    r"\array",
                    "l",
                    [
                        [["3", "x", "-", "5", "y", "+", "4", "z", "=", "0"]],
                        [["x", "-", "y", "+", "8", "z", "=", "0"]],
                        [["2", "x", "-", "6", "y", "+", "z", "=", "0"]],
                    ],
                ],
                r"\right",
                ".",
            ]
        ],
    ),
    (
        "matrix with alignment",
        r"\begin{matrix*}[r]a & b \\ c & d \end{matrix*}",
        [r"\matrix*", "r", [["a", "b"], ["c", "d"]]],
    ),
    (
        "matrix with empty alignment",
        r"\begin{matrix*}[]a & b \\ c & d \end{matrix*}",
        [r"\matrix*", [["a", "b"], ["c", "d"]]],
    ),
    (
        "matrix with negative sign",
        r"\begin{matrix}-a & b \\ c & d \end{matrix}",
        [r"\matrix", [[["-", "a"], "b"], ["c", "d"]]],
    ),
    (
        "matrix with just negative sign #1",
        r"\begin{matrix}-\end{matrix}",
        [r"\matrix", ["-"]],
    ),
    (
        "complex matrix",
        r"\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}",
        [
            r"\matrix",
            [
                [["_", "a", ["1"]], ["_", "b", ["2"]]],
                [["_", "c", ["3"]], ["_", "d", ["4"]]],
            ],
        ],
    ),
    (
        "simple array",
        r"\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}",
        [r"\array", "cc", [["1", "2"], ["3", "4"]]],
    ),
    (
        "issue #33",
        r"""\begin{bmatrix}
     a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
     a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
     \vdots  & \vdots  & \ddots & \vdots  \\
     a_{m,1} & a_{m,2} & \cdots & a_{m,n}
    \end{bmatrix}""",
        [
            r"\bmatrix",
            [
                [
                    ["_", "a", ["1", ",", "1"]],
                    ["_", "a", ["1", ",", "2"]],
                    r"\cdots",
                    ["_", "a", ["1", ",", "n"]],
                ],
                [
                    ["_", "a", ["2", ",", "1"]],
                    ["_", "a", ["2", ",", "2"]],
                    r"\cdots",
                    ["_", "a", ["2", ",", "n"]],
                ],
                [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
                [
                    ["_", "a", ["m", ",", "1"]],
                    ["_", "a", ["m", ",", "2"]],
                    r"\cdots",
                    ["_", "a", ["m", ",", "n"]],
                ],
            ],
        ],
    ),
    (
        "issue #42",
        r"\sqrt { ( - 25 ) ^ { 2 } } = \pm 25",
        [r"\sqrt", ["^", ["(", "-", "25", ")"], ["2"]], "=", r"\pm", "25"],
    ),
    (
        "issue #44",
        r"\left(- x^{3} + 5\right)^{5}",
        ["^", [r"\left", "(", ["-", "^", "x", ["3"], "+", "5"], r"\right", ")"], ["5"]],
    ),
    (
        "issue #55",
        r"\begin{array}{rcl}ABC&=&a\\A&=&abc\end{array}",
        [r"\array", "rcl", [[["A", "B", "C"], "=", "a"], ["A", "=", ["a", "b", "c"]]]],
    ),
    (
        "array with horizontal line",
        r"\begin{array}{cr} 1 & 2 \\ 3 & 4 \\ \hline 5 & 6 \end{array}",
        [r"\array", "cr", [["1", "2"], ["3", "4"], [r"\hline", "5", "6"]]],
    ),
    (
        "array with horizontal lines",
        r"\begin{array}{cr} 1 & 2 \\ \hline 3 & 4 \\ \hline 5 & 6 \end{array}",
        [r"\array", "cr", [["1", "2"], [r"\hline", "3", "4"], [r"\hline", "5", "6"]]],
    ),
    ("issue #60", r"\mathrm{...}", [r"\mathrm", [".", ".", "."]]),
    (
        "issue #61",
        r"\frac{x + 4}{x + \frac{123 \left(\sqrt{x} + 5\right)}{x + 4} - 8}",
        [
            r"\frac",
            ["x", "+", "4"],
            [
                "x",
                "+",
                r"\frac",
                ["123", [r"\left", "(", [r"\sqrt", ["x"], "+", "5"], r"\right", ")"]],
                ["x", "+", "4"],
                "-",
                "8",
            ],
        ],
    ),
    (
        "issue #63",
        r"\sqrt {\sqrt {\left( x^{3}\right) + v}}",
        [
            r"\sqrt",
            [r"\sqrt", [[r"\left", "(", ["^", "x", ["3"]], r"\right", ")"], "+", "v"]],
        ],
    ),
    (
        r"group after \right",
        r"\left(x\right){5}",
        [[r"\left", "(", ["x"], r"\right", ")"], ["5"]],
    ),
    (r"empty nth root", r"\sqrt[3]{}", ["\\root", "", ["3"]]),
    (r"empty subscript", r"1_{}", ["_", "1", []]),
    (r"empty array", r"\array{}", [r"\array", []]),
    (r"empty array with empty group", r"\array{{}}", [r"\array", []]),
    (
        "issue #77",
        r"\left[\begin{matrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{matrix}\right]",
        [
            [
                r"\left",
                "[",
                [
                    r"\matrix",
                    [
                        ["1", "0", "0", "0"],
                        ["0", "1", "0", "0"],
                        ["0", "0", "1", "0"],
                        ["0", "0", "0", "1"],
                    ],
                ],
                r"\right",
                "]",
            ]
        ],
    ),
    (
        "issue #78",
        r"x^{x^{x^{x}}} \left(x^{x^{x}} \left(x^{x} \left(\log{\left(x \right)} + 1\right) \log{\left(x \right)} + "
        r"\frac{x^{x}}{x}\right) \log{\left(x \right)} + \frac{x^{x^{x}}}{x}\right)",
        [
            "^",
            "x",
            ["^", "x", ["^", "x", ["x"]]],
            [
                r"\left",
                "(",
                [
                    "^",
                    "x",
                    ["^", "x", ["x"]],
                    [
                        r"\left",
                        "(",
                        [
                            "^",
                            "x",
                            ["x"],
                            [
                                r"\left",
                                "(",
                                [
                                    r"\log",
                                    [[r"\left", "(", ["x"], r"\right", ")"]],
                                    "+",
                                    "1",
                                ],
                                r"\right",
                                ")",
                            ],
                            r"\log",
                            [[r"\left", "(", ["x"], r"\right", ")"]],
                            "+",
                            r"\frac",
                            ["^", "x", ["x"]],
                            ["x"],
                        ],
                        r"\right",
                        ")",
                    ],
                    r"\log",
                    [[r"\left", "(", ["x"], r"\right", ")"]],
                    "+",
                    r"\frac",
                    ["^", "x", ["^", "x", ["x"]]],
                    ["x"],
                ],
                r"\right",
                ")",
            ],
        ],
    ),
    (r"logarithm with base", r"\log_2{x}", ["_", r"\log", "2", ["x"]]),
    ("issue #79 - empty root", r"\sqrt[]{3}", [r"\sqrt", ["3"]]),
    (
        "issue #79 - exponent after fraction",
        r"\frac{3}{\frac{1}{2}{x}^{2}}",
        [r"\frac", ["3"], [r"\frac", ["1"], ["2"], "^", ["x"], ["2"]]],
    ),
    (
        "issue #79",
        r"\frac{3}{\frac{1}{2}{x}^{2}-\frac{3\sqrt[]{3}}{2}x+3}",
        [
            r"\frac",
            ["3"],
            [
                r"\frac",
                ["1"],
                ["2"],
                "^",
                ["x"],
                ["2"],
                "-",
                r"\frac",
                ["3", r"\sqrt", ["3"]],
                ["2"],
                "x",
                "+",
                "3",
            ],
        ],
    ),
    ("exponent without base works", "^3", ["^", "", "3"]),
]

PARAMS_WITH_EXCEPTION = [
    (r"missing \right", r"\left(x", ExtraLeftOrMissingRight),
    ("fraction without numerator", r"{ \over 2}", NumeratorNotFoundError),
    ("fraction without denominator", r"{1 \over }", DenominatorNotFoundError),
    ("missing subscript", r"1_", MissingSuperScriptOrSubscript),
    ("missing superscript", r"1^", MissingSuperScriptOrSubscript),
]


@pytest.mark.parametrize(
    "name, latex, expected", ids=[x[0] for x in PARAMS], argvalues=PARAMS,
)
def test_aggregator(name: str, latex: str, expected: list):
    assert aggregate(latex) == expected, name


@pytest.mark.parametrize(
    "name, latex, exception",
    ids=[x[0] for x in PARAMS_WITH_EXCEPTION],
    argvalues=PARAMS_WITH_EXCEPTION,
)
def test_missing_right(name: str, latex: str, exception: Exception):
    with pytest.raises(exception):
        aggregate(latex)
