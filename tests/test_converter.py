import sys

import pytest
from multidict import MultiDict
from xmljson import BadgerFish

# noinspection PyProtectedMember
from latex2mathml.converter import _convert, convert


@pytest.mark.parametrize(
    "latex, json",
    [
        pytest.param("x", {"mi": "x"}, id="single-identifier"),
        pytest.param("xyz", MultiDict([("mi", "x"), ("mi", "y"), ("mi", "z")]), id="multiple-identifier"),
        pytest.param("3", {"mn": "3"}, id="single-number"),
        pytest.param("333", {"mn": "333"}, id="multiple-numbers"),
        pytest.param("12.34", {"mn": "12.34"}, id="decimal-numbers"),
        pytest.param("12x", MultiDict([("mn", "12"), ("mi", "x")]), id="numbers-and-identifiers"),
        pytest.param("+", {"mo": "&#x0002B;"}, id="single-operator"),
        pytest.param("3-2", MultiDict([("mn", "3"), ("mo", "&#x02212;"), ("mn", "2")]), id="numbers-and-operators"),
        pytest.param(
            "3x*2",
            MultiDict([("mn", "3"), ("mi", "x"), ("mo", "&#x0002A;"), ("mn", "2")]),
            id="numbers-identifiers-and-operators",
        ),
        pytest.param("{a}", {"mrow": {"mi": "a"}}, id="single-group"),
        pytest.param("{a}{b}", MultiDict([("mrow", {"mi": "a"}), ("mrow", {"mi": "b"})]), id="multiple-groups"),
        pytest.param(
            "{a+{b}}", {"mrow": MultiDict([("mi", "a"), ("mo", "&#x0002B;"), ("mrow", {"mi": "b"})])}, id="inner-group"
        ),
        pytest.param(r"1 \over 2", {"mfrac": MultiDict([("mn", "1"), ("mn", "2")])}, id="over"),
        pytest.param(
            r"{1 \over 2}", {"mrow": {"mfrac": MultiDict([("mn", "1"), ("mn", "2")])}}, id="over-inside-braces"
        ),
        pytest.param(
            r"\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}",
            {
                "mtable": MultiDict(
                    [
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"msub": MultiDict([("mi", "a"), ("mrow", {"mn": "1"})])}),
                                    ("mtd", {"msub": MultiDict([("mi", "b"), ("mrow", {"mn": "2"})])}),
                                ]
                            ),
                        ),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"msub": MultiDict([("mi", "c"), ("mrow", {"mn": "3"})])}),
                                    ("mtd", {"msub": MultiDict([("mi", "d"), ("mrow", {"mn": "4"})])}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="complex-matrix",
        ),
        pytest.param(
            r"\left\{ \begin{array} { l } { 3x - 5y + 4z = 0} \\ { x - y + 8z = 0} \\ { 2x - 6y + z = 0} \end{array} "
            r"\right.",
            {
                "mrow": MultiDict(
                    [
                        ("mo", {"@stretchy": "true", "@fence": "true", "@form": "prefix", "$": "&#x0007B;"}),
                        (
                            "mtable",
                            MultiDict(
                                [
                                    (
                                        "mtr",
                                        {
                                            "mtd": {
                                                "@columnalign": "left",
                                                "mrow": MultiDict(
                                                    [
                                                        ("mn", "3"),
                                                        ("mi", "x"),
                                                        ("mo", "&#x02212;"),
                                                        ("mn", "5"),
                                                        ("mi", "y"),
                                                        ("mo", "&#x0002B;"),
                                                        ("mn", "4"),
                                                        ("mi", "z"),
                                                        ("mo", "&#x0003D;"),
                                                        ("mn", "0"),
                                                    ]
                                                ),
                                            },
                                        },
                                    ),
                                    (
                                        "mtr",
                                        {
                                            "mtd": {
                                                "@columnalign": "left",
                                                "mrow": MultiDict(
                                                    [
                                                        ("mi", "x"),
                                                        ("mo", "&#x02212;"),
                                                        ("mi", "y"),
                                                        ("mo", "&#x0002B;"),
                                                        ("mn", "8"),
                                                        ("mi", "z"),
                                                        ("mo", "&#x0003D;"),
                                                        ("mn", "0"),
                                                    ]
                                                ),
                                            },
                                        },
                                    ),
                                    (
                                        "mtr",
                                        {
                                            "mtd": {
                                                "@columnalign": "left",
                                                "mrow": MultiDict(
                                                    [
                                                        ("mn", "2"),
                                                        ("mi", "x"),
                                                        ("mo", "&#x02212;"),
                                                        ("mn", "6"),
                                                        ("mi", "y"),
                                                        ("mo", "&#x0002B;"),
                                                        ("mi", "z"),
                                                        ("mo", "&#x0003D;"),
                                                        ("mn", "0"),
                                                    ]
                                                ),
                                            },
                                        },
                                    ),
                                ]
                            ),
                        ),
                        ("mo", {"@stretchy": "true", "@fence": "true", "@form": "postfix"}),
                    ]
                )
            },
            id="null-delimiter",
        ),
        pytest.param("a_b", {"msub": MultiDict([("mi", "a"), ("mi", "b")])}, id="subscript"),
        pytest.param("a^b", {"msup": MultiDict([("mi", "a"), ("mi", "b")])}, id="superscript"),
        pytest.param(
            "a_b^c", {"msubsup": MultiDict([("mi", "a"), ("mi", "b"), ("mi", "c")])}, id="subscript-and-superscript"
        ),
        pytest.param(
            "a^b_c", {"msubsup": MultiDict([("mi", "a"), ("mi", "c"), ("mi", "b")])}, id="superscript-and-subscript"
        ),
        pytest.param(
            "{a_b}", {"mrow": {"msub": MultiDict([("mi", "a"), ("mi", "b")])}}, id="subscript-within-curly-braces"
        ),
        pytest.param(
            "{a^b}", {"mrow": {"msup": MultiDict([("mi", "a"), ("mi", "b")])}}, id="superscript-within-curly-braces"
        ),
        pytest.param(
            "a^{i+1}_3",
            {
                "msubsup": MultiDict(
                    [("mi", "a"), ("mn", "3"), ("mrow", MultiDict([("mi", "i"), ("mo", "&#x0002B;"), ("mn", "1")]))]
                )
            },
            id="superscript-subscript-and-curly-braces",
        ),
        pytest.param(
            r"\frac{1}{2}", {"mfrac": MultiDict([("mrow", {"mn": "1"}), ("mrow", {"mn": "2"})])}, id="simple-fraction"
        ),
        pytest.param(r"\sqrt{2}", {"msqrt": {"mrow": {"mn": "2"}}}, id="square-root"),
        pytest.param(r"\sqrt[3]{2}", {"mroot": MultiDict([("mrow", {"mn": "2"}), ("mn", "3")])}, id="root"),
        pytest.param(
            r"\binom{2}{3}",
            MultiDict(
                [
                    ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "&#x00028;"}),
                    ("mfrac", MultiDict([("@linethickness", "0"), ("mrow", {"mn": "2"}), ("mrow", {"mn": "3"})])),
                    ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "&#x00029;"}),
                ]
            ),
            id="binomial",
        ),
        pytest.param(
            r"\left(x\right)",
            MultiDict(
                [
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@stretchy": "true", "@fence": "true", "@form": "prefix", "$": "&#x00028;"}),
                                ("mi", "x"),
                                ("mo", {"@stretchy": "true", "@fence": "true", "@form": "postfix", "$": "&#x00029;"}),
                            ]
                        ),
                    ),
                ]
            ),
            id="left-and-right",
        ),
        pytest.param(r"\,", {"mspace": {"@width": "0.167em"}}, id="space"),
        pytest.param(
            r"\overline{a}",
            {"mover": MultiDict([("mrow", {"mi": "a"}), ("mo", {"@stretchy": "true", "$": "&#x000AF;"})])},
            id="overline",
        ),
        pytest.param(
            r"\underline{a}",
            {"munder": MultiDict([("mrow", {"mi": "a"}), ("mo", {"@stretchy": "true", "$": "&#x00332;"})])},
            id="underline",
        ),
        pytest.param(
            r"\begin{matrix}a & b \\ c & d \end{matrix}",
            {
                "mtable": MultiDict(
                    [
                        ("mtr", MultiDict([("mtd", {"mi": "a"}), ("mtd", {"mi": "b"})])),
                        ("mtr", MultiDict([("mtd", {"mi": "c"}), ("mtd", {"mi": "d"})])),
                    ]
                ),
            },
            id="matrix",
        ),
        pytest.param(
            r"\matrix{a & b \\ c & d}",
            {
                "mtable": MultiDict(
                    [
                        ("mtr", MultiDict([("mtd", {"mi": "a"}), ("mtd", {"mi": "b"})])),
                        ("mtr", MultiDict([("mtd", {"mi": "c"}), ("mtd", {"mi": "d"})])),
                    ]
                ),
            },
            id="matrix-without-begin-and-end",
        ),
        pytest.param(
            r"\begin{matrix*}[r]a & b \\ c & d \end{matrix*}",
            {
                "mtable": MultiDict(
                    [
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "right", "mi": "a"}),
                                    ("mtd", {"@columnalign": "right", "mi": "b"}),
                                ]
                            ),
                        ),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "right", "mi": "c"}),
                                    ("mtd", {"@columnalign": "right", "mi": "d"}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="matrix-with-alignment",
        ),
        pytest.param(
            r"\begin{matrix}-a & b \\ c & d \end{matrix}",
            {
                "mtable": MultiDict(
                    [
                        (
                            "mtr",
                            MultiDict([("mtd", MultiDict([("mo", "&#x02212;"), ("mi", "a")])), ("mtd", {"mi": "b"})]),
                        ),
                        ("mtr", MultiDict([("mtd", {"mi": "c"}), ("mtd", {"mi": "d"})])),
                    ]
                ),
            },
            id="matrix-with-negative-sign",
        ),
        pytest.param(
            r"\begin{pmatrix}a & b \\ c & d \end{pmatrix}",
            MultiDict(
                [
                    ("mo", "&#x00028;"),
                    (
                        "mtable",
                        MultiDict(
                            [
                                ("mtr", MultiDict([("mtd", {"mi": "a"}), ("mtd", {"mi": "b"})])),
                                ("mtr", MultiDict([("mtd", {"mi": "c"}), ("mtd", {"mi": "d"})])),
                            ]
                        ),
                    ),
                    ("mo", "&#x00029;"),
                ]
            ),
            id="pmatrix",
        ),
        pytest.param(
            r"\begin{array}{cr} 1 & 2 \\ 3 & 4 \end{array}",
            {
                "mtable": MultiDict(
                    [
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "center", "mn": "1"}),
                                    ("mtd", {"@columnalign": "right", "mn": "2"}),
                                ]
                            ),
                        ),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "center", "mn": "3"}),
                                    ("mtd", {"@columnalign": "right", "mn": "4"}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="simple-array",
        ),
        pytest.param(
            r"\begin{array}{c|rl} 1 & 2 & 3 \\ 4 & 5 & 6 \end{array}",
            {
                "mtable": MultiDict(
                    [
                        ("@columnlines", "solid none"),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "center", "mn": "1"}),
                                    ("mtd", {"@columnalign": "right", "mn": "2"}),
                                    ("mtd", {"@columnalign": "left", "mn": "3"}),
                                ]
                            ),
                        ),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "center", "mn": "4"}),
                                    ("mtd", {"@columnalign": "right", "mn": "5"}),
                                    ("mtd", {"@columnalign": "left", "mn": "6"}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="array-with-vertical-bar",
        ),
        pytest.param(
            r"\begin{array}{cr} 1 & 2 \\ 3 & 4 \\ \hline 5 & 6 \\ \hdashline 7 & 8 \end{array}",
            {
                "mtable": MultiDict(
                    [
                        ("@rowlines", "none solid dashed"),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "center", "mn": "1"}),
                                    ("mtd", {"@columnalign": "right", "mn": "2"}),
                                ]
                            ),
                        ),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "center", "mn": "3"}),
                                    ("mtd", {"@columnalign": "right", "mn": "4"}),
                                ]
                            ),
                        ),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "center", "mn": "5"}),
                                    ("mtd", {"@columnalign": "right", "mn": "6"}),
                                ]
                            ),
                        ),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "center", "mn": "7"}),
                                    ("mtd", {"@columnalign": "right", "mn": "8"}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="array-with-horizontal-lines",
        ),
        pytest.param(
            r"""\begin{bmatrix}
             a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
             a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
             \vdots  & \vdots  & \ddots & \vdots  \\
             a_{m,1} & a_{m,2} & \cdots & a_{m,n}
            \end{bmatrix}""",
            MultiDict(
                [
                    ("mo", "&#x0005B;"),
                    (
                        "mtable",
                        MultiDict(
                            [
                                (
                                    "mtr",
                                    MultiDict(
                                        [
                                            (
                                                "mtd",
                                                {
                                                    "msub": MultiDict(
                                                        [
                                                            ("mi", "a"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [("mn", "1"), ("mo", "&#x0002C;"), ("mn", "1")]
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                },
                                            ),
                                            (
                                                "mtd",
                                                {
                                                    "msub": MultiDict(
                                                        [
                                                            ("mi", "a"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [("mn", "1"), ("mo", "&#x0002C;"), ("mn", "2")]
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                },
                                            ),
                                            ("mtd", {"mo": "&#x022EF;"}),
                                            (
                                                "mtd",
                                                {
                                                    "msub": MultiDict(
                                                        [
                                                            ("mi", "a"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [("mn", "1"), ("mo", "&#x0002C;"), ("mi", "n")]
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                },
                                            ),
                                        ]
                                    ),
                                ),
                                (
                                    "mtr",
                                    MultiDict(
                                        [
                                            (
                                                "mtd",
                                                {
                                                    "msub": MultiDict(
                                                        [
                                                            ("mi", "a"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [("mn", "2"), ("mo", "&#x0002C;"), ("mn", "1")]
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                },
                                            ),
                                            (
                                                "mtd",
                                                {
                                                    "msub": MultiDict(
                                                        [
                                                            ("mi", "a"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [("mn", "2"), ("mo", "&#x0002C;"), ("mn", "2")]
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                },
                                            ),
                                            ("mtd", {"mo": "&#x022EF;"}),
                                            (
                                                "mtd",
                                                {
                                                    "msub": MultiDict(
                                                        [
                                                            ("mi", "a"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [("mn", "2"), ("mo", "&#x0002C;"), ("mi", "n")]
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                },
                                            ),
                                        ]
                                    ),
                                ),
                                (
                                    "mtr",
                                    MultiDict(
                                        [
                                            ("mtd", {"mo": "&#x022EE;"}),
                                            ("mtd", {"mo": "&#x022EE;"}),
                                            ("mtd", {"mo": "&#x022F1;"}),
                                            ("mtd", {"mo": "&#x022EE;"}),
                                        ]
                                    ),
                                ),
                                (
                                    "mtr",
                                    MultiDict(
                                        [
                                            (
                                                "mtd",
                                                {
                                                    "msub": MultiDict(
                                                        [
                                                            ("mi", "a"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [("mi", "m"), ("mo", "&#x0002C;"), ("mn", "1")]
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                },
                                            ),
                                            (
                                                "mtd",
                                                {
                                                    "msub": MultiDict(
                                                        [
                                                            ("mi", "a"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [("mi", "m"), ("mo", "&#x0002C;"), ("mn", "2")]
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                },
                                            ),
                                            ("mtd", {"mo": "&#x022EF;"}),
                                            (
                                                "mtd",
                                                {
                                                    "msub": MultiDict(
                                                        [
                                                            ("mi", "a"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [("mi", "m"), ("mo", "&#x0002C;"), ("mi", "n")]
                                                                ),
                                                            ),
                                                        ]
                                                    )
                                                },
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("mo", "&#x0005D;"),
                ]
            ),
            id="issue-33",
        ),
        pytest.param(
            r"\sqrt { ( - 25 ) ^ { 2 } } = \pm 25",
            MultiDict(
                [
                    (
                        "msqrt",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mo", {"$": "&#x00028;", "@stretchy": "false"}),
                                    ("mo", "&#x02212;"),
                                    ("mn", "25"),
                                    (
                                        "msup",
                                        MultiDict(
                                            [
                                                ("mo", {"$": "&#x00029;", "@stretchy": "false"}),
                                                ("mrow", {"mn": "2"}),
                                            ]
                                        ),
                                    ),
                                ]
                            )
                        },
                    ),
                    ("mo", "&#x0003D;"),
                    ("mi", "&#x000B1;"),
                    ("mn", "25"),
                ]
            ),
            id="issue-42",
        ),
        pytest.param("2 < 5", MultiDict([("mn", "2"), ("mo", "&#x0003C;"), ("mn", "5")]), id="issue-45-lt"),
        pytest.param("2 > 5", MultiDict([("mn", "2"), ("mo", "&#x0003E;"), ("mn", "5")]), id="issue-45-gt"),
        pytest.param(r"\And", MultiDict([("mi", "&#x00026;")]), id="And"),
        pytest.param(
            r"\left(- x^{3} + 5\right)^{5}",
            MultiDict(
                [
                    (
                        "msup",
                        MultiDict(
                            [
                                (
                                    "mrow",
                                    MultiDict(
                                        [
                                            (
                                                "mo",
                                                {
                                                    "@stretchy": "true",
                                                    "@fence": "true",
                                                    "@form": "prefix",
                                                    "$": "&#x00028;",
                                                },
                                            ),
                                            ("mo", "&#x02212;"),
                                            ("msup", MultiDict([("mi", "x"), ("mrow", {"mn": "3"})])),
                                            ("mo", "&#x0002B;"),
                                            ("mn", "5"),
                                            (
                                                "mo",
                                                {
                                                    "@stretchy": "true",
                                                    "@fence": "true",
                                                    "@form": "postfix",
                                                    "$": "&#x00029;",
                                                },
                                            ),
                                        ]
                                    ),
                                ),
                                ("mrow", {"mn": "5"}),
                            ]
                        ),
                    )
                ]
            ),
            id="issue-44",
        ),
        pytest.param(r"\mathbb{R}", {"mi": "&#x0211D;"}, id="issue-51"),
        pytest.param(
            r"\bar{z_1} = z_2",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict(
                            [
                                ("mrow", {"msub": MultiDict([("mi", "z"), ("mn", "1")])}),
                                ("mo", {"@stretchy": "true", "$": "&#x000AF;"}),
                            ]
                        ),
                    ),
                    ("mo", "&#x0003D;"),
                    ("msub", MultiDict([("mi", "z"), ("mn", "2")])),
                ]
            ),
            id="issue-52",
        ),
        pytest.param(
            r"\mathrm{...}",
            {"mrow": MultiDict([("mo", "&#x0002E;"), ("mo", "&#x0002E;"), ("mo", "&#x0002E;")])},
            id="issue-60-1",
        ),
        pytest.param(
            r"\mathrm{...}+\mathrm{...}",
            MultiDict(
                [
                    ("mrow", MultiDict([("mo", "&#x0002E;"), ("mo", "&#x0002E;"), ("mo", "&#x0002E;")])),
                    ("mo", "&#x0002B;"),
                    ("mrow", MultiDict([("mo", "&#x0002E;"), ("mo", "&#x0002E;"), ("mo", "&#x0002E;")])),
                ]
            ),
            id="issue-60-2",
        ),
        pytest.param(
            r"\frac{x + 4}{x + \frac{123 \left(\sqrt{x} + 5\right)}{x + 4} - 8}",
            {
                "mfrac": MultiDict(
                    [
                        ("mrow", MultiDict([("mi", "x"), ("mo", "&#x0002B;"), ("mn", "4")])),
                        (
                            "mrow",
                            MultiDict(
                                [
                                    ("mi", "x"),
                                    ("mo", "&#x0002B;"),
                                    (
                                        "mfrac",
                                        MultiDict(
                                            [
                                                (
                                                    "mrow",
                                                    MultiDict(
                                                        [
                                                            ("mn", "123"),
                                                            (
                                                                "mrow",
                                                                MultiDict(
                                                                    [
                                                                        (
                                                                            "mo",
                                                                            {
                                                                                "@stretchy": "true",
                                                                                "@fence": "true",
                                                                                "@form": "prefix",
                                                                                "$": "&#x00028;",
                                                                            },
                                                                        ),
                                                                        ("msqrt", {"mrow": {"mi": "x"}}),
                                                                        ("mo", "&#x0002B;"),
                                                                        ("mn", "5"),
                                                                        (
                                                                            "mo",
                                                                            {
                                                                                "@stretchy": "true",
                                                                                "@fence": "true",
                                                                                "@form": "postfix",
                                                                                "$": "&#x00029;",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                            ),
                                                        ]
                                                    ),
                                                ),
                                                ("mrow", MultiDict([("mi", "x"), ("mo", "&#x0002B;"), ("mn", "4")])),
                                            ]
                                        ),
                                    ),
                                    ("mo", "&#x02212;"),
                                    ("mn", "8"),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="issue-61",
        ),
        pytest.param(
            r"\sqrt {\sqrt {\left( x^{3}\right) + v}}",
            {
                "msqrt": {
                    "mrow": {
                        "msqrt": {
                            "mrow": MultiDict(
                                [
                                    (
                                        "mrow",
                                        MultiDict(
                                            [
                                                (
                                                    "mo",
                                                    {
                                                        "@stretchy": "true",
                                                        "@fence": "true",
                                                        "@form": "prefix",
                                                        "$": "&#x00028;",
                                                    },
                                                ),
                                                ("msup", MultiDict([("mi", "x"), ("mrow", {"mn": 3})])),
                                                (
                                                    "mo",
                                                    {
                                                        "@stretchy": "true",
                                                        "@fence": "true",
                                                        "@form": "postfix",
                                                        "$": "&#x00029;",
                                                    },
                                                ),
                                            ]
                                        ),
                                    ),
                                    ("mo", "&#x0002B;"),
                                    ("mi", "v"),
                                ]
                            ),
                        }
                    }
                }
            },
            id="issue-63",
        ),
        pytest.param(r"1_{}", {"msub": MultiDict([("mn", "1"), ("mrow", {})])}, id="empty-subscript"),
        pytest.param(
            r"\begin{Bmatrix}\end{Bmatrix}",
            MultiDict([("mo", "&#x0007B;"), ("mtable", {}), ("mo", "&#x0007D;")]),
            id="Bmatrix",
        ),
        pytest.param(
            r"\begin{vmatrix}\end{vmatrix}",
            MultiDict([("mo", "&#x0007C;"), ("mtable", {}), ("mo", "&#x0007C;")]),
            id="vmatrix",
        ),
        pytest.param(
            r"\begin{Vmatrix}\end{Vmatrix}",
            MultiDict([("mo", "&#x02016;"), ("mtable", {}), ("mo", "&#x02016;")]),
            id=r"Vmatrix",
        ),
        pytest.param(
            r"\begin{matrix}1^2\end{matrix}",
            {"mtable": {"mtr": {"mtd": {"msup": MultiDict([("mn", "1"), ("mn", "2")])}}}},
            id="command-inside-matrix",
        ),
        pytest.param(r"\e", {"mi": r"\e"}, id=r"\e"),
        pytest.param(
            r"\left[\begin{matrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{matrix}\right]",
            {
                "mrow": MultiDict(
                    [
                        ("mo", {"@stretchy": "true", "@fence": "true", "@form": "prefix", "$": "["}),
                        (
                            "mtable",
                            MultiDict(
                                [
                                    (
                                        "mtr",
                                        MultiDict(
                                            [
                                                ("mtd", {"mn": "1"}),
                                                ("mtd", {"mn": "0"}),
                                                ("mtd", {"mn": "0"}),
                                                ("mtd", {"mn": "0"}),
                                            ]
                                        ),
                                    ),
                                    (
                                        "mtr",
                                        MultiDict(
                                            [
                                                ("mtd", {"mn": "0"}),
                                                ("mtd", {"mn": "1"}),
                                                ("mtd", {"mn": "0"}),
                                                ("mtd", {"mn": "0"}),
                                            ]
                                        ),
                                    ),
                                    (
                                        "mtr",
                                        MultiDict(
                                            [
                                                ("mtd", {"mn": "0"}),
                                                ("mtd", {"mn": "0"}),
                                                ("mtd", {"mn": "1"}),
                                                ("mtd", {"mn": "0"}),
                                            ]
                                        ),
                                    ),
                                    (
                                        "mtr",
                                        MultiDict(
                                            [
                                                ("mtd", {"mn": "0"}),
                                                ("mtd", {"mn": "0"}),
                                                ("mtd", {"mn": "0"}),
                                                ("mtd", {"mn": "1"}),
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                        ("mo", {"@stretchy": "true", "@fence": "true", "@form": "postfix", "$": "]"}),
                    ]
                )
            },
            id="issue-77",
        ),
        pytest.param(r"\log{x}", MultiDict([("mi", "log"), ("mrow", {"mi": "x"})]), id="logarithm"),
        pytest.param(
            r"\log_2{x}",
            MultiDict([("msub", MultiDict([("mi", "log"), ("mn", "2")])), ("mrow", {"mi": "x"})]),
            id="logarithm-with-base",
        ),
        pytest.param("^3", {"msup": MultiDict([("mi", ""), ("mn", "3")])}, id="exponent-without-base-works"),
        pytest.param(
            r"\lim_{x \to +\infty} f(x)",
            MultiDict(
                [
                    (
                        "munder",
                        MultiDict(
                            [
                                ("mo", "lim"),
                                (
                                    "mrow",
                                    MultiDict(
                                        [("mi", "x"), ("mo", "&#x02192;"), ("mo", "&#x0002B;"), ("mo", "&#x0221E;")]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("mi", "f"),
                    ("mo", {"$": "&#x00028;", "@stretchy": "false"}),
                    ("mi", "x"),
                    ("mo", {"$": "&#x00029;", "@stretchy": "false"}),
                ]
            ),
            id="limit-at-plus-infinity",
        ),
        pytest.param(
            r"\inf_{x > s}f(x)",
            MultiDict(
                [
                    (
                        "munder",
                        MultiDict(
                            [("mo", "inf"), ("mrow", MultiDict([("mi", "x"), ("mo", "&#x0003E;"), ("mi", "s")]))]
                        ),
                    ),
                    ("mi", "f"),
                    ("mo", {"$": "&#x00028;", "@stretchy": "false"}),
                    ("mi", "x"),
                    ("mo", {"$": "&#x00029;", "@stretchy": "false"}),
                ]
            ),
            id="inf",
        ),
        pytest.param(
            r"\int\limits_{0}^{\pi}",
            {"munderover": MultiDict([("mo", "&#x0222B;"), ("mrow", {"mn": "0"}), ("mrow", {"mi": "&#x003C0;"})])},
            id="issue-76",
        ),
        pytest.param(
            r"\substack{ \xi{2}=g{\left(x \right)}}",
            {
                "mstyle": {
                    "@scriptlevel": "1",
                    "mtable": {
                        "mtr": {
                            "mtd": MultiDict(
                                [
                                    ("mi", "&#x003BE;"),
                                    ("mrow", {"mn": "2"}),
                                    ("mo", "&#x0003D;"),
                                    ("mi", "g"),
                                    (
                                        "mrow",
                                        {
                                            "mrow": MultiDict(
                                                [
                                                    (
                                                        "mo",
                                                        {
                                                            "@stretchy": "true",
                                                            "@fence": "true",
                                                            "@form": "prefix",
                                                            "$": "&#x00028;",
                                                        },
                                                    ),
                                                    ("mi", "x"),
                                                    (
                                                        "mo",
                                                        {
                                                            "@stretchy": "true",
                                                            "@fence": "true",
                                                            "@form": "postfix",
                                                            "$": "&#x00029;",
                                                        },
                                                    ),
                                                ]
                                            ),
                                        },
                                    ),
                                ]
                            )
                        }
                    },
                }
            },
            id="issue-75-1-row",
        ),
        pytest.param(
            r"\sum_{\substack{1\le i\le n\\ i\ne j}}",
            {
                "munder": MultiDict(
                    [
                        ("mo", "&#x02211;"),
                        (
                            "mrow",
                            {
                                "mstyle": {
                                    "@scriptlevel": "1",
                                    "mtable": MultiDict(
                                        [
                                            (
                                                "mtr",
                                                {
                                                    "mtd": MultiDict(
                                                        [
                                                            ("mn", "1"),
                                                            ("mo", "&#x02264;"),
                                                            ("mi", "i"),
                                                            ("mo", "&#x02264;"),
                                                            ("mi", "n"),
                                                        ]
                                                    )
                                                },
                                            ),
                                            (
                                                "mtr",
                                                {"mtd": MultiDict([("mi", "i"), ("mo", "&#x02260;"), ("mi", "j")])},
                                            ),
                                        ]
                                    ),
                                }
                            },
                        ),
                    ]
                )
            },
            id="issue-75-2-rows",
        ),
        pytest.param(
            r"\tan x+\sec x+\cos x+\sin x+\cot x+\csc x+\arccos x+\arcsin x+\arctan x +\cosh x+\coth x",
            MultiDict(
                [
                    ("mi", "tan"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "sec"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "cos"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "sin"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "cot"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "csc"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "arccos"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "arcsin"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "arctan"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "cosh"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "coth"),
                    ("mi", "x"),
                ]
            ),
            id="issue-91",
        ),
        pytest.param(r"p_{\max}", {"msub": MultiDict([("mi", "p"), ("mrow", {"mo": "max"})])}, id="issue-98"),
        pytest.param(
            r"\overrightarrow {a}",
            {"mover": MultiDict([("mrow", {"mi": "a"}), ("mo", {"@stretchy": "true", "$": "&#x02192;"})])},
            id="issue-100",
        ),
        pytest.param(
            r"\vec{AB}",
            {
                "mover": MultiDict(
                    [("mrow", MultiDict([("mi", "A"), ("mi", "B")])), ("mo", {"@stretchy": "true", "$": "&#x02192;"})]
                )
            },
            id="issue-103",
        ),
        pytest.param(
            r"\begin{cases} {x=1} \\ {y=-2}\end{cases}",
            MultiDict(
                [
                    ("mo", {"@stretchy": "true", "@fence": "true", "@form": "prefix", "$": "&#x0007B;"}),
                    (
                        "mtable",
                        MultiDict(
                            [
                                (
                                    "mtr",
                                    {
                                        "mtd": MultiDict(
                                            [
                                                ("@columnalign", "left"),
                                                ("mrow", MultiDict([("mi", "x"), ("mo", "&#x0003D;"), ("mn", "1")])),
                                            ]
                                        )
                                    },
                                ),
                                (
                                    "mtr",
                                    {
                                        "mtd": MultiDict(
                                            [
                                                ("@columnalign", "left"),
                                                (
                                                    "mrow",
                                                    MultiDict(
                                                        [
                                                            ("mi", "y"),
                                                            ("mo", "&#x0003D;"),
                                                            ("mo", "&#x02212;"),
                                                            ("mn", "2"),
                                                        ]
                                                    ),
                                                ),
                                            ]
                                        )
                                    },
                                ),
                            ]
                        ),
                    ),
                ]
            ),
            id="issue-106",
        ),
        pytest.param(r"\max f", MultiDict([("mo", "max"), ("mi", "f")]), id="issue-108-1"),
        pytest.param(
            r"\max \{a, b, c\}",
            MultiDict(
                [
                    ("mo", "max"),
                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                    ("mi", "a"),
                    ("mo", "&#x0002C;"),
                    ("mi", "b"),
                    ("mo", "&#x0002C;"),
                    ("mi", "c"),
                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                ]
            ),
            id="issue-108-2",
        ),
        pytest.param(
            r"\min{(x, y)}",
            MultiDict(
                [
                    ("mo", "min"),
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@stretchy": "false", "$": "&#x00028;"}),
                                ("mi", "x"),
                                ("mo", "&#x0002C;"),
                                ("mi", "y"),
                                ("mo", {"@stretchy": "false", "$": "&#x00029;"}),
                            ]
                        ),
                    ),
                ]
            ),
            id="issue-108-3",
        ),
        pytest.param(r"\dot A", {"mover": MultiDict([("mi", "A"), ("mo", "&#x002D9;")])}, id="issue-112-1"),
        pytest.param(
            r"\dot{A}",
            {"mover": MultiDict([("mrow", MultiDict([("mi", "A")])), ("mo", "&#x002D9;")])},
            id="issue-112-2",
        ),
        pytest.param(r"\operatorname{sn}x", MultiDict([("mi", "sn"), ("mi", "x")]), id="issue-109-1"),
        pytest.param(
            r"\operatorname{sn}(x+y)",
            MultiDict(
                [
                    ("mi", "sn"),
                    ("mo", {"@stretchy": "false", "$": "&#x00028;"}),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "y"),
                    ("mo", {"@stretchy": "false", "$": "&#x00029;"}),
                ]
            ),
            id="issue-109-2",
        ),
        pytest.param(
            r"\text{Let}\ x=\text{number of cats}.",
            MultiDict(
                [
                    ("mtext", "Let"),
                    ("mtext", "&#x000A0;"),
                    ("mi", "x"),
                    ("mo", "&#x0003D;"),
                    ("mtext", "number&#x000A0;of&#x000A0;cats"),
                    ("mo", "&#x0002E;"),
                ]
            ),
            id="issue-118",
        ),
        pytest.param(
            r"F(a,n)=\overset{a-a-a\cdots-a}{}ntext{个}a",
            MultiDict(
                [
                    ("mi", "F"),
                    ("mo", {"@stretchy": "false", "$": "&#x00028;"}),
                    ("mi", "a"),
                    ("mo", "&#x0002C;"),
                    ("mi", "n"),
                    ("mo", {"@stretchy": "false", "$": "&#x00029;"}),
                    ("mo", "&#x0003D;"),
                    (
                        "mover",
                        MultiDict(
                            [
                                ("mrow", ""),
                                (
                                    "mrow",
                                    MultiDict(
                                        [
                                            ("mi", "a"),
                                            ("mo", "&#x02212;"),
                                            ("mi", "a"),
                                            ("mo", "&#x02212;"),
                                            ("mi", "a"),
                                            ("mo", "&#x022EF;"),
                                            ("mo", "&#x02212;"),
                                            ("mi", "a"),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("mi", "n"),
                    ("mi", "t"),
                    ("mi", "e"),
                    ("mi", "x"),
                    ("mi", "t"),
                    ("mrow", {"mi": "个"}),
                    ("mi", "a"),
                ]
            ),
            id="issue-125-1-overset",
        ),
        pytest.param(
            r"a\,\overset{?}{=}\,b",
            MultiDict(
                [
                    ("mi", "a"),
                    ("mspace", {"@width": "0.167em"}),
                    ("mover", MultiDict([("mrow", {"mo": "&#x0003D;"}), ("mrow", {"mo": "&#x0003F;"})])),
                    ("mspace", {"@width": "0.167em"}),
                    ("mi", "b"),
                ]
            ),
            id="issue-125-2-overset",
        ),
        pytest.param(r"\underset ab", {"munder": MultiDict([("mi", "b"), ("mi", "a")])}, id="issue-125-3-underset"),
        pytest.param(
            r"a\mathop{t}b\mathop{t}c",
            MultiDict([("mi", "a"), ("mrow", {"mi": "t"}), ("mi", "b"), ("mrow", {"mi": "t"}), ("mi", "c")]),
            id="issue-125-4-mathop",
        ),
        pytest.param(
            r"\mathop{x}\limits_0^1",
            {"munderover": MultiDict([("mrow", {"mi": "x"}), ("mn", "0"), ("mn", "1")])},
            id="issue-125-4-limits",
        ),
        pytest.param(
            r"\Bigg[\bigg[\Big[\big[[",
            MultiDict(
                [
                    ("mo", {"@minsize": "2.470em", "@maxsize": "2.470em", "$": "["}),
                    ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "["}),
                    ("mo", {"@minsize": "1.623em", "@maxsize": "1.623em", "$": "["}),
                    ("mo", {"@minsize": "1.2em", "@maxsize": "1.2em", "$": "["}),
                    ("mo", {"@stretchy": "false", "$": "["}),
                ]
            ),
            id="big",
        ),
        pytest.param(
            r"x\rm {\text{var} = 1+\{b\}}\sf \Delta",
            MultiDict(
                [
                    ("mi", "x"),
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mtext", "var"),
                                ("mo", "&#x0003D;"),
                                ("mn", "1"),
                                ("mo", "&#x0002B;"),
                                ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                ("mi", {"@mathvariant": "normal", "$": "b"}),
                                ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                            ]
                        ),
                    ),
                    ("mi", {"@mathvariant": "sans-serif", "$": "&#x00394;"}),
                ]
            ),
            id="global-fonts",
        ),
        pytest.param(
            "f'(x) = 2x, f''(x) = 2",
            MultiDict(
                [
                    ("msup", MultiDict([("mi", "f"), ("mi", "&#x02032;")])),
                    ("mo", {"$": "&#x00028;", "@stretchy": "false"}),
                    ("mi", "x"),
                    ("mo", {"$": "&#x00029;", "@stretchy": "false"}),
                    ("mo", "&#x0003D;"),
                    ("mn", "2"),
                    ("mi", "x"),
                    ("mo", "&#x0002C;"),
                    ("msup", MultiDict([("mi", "f"), ("mi", "&#x02033;")])),
                    ("mo", {"$": "&#x00028;", "@stretchy": "false"}),
                    ("mi", "x"),
                    ("mo", {"$": "&#x00029;", "@stretchy": "false"}),
                    ("mo", "&#x0003D;"),
                    ("mn", "2"),
                ]
            ),
            id="prime",
        ),
        pytest.param(
            "'x",
            MultiDict([("msup", MultiDict([("mi", ""), ("mi", "&#x02032;")])), ("mi", "x")]),
            id="prime-no-base",
        ),
        pytest.param(
            r"""|\,|\:|\>|\;|\\|\!|\quad|\qquad|\hspace1em|\hspace{10ex}|\enspace|\hskip1em|\kern-1.5pt|\mskip18mu|
            \mspace18mu|\negthinspace|\negmedspace|\negthickspace|\nobreakspace|\space|\thinspace|""",
            MultiDict(
                [
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "0.167em"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "0.222em"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "0.222em"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "0.278em"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@linebreak": "newline"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "negativethinmathspace"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "1em"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "2em"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "1em"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "10ex"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "0.5em"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "1em"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "-1.5pt"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "18mu"}),  # TODO: convert to em?
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "18mu"}),  # TODO: convert to em?
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "negativethinmathspace"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "negativemediummathspace"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "negativethickmathspace"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mtext", "&#x000A0;"),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mtext", "&#x000A0;"),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mspace", {"@width": "thinmathspace"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                ]
            ),
            id="spaces",
        ),
        pytest.param(
            r"|x|",
            MultiDict(
                [
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                    ("mi", "x"),
                    ("mo", {"@stretchy": "false", "$": "&#x0007C;"}),
                ]
            ),
            id="pipe",
        ),
        pytest.param(
            r"\|x\|",
            MultiDict(
                [
                    ("mo", {"@fence": "false", "@stretchy": "false", "$": "&#x02016;"}),
                    ("mi", "x"),
                    ("mo", {"@fence": "false", "@stretchy": "false", "$": "&#x02016;"}),
                ]
            ),
            id="double-pipe",
        ),
        pytest.param(
            "Hello~World",
            MultiDict(
                [
                    ("mi", "H"),
                    ("mi", "e"),
                    ("mi", "l"),
                    ("mi", "l"),
                    ("mi", "o"),
                    ("mtext", "&#x000A0;"),
                    ("mi", "W"),
                    ("mi", "o"),
                    ("mi", "r"),
                    ("mi", "l"),
                    ("mi", "d"),
                ]
            ),
            id="tilde",
        ),
        pytest.param(r"\text{ Hello~World }", {"mtext": "&#x000A0;Hello~World&#x000A0;"}, id="tilde-and-space-in-text"),
        pytest.param(
            r"""% this is hidden
            100\%!% this is hidden, too""",
            MultiDict([("mn", "100"), ("mi", "&#x00025;"), ("mo", "&#x00021;")]),
            id="comments",
        ),
        pytest.param(
            r"\#\$\%\&\_\{\}",
            MultiDict(
                [
                    ("mi", "&#x00023;"),
                    ("mi", "&#x00024;"),
                    ("mi", "&#x00025;"),
                    ("mi", "&#x00026;"),
                    ("mi", "&#x0005F;"),
                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                ]
            ),
            id="escaped-characters",
        ),
        pytest.param(
            r"{a \above 1pt b} + {c \above {1.5pt} d}",
            MultiDict(
                [
                    ("mrow", {"mfrac": MultiDict([("@linethickness", "1pt"), ("mi", "a"), ("mi", "b")])}),
                    ("mo", "&#x0002B;"),
                    ("mrow", {"mfrac": MultiDict([("@linethickness", "1.5pt"), ("mi", "c"), ("mi", "d")])}),
                ]
            ),
            id="above",
        ),
        pytest.param(
            r"\acute a \acute{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x000B4;")]),
                    ),
                    (
                        "mover",
                        MultiDict(
                            [
                                (
                                    "mrow",
                                    MultiDict(
                                        [
                                            ("mi", "b"),
                                            ("mi", "c"),
                                        ]
                                    ),
                                ),
                                ("mo", "&#x000B4;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="acute",
        ),
        pytest.param(
            r"a \atop {b \atopwithdelims | \} c}",
            {
                "mfrac": MultiDict(
                    [
                        ("@linethickness", "0"),
                        ("mi", "a"),
                        (
                            "mrow",
                            MultiDict(
                                [
                                    ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "&#x0007C;"}),
                                    (
                                        "mfrac",
                                        MultiDict(
                                            [
                                                ("@linethickness", "0"),
                                                ("mi", "b"),
                                                ("mi", "c"),
                                            ]
                                        ),
                                    ),
                                    ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "}"}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="atop-and-atopwithdelims",
        ),
        pytest.param(
            r"{a \abovewithdelims [ ] 1pt b} + {c \abovewithdelims . . {1.5pt} d}",
            MultiDict(
                [
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "["}),
                                (
                                    "mfrac",
                                    MultiDict(
                                        [
                                            ("@linethickness", "1pt"),
                                            ("mi", "a"),
                                            ("mi", "b"),
                                        ]
                                    ),
                                ),
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "]"}),
                            ]
                        ),
                    ),
                    ("mo", "&#x0002B;"),
                    (
                        "mrow",
                        {
                            "mfrac": MultiDict(
                                [
                                    ("@linethickness", "1.5pt"),
                                    ("mi", "c"),
                                    ("mi", "d"),
                                ]
                            ),
                        },
                    ),
                ]
            ),
            id="abovewithdelims",
        ),
        pytest.param(
            r"\Bbb {\text{var} = 1+\{b\}}",
            {
                "mrow": MultiDict(
                    [
                        ("mtext", {"@mathvariant": "double-struck", "$": "var"}),
                        ("mo", {"@mathvariant": "double-struck", "$": "&#x0003D;"}),
                        ("mn", {"@mathvariant": "double-struck", "$": "1"}),
                        ("mo", {"@mathvariant": "double-struck", "$": "&#x0002B;"}),
                        ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                        ("mi", {"@mathvariant": "double-struck", "$": "b"}),
                        ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                    ]
                )
            },
            id="blackboard-bold",
        ),
        pytest.param(
            r"\Bbb{AB}C",
            MultiDict(
                [
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mi", {"@mathvariant": "double-struck", "$": "A"}),
                                ("mi", {"@mathvariant": "double-struck", "$": "B"}),
                            ]
                        ),
                    ),
                    ("mi", "C"),
                ]
            ),
            id="Bbb-group",
        ),
        pytest.param(r"\bigcirc", {"mi": "&#x025EF;"}, id="bigcirc"),
        pytest.param(
            r"\boldsymbol {\text{var} = 1+\{b\}}",
            {
                "mrow": MultiDict(
                    [
                        ("mtext", "var"),
                        ("mo", {"@mathvariant": "bold", "$": "&#x0003D;"}),
                        ("mn", {"@mathvariant": "bold", "$": "1"}),
                        ("mo", {"@mathvariant": "bold", "$": "&#x0002B;"}),
                        ("mo", {"@stretchy": "false", "@mathvariant": "bold", "$": "&#x0007B;"}),
                        ("mi", {"@mathvariant": "bold-italic", "$": "b"}),
                        ("mo", {"@stretchy": "false", "@mathvariant": "bold", "$": "&#x0007D;"}),
                    ]
                )
            },
            id="boldsymbol",
        ),
        pytest.param(r"\boxed \Box", {"menclose": {"@notation": "box", "mi": "&#x025FB;"}}, id="boxed-box"),
        pytest.param(
            r"\breve a \breve{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x002D8;")]),
                    ),
                    (
                        "mover",
                        MultiDict(
                            [
                                (
                                    "mrow",
                                    MultiDict(
                                        [
                                            ("mi", "b"),
                                            ("mi", "c"),
                                        ]
                                    ),
                                ),
                                ("mo", "&#x002D8;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="breve",
        ),
        pytest.param(
            r"{\brace} + {a \brace b}",
            MultiDict(
                [
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "{"}),
                                ("mfrac", MultiDict([("@linethickness", "0"), ("mrow", ""), ("mrow", "")])),
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "}"}),
                            ]
                        ),
                    ),
                    ("mo", "&#x0002B;"),
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "{"}),
                                ("mfrac", MultiDict([("@linethickness", "0"), ("mi", "a"), ("mi", "b")])),
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "}"}),
                            ]
                        ),
                    ),
                ]
            ),
            id="brace",
        ),
        pytest.param(
            r"{\brack} + {a \brack b}",
            MultiDict(
                [
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "["}),
                                ("mfrac", MultiDict([("@linethickness", "0"), ("mrow", ""), ("mrow", "")])),
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "]"}),
                            ]
                        ),
                    ),
                    ("mo", "&#x0002B;"),
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "["}),
                                ("mfrac", MultiDict([("@linethickness", "0"), ("mi", "a"), ("mi", "b")])),
                                ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "]"}),
                            ]
                        ),
                    ),
                ]
            ),
            id="brace",
        ),
        pytest.param(
            r"{\cal {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", {"@mathvariant": "script", "$": "var"}),
                                    ("mo", {"@mathvariant": "script", "$": "&#x0003D;"}),
                                    ("mn", {"@mathvariant": "script", "$": "1"}),
                                    ("mo", {"@mathvariant": "script", "$": "&#x0002B;"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                    ("mi", {"@mathvariant": "script", "$": "b"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="calligraphic-mode",
        ),
        pytest.param(r"a\centerdot b", MultiDict([("mi", "a"), ("mo", "&#x02B1D;"), ("mi", "b")]), id="centerdot"),
        pytest.param(
            r"\cfrac{2}{1+ \cfrac{2}{1}}",
            {
                "mfrac": MultiDict(
                    [
                        ("mstyle", {"@displaystyle": "false", "@scriptlevel": "0", "mrow": {"mn": "2"}}),
                        (
                            "mstyle",
                            {
                                "@displaystyle": "false",
                                "@scriptlevel": "0",
                                "mrow": MultiDict(
                                    [
                                        ("mn", "1"),
                                        ("mo", "&#x0002B;"),
                                        (
                                            "mfrac",
                                            MultiDict(
                                                [
                                                    (
                                                        "mstyle",
                                                        {
                                                            "@displaystyle": "false",
                                                            "@scriptlevel": "0",
                                                            "mrow": {"mn": "2"},
                                                        },
                                                    ),
                                                    (
                                                        "mstyle",
                                                        {
                                                            "@displaystyle": "false",
                                                            "@scriptlevel": "0",
                                                            "mrow": {"mn": "1"},
                                                        },
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            },
                        ),
                    ]
                )
            },
            id="cfrac",
        ),
        pytest.param(
            r"\check a \check{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x002C7;")]),
                    ),
                    (
                        "mover",
                        MultiDict(
                            [
                                (
                                    "mrow",
                                    MultiDict(
                                        [
                                            ("mi", "b"),
                                            ("mi", "c"),
                                        ]
                                    ),
                                ),
                                ("mo", "&#x002C7;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="check",
        ),
        pytest.param(
            r"a \choose b",
            MultiDict(
                [
                    ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "&#x00028;"}),
                    ("mfrac", MultiDict([("@linethickness", "0"), ("mi", "a"), ("mi", "b")])),
                    ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "&#x00029;"}),
                ]
            ),
            id="choose",
        ),
        pytest.param(r"\circledS", {"mi": "&#x024C8;"}, id="circledS"),
        pytest.param(
            r"{a\color{red}bc}d",
            MultiDict(
                [
                    (
                        "mrow",
                        MultiDict(
                            [("mi", "a"), ("mstyle", MultiDict([("@mathcolor", "red"), ("mi", "b"), ("mi", "c")]))]
                        ),
                    ),
                    ("mi", "d"),
                ]
            ),
            id="color",
        ),
        pytest.param(
            r"\color{}ab",
            MultiDict([("mstyle", MultiDict([("@mathcolor", ""), ("mi", "a"), ("mi", "b")]))]),
            id="empty-color-works",
        ),
        pytest.param(
            r"\dbinom a b",
            {
                "mstyle": MultiDict(
                    [
                        ("@displaystyle", "true"),
                        ("@scriptlevel", "0"),
                        ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "&#x00028;"}),
                        ("mfrac", MultiDict([("@linethickness", "0"), ("mi", "a"), ("mi", "b")])),
                        ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "&#x00029;"}),
                    ]
                )
            },
            id="binomial-coefficients",
        ),
        pytest.param(
            r"\ddot a \dddot b \ddddot c",
            MultiDict(
                [
                    ("mover", MultiDict([("mi", "a"), ("mo", "&#x000A8;")])),
                    ("mover", MultiDict([("mi", "b"), ("mo", "&#x020DB;")])),
                    ("mover", MultiDict([("mi", "c"), ("mo", "&#x020DC;")])),
                ]
            ),
            id="ddot-dddot-ddddot",
        ),
        pytest.param(
            r"\deg(f(x))",
            MultiDict(
                [
                    ("mi", "deg"),
                    ("mo", {"@stretchy": "false", "$": "&#x00028;"}),
                    ("mi", "f"),
                    ("mo", {"@stretchy": "false", "$": "&#x00028;"}),
                    ("mi", "x"),
                    ("mo", {"@stretchy": "false", "$": "&#x00029;"}),
                    ("mo", {"@stretchy": "false", "$": "&#x00029;"}),
                ]
            ),
            id="degree-polynomial",
        ),
        pytest.param(
            r"\det(A)",
            MultiDict(
                [
                    ("mo", {"@movablelimits": "true", "$": "det"}),
                    ("mo", {"@stretchy": "false", "$": "&#x00028;"}),
                    ("mi", "A"),
                    ("mo", {"@stretchy": "false", "$": "&#x00029;"}),
                ]
            ),
            id="determinant",
        ),
        pytest.param(
            r"\dim(A)",
            MultiDict(
                [
                    ("mi", "dim"),
                    ("mo", {"@stretchy": "false", "$": "&#x00028;"}),
                    ("mi", "A"),
                    ("mo", {"@stretchy": "false", "$": "&#x00029;"}),
                ]
            ),
            id="dimension-vector-space",
        ),
        pytest.param(
            r"\dfrac a b",
            {"mstyle": {"@displaystyle": "true", "@scriptlevel": "0", "mfrac": MultiDict([("mi", "a"), ("mi", "b")])}},
            id="dfrac",
        ),
        pytest.param(r"\diagdown \diagup", MultiDict([("mi", "&#x02572;"), ("mi", "&#x02571;")]), id="diagdown-diagup"),
        pytest.param(
            r"x_1, \dots, x_n",
            MultiDict(
                [
                    ("msub", MultiDict([("mi", "x"), ("mn", "1")])),
                    ("mo", "&#x0002C;"),
                    ("mo", "&#x02026;"),
                    ("mo", "&#x0002C;"),
                    ("msub", MultiDict([("mi", "x"), ("mi", "n")])),
                ]
            ),
            id="dots",
        ),
        pytest.param(
            r"x_1 + \dotsb + x_n",
            MultiDict(
                [
                    ("msub", MultiDict([("mi", "x"), ("mn", "1")])),
                    ("mo", "&#x0002B;"),
                    ("mo", "&#x022EF;"),
                    ("mo", "&#x0002B;"),
                    ("msub", MultiDict([("mi", "x"), ("mi", "n")])),
                ]
            ),
            id="dotsb",
        ),
        pytest.param(
            r"x_1, \dotsc, x_n",
            MultiDict(
                [
                    ("msub", MultiDict([("mi", "x"), ("mn", "1")])),
                    ("mo", "&#x0002C;"),
                    ("mo", "&#x02026;"),
                    ("mo", "&#x0002C;"),
                    ("msub", MultiDict([("mi", "x"), ("mi", "n")])),
                ]
            ),
            id="dotsc",
        ),
        pytest.param(
            r"A_1 \dotsi A_n",
            MultiDict(
                [
                    ("msub", MultiDict([("mi", "A"), ("mn", "1")])),
                    ("mo", "&#x022EF;"),
                    ("msub", MultiDict([("mi", "A"), ("mi", "n")])),
                ]
            ),
            id="dotsi",
        ),
        pytest.param(
            r"x_1 \dotsm x_n",
            MultiDict(
                [
                    ("msub", MultiDict([("mi", "x"), ("mn", "1")])),
                    ("mo", "&#x022EF;"),
                    ("msub", MultiDict([("mi", "x"), ("mi", "n")])),
                ]
            ),
            id="dotsm",
        ),
        pytest.param(
            r"A_1 \dotso A_n",
            MultiDict(
                [
                    ("msub", MultiDict([("mi", "A"), ("mn", "1")])),
                    ("mo", "&#x02026;"),
                    ("msub", MultiDict([("mi", "A"), ("mi", "n")])),
                ]
            ),
            id="dotso",
        ),
        pytest.param(
            r"\frac ab + {\displaystyle \frac cd + \frac ef} + \frac gh",
            MultiDict(
                [
                    ("mfrac", MultiDict([("mi", "a"), ("mi", "b")])),
                    ("mo", "&#x0002B;"),
                    (
                        "mrow",
                        {
                            "mstyle": MultiDict(
                                [
                                    ("@displaystyle", "true"),
                                    ("@scriptlevel", "0"),
                                    ("mfrac", MultiDict([("mi", "c"), ("mi", "d")])),
                                    ("mo", "&#x0002B;"),
                                    ("mfrac", MultiDict([("mi", "e"), ("mi", "f")])),
                                ]
                            )
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mfrac", MultiDict([("mi", "g"), ("mi", "h")])),
                ]
            ),
            id="displaystyle",
        ),
        pytest.param(
            r"\frac ab+\displaystyle\frac cd+\textstyle\frac ef+\scriptstyle\frac gh+\scriptscriptstyle\frac ij",
            MultiDict(
                [
                    ("mfrac", MultiDict([("mi", "a"), ("mi", "b")])),
                    ("mo", "&#x0002B;"),
                    (
                        "mstyle",
                        MultiDict(
                            [
                                ("@displaystyle", "true"),
                                ("@scriptlevel", "0"),
                                ("mfrac", MultiDict([("mi", "c"), ("mi", "d")])),
                                ("mo", "&#x0002B;"),
                                (
                                    "mstyle",
                                    MultiDict(
                                        [
                                            ("@displaystyle", "false"),
                                            ("@scriptlevel", "0"),
                                            ("mfrac", MultiDict([("mi", "e"), ("mi", "f")])),
                                            ("mo", "&#x0002B;"),
                                            (
                                                "mstyle",
                                                MultiDict(
                                                    [
                                                        ("@displaystyle", "false"),
                                                        ("@scriptlevel", "1"),
                                                        ("mfrac", MultiDict([("mi", "g"), ("mi", "h")])),
                                                        ("mo", "&#x0002B;"),
                                                        (
                                                            "mstyle",
                                                            MultiDict(
                                                                [
                                                                    ("@displaystyle", "false"),
                                                                    ("@scriptlevel", "2"),
                                                                    ("mfrac", MultiDict([("mi", "i"), ("mi", "j")])),
                                                                ]
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                ]
            ),
            id="styles",
        ),
        pytest.param(
            r"""
            \displaylines{
                a = a\cr
                \text{if } a=b \text{ then } b=a\\
                \text{if } a=b \text{ and } b=c \text{ then } a=c
            }
            """,
            {
                "mtable": MultiDict(
                    [
                        ("@rowspacing", "0.5em"),
                        ("@columnspacing", "1em"),
                        ("@displaystyle", "true"),
                        ("mtr", {"mtd": MultiDict([("mi", "a"), ("mo", "&#x0003D;"), ("mi", "a")])}),
                        (
                            "mtr",
                            {
                                "mtd": MultiDict(
                                    [
                                        ("mtext", "if&#x000A0;"),
                                        ("mi", "a"),
                                        ("mo", "&#x0003D;"),
                                        ("mi", "b"),
                                        ("mtext", "&#x000A0;then&#x000A0;"),
                                        ("mi", "b"),
                                        ("mo", "&#x0003D;"),
                                        ("mi", "a"),
                                    ]
                                )
                            },
                        ),
                        (
                            "mtr",
                            {
                                "mtd": MultiDict(
                                    [
                                        ("mtext", "if&#x000A0;"),
                                        ("mi", "a"),
                                        ("mo", "&#x0003D;"),
                                        ("mi", "b"),
                                        ("mtext", "&#x000A0;and&#x000A0;"),
                                        ("mi", "b"),
                                        ("mo", "&#x0003D;"),
                                        ("mi", "c"),
                                        ("mtext", "&#x000A0;then&#x000A0;"),
                                        ("mi", "a"),
                                        ("mo", "&#x0003D;"),
                                        ("mi", "c"),
                                    ]
                                )
                            },
                        ),
                    ]
                )
            },
            id="displaylines",
        ),
        pytest.param(r"\emptyset", {"mo": "&#x02205;"}, id="emptyset"),
        pytest.param(r"\exp x", MultiDict([("mi", "exp"), ("mi", "x")]), id="exponential-function"),
        pytest.param(
            r"\fbox{ Hello! }", {"menclose": {"@notation": "box", "mtext": "&#x000A0;Hello!&#x000A0;"}}, id="fbox"
        ),
        pytest.param(
            r"{\frak {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", {"@mathvariant": "fraktur", "$": "var"}),
                                    ("mo", {"@mathvariant": "fraktur", "$": "&#x0003D;"}),
                                    ("mn", {"@mathvariant": "fraktur", "$": "1"}),
                                    ("mo", {"@mathvariant": "fraktur", "$": "&#x0002B;"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                    ("mi", {"@mathvariant": "fraktur", "$": "b"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="fraktur",
        ),
        pytest.param(
            r"\gcd_{\rm sub}^{\rm sup}",
            {
                "munderover": MultiDict(
                    [
                        ("mo", {"@movablelimits": "true", "$": "gcd"}),
                        (
                            "mrow",
                            MultiDict(
                                [
                                    ("mi", {"@mathvariant": "normal", "$": "s"}),
                                    ("mi", {"@mathvariant": "normal", "$": "u"}),
                                    ("mi", {"@mathvariant": "normal", "$": "b"}),
                                ]
                            ),
                        ),
                        (
                            "mrow",
                            MultiDict(
                                [
                                    ("mi", {"@mathvariant": "normal", "$": "s"}),
                                    ("mi", {"@mathvariant": "normal", "$": "u"}),
                                    ("mi", {"@mathvariant": "normal", "$": "p"}),
                                ]
                            ),
                        ),
                    ]
                ),
            },
            id="greatest-common-divisor",
        ),
        pytest.param(
            r"\genfrac\{]{1pt}{0}{a+b}{c+d}",
            {
                "mstyle": MultiDict(
                    [
                        ("@displaystyle", "true"),
                        ("@scriptlevel", "0"),
                        ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "{"}),
                        (
                            "mfrac",
                            MultiDict(
                                [
                                    ("@linethickness", "1pt"),
                                    ("mrow", MultiDict([("mi", "a"), ("mo", "&#x0002B;"), ("mi", "b")])),
                                    ("mrow", MultiDict([("mi", "c"), ("mo", "&#x0002B;"), ("mi", "d")])),
                                ]
                            ),
                        ),
                        ("mo", {"@minsize": "2.047em", "@maxsize": "2.047em", "$": "]"}),
                    ]
                ),
            },
            id="genfrac-displaystyle",
        ),
        pytest.param(
            r"\genfrac(|{1pt}{1}{a+b}{c+d}",
            {
                "mstyle": MultiDict(
                    [
                        ("@displaystyle", "false"),
                        ("@scriptlevel", "0"),
                        ("mo", {"@minsize": "1.2em", "@maxsize": "1.2em", "$": "&#x00028;"}),
                        (
                            "mfrac",
                            MultiDict(
                                [
                                    ("@linethickness", "1pt"),
                                    ("mrow", MultiDict([("mi", "a"), ("mo", "&#x0002B;"), ("mi", "b")])),
                                    ("mrow", MultiDict([("mi", "c"), ("mo", "&#x0002B;"), ("mi", "d")])),
                                ]
                            ),
                        ),
                        ("mo", {"@minsize": "1.2em", "@maxsize": "1.2em", "$": "&#x0007C;"}),
                    ]
                ),
            },
            id="genfrac-textstyle",
        ),
        pytest.param(
            r"\genfrac(.{1pt}{2}{a+b}{c+d}",
            {
                "mstyle": MultiDict(
                    [
                        ("@displaystyle", "false"),
                        ("@scriptlevel", "1"),
                        ("mo", {"@minsize": "1.2em", "@maxsize": "1.2em", "$": "&#x00028;"}),
                        (
                            "mfrac",
                            MultiDict(
                                [
                                    ("@linethickness", "1pt"),
                                    ("mrow", MultiDict([("mi", "a"), ("mo", "&#x0002B;"), ("mi", "b")])),
                                    ("mrow", MultiDict([("mi", "c"), ("mo", "&#x0002B;"), ("mi", "d")])),
                                ]
                            ),
                        ),
                    ]
                ),
            },
            id="genfrac-scriptstyle",
        ),
        pytest.param(
            r"\genfrac\{\}{1pt}{3}{a+b}{c+d}",
            {
                "mstyle": MultiDict(
                    [
                        ("@displaystyle", "false"),
                        ("@scriptlevel", "2"),
                        ("mo", {"@minsize": "1.2em", "@maxsize": "1.2em", "$": "{"}),
                        (
                            "mfrac",
                            MultiDict(
                                [
                                    ("@linethickness", "1pt"),
                                    ("mrow", MultiDict([("mi", "a"), ("mo", "&#x0002B;"), ("mi", "b")])),
                                    ("mrow", MultiDict([("mi", "c"), ("mo", "&#x0002B;"), ("mi", "d")])),
                                ]
                            ),
                        ),
                        ("mo", {"@minsize": "1.2em", "@maxsize": "1.2em", "$": "}"}),
                    ]
                ),
            },
            id="genfrac-scriptscriptstyle",
        ),
        pytest.param(r"\gggtr", {"mo": "&#x022D9;"}, id="gggtr"),
        pytest.param(r"\gvertneqq", {"mo": "&#x02269;"}, id="gvertneqq"),
        pytest.param(r"\gt", {"mo": "&#x0003E;"}, id="gt"),
        pytest.param(
            r"\grave a \grave{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x00060;")]),
                    ),
                    (
                        "mover",
                        MultiDict(
                            [
                                (
                                    "mrow",
                                    MultiDict(
                                        [
                                            ("mi", "b"),
                                            ("mi", "c"),
                                        ]
                                    ),
                                ),
                                ("mo", "&#x00060;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="grave",
        ),
        pytest.param(
            r"\hat a \hat{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x0005E;")]),
                    ),
                    (
                        "mover",
                        MultiDict(
                            [
                                (
                                    "mrow",
                                    MultiDict(
                                        [
                                            ("mi", "b"),
                                            ("mi", "c"),
                                        ]
                                    ),
                                ),
                                ("mo", "&#x0005E;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="hat",
        ),
        pytest.param(r"\hom", {"mi": "hom"}, id="hom"),
        pytest.param(
            r"\href{https://github.com/roniemartinez/latex2mathml}{\text{latex2mathml}}",
            {"mtext": {"@href": "https://github.com/roniemartinez/latex2mathml", "mrow": {"mtext": "latex2mathml"}}},
            id="href",
        ),
        pytest.param(
            r"[{[\Huge[\huge[[}[",
            MultiDict(
                [
                    ("mo", {"@stretchy": "false", "$": "["}),
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@stretchy": "false", "$": "["}),
                                (
                                    "mstyle",
                                    MultiDict(
                                        [
                                            ("@mathsize", "2.49em"),
                                            ("mo", {"@stretchy": "false", "$": "["}),
                                            (
                                                "mstyle",
                                                MultiDict(
                                                    [
                                                        ("@mathsize", "2.07em"),
                                                        ("mo", {"@stretchy": "false", "$": "["}),
                                                        ("mo", {"@stretchy": "false", "$": "["}),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("mo", {"@stretchy": "false", "$": "["}),
                ]
            ),
            id="huge",
        ),
        pytest.param(
            r"\sqrt[abc]{123}",
            {
                "mroot": MultiDict(
                    [("mrow", {"mn": "123"}), ("mrow", MultiDict([("mi", "a"), ("mi", "b"), ("mi", "c")]))]
                )
            },
            id="sqrt-with-multiple-root-nodes",
        ),
        pytest.param(
            r"\begin{array}{l} \text{Side Angle Side}\\ \text{S}\hphantom{\text{ide }}\text{A}\hphantom{\text{ngle }}"
            r"\text{S} \end{array}",
            {
                "mtable": MultiDict(
                    [
                        (
                            "mtr",
                            {
                                "mtd": {"@columnalign": "left", "mtext": "Side&#x000A0;Angle&#x000A0;Side"},
                            },
                        ),
                        (
                            "mtr",
                            {
                                "mtd": MultiDict(
                                    [
                                        ("@columnalign", "left"),
                                        ("mtext", "S"),
                                        (
                                            "mpadded",
                                            {
                                                "@height": "0",
                                                "@depth": "0",
                                                "mphantom": {"mrow": {"mtext": "ide&#x000A0;"}},
                                            },
                                        ),
                                        ("mtext", "A"),
                                        (
                                            "mpadded",
                                            {
                                                "@height": "0",
                                                "@depth": "0",
                                                "mphantom": {"mrow": {"mtext": "ngle&#x000A0;"}},
                                            },
                                        ),
                                        ("mtext", "S"),
                                    ]
                                )
                            },
                        ),
                    ]
                )
            },
            id="hphantom",
        ),
        pytest.param(
            r"\idotsint", MultiDict([("mo", "&#x0222B;"), ("mo", "&#x022EF;"), ("mo", "&#x0222B;")]), id="idotsint"
        ),
        pytest.param(r"\intop", {"mo": {"@movablelimits": "true", "$": "&#x0222B;"}}, id="intop"),
        pytest.param(r"\injlim", {"mo": {"@movablelimits": "true", "$": "inj&#x02006;lim"}}, id="injlim"),
        pytest.param(r"\ker", {"mi": "ker"}, id="ker"),
        pytest.param(
            r"[{[\LARGE[\Large[\large[[}[",
            MultiDict(
                [
                    ("mo", {"@stretchy": "false", "$": "["}),
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@stretchy": "false", "$": "["}),
                                (
                                    "mstyle",
                                    MultiDict(
                                        [
                                            ("@mathsize", "1.73em"),
                                            ("mo", {"@stretchy": "false", "$": "["}),
                                            (
                                                "mstyle",
                                                MultiDict(
                                                    [
                                                        ("@mathsize", "1.44em"),
                                                        ("mo", {"@stretchy": "false", "$": "["}),
                                                        (
                                                            "mstyle",
                                                            MultiDict(
                                                                [
                                                                    ("@mathsize", "1.2em"),
                                                                    ("mo", {"@stretchy": "false", "$": "["}),
                                                                    ("mo", {"@stretchy": "false", "$": "["}),
                                                                ]
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("mo", {"@stretchy": "false", "$": "["}),
                ]
            ),
            id="large",
        ),
        pytest.param(
            r"[{[\normalsize[\scriptsize[[}[",
            MultiDict(
                [
                    ("mo", {"@stretchy": "false", "$": "["}),
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mo", {"@stretchy": "false", "$": "["}),
                                (
                                    "mstyle",
                                    MultiDict(
                                        [
                                            ("@mathsize", "1em"),
                                            ("mo", {"@stretchy": "false", "$": "["}),
                                            (
                                                "mstyle",
                                                MultiDict(
                                                    [
                                                        ("@mathsize", "0.7em"),
                                                        ("mo", {"@stretchy": "false", "$": "["}),
                                                        ("mo", {"@stretchy": "false", "$": "["}),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("mo", {"@stretchy": "false", "$": "["}),
                ]
            ),
            id="normalsize-scriptsize",
        ),
        pytest.param(
            r"\mathbb{AB}C",
            MultiDict(
                [
                    (
                        "mrow",
                        MultiDict(
                            [
                                ("mi", {"@mathvariant": "double-struck", "$": "A"}),
                                ("mi", {"@mathvariant": "double-struck", "$": "B"}),
                            ]
                        ),
                    ),
                    ("mi", "C"),
                ]
            ),
            id="mathbb",
        ),
        pytest.param(
            r"\mathbf {\text{var} = 1+\{b\}}",
            {
                "mrow": MultiDict(
                    [
                        ("mtext", {"@mathvariant": "bold", "$": "var"}),
                        ("mo", {"@mathvariant": "bold", "$": "&#x0003D;"}),
                        ("mn", {"@mathvariant": "bold", "$": "1"}),
                        ("mo", {"@mathvariant": "bold", "$": "&#x0002B;"}),
                        ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                        ("mi", {"@mathvariant": "bold", "$": "b"}),
                        ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                    ]
                )
            },
            id="mathbf",
        ),
        pytest.param(
            r"{\mathcal {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", {"@mathvariant": "script", "$": "var"}),
                                    ("mo", {"@mathvariant": "script", "$": "&#x0003D;"}),
                                    ("mn", {"@mathvariant": "script", "$": "1"}),
                                    ("mo", {"@mathvariant": "script", "$": "&#x0002B;"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                    ("mi", {"@mathvariant": "script", "$": "b"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="mathcal",
        ),
        pytest.param(
            r"{\mathfrak {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", {"@mathvariant": "fraktur", "$": "var"}),
                                    ("mo", {"@mathvariant": "fraktur", "$": "&#x0003D;"}),
                                    ("mn", {"@mathvariant": "fraktur", "$": "1"}),
                                    ("mo", {"@mathvariant": "fraktur", "$": "&#x0002B;"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                    ("mi", {"@mathvariant": "fraktur", "$": "b"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="mathfrak",
        ),
        pytest.param(
            r"{\mathit {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", {"@mathvariant": "italic", "$": "var"}),
                                    ("mo", {"@mathvariant": "italic", "$": "&#x0003D;"}),
                                    ("mn", {"@mathvariant": "italic", "$": "1"}),
                                    ("mo", {"@mathvariant": "italic", "$": "&#x0002B;"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                    ("mi", {"@mathvariant": "italic", "$": "b"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="mathit",
        ),
        pytest.param(
            r"{\mathrm {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", "var"),
                                    ("mo", "&#x0003D;"),
                                    ("mn", "1"),
                                    ("mo", "&#x0002B;"),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                    ("mi", {"@mathvariant": "normal", "$": "b"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="mathrm",
        ),
        # FIXME: no way to distinguish \mathcal and \mathscr for now
        pytest.param(
            r"{\mathscr {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", {"@mathvariant": "script", "$": "var"}),
                                    ("mo", {"@mathvariant": "script", "$": "&#x0003D;"}),
                                    ("mn", {"@mathvariant": "script", "$": "1"}),
                                    ("mo", {"@mathvariant": "script", "$": "&#x0002B;"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                    ("mi", {"@mathvariant": "script", "$": "b"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="mathscr",
        ),
        pytest.param(
            r"{\mathsf {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", "var"),
                                    ("mo", "&#x0003D;"),
                                    ("mn", "1"),
                                    ("mo", "&#x0002B;"),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                    ("mi", {"@mathvariant": "sans-serif", "$": "b"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="mathsf",
        ),
        pytest.param(
            r"{\mathtt {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", {"@mathvariant": "monospace", "$": "var"}),
                                    ("mo", {"@mathvariant": "monospace", "$": "&#x0003D;"}),
                                    ("mn", {"@mathvariant": "monospace", "$": "1"}),
                                    ("mo", {"@mathvariant": "monospace", "$": "&#x0002B;"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007B;"}),
                                    ("mi", {"@mathvariant": "monospace", "$": "b"}),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="mathtt",
        ),
        # FIXME: convert with correct spacing
        pytest.param(
            r"\mathop{a}\mathord{b}\mathpunct{c}\mathbin{d}\mathrel{e}",
            MultiDict(
                [
                    ("mrow", {"mi": "a"}),
                    ("mrow", {"mi": "b"}),
                    ("mrow", {"mi": "c"}),
                    ("mrow", {"mi": "d"}),
                    ("mrow", {"mi": "e"}),
                ]
            ),
            id="math-commands-that-currently-does-nothing",
        ),
    ],
)
def test_converter(latex: str, json: MultiDict) -> None:
    parent = {
        "math": {
            "@xmlns": "http://www.w3.org/1998/Math/MathML",
            "@display": "block",
            "mrow": json,
        }
    }
    bf = BadgerFish(dict_type=MultiDict)
    math = bf.etree(parent)
    assert convert(latex, display="block") == _convert(math[0])


@pytest.mark.skipif(sys.version_info < (3, 8), reason="xml.etree sorts attributes in 3.7 and below")
def test_attributes() -> None:
    assert (
        convert("1")
        == '<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn></mrow></math>'
    )
    assert (
        convert("1", display="block")
        == '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mn>1</mn></mrow></math>'
    )
