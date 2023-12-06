from xml.etree.cElementTree import Element

import pytest
from multidict import MultiDict
from xmljson import BadgerFish

# noinspection PyProtectedMember
from latex2mathml.converter import _convert, convert, convert_to_element


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
                        "msub",
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
                        "msub",
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
            r"\int\limits^{\pi}_{0}",
            {"munderover": MultiDict([("mo", "&#x0222B;"), ("mrow", {"mn": "0"}), ("mrow", {"mi": "&#x003C0;"})])},
            id="issue-301-a",
        ),
        pytest.param(
            r"\int\limits_{\pi}",
            {"munder": MultiDict([("mo", "&#x0222B;"), ("mrow", {"mi": "&#x003C0;"})])},
            id="issue-301-b",
        ),
        pytest.param(
            r"\int\limits^{\pi}",
            {"mover": MultiDict([("mo", "&#x0222B;"), ("mrow", {"mi": "&#x003C0;"})])},
            id="issue-301-c",
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
                "msub": MultiDict(
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
            r"\tan x+\sec x+\cos x+\sin x+\cot x+\csc x+\arccos x+\arcsin x+\arctan x +\cosh x+\coth x+\sinh x+\tanh x",
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
                    ("mo", "&#x0002B;"),
                    ("mi", "sinh"),
                    ("mi", "x"),
                    ("mo", "&#x0002B;"),
                    ("mi", "tanh"),
                    ("mi", "x"),
                ]
            ),
            id="issue-91",
        ),
        pytest.param(r"p_{\max}", {"msub": MultiDict([("mi", "p"), ("mrow", {"mo": "max"})])}, id="issue-98"),
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
                                            "mtd": MultiDict(
                                                [
                                                    ("@columnalign", "left"),
                                                    (
                                                        "mrow",
                                                        MultiDict([("mi", "x"), ("mo", "&#x0003D;"), ("mn", "1")]),
                                                    ),
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
                )
            },
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
        pytest.param(r"\operatorname{sn}x", MultiDict([("mo", "sn"), ("mi", "x")]), id="issue-109-1"),
        pytest.param(
            r"\operatorname{sn}(x+y)",
            MultiDict(
                [
                    ("mo", "sn"),
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
            r"""|\,|\:|\>|\;|\\|\!|\quad|\qquad|\hspace1em|\hspace{10ex}|\enspace|\hskip1em|\kern-1.5pt|\mkern10mu|
            \mskip18mu|\mspace18mu|\negthinspace|\negmedspace|\negthickspace|\nobreakspace|\space|\thinspace|""",
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
                    ("mspace", {"@width": "10mu"}),  # TODO: convert to em?
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
                        MultiDict([("mi", "a"), ("mo", {"@stretchy": "false", "$": "&#x0005E;"})]),
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
                                ("mo", {"@stretchy": "false", "$": "&#x0005E;"}),
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
            r"\idotsint",
            {"mrow": MultiDict([("mo", "&#x0222B;"), ("mo", "&#x022EF;"), ("mo", "&#x0222B;")])},
            id="idotsint",
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
        pytest.param(
            r"\hbox{This is a sentence.}",
            {
                "mstyle": {
                    "@displaystyle": "false",
                    "@scriptlevel": "0",
                    "mtext": "This&#x000A0;is&#x000A0;a&#x000A0;sentence.",
                }
            },
            id="hbox",
        ),
        pytest.param(
            r"\hbox{left $x > 0$ center \$x > 0\$ right}",
            {
                "mstyle": MultiDict(
                    [
                        ("@displaystyle", "false"),
                        ("@scriptlevel", "0"),
                        ("mtext", "left&#x000A0;"),
                        ("mrow", MultiDict([("mi", "x"), ("mo", "&#x0003E;"), ("mn", "0")])),
                        ("mtext", r"&#x000A0;center&#x000A0;\$x&#x000A0;>&#x000A0;0\$&#x000A0;right"),
                    ]
                )
            },
            id="hbox-with-math-mode",
        ),
        pytest.param(
            r"\hbox{\alpha $\alpha$}",
            {
                "mstyle": MultiDict(
                    [
                        ("@displaystyle", "false"),
                        ("@scriptlevel", "0"),
                        ("mtext", r"\alpha&#x000A0;"),
                        ("mrow", {"mi": "&#x003B1;"}),
                    ]
                )
            },
            id="hbox-with-backslash-in-text",
        ),
        pytest.param(
            r"\begin{matrix} xxxxxx & xxxxxx & xxxxxx \cr ab & \hfil ab & ab\hfil\cr \end{matrix}",
            {
                "mtable": MultiDict(
                    [
                        (
                            "mtr",
                            MultiDict(
                                [
                                    (
                                        "mtd",
                                        MultiDict(
                                            [
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                            ]
                                        ),
                                    ),
                                    (
                                        "mtd",
                                        MultiDict(
                                            [
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                            ]
                                        ),
                                    ),
                                    (
                                        "mtd",
                                        MultiDict(
                                            [
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                                ("mi", "x"),
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", MultiDict([("mi", "a"), ("mi", "b")])),
                                    ("mtd", MultiDict([("@columnalign", "right"), ("mi", "a"), ("mi", "b")])),
                                    ("mtd", MultiDict([("@columnalign", "left"), ("mi", "a"), ("mi", "b")])),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="hfil",
        ),
        pytest.param(r"\ldotp", {"mo": "&#x0002E;"}, id="ldotp"),
        pytest.param(r"\lg", {"mi": "lg"}, id="lg"),
        pytest.param(r"\liminf", {"mo": {"@movablelimits": "true", "$": "lim&#x02006;inf"}}, id="liminf"),
        pytest.param(r"\limsup", {"mo": {"@movablelimits": "true", "$": "lim&#x02006;sup"}}, id="limsup"),
        pytest.param(r"\llless", {"mo": "&#x022D8;"}, id="llless"),
        pytest.param(r"\lt", {"mo": "&#x0003C;"}, id="lt"),
        pytest.param(r"\lvert", {"mo": "&#x0007C;"}, id="lvert"),
        pytest.param(r"\lVert", {"mo": "&#x02016;"}, id="lVert"),
        pytest.param(r"\lvertneqq", {"mo": "&#x02268;"}, id="lvertneqq"),
        pytest.param(r"\ngeqq", {"mo": "&#x02271;"}, id="ngeqq"),
        pytest.param(r"\nshortmid", {"mo": "&#x02224;"}, id="nshortmid"),
        pytest.param(r"\nshortparallel", {"mo": "&#x02226;"}, id="nshortparallel"),
        pytest.param(r"\nsubseteqq", {"mo": "&#x02288;"}, id="nsubseteqq"),
        pytest.param(r"\omicron", {"mo": "&#x003BF;"}, id="omicron"),
        pytest.param(r"\Pr", {"mo": {"@movablelimits": "true", "$": "Pr"}}, id="Pr"),
        pytest.param(r"\projlim", {"mo": {"@movablelimits": "true", "$": "proj&#x02006;lim"}}, id="projlim"),
        pytest.param(r"\rvert", {"mo": "&#x0007C;"}, id="rvert"),
        pytest.param(r"\rVert", {"mo": "&#x02016;"}, id="rVert"),
        pytest.param(r"\S", {"mo": "&#x000A7;"}, id="S"),
        pytest.param(r"\shortmid", {"mo": "&#x02223;"}, id="shortmid"),
        pytest.param(r"\smallfrown", {"mo": "&#x02322;"}, id="smallfrown"),
        pytest.param(r"\smallint", {"mo": {"@largeop": "false", "$": "&#x0222B;"}}, id="smallint"),
        pytest.param(r"\smallsmile", {"mo": "&#x02323;"}, id="smallsmile"),
        pytest.param(r"\surd", {"mo": {"@stretchy": "false", "$": "&#x0221A;"}}, id="surd"),
        pytest.param(r"\thicksim", {"mo": "&#x0223C;"}, id="thicksim"),
        pytest.param(r"\thickapprox", {"mo": "&#x02248;"}, id="thickapprox"),
        pytest.param(r"\varsubsetneqq", {"mo": "&#x02ACB;"}, id="varsubsetneqq"),
        pytest.param(r"\varsupsetneq", {"mo": "&#x0228B;"}, id="varsupsetneq"),
        pytest.param(r"\varsupsetneqq", {"mo": "&#x02ACC;"}, id="varsupsetneqq"),
        pytest.param(
            r"[{[\small[\tiny[\Tiny[[}[",
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
                                            ("@mathsize", "0.85em"),
                                            ("mo", {"@stretchy": "false", "$": "["}),
                                            (
                                                "mstyle",
                                                MultiDict(
                                                    [
                                                        ("@mathsize", "0.5em"),
                                                        ("mo", {"@stretchy": "false", "$": "["}),
                                                        (
                                                            "mstyle",
                                                            MultiDict(
                                                                [
                                                                    ("@mathsize", "0.6em"),
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
            id="small-tiny",
        ),
        pytest.param(
            r"\mbox{This is a sentence.}",
            {
                "mstyle": {
                    "@displaystyle": "false",
                    "@scriptlevel": "0",
                    "mtext": "This&#x000A0;is&#x000A0;a&#x000A0;sentence.",
                }
            },
            id="mbox",
        ),
        pytest.param(
            r"\frac{\style{color:red}{x+1}}{\style{color:green}y+2}",
            {
                "mfrac": MultiDict(
                    [
                        (
                            "mrow",
                            {
                                "mrow": MultiDict(
                                    [("@style", "color:red"), ("mi", "x"), ("mo", "&#x0002B;"), ("mn", "1")]
                                )
                            },
                        ),
                        (
                            "mrow",
                            MultiDict([("mi", {"@style": "color:green", "$": "y"}), ("mo", "&#x0002B;"), ("mn", "2")]),
                        ),
                    ]
                )
            },
            id="style",
        ),
        pytest.param(
            r"\mathring a \mathring{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x002DA;")]),
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
                                ("mo", "&#x002DA;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="mathring",
        ),
        pytest.param(
            r"\overleftarrow a \overleftarrow{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x02190;")]),
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
                                ("mo", "&#x02190;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="overleftarrow",
        ),
        pytest.param(
            r"\overleftrightarrow a \overleftrightarrow{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x02194;")]),
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
                                ("mo", "&#x02194;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="overleftrightarrow",
        ),
        pytest.param(
            r"\overline a \overline{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", {"@accent": "true", "$": "&#x02015;"})]),
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
                                ("mo", {"@accent": "true", "$": "&#x02015;"}),
                            ]
                        ),
                    ),
                ]
            ),
            id="overline",
        ),
        pytest.param(
            r"\overparen a \overparen{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x023DC;")]),
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
                                ("mo", "&#x023DC;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="overparen",
        ),
        pytest.param(
            r"\overrightarrow a \overrightarrow{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x02192;")]),
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
                                ("mo", "&#x02192;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="overrightarrow",
        ),
        pytest.param(
            r"\tilde a \tilde{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", {"@stretchy": "false", "$": "&#x0007E;"})]),
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
                                ("mo", {"@stretchy": "false", "$": "&#x0007E;"}),
                            ]
                        ),
                    ),
                ]
            ),
            id="tilde",
        ),
        pytest.param(
            r"\underleftarrow a \underleftarrow{bc}",
            MultiDict(
                [
                    (
                        "munder",
                        MultiDict([("mi", "a"), ("mo", "&#x02190;")]),
                    ),
                    (
                        "munder",
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
                                ("mo", "&#x02190;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="underleftarrow",
        ),
        pytest.param(
            r"\underrightarrow a \underrightarrow{bc}",
            MultiDict(
                [
                    (
                        "munder",
                        MultiDict([("mi", "a"), ("mo", "&#x02192;")]),
                    ),
                    (
                        "munder",
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
                                ("mo", "&#x02192;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="underrightarrow",
        ),
        pytest.param(
            r"\underleftrightarrow a \underleftrightarrow{bc}",
            MultiDict(
                [
                    (
                        "munder",
                        MultiDict([("mi", "a"), ("mo", "&#x02194;")]),
                    ),
                    (
                        "munder",
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
                                ("mo", "&#x02194;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="underleftrightarrow",
        ),
        pytest.param(
            r"\underline a \underline{bc}",
            MultiDict(
                [
                    (
                        "munder",
                        MultiDict([("mi", "a"), ("mo", {"@accent": "true", "$": "&#x02015;"})]),
                    ),
                    (
                        "munder",
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
                                ("mo", {"@accent": "true", "$": "&#x02015;"}),
                            ]
                        ),
                    ),
                ]
            ),
            id="underline",
        ),
        pytest.param(
            r"\underparen a \underparen{bc}",
            MultiDict(
                [
                    (
                        "munder",
                        MultiDict([("mi", "a"), ("mo", "&#x023DD;")]),
                    ),
                    (
                        "munder",
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
                                ("mo", "&#x023DD;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="underparen",
        ),
        pytest.param(
            r"\widehat a \widehat{bc}",
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
            id="widehat",
        ),
        pytest.param(
            r"\widetilde a \widetilde{bc}",
            MultiDict(
                [
                    (
                        "mover",
                        MultiDict([("mi", "a"), ("mo", "&#x0007E;")]),
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
                                ("mo", "&#x0007E;"),
                            ]
                        ),
                    ),
                ]
            ),
            id="widetilde",
        ),
        pytest.param(r"\phantom a", {"mphantom": {"mi": "a"}}, id="phantom"),
        pytest.param(r"\vphantom a", {"mpadded": {"@width": "0", "mphantom": {"mi": "a"}}}, id="vphantom"),
        pytest.param(
            r"\sideset{_1^2}{_3^4}\sum",
            {
                "mrow": MultiDict(
                    [
                        (
                            "msubsup",
                            MultiDict(
                                [
                                    (
                                        "mpadded",
                                        {
                                            "@width": "0",
                                            "mphantom": {"mo": {"@movablelimits": "false", "$": "&#x02211;"}},
                                        },
                                    ),
                                    ("mn", "1"),
                                    ("mn", "2"),
                                ]
                            ),
                        ),
                        ("mstyle", {"@scriptlevel": "0", "mspace": {"@width": "-0.167em"}}),
                        (
                            "msubsup",
                            MultiDict(
                                [("mo", {"@movablelimits": "false", "$": "&#x02211;"}), ("mn", "3"), ("mn", "4")]
                            ),
                        ),
                    ]
                )
            },
            id="sideset",
        ),
        pytest.param(
            r"\sideset{_1^2}{_3^4}{\sum}",
            {
                "mrow": MultiDict(
                    [
                        (
                            "msubsup",
                            MultiDict(
                                [
                                    (
                                        "mpadded",
                                        {
                                            "@width": "0",
                                            "mphantom": {"mrow": {"@movablelimits": "false", "mo": "&#x02211;"}},
                                        },
                                    ),
                                    ("mn", "1"),
                                    ("mn", "2"),
                                ]
                            ),
                        ),
                        ("mstyle", {"@scriptlevel": "0", "mspace": {"@width": "-0.167em"}}),
                        (
                            "msubsup",
                            MultiDict(
                                [("mrow", {"@movablelimits": "false", "mo": "&#x02211;"}), ("mn", "3"), ("mn", "4")]
                            ),
                        ),
                    ]
                )
            },
            id="307-a",
        ),
        pytest.param(
            r"\sideset{^{°}}{}{C}",
            {
                "mrow": MultiDict(
                    [
                        (
                            "msup",
                            MultiDict(
                                [
                                    (
                                        "mpadded",
                                        {
                                            "@width": "0",
                                            "mphantom": {"mrow": {"@movablelimits": "false", "mi": "C"}},
                                        },
                                    ),
                                    ("mrow", {"mi": "°"}),
                                ]
                            ),
                        ),
                        ("mstyle", {"@scriptlevel": "0", "mspace": {"@width": "-0.167em"}}),
                        ("mrow", {"mrow": {"@movablelimits": "false", "mi": "C"}}),
                    ]
                )
            },
            id="307-b",
        ),
        pytest.param(
            r"\tbinom{2}{3}",
            {
                "mstyle": MultiDict(
                    [
                        ("@displaystyle", "false"),
                        ("@scriptlevel", "0"),
                        ("mo", {"@minsize": "1.2em", "@maxsize": "1.2em", "$": "&#x00028;"}),
                        ("mfrac", MultiDict([("@linethickness", "0"), ("mrow", {"mn": "2"}), ("mrow", {"mn": "3"})])),
                        ("mo", {"@minsize": "1.2em", "@maxsize": "1.2em", "$": "&#x00029;"}),
                    ]
                )
            },
            id="tbinom",
        ),
        pytest.param(
            r"\tfrac{1}{2}",
            {
                "mstyle": {
                    "@displaystyle": "false",
                    "@scriptlevel": "0",
                    "mfrac": MultiDict([("mrow", {"mn": "1"}), ("mrow", {"mn": "2"})]),
                }
            },
            id="tfrac",
        ),
        pytest.param(
            r"{\mit {\text{var} = 1+\{b\}}} + B",
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
                                    ("mi", "b"),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007D;"}),
                                ]
                            ),
                        },
                    ),
                    ("mo", "&#x0002B;"),
                    ("mi", "B"),
                ]
            ),
            id="mit",
        ),
        pytest.param(
            r"{\oldstyle {\text{var} = 1+\{b\}}} + B",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mrow": MultiDict(
                                [
                                    ("mtext", {"@mathvariant": "normal", "$": "var"}),
                                    ("mo", {"@mathvariant": "normal", "$": "&#x0003D;"}),
                                    ("mn", {"@mathvariant": "normal", "$": "1"}),
                                    ("mo", {"@mathvariant": "normal", "$": "&#x0002B;"}),
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
            id="oldstyle",
        ),
        pytest.param(
            r"{\scr {\text{var} = 1+\{b\}}} + B",
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
            id="scr",
        ),
        pytest.param(
            r"{\tt {\text{var} = 1+\{b\}}} + B",
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
            id="tt",
        ),
        pytest.param(
            r"\textbf{ Hello~World }",
            {"mtext": {"@mathvariant": "bold", "$": "&#x000A0;Hello~World&#x000A0;"}},
            id="textbf",
        ),
        pytest.param(
            r"\textit{ Hello~World }",
            {"mtext": {"@mathvariant": "italic", "$": "&#x000A0;Hello~World&#x000A0;"}},
            id="textit",
        ),
        pytest.param(r"\textrm{ Hello~World }", {"mtext": "&#x000A0;Hello~World&#x000A0;"}, id="textrm"),
        pytest.param(
            r"\textsf{ Hello~World }",
            {"mtext": {"@mathvariant": "sans-serif", "$": "&#x000A0;Hello~World&#x000A0;"}},
            id="textsf",
        ),
        pytest.param(
            r"\texttt{ Hello~World }",
            {"mtext": {"@mathvariant": "monospace", "$": "&#x000A0;Hello~World&#x000A0;"}},
            id="texttt",
        ),
        pytest.param(
            r"\LaTeX",
            {
                "mrow": MultiDict(
                    [
                        ("mi", "L"),
                        ("mspace", {"@width": "-.325em"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@height", "+.21ex"),
                                    ("@depth", "-.21ex"),
                                    ("@voffset", "+.21ex"),
                                    ("mstyle", {"@displaystyle": "false", "@scriptlevel": "1", "mrow": {"mi": "A"}}),
                                ]
                            ),
                        ),
                        ("mspace", {"@width": "-.17em"}),
                        ("mi", "T"),
                        ("mspace", {"@width": "-.14em"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@height", "-.5ex"),
                                    ("@depth", "+.5ex"),
                                    ("@voffset", "-.5ex"),
                                    ("mrow", {"mi": "E"}),
                                ]
                            ),
                        ),
                        ("mspace", {"@width": "-.115em"}),
                        ("mi", "X"),
                    ]
                )
            },
            id="LaTeX",
        ),
        pytest.param(
            r"\Bbb \LaTeX",
            {
                "mrow": MultiDict(
                    [
                        ("mi", {"@mathvariant": "double-struck", "$": "L"}),
                        ("mspace", {"@width": "-.325em"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@height", "+.21ex"),
                                    ("@depth", "-.21ex"),
                                    ("@voffset", "+.21ex"),
                                    (
                                        "mstyle",
                                        {
                                            "@displaystyle": "false",
                                            "@scriptlevel": "1",
                                            "mrow": {"mi": {"@mathvariant": "double-struck", "$": "A"}},
                                        },
                                    ),
                                ]
                            ),
                        ),
                        ("mspace", {"@width": "-.17em"}),
                        ("mi", {"@mathvariant": "double-struck", "$": "T"}),
                        ("mspace", {"@width": "-.14em"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@height", "-.5ex"),
                                    ("@depth", "+.5ex"),
                                    ("@voffset", "-.5ex"),
                                    ("mrow", {"mi": {"@mathvariant": "double-struck", "$": "E"}}),
                                ]
                            ),
                        ),
                        ("mspace", {"@width": "-.115em"}),
                        ("mi", {"@mathvariant": "double-struck", "$": "X"}),
                    ]
                )
            },
            id="LaTeX-with-style",
        ),
        pytest.param(
            r"\TeX",
            {
                "mrow": MultiDict(
                    [
                        ("mi", "T"),
                        ("mspace", {"@width": "-.14em"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@height", "-.5ex"),
                                    ("@depth", "+.5ex"),
                                    ("@voffset", "-.5ex"),
                                    ("mrow", {"mi": "E"}),
                                ]
                            ),
                        ),
                        ("mspace", {"@width": "-.115em"}),
                        ("mi", "X"),
                    ]
                )
            },
            id="TeX",
        ),
        pytest.param(
            r"\rm \TeX",
            {
                "mrow": MultiDict(
                    [
                        ("mi", {"@mathvariant": "normal", "$": "T"}),
                        ("mspace", {"@width": "-.14em"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@height", "-.5ex"),
                                    ("@depth", "+.5ex"),
                                    ("@voffset", "-.5ex"),
                                    ("mrow", {"mi": {"@mathvariant": "normal", "$": "E"}}),
                                ]
                            ),
                        ),
                        ("mspace", {"@width": "-.115em"}),
                        ("mi", {"@mathvariant": "normal", "$": "X"}),
                    ]
                )
            },
            id="TeX-with-style",
        ),
        pytest.param(
            r"\skew7\hat A",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mover": MultiDict(
                                [
                                    ("mrow", MultiDict([("mi", "A"), ("mspace", {"@width": "0.389em"})])),
                                    ("mo", {"@stretchy": "false", "$": "&#x0005E;"}),
                                ]
                            ),
                        },
                    ),
                    ("mspace", {"@width": "-0.389em"}),
                ]
            ),
            id="skew",
        ),
        pytest.param(
            r"\skew{8}\tilde M",
            MultiDict(
                [
                    (
                        "mrow",
                        {
                            "mover": MultiDict(
                                [
                                    ("mrow", MultiDict([("mi", "M"), ("mspace", {"@width": "0.444em"})])),
                                    ("mo", {"@stretchy": "false", "$": "&#x0007E;"}),
                                ]
                            ),
                        },
                    ),
                    ("mspace", {"@width": "-0.444em"}),
                ]
            ),
            id="skew-with-braces",
        ),
        pytest.param(
            r"\mod 5",
            MultiDict(
                [
                    ("mspace", {"@width": "1em"}),
                    ("mi", "mod"),
                    ("mspace", {"@width": "0.333em"}),
                    ("mn", "5"),
                ]
            ),
            id="mod",
        ),
        pytest.param(
            r"\pmod 5",
            MultiDict(
                [
                    ("mspace", {"@width": "1em"}),
                    ("mo", "&#x00028;"),
                    ("mi", "mod"),
                    ("mspace", {"@width": "0.333em"}),
                    ("mn", "5"),
                    ("mo", "&#x00029;"),
                ]
            ),
            id="pmod",
        ),
        pytest.param(
            r"\left\{\middle|\right\}",
            {
                "mrow": MultiDict(
                    [
                        ("mo", {"@stretchy": "true", "@fence": "true", "@form": "prefix", "$": "&#x0007B;"}),
                        (
                            "mo",
                            {
                                "@stretchy": "true",
                                "@fence": "true",
                                "@lspace": "0.05em",
                                "@rspace": "0.05em",
                                "$": "&#x0007C;",
                            },
                        ),
                        ("mo", {"@stretchy": "true", "@fence": "true", "@form": "postfix", "$": "&#x0007D;"}),
                    ]
                )
            },
            id="middle",
        ),
        pytest.param(r"9 \bmod2", MultiDict([("mn", "9"), ("mo", "mod"), ("mn", "2")]), id="bmod"),
        pytest.param(r"\overbrace3", {"mover": MultiDict([("mn", "3"), ("mo", "&#x23DE;")])}, id="overbrace-a"),
        pytest.param(
            r"\overbrace3^a",
            {"mover": MultiDict([("mover", MultiDict([("mn", "3"), ("mo", "&#x23DE;")])), ("mi", "a")])},
            id="overbrace-b",
        ),
        pytest.param(
            r"\overbrace3^a_x",
            {
                "munderover": MultiDict(
                    [("mover", MultiDict([("mn", "3"), ("mo", "&#x23DE;")])), ("mi", "x"), ("mi", "a")]
                )
            },
            id="overbrace-c",
        ),
        pytest.param(r"\underbrace3", {"munder": MultiDict([("mn", "3"), ("mo", "&#x23DF;")])}, id="underbrace-a"),
        pytest.param(
            r"\underbrace3_a",
            {"munder": MultiDict([("munder", MultiDict([("mn", "3"), ("mo", "&#x23DF;")])), ("mi", "a")])},
            id="underbrace-b",
        ),
        pytest.param(
            r"\underbrace3_a^x",
            {
                "munderover": MultiDict(
                    [("munder", MultiDict([("mn", "3"), ("mo", "&#x23DF;")])), ("mi", "a"), ("mi", "x")]
                )
            },
            id="underbrace-c",
        ),
        pytest.param(
            r"\xleftarrow x",
            {
                "mover": MultiDict(
                    [
                        ("mstyle", {"@scriptlevel": "0", "mo": "&#x2190;"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@width", "+0.833em"),
                                    ("@lspace", "0.556em"),
                                    ("@voffset", "-.2em"),
                                    ("@height", "-.2em"),
                                    ("mi", "x"),
                                    ("mspace", {"@depth": ".25em"}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="xleftarrow",
        ),
        pytest.param(
            r"\xleftarrow[y] x",
            {
                "munderover": MultiDict(
                    [
                        ("mstyle", {"@scriptlevel": "0", "mo": "&#x2190;"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@width", "+0.833em"),
                                    ("@lspace", "0.556em"),
                                    ("@voffset", "-.2em"),
                                    ("@height", "-.2em"),
                                    ("mrow", {"mi": "y"}),
                                    ("mspace", {"@depth": ".25em"}),
                                ]
                            ),
                        ),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@width", "+0.833em"),
                                    ("@lspace", "0.556em"),
                                    ("@voffset", "-.2em"),
                                    ("@height", "-.2em"),
                                    ("mi", "x"),
                                    ("mspace", {"@depth": ".25em"}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="xleftarrow-with-argument",
        ),
        pytest.param(
            r"\xrightarrow x",
            {
                "mover": MultiDict(
                    [
                        ("mstyle", {"@scriptlevel": "0", "mo": "&#x2192;"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@width", "+0.833em"),
                                    ("@lspace", "0.556em"),
                                    ("@voffset", "-.2em"),
                                    ("@height", "-.2em"),
                                    ("mi", "x"),
                                    ("mspace", {"@depth": ".25em"}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="xrightarrow",
        ),
        pytest.param(
            r"\xrightarrow[y] x",
            {
                "munderover": MultiDict(
                    [
                        ("mstyle", {"@scriptlevel": "0", "mo": "&#x2192;"}),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@width", "+0.833em"),
                                    ("@lspace", "0.556em"),
                                    ("@voffset", "-.2em"),
                                    ("@height", "-.2em"),
                                    ("mrow", {"mi": "y"}),
                                    ("mspace", {"@depth": ".25em"}),
                                ]
                            ),
                        ),
                        (
                            "mpadded",
                            MultiDict(
                                [
                                    ("@width", "+0.833em"),
                                    ("@lspace", "0.556em"),
                                    ("@voffset", "-.2em"),
                                    ("@height", "-.2em"),
                                    ("mi", "x"),
                                    ("mspace", {"@depth": ".25em"}),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="xrightarrow-with-argument",
        ),
        pytest.param(
            r"\bigl(\begin{smallmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ \end{smallmatrix}\bigr)",
            MultiDict(
                [
                    (
                        "mo",
                        {
                            "@stretchy": "true",
                            "@fence": "true",
                            "@minsize": "1.2em",
                            "@maxsize": "1.2em",
                            "$": "(",
                        },
                    ),
                    (
                        "mstyle",
                        {
                            "@scriptlevel": "1",
                            "mtable": MultiDict(
                                [
                                    ("@rowspacing", "0.1em"),
                                    ("@columnspacing", "0.2778em"),
                                    (
                                        "mtr",
                                        MultiDict([("mtd", {"mn": "1"}), ("mtd", {"mn": "2"}), ("mtd", {"mn": "3"})]),
                                    ),
                                    (
                                        "mtr",
                                        MultiDict([("mtd", {"mn": "4"}), ("mtd", {"mn": "5"}), ("mtd", {"mn": "6"})]),
                                    ),
                                ]
                            ),
                        },
                    ),
                    (
                        "mo",
                        {
                            "@stretchy": "true",
                            "@fence": "true",
                            "@minsize": "1.2em",
                            "@maxsize": "1.2em",
                            "$": ")",
                        },
                    ),
                ]
            ),
            id="bigl-smallmatrix-bigr",
        ),
        pytest.param(
            r"\not\in\not a\not\operatorname{R}\not",
            MultiDict(
                [
                    ("mo", "&#x02209;"),
                    ("mpadded", MultiDict([("@width", "0"), ("mtext", "&#x029F8;")])),
                    ("mi", "a"),
                    ("mpadded", MultiDict([("@width", "0"), ("mtext", "&#x029F8;")])),
                    ("mo", "R"),
                    ("mpadded", MultiDict([("@width", "0"), ("mtext", "&#x029F8;")])),
                ]
            ),
            id="not",
        ),
        pytest.param(
            r"\begin{split}  x &= y \\  &=z  \end{split}",
            {
                "mtable": MultiDict(
                    [
                        ("@displaystyle", "true"),
                        ("@columnspacing", "0em"),
                        ("@rowspacing", "3pt"),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "right", "mi": "x"}),
                                    (
                                        "mtd",
                                        MultiDict(
                                            [("@columnalign", "left"), ("mi", ""), ("mo", "&#x0003D;"), ("mi", "y")]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "right"}),
                                    (
                                        "mtd",
                                        MultiDict(
                                            [("@columnalign", "left"), ("mi", ""), ("mo", "&#x0003D;"), ("mi", "z")]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="split",
        ),
        pytest.param(
            r"\begin{align*}x &=y & w &=z  & a&=b \end{align*}",
            {
                "mtable": MultiDict(
                    [
                        ("@displaystyle", "true"),
                        ("@rowspacing", "3pt"),
                        ("@columnspacing", "0em 2em 0em 2em 0em 2em"),
                        (
                            "mtr",
                            MultiDict(
                                [
                                    ("mtd", {"@columnalign": "right", "mi": "x"}),
                                    (
                                        "mtd",
                                        MultiDict(
                                            [("@columnalign", "left"), ("mi", ""), ("mo", "&#x0003D;"), ("mi", "y")]
                                        ),
                                    ),
                                    ("mtd", {"@columnalign": "right", "mi": "w"}),
                                    (
                                        "mtd",
                                        MultiDict(
                                            [("@columnalign", "left"), ("mi", ""), ("mo", "&#x0003D;"), ("mi", "z")]
                                        ),
                                    ),
                                    ("mtd", {"@columnalign": "right", "mi": "a"}),
                                    (
                                        "mtd",
                                        MultiDict(
                                            [("@columnalign", "left"), ("mi", ""), ("mo", "&#x0003D;"), ("mi", "b")]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                )
            },
            id="align",
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


def test_attributes() -> None:
    assert (
        convert("1")
        == '<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn></mrow></math>'
    )
    assert (
        convert("1", display="block")
        == '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mn>1</mn></mrow></math>'
    )


def test_convert_to_element() -> None:
    bf = BadgerFish()

    element = convert_to_element("1")
    assert bf.data(element) == {
        "math": {
            "@display": "inline",
            "@xmlns": "http://www.w3.org/1998/Math/MathML",
            "mrow": {"mn": {"$": 1}},
        },
    }, "should convert to element"

    parent = Element("div")
    convert_to_element("1", parent=parent)
    assert bf.data(parent) == {
        "div": {
            "math": {
                "@display": "inline",
                "@xmlns": "http://www.w3.org/1998/Math/MathML",
                "mrow": {"mn": {"$": 1}},
            },
        }
    }, "should convert to element as child of parent"
