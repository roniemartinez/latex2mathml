import string
from typing import Any, List, Tuple, Union

import pytest

from latex2mathml.aggregator import Node, aggregate, find_opening_parenthesis
from latex2mathml.exceptions import (
    DenominatorNotFoundError,
    ExtraLeftOrMissingRight,
    MissingSuperScriptOrSubscript,
    NumeratorNotFoundError,
)


@pytest.mark.parametrize(
    "latex, expected",
    [
        pytest.param(string.ascii_letters, [Node(token=c) for c in string.ascii_letters], id="alphabets"),
        pytest.param("{{}}", [Node(token="{}", children=(Node(token="{}"),))], id="empty-group"),
        pytest.param(string.digits, [Node(token=string.digits)], id="numbers"),
        pytest.param("12.56", [Node(token="12.56")], id="decimals"),
        pytest.param("5x", [Node(token="5"), Node(token="x")], id="numbers-and-alphabets"),
        pytest.param("5.8x", [Node(token="5.8"), Node(token="x")], id="decimals-and-alphabets"),
        pytest.param("3 x", [Node(token="3"), Node(token="x")], id="string-with-space"),
        pytest.param("+-*/=()[]", [Node(token=c) for c in "+-*/=()[]"], id="operators"),
        pytest.param("3 + 5x - 5y = 7", [Node(token=c) for c in "3+5x-5y=7"], id="numbers-alphabets-and-operators"),
        pytest.param(r"\alpha\beta", [Node(token=r"\alpha"), Node(token=r"\beta")], id="symbols"),
        pytest.param(
            r"\frac2x",
            [Node(token=r"\frac", children=(Node(token="2"), Node(token="x")))],
            id="symbols-appended-with-number",
        ),
        pytest.param("{a}", [Node(token="{}", children=(Node(token="a"),))], id="single-group"),
        pytest.param(
            "{a}{b}",
            [Node(token="{}", children=(Node(token="a"),)), Node(token="{}", children=(Node(token="b"),))],
            id="multiple-groups",
        ),
        pytest.param(
            "{a+{b}}",
            [
                Node(
                    token="{}",
                    children=(
                        Node(token="a"),
                        Node(token="+"),
                        Node(token="{}", children=(Node(token="b"),)),
                    ),
                )
            ],
            id="inner-group",
        ),
        pytest.param(
            "a_b",
            [Node(token="_", children=(Node(token="a"), Node(token="b")))],
            id="subscript-1",
        ),
        pytest.param(
            "{a_b}",
            [Node(token="{}", children=(Node(token="_", children=(Node(token="a"), Node(token="b"))),))],
            id="subscript-2",
        ),
        pytest.param("1_2", [Node(token="_", children=(Node(token="1"), Node(token="2")))], id="subscript-3"),
        pytest.param("1.2_2", [Node(token="_", children=(Node(token="1.2"), Node(token="2")))], id="subscript-4"),
        pytest.param("a^b", [Node(token="^", children=(Node(token="a"), Node(token="b")))], id="superscript-1"),
        pytest.param(
            "{a^b}",
            [Node(token="{}", children=(Node(token="^", children=(Node(token="a"), Node(token="b"))),))],
            id="superscript-2",
        ),
        pytest.param(
            "a^{i+1}_3",
            [
                Node(
                    token="_^",
                    children=(
                        Node(token="a"),
                        Node(token="3"),
                        Node(token="{}", children=(Node(token="i"), Node(token="+"), Node(token="1"))),
                    ),
                )
            ],
            id="superscript-3",
        ),
        pytest.param(
            "a_b^c",
            [Node(token="_^", children=(Node(token="a"), Node(token="b"), Node(token="c")))],
            id="subscript-and-superscript-1",
        ),
        pytest.param(
            "a^b_c",
            [Node(token="_^", children=(Node(token="a"), Node(token="c"), Node(token="b")))],
            id="subscript-and-superscript-2",
        ),
        pytest.param(
            r"\sqrt[3]{2}",
            [Node(token=r"\sqrt", children=(Node(token="{}", children=(Node(token="2"),)),), root="3")],
            id="root",
        ),
        pytest.param(
            r"\frac{1}{2}",
            [
                Node(
                    token=r"\frac",
                    children=(
                        Node(token="{}", children=(Node(token="1"),)),
                        Node(token="{}", children=(Node(token="2"),)),
                    ),
                ),
            ],
            id="fraction-1",
        ),
        pytest.param(
            r"1 \over 2",
            [Node(token=r"\frac", children=(Node(token="1"), Node(token="2")))],
            id="fraction-2",
        ),
        pytest.param(
            r"{1 \over 2}",
            [Node(token="{}", children=(Node(token=r"\frac", children=(Node(token="1"), Node(token="2"))),))],
            id="fraction-3",
        ),
        pytest.param(
            r"\left\{\right.",
            [Node(token=r"\left", children=(Node(token=r"\right", delimiter="."),), delimiter=r"\{")],
            id="null-delimiter-1",
        ),
        # pytest.param(r"\matrix{a & b \\ c & d}", [r"\matrix", [["a", "b"], ["c", "d"]]], id="matrix-1"),
        # pytest.param(
        #     r"\begin{matrix}a & b \\ c & d \end{matrix}", [r"\matrix", [["a", "b"], ["c", "d"]]], id="matrix-2"
        # ),
        # pytest.param(
        #     r"\left\{ \begin{array} { l } { 3x - 5y + 4z = 0} \\ { x - y + 8z = 0} \\ { 2x - 6y + z = 0} "
        #     r"\end{array}\right.",
        #     [
        #         [
        #             r"\left",
        #             r"\{",
        #             [
        #                 r"\array",
        #                 "l",
        #                 [
        #                     [["3", "x", "-", "5", "y", "+", "4", "z", "=", "0"]],
        #                     [["x", "-", "y", "+", "8", "z", "=", "0"]],
        #                     [["2", "x", "-", "6", "y", "+", "z", "=", "0"]],
        #                 ],
        #             ],
        #             r"\right",
        #             ".",
        #         ]
        #     ],
        #     id="null-delimiter-2",
        # ),
        # pytest.param(
        #     r"\begin{matrix*}[r]a & b \\ c & d \end{matrix*}",
        #     [r"\matrix*", "r", [["a", "b"], ["c", "d"]]],
        #     id="matrix-with-alignment",
        # ),
        # pytest.param(
        #     r"\begin{matrix*}[]a & b \\ c & d \end{matrix*}",
        #     [r"\matrix*", [["a", "b"], ["c", "d"]]],
        #     id="matrix-with-empty-alignment",
        # ),
        # pytest.param(
        #     r"\begin{matrix}-a & b \\ c & d \end{matrix}",
        #     [r"\matrix", [[["-", "a"], "b"], ["c", "d"]]],
        #     id="matrix-with-negative-sign",
        # ),
        # pytest.param(r"\begin{matrix}-\end{matrix}", [r"\matrix", ["-"]], id="matrix-with-just-negative-sign-1"),
        # pytest.param(
        #     r"\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}",
        #     [
        #         r"\matrix",
        #         [
        #             [["_", "a", ["1"]], ["_", "b", ["2"]]],
        #             [["_", "c", ["3"]], ["_", "d", ["4"]]],
        #         ],
        #     ],
        #     id="complex-matrix",
        # ),
        # pytest.param(
        #     r"\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}",
        #     [r"\array", "cc", [["1", "2"], ["3", "4"]]],
        #     id="simple-array",
        # ),
        # pytest.param(
        #     r"""\begin{bmatrix}
        #      a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
        #      a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
        #      \vdots  & \vdots  & \ddots & \vdots  \\
        #      a_{m,1} & a_{m,2} & \cdots & a_{m,n}
        #     \end{bmatrix}""",
        #     [
        #         r"\bmatrix",
        #         [
        #             [
        #                 ["_", "a", ["1", ",", "1"]],
        #                 ["_", "a", ["1", ",", "2"]],
        #                 r"\cdots",
        #                 ["_", "a", ["1", ",", "n"]],
        #             ],
        #             [
        #                 ["_", "a", ["2", ",", "1"]],
        #                 ["_", "a", ["2", ",", "2"]],
        #                 r"\cdots",
        #                 ["_", "a", ["2", ",", "n"]],
        #             ],
        #             [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
        #             [
        #                 ["_", "a", ["m", ",", "1"]],
        #                 ["_", "a", ["m", ",", "2"]],
        #                 r"\cdots",
        #                 ["_", "a", ["m", ",", "n"]],
        #             ],
        #         ],
        #     ],
        #     id="issue-33",
        # ),
        pytest.param(
            r"\sqrt { ( - 25 ) ^ { 2 } } = \pm 25",
            [
                Node(
                    token=r"\sqrt",
                    children=(
                        Node(
                            token="{}",
                            children=(
                                Node(
                                    token="^",
                                    children=(
                                        Node(token="()", children=(Node(token="-"), Node(token="25"))),
                                        Node(token="{}", children=(Node(token="2"),)),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                Node(token="="),
                Node(token=r"\pm"),
                Node(token="25"),
            ],
            id="issue-42",
        ),
        pytest.param(
            r"\left(- x^{3} + 5\right)^{5}",
            [
                Node(
                    token="^",
                    children=(
                        Node(
                            token=r"\left",
                            children=(
                                Node(token="-"),
                                Node(
                                    token="^", children=(Node(token="x"), Node(token="{}", children=(Node(token="3"),)))
                                ),
                                Node(token="+"),
                                Node(token="5"),
                                Node(token=r"\right", delimiter=")"),
                            ),
                            delimiter="(",
                        ),
                        Node(token="{}", children=(Node(token="5"),)),
                    ),
                )
            ],
            id="issue-44",
        ),
        # pytest.param(
        #     r"\begin{array}{rcl}ABC&=&a\\A&=&abc\end{array}",
        #     [r"\array", "rcl", [[["A", "B", "C"], "=", "a"], ["A", "=", ["a", "b", "c"]]]],
        #     id="issue-55",
        # ),
        # pytest.param(
        #     r"\begin{array}{cr} 1 & 2 \\ 3 & 4 \\ \hline 5 & 6 \end{array}",
        #     [r"\array", "cr", [["1", "2"], ["3", "4"], [r"\hline", "5", "6"]]],
        #     id="array-with-horizontal-line",
        # ),
        # pytest.param(
        #     r"\begin{array}{cr} 1 & 2 \\ \hline 3 & 4 \\ \hline 5 & 6 \end{array}",
        #     [r"\array", "cr", [["1", "2"], [r"\hline", "3", "4"], [r"\hline", "5", "6"]]],
        #     id="array-with-horizontal-lines",
        # ),
        pytest.param(
            r"\mathrm{...}",
            [Node(token=r"\mathrm"), Node(token="{}", children=(Node(token="."), Node(token="."), Node(token=".")))],
            id="issue-60",
        ),
        pytest.param(
            r"\frac{x + 4}{x + \frac{123 \left(\sqrt{x} + 5\right)}{x + 4} - 8}",
            [
                Node(
                    token=r"\frac",
                    children=(
                        Node(token="{}", children=(Node(token="x"), Node(token="+"), Node(token="4"))),
                        Node(
                            token="{}",
                            children=(
                                Node(token="x"),
                                Node(token="+"),
                                Node(
                                    token=r"\frac",
                                    children=(
                                        Node(
                                            token="{}",
                                            children=(
                                                Node(token="123"),
                                                Node(
                                                    token=r"\left",
                                                    children=(
                                                        Node(
                                                            token=r"\sqrt",
                                                            children=(Node(token="{}", children=(Node(token="x"),)),),
                                                        ),
                                                        Node(token="+"),
                                                        Node(token="5"),
                                                        Node(token=r"\right", delimiter=")"),
                                                    ),
                                                    delimiter="(",
                                                ),
                                            ),
                                        ),
                                        Node(token="{}", children=(Node(token="x"), Node(token="+"), Node(token="4"))),
                                    ),
                                ),
                                Node(token="-"),
                                Node(token="8"),
                            ),
                        ),
                    ),
                )
            ],
            id="issue-61",
        ),
        pytest.param(
            r"\sqrt {\sqrt {\left( x^{3}\right) + v}}",
            [
                Node(
                    token=r"\sqrt",
                    children=(
                        Node(
                            token="{}",
                            children=(
                                Node(
                                    token=r"\sqrt",
                                    children=(
                                        Node(
                                            token="{}",
                                            children=(
                                                Node(
                                                    token=r"\left",
                                                    children=(
                                                        Node(
                                                            token="^",
                                                            children=(
                                                                Node(token="x"),
                                                                Node(token="{}", children=(Node(token="3"),)),
                                                            ),
                                                        ),
                                                        Node(token=r"\right", delimiter=")"),
                                                    ),
                                                    delimiter="(",
                                                ),
                                                Node(token="+"),
                                                Node(token="v"),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                )
            ],
            id="issue-63",
        ),
        pytest.param(
            r"\left(\left(x\right)\right)",
            [
                Node(
                    token=r"\left",
                    children=(
                        Node(
                            token=r"\left",
                            children=(
                                Node(token="x"),
                                Node(token=r"\right", delimiter=")"),
                            ),
                            delimiter="(",
                        ),
                        Node(token=r"\right", delimiter=")"),
                    ),
                    delimiter="(",
                )
            ],
            id=r"nested-left-right",
        ),
        pytest.param(
            r"\left(x\right){5}",
            [
                Node(
                    token=r"\left",
                    children=(Node(token="x"), Node(token=r"\right", delimiter=")")),
                    delimiter="(",
                ),
                Node(token="{}", children=(Node(token="5"),)),
            ],
            id=r"group-after-right",
        ),
        pytest.param(
            r"\sqrt[3]{}",
            [Node(token=r"\sqrt", children=(Node(token="{}"),), root="3")],
            id="empty-nth-root",
        ),
        pytest.param(
            r"1_{}",
            [Node(token="_", children=(Node(token="1"), Node(token="{}")))],
            id="empty-subscript",
        ),
        # pytest.param(r"\array{}", [r"\array", []], id="empty-array"),
        # pytest.param(r"\array{{}}", [r"\array", []], id="empty-array-with-empty-group"),
        # pytest.param(
        #     r"\left[\begin{matrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{matrix}\right]",
        #     [
        #         [
        #             r"\left",
        #             "[",
        #             [
        #                 r"\matrix",
        #                 [
        #                     ["1", "0", "0", "0"],
        #                     ["0", "1", "0", "0"],
        #                     ["0", "0", "1", "0"],
        #                     ["0", "0", "0", "1"],
        #                 ],
        #             ],
        #             r"\right",
        #             "]",
        #         ]
        #     ],
        #     id="issue-77",
        # ),
        pytest.param(
            r"\left({x}\right)",
            [
                Node(
                    token=r"\left",
                    children=(
                        Node(token="{}", children=(Node(token="x"),)),
                        Node(token=r"\right", delimiter=")"),
                    ),
                    delimiter="(",
                )
            ],
            id="issue-78-1",
        ),
        pytest.param(
            r"\left(\frac{x^{x^{x}}}{x}\right)",
            [
                Node(
                    token=r"\left",
                    children=(
                        Node(
                            token=r"\frac",
                            children=(
                                Node(
                                    token="{}",
                                    children=(
                                        Node(
                                            token="^",
                                            children=(
                                                Node(token="x"),
                                                Node(
                                                    token="{}",
                                                    children=(
                                                        Node(
                                                            token="^",
                                                            children=(
                                                                Node(token="x"),
                                                                Node(token="{}", children=(Node(token="x"),)),
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                                Node(token="{}", children=(Node(token="x"),)),
                            ),
                        ),
                        Node(token=r"\right", delimiter=")"),
                    ),
                    delimiter="(",
                )
            ],
            id="issue-78-2",
        ),
        pytest.param(
            r"x^{x^{x^{x}}} \left(x^{x^{x}} \left(x^{x} \left(\log{\left(x \right)} + 1\right) \log{\left(x \right)} + "
            r"\frac{x^{x}}{x}\right) \log{\left(x \right)} + \frac{x^{x^{x}}}{x}\right)",
            [
                Node(
                    token="^",
                    children=(
                        Node(token="x"),
                        Node(
                            token="{}",
                            children=(
                                Node(
                                    token="^",
                                    children=(
                                        Node(token="x"),
                                        Node(
                                            token="{}",
                                            children=(
                                                Node(
                                                    token="^",
                                                    children=(
                                                        Node(token="x"),
                                                        Node(token="{}", children=(Node(token="x"),)),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                Node(
                    token=r"\left",
                    children=(
                        Node(
                            token="^",
                            children=(
                                Node(token="x"),
                                Node(
                                    token="{}",
                                    children=(
                                        Node(
                                            token="^",
                                            children=(Node(token="x"), Node(token="{}", children=(Node(token="x"),))),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        Node(
                            token=r"\left",
                            children=(
                                Node(
                                    token="^", children=(Node(token="x"), Node(token="{}", children=(Node(token="x"),)))
                                ),
                                Node(
                                    token=r"\left",
                                    children=(
                                        Node(token=r"\log"),
                                        Node(
                                            token="{}",
                                            children=(
                                                Node(
                                                    token=r"\left",
                                                    children=(Node(token="x"), Node(token=r"\right", delimiter=")")),
                                                    delimiter="(",
                                                ),
                                            ),
                                        ),
                                        Node(token="+"),
                                        Node(token="1"),
                                        Node(token=r"\right", delimiter=")"),
                                    ),
                                    delimiter="(",
                                ),
                                Node(token=r"\log"),
                                Node(
                                    token="{}",
                                    children=(
                                        Node(
                                            token=r"\left",
                                            children=(Node(token="x"), Node(token=r"\right", delimiter=")")),
                                            delimiter="(",
                                        ),
                                    ),
                                ),
                                Node(token="+"),
                                Node(
                                    token=r"\frac",
                                    children=(
                                        Node(
                                            token="{}",
                                            children=(
                                                Node(
                                                    token="^",
                                                    children=(
                                                        Node(token="x"),
                                                        Node(token="{}", children=(Node(token="x"),)),
                                                    ),
                                                ),
                                            ),
                                        ),
                                        Node(token="{}", children=(Node(token="x"),)),
                                    ),
                                ),
                                Node(token=r"\right", delimiter=")"),
                            ),
                            delimiter="(",
                        ),
                        Node(token=r"\log"),
                        Node(
                            token="{}",
                            children=(
                                Node(
                                    token=r"\left",
                                    children=(Node(token="x"), Node(token=r"\right", delimiter=")")),
                                    delimiter="(",
                                ),
                            ),
                        ),
                        Node(token="+"),
                        Node(
                            token=r"\frac",
                            children=(
                                Node(
                                    token="{}",
                                    children=(
                                        Node(
                                            token="^",
                                            children=(
                                                Node(token="x"),
                                                Node(
                                                    token="{}",
                                                    children=(
                                                        Node(
                                                            token="^",
                                                            children=(
                                                                Node(token="x"),
                                                                Node(token="{}", children=(Node(token="x"),)),
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                                Node(token="{}", children=(Node(token="x"),)),
                            ),
                        ),
                        Node(token=r"\right", delimiter=")"),
                    ),
                    delimiter="(",
                ),
            ],
            id="issue-78-3",
        ),
        pytest.param(
            r"\log_2{x}",
            [
                Node(token="_", children=(Node(token=r"\log"), Node(token="2"))),
                Node(token="{}", children=(Node(token="x"),)),
            ],
            id="logarithm-with-base",
        ),
        pytest.param(
            r"\sqrt[]{3}",
            [Node(token=r"\sqrt", children=(Node(token="{}", children=(Node(token="3"),)),))],
            id="issue-79-empty-root",
        ),
        pytest.param(
            r"\frac{3}{\frac{1}{2}{x}^{2}}",
            [
                Node(
                    token=r"\frac",
                    children=(
                        Node(token="{}", children=(Node(token="3"),)),
                        Node(
                            token="{}",
                            children=(
                                Node(
                                    token=r"\frac",
                                    children=(
                                        Node(token="{}", children=(Node(token="1"),)),
                                        Node(token="{}", children=(Node(token="2"),)),
                                    ),
                                ),
                                Node(
                                    token="^",
                                    children=(
                                        Node(token="{}", children=(Node(token="x"),)),
                                        Node(token="{}", children=(Node(token="2"),)),
                                    ),
                                ),
                            ),
                        ),
                    ),
                )
            ],
            id="issue-79-exponent-after-fraction",
        ),
        pytest.param(
            r"\frac{3}{\frac{1}{2}{x}^{2}-\frac{3\sqrt[]{3}}{2}x+3}",
            [
                Node(
                    token=r"\frac",
                    children=(
                        Node(token="{}", children=(Node(token="3"),)),
                        Node(
                            token="{}",
                            children=(
                                Node(
                                    token=r"\frac",
                                    children=(
                                        Node(token="{}", children=(Node(token="1"),)),
                                        Node(token="{}", children=(Node(token="2"),)),
                                    ),
                                ),
                                Node(
                                    token="^",
                                    children=(
                                        Node(token="{}", children=(Node(token="x"),)),
                                        Node(token="{}", children=(Node(token="2"),)),
                                    ),
                                ),
                                Node(token="-"),
                                Node(
                                    token=r"\frac",
                                    children=(
                                        Node(
                                            token="{}",
                                            children=(
                                                Node(token="3"),
                                                Node(
                                                    token=r"\sqrt",
                                                    children=(Node(token="{}", children=(Node(token="3"),)),),
                                                ),
                                            ),
                                        ),
                                        Node(token="{}", children=(Node(token="2"),)),
                                    ),
                                ),
                                Node(token="x"),
                                Node(token="+"),
                                Node(token="3"),
                            ),
                        ),
                    ),
                )
            ],
            id="issue-79",
        ),
        pytest.param(
            "^3", [Node(token="^", children=(Node(token=""), Node(token="3")))], id="superscript-without-base-works"
        ),
        pytest.param(
            "_3", [Node(token="_", children=(Node(token=""), Node(token="3")))], id="subscript-without-base-works"
        ),
        pytest.param(
            r"\lim_{x \to +\infty} f(x)",
            [
                Node(
                    token="_",
                    children=(
                        Node(token=r"\lim"),
                        Node(
                            token="{}",
                            children=(Node(token="x"), Node(token=r"\to"), Node(token="+"), Node(token=r"\infty")),
                        ),
                    ),
                ),
                Node(token="f"),
                Node(token="()", children=(Node(token="x"),)),
            ],
            id="limit-at-plus-infinity",
        ),
        pytest.param(
            r"\inf_{x > s}f(x)",
            [
                Node(
                    token="_",
                    children=(
                        Node(token=r"\inf"),
                        Node(token="{}", children=(Node(token="x"), Node(token=">"), Node(token="s"))),
                    ),
                ),
                Node(token="f"),
                Node(token="()", children=(Node(token="x"),)),
            ],
            id="inf",
        ),
        pytest.param(
            r"\sup_{x \in \mathbb{R}}f(x)",
            [
                Node(
                    token="_",
                    children=(
                        Node(token=r"\sup"),
                        Node(token="{}", children=(Node(token="x"), Node(token=r"\in"), Node(token="&#x0211D;"))),
                    ),
                ),
                Node(token="f"),
                Node(token="()", children=(Node(token="x"),)),
            ],
            id="sup",
        ),
        pytest.param(
            r"\max_{x \in [a,b]}f(x)",
            [
                Node(
                    token="_",
                    children=(
                        Node(token=r"\max"),
                        Node(
                            token="{}",
                            children=(
                                Node(token="x"),
                                Node(token=r"\in"),
                                Node(token="[]", children=(Node(token="a"), Node(token=","), Node(token="b"))),
                            ),
                        ),
                    ),
                ),
                Node(token="f"),
                Node(token="()", children=(Node(token="x"),)),
            ],
            id="max",
        ),
        pytest.param(
            r"\min_{x \in [\alpha,\beta]}f(x)",
            [
                Node(
                    token="_",
                    children=(
                        Node(token=r"\min"),
                        Node(
                            token="{}",
                            children=(
                                Node(token="x"),
                                Node(token=r"\in"),
                                Node(
                                    token="[]", children=(Node(token=r"\alpha"), Node(token=","), Node(token=r"\beta"))
                                ),
                            ),
                        ),
                    ),
                ),
                Node(token="f"),
                Node(token="()", children=(Node(token="x"),)),
            ],
            id="min",
        ),
        pytest.param(
            r"\int\limits_{0}^{\pi}",
            [
                Node(token=r"\int"),
                Node(
                    token="_^",
                    children=(
                        Node(token=r"\limits"),
                        Node(token="{}", children=(Node(token="0"),)),
                        Node(token="{}", children=(Node(token=r"\pi"),)),
                    ),
                ),
            ],
            id="issue-76",
        ),
        pytest.param(
            r"\sum_{\substack{1\le i\le n\\ i\ne j}}",
            [
                Node(
                    token="_",
                    children=(
                        Node(token=r"\sum"),
                        Node(
                            token="{}",
                            children=(
                                Node(token=r"\substack"),
                                Node(
                                    token="{}",
                                    children=(
                                        Node(token="1"),
                                        Node(token=r"\le"),
                                        Node(token="i"),
                                        Node(token=r"\le"),
                                        Node(token="n"),
                                        Node(token=r"\\"),
                                        Node(token="i"),
                                        Node(token=r"\ne"),
                                        Node(token="j"),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ],
            id="issue-75",
        ),
        pytest.param(
            r"\mathrm{AA}",
            [Node(token=r"\mathrm"), Node(token="{}", children=(Node(token="A"), Node(token="A")))],
            id="issue-94",
        ),
        pytest.param(
            r"(1+(x-y)^{2})",
            [
                Node(
                    token="()",
                    children=(
                        Node(token="1"),
                        Node(token="+"),
                        Node(
                            token="^",
                            children=(
                                Node(token="()", children=(Node(token="x"), Node(token="-"), Node(token="y"))),
                                Node(token="{}", children=(Node(token="2"),)),
                            ),
                        ),
                    ),
                )
            ],
            id="issue-96",
        ),
        pytest.param(
            r"p_{\max}",
            [Node(token="_", children=(Node(token="p"), Node(token="{}", children=(Node(token=r"\max"),))))],
            id="issue-98",
        ),
        pytest.param(
            r"\vec{AB}",
            [Node(token=r"\vec"), Node(token="{}", children=(Node(token="A"), Node(token="B")))],
            id="issue-103",
        ),
        pytest.param(r"\max f", [Node(token=r"\max"), Node(token="f")], id="issue-108-1"),
        pytest.param(
            r"\max \{a, b, c\}",
            [
                Node(token=r"\max"),
                Node(token=r"\{"),
                Node(token="a"),
                Node(token=","),
                Node(token="b"),
                Node(token=","),
                Node(token="c"),
                Node(token=r"\}"),
            ],
            id="issue-108-2",
        ),
        pytest.param(
            r"\min{(x, y)}",
            [
                Node(token=r"\min"),
                Node(
                    token="{}",
                    children=(Node(token="()", children=(Node(token="x"), Node(token=","), Node(token="y"))),),
                ),
            ],
            id="issue-108-3",
        ),
        pytest.param(
            r"x = {-b \pm \sqrt{b^2-4ac} \over 2a}",
            # FIXME: -b \pm should be inside \frac
            [
                Node(token="x"),
                Node(token="="),
                Node(
                    token="{}",
                    children=(
                        Node(token="-"),
                        Node(token="b"),
                        Node(token=r"\pm"),
                        Node(
                            token=r"\frac",
                            children=(
                                Node(
                                    token=r"\sqrt",
                                    children=(
                                        Node(
                                            token="{}",
                                            children=(
                                                Node(token="^", children=(Node(token="b"), Node(token="2"))),
                                                Node(token="-"),
                                                Node(token="4"),
                                                Node(token="a"),
                                                Node(token="c"),
                                            ),
                                        ),
                                    ),
                                ),
                                Node(
                                    token="{}",
                                    children=(
                                        Node(token="2"),
                                        Node(token="a"),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ],
            id="quadratic-equation",
        ),
    ],
)
def test_aggregator(latex: str, expected: list) -> None:
    assert aggregate(latex) == expected


@pytest.mark.parametrize(
    "latex, exception",
    [
        pytest.param(r"\left(x", ExtraLeftOrMissingRight, id=r"missing-\right"),
        pytest.param(r"{ \over 2}", NumeratorNotFoundError, id="fraction-without-numerator"),
        pytest.param(r"{1 \over }", DenominatorNotFoundError, id="fraction-without-denominator"),
        pytest.param(r"1_", MissingSuperScriptOrSubscript, id="missing-subscript"),
        pytest.param(r"1^", MissingSuperScriptOrSubscript, id="missing-superscript"),
    ],
)
def test_missing_right(latex: str, exception: Union[Tuple[Any, ...], Any]) -> None:
    with pytest.raises(exception):
        aggregate(latex)


@pytest.mark.parametrize(
    "tokens, index",
    [
        pytest.param(["("], 0, id="index-0-1"),
        pytest.param(["(", "(", ")"], 0, id="index-0-2"),
        pytest.param(["(", "("], 1, id="index-1"),
        pytest.param(["(", "(", "("], 2, id="index-2"),
    ],
)
def test_find_opening_parenthesis(tokens: List[Any], index: int) -> None:
    assert find_opening_parenthesis(tokens) == index


def test_find_opening_parenthesis_raises_error() -> None:
    with pytest.raises(ExtraLeftOrMissingRight):
        find_opening_parenthesis([])
