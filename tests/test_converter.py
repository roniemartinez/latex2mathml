#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import sys

import pytest
from multidict import MultiDict
from xmljson import BadgerFish

# noinspection PyProtectedMember
from latex2mathml.converter import _convert, convert

PARAMS = [
    ("single identifier", "x", {"mi": "x"}),
    ("multiple identifier", "xyz", MultiDict([("mi", "x"), ("mi", "y"), ("mi", "z")])),
    ("single number", "3", {"mn": "3"}),
    ("multiple numbers", "333", {"mn": "333"}),
    ("decimal numbers", "12.34", {"mn": "12.34"}),
    ("numbers and identifiers", "12x", MultiDict([("mn", "12"), ("mi", "x")])),
    ("single operator", "+", {"mo": "&#x0002B;"}),
    (
        "numbers and operators",
        "3-2",
        MultiDict([("mn", "3"), ("mo", "&#x02212;"), ("mn", "2")]),
    ),
    (
        "numbers, identifiers and operators",
        "3x*2",
        MultiDict([("mn", "3"), ("mi", "x"), ("mo", "&#x0002A;"), ("mn", "2")]),
    ),
    ("single group", "{a}", {"mrow": {"mi": "a"}}),
    (
        "multiple groups",
        "{a}{b}",
        MultiDict([("mrow", {"mi": "a"}), ("mrow", {"mi": "b"})]),
    ),
    (
        "inner group",
        "{a+{b}}",
        {"mrow": MultiDict([("mi", "a"), ("mo", "&#x0002B;"), ("mrow", {"mi": "b"})])},
    ),
    (
        "over",
        r"1 \over 2",
        {"mfrac": MultiDict([("mrow", {"mn": "1"}), ("mrow", {"mn": "2"})])},
    ),
    (
        "over inside braces",
        r"{1 \over 2}",
        {"mrow": {"mfrac": MultiDict([("mrow", {"mn": "1"}), ("mrow", {"mn": "2"})])}},
    ),
    (
        "complex matrix",
        r"\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}",
        {
            "mtable": MultiDict(
                [
                    (
                        "mtr",
                        MultiDict(
                            [
                                (
                                    "mtd",
                                    {
                                        "msub": MultiDict(
                                            [("mi", "a"), ("mrow", {"mn": "1"})]
                                        )
                                    },
                                ),
                                (
                                    "mtd",
                                    {
                                        "msub": MultiDict(
                                            [("mi", "b"), ("mrow", {"mn": "2"})]
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
                                            [("mi", "c"), ("mrow", {"mn": "3"})]
                                        )
                                    },
                                ),
                                (
                                    "mtd",
                                    {
                                        "msub": MultiDict(
                                            [("mi", "d"), ("mrow", {"mn": "4"})]
                                        )
                                    },
                                ),
                            ]
                        ),
                    ),
                ]
            )
        },
    ),
    (
        "null delimiter",
        r"\left\{ \begin{array} { l } { 3x - 5y + 4z = 0} \\ { x - y + 8z = 0} \\ { 2x - 6y + z = 0} \end{array} "
        r"\right.",
        {
            "mrow": MultiDict(
                [
                    (
                        "mo",
                        MultiDict(
                            [
                                ("@stretchy", "true"),
                                ("@fence", "true"),
                                ("@form", "prefix"),
                                ("$", "&#x0007B;"),
                            ]
                        ),
                    ),
                    (
                        "mrow",
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
                                                            ("@columnalign", "left"),
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
                                                    MultiDict(
                                                        [
                                                            ("@columnalign", "left"),
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
                                                    MultiDict(
                                                        [
                                                            ("@columnalign", "left"),
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
                                                ),
                                            ]
                                        ),
                                    ),
                                ]
                            )
                        },
                    ),
                    (
                        "mo",
                        MultiDict(
                            [
                                ("@stretchy", "true"),
                                ("@fence", "true"),
                                ("@form", "postfix"),
                            ]
                        ),
                    ),
                ]
            )
        },
    ),
    ("subscript", "a_b", {"msub": MultiDict([("mi", "a"), ("mi", "b")])}),
    ("superscript", "a^b", {"msup": MultiDict([("mi", "a"), ("mi", "b")])}),
    (
        "subscript and superscript",
        "a_b^c",
        {"msubsup": MultiDict([("mi", "a"), ("mi", "b"), ("mi", "c")])},
    ),
    (
        "superscript and subscript",
        "a^b_c",
        {"msubsup": MultiDict([("mi", "a"), ("mi", "c"), ("mi", "b")])},
    ),
    (
        "subscript within curly braces",
        "{a_b}",
        {"mrow": {"msub": MultiDict([("mi", "a"), ("mi", "b")])}},
    ),
    (
        "superscript within curly braces",
        "{a^b}",
        {"mrow": {"msup": MultiDict([("mi", "a"), ("mi", "b")])}},
    ),
    (
        "superscript, subscript and curly braces",
        "a^{i+1}_3",
        {
            "msubsup": MultiDict(
                [
                    ("mi", "a"),
                    ("mn", "3"),
                    (
                        "mrow",
                        MultiDict([("mi", "i"), ("mo", "&#x0002B;"), ("mn", "1")]),
                    ),
                ]
            )
        },
    ),
    (
        "simple fraction",
        r"\frac{1}{2}",
        {"mfrac": MultiDict([("mrow", {"mn": "1"}), ("mrow", {"mn": "2"})])},
    ),
    ("square root", r"\sqrt{2}", {"msqrt": {"mrow": {"mn": "2"}}}),
    (
        "root",
        r"\sqrt[3]{2}",
        {"mroot": MultiDict([("mrow", {"mn": "2"}), ("mrow", {"mn": "3"})])},
    ),
    (
        "binomial",
        r"\binom{2}{3}",
        MultiDict(
            [
                ("mo", "&#x00028;"),
                (
                    "mfrac",
                    MultiDict(
                        [
                            ("@linethickness", "0"),
                            ("mrow", {"mn": "2"}),
                            ("mrow", {"mn": "3"}),
                        ]
                    ),
                ),
                ("mo", "&#x00029;"),
            ]
        ),
    ),
    (
        "left and right",
        r"\left(x\right)",
        MultiDict(
            [
                (
                    "mrow",
                    MultiDict(
                        [
                            (
                                "mo",
                                MultiDict(
                                    [
                                        ("@stretchy", "true"),
                                        ("@fence", "true"),
                                        ("@form", "prefix"),
                                        ("$", "&#x00028;"),
                                    ]
                                ),
                            ),
                            ("mrow", {"mi": "x"}),
                            (
                                "mo",
                                MultiDict(
                                    [
                                        ("@stretchy", "true"),
                                        ("@fence", "true"),
                                        ("@form", "postfix"),
                                        ("$", "&#x00029;"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    ("space", r"\,", {"mspace": {"@width": "0.167em"}}),
    (
        "overline",
        r"\overline{a}",
        {
            "mover": MultiDict(
                [("mrow", {"mi": "a"}), ("mo", {"@stretchy": "true", "$": "&#x000AF;"})]
            )
        },
    ),
    (
        "underline",
        r"\underline{a}",
        {
            "munder": MultiDict(
                [("mrow", {"mi": "a"}), ("mo", {"@stretchy": "true", "$": "&#x00332;"})]
            )
        },
    ),
    (
        "matrix",
        r"\begin{matrix}a & b \\ c & d \end{matrix}",
        {
            "mtable": MultiDict(
                [
                    ("mtr", MultiDict([("mtd", {"mi": "a"}), ("mtd", {"mi": "b"})]),),
                    ("mtr", MultiDict([("mtd", {"mi": "c"}), ("mtd", {"mi": "d"})]),),
                ]
            ),
        },
    ),
    (
        "matrix without begin and end",
        r"\matrix{a & b \\ c & d}",
        {
            "mtable": MultiDict(
                [
                    ("mtr", MultiDict([("mtd", {"mi": "a"}), ("mtd", {"mi": "b"})]),),
                    ("mtr", MultiDict([("mtd", {"mi": "c"}), ("mtd", {"mi": "d"})]),),
                ]
            ),
        },
    ),
    (
        "matrix with alignment",
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
    ),
    (
        "matrix with negative sign",
        r"\begin{matrix}-a & b \\ c & d \end{matrix}",
        {
            "mtable": MultiDict(
                [
                    (
                        "mtr",
                        MultiDict(
                            [
                                ("mtd", MultiDict([("mo", "&#x02212;"), ("mi", "a")])),
                                ("mtd", {"mi": "b"}),
                            ]
                        ),
                    ),
                    ("mtr", MultiDict([("mtd", {"mi": "c"}), ("mtd", {"mi": "d"})]),),
                ]
            ),
        },
    ),
    (
        "pmatrix",
        r"\begin{pmatrix}a & b \\ c & d \end{pmatrix}",
        MultiDict(
            [
                ("mo", "&#x00028;"),
                (
                    "mtable",
                    MultiDict(
                        [
                            (
                                "mtr",
                                MultiDict([("mtd", {"mi": "a"}), ("mtd", {"mi": "b"})]),
                            ),
                            (
                                "mtr",
                                MultiDict([("mtd", {"mi": "c"}), ("mtd", {"mi": "d"})]),
                            ),
                        ]
                    ),
                ),
                ("mo", "&#x00029;"),
            ]
        ),
    ),
    (
        "simple array",
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
    ),
    (
        "array with vertical bar",
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
    ),
    (
        "array with horizontal lines",
        r"\begin{array}{cr} 1 & 2 \\ 3 & 4 \\ \hline 5 & 6 \end{array}",
        {
            "mtable": MultiDict(
                [
                    ("@rowlines", "none solid"),
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
                ]
            )
        },
    ),
    (
        "issue #33",
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
                                                                [
                                                                    ("mn", "1"),
                                                                    ("mi", ","),
                                                                    ("mn", "1"),
                                                                ]
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
                                                                [
                                                                    ("mn", "1"),
                                                                    ("mi", ","),
                                                                    ("mn", "2"),
                                                                ]
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
                                                                [
                                                                    ("mn", "1"),
                                                                    ("mi", ","),
                                                                    ("mi", "n"),
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
                                                                [
                                                                    ("mn", "2"),
                                                                    ("mi", ","),
                                                                    ("mn", "1"),
                                                                ]
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
                                                                [
                                                                    ("mn", "2"),
                                                                    ("mi", ","),
                                                                    ("mn", "2"),
                                                                ]
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
                                                                [
                                                                    ("mn", "2"),
                                                                    ("mi", ","),
                                                                    ("mi", "n"),
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
                                                                [
                                                                    ("mi", "m"),
                                                                    ("mi", ","),
                                                                    ("mn", "1"),
                                                                ]
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
                                                                [
                                                                    ("mi", "m"),
                                                                    ("mi", ","),
                                                                    ("mn", "2"),
                                                                ]
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
                                                                [
                                                                    ("mi", "m"),
                                                                    ("mi", ","),
                                                                    ("mi", "n"),
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
                ),
                ("mo", "&#x0005D;"),
            ]
        ),
    ),
    (
        "issue #42",
        r"\sqrt { ( - 25 ) ^ { 2 } } = \pm 25",
        MultiDict(
            [
                (
                    "msqrt",
                    {
                        "mrow": MultiDict(
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
                                                                "$": "&#x00028;",
                                                                "@stretchy": "false",
                                                            },
                                                        ),
                                                        ("mo", {"$": "&#x02212;"}),
                                                        ("mn", {"$": "25"}),
                                                        (
                                                            "mo",
                                                            {
                                                                "$": "&#x00029;",
                                                                "@stretchy": "false",
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            ("mrow", {"mn": {"$": "2"}}),
                                        ]
                                    ),
                                ),
                            ]
                        )
                    },
                ),
                ("mo", {"$": "&#x0003D;"}),
                ("mi", {"$": "&#x000B1;"}),
                ("mn", {"$": "25"}),
            ]
        ),
    ),
    (
        "issue #45 lt",
        "2 < 5",
        MultiDict([("mn", {"$": "2"}), ("mo", {"$": "&lt;"}), ("mn", {"$": "5"})]),
    ),
    (
        "issue #45 gt",
        "2 > 5",
        MultiDict([("mn", {"$": "2"}), ("mo", {"$": "&gt;"}), ("mn", {"$": "5"})]),
    ),
    ("issue #45 amp", "&", {"mo": "&amp;"}),
    (
        "issue #44",
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
                                            MultiDict(
                                                [
                                                    ("@stretchy", "true"),
                                                    ("@fence", "true"),
                                                    ("@form", "prefix"),
                                                    ("$", "&#x00028;"),
                                                ]
                                            ),
                                        ),
                                        (
                                            "mrow",
                                            MultiDict(
                                                [
                                                    ("mo", "&#x02212;"),
                                                    (
                                                        "msup",
                                                        MultiDict(
                                                            [
                                                                ("mi", "x"),
                                                                ("mrow", {"mn": "3"},),
                                                            ]
                                                        ),
                                                    ),
                                                    ("mo", "&#x0002B;"),
                                                    ("mn", "5"),
                                                ]
                                            ),
                                        ),
                                        (
                                            "mo",
                                            MultiDict(
                                                [
                                                    ("@stretchy", "true"),
                                                    ("@fence", "true"),
                                                    ("@form", "postfix"),
                                                    ("$", "&#x00029;"),
                                                ]
                                            ),
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
    ),
    ("issue #51", r"\mathbb{R}", {"mi": "&#x0211D;"}),
    (
        "issue #60-1",
        r"\mathrm{...}",
        {"mrow": MultiDict([("mo", "."), ("mo", "."), ("mo", ".")])},
    ),
    (
        "issue #52",
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
    ),
    (
        "issue #60-2",
        r"\mathrm{...}+\mathrm{...}",
        MultiDict(
            [
                ("mrow", MultiDict([("mo", "."), ("mo", "."), ("mo", ".")])),
                ("mo", "&#x0002B;"),
                ("mrow", MultiDict([("mo", "."), ("mo", "."), ("mo", ".")])),
            ]
        ),
    ),
    (
        "issue #61",
        r"\frac{x + 4}{x + \frac{123 \left(\sqrt{x} + 5\right)}{x + 4} - 8}",
        {
            "mfrac": MultiDict(
                [
                    (
                        "mrow",
                        MultiDict([("mi", "x"), ("mo", "&#x0002B;"), ("mn", "4")]),
                    ),
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
                                                                        MultiDict(
                                                                            [
                                                                                (
                                                                                    "@stretchy",
                                                                                    "true",
                                                                                ),
                                                                                (
                                                                                    "@fence",
                                                                                    "true",
                                                                                ),
                                                                                (
                                                                                    "@form",
                                                                                    "prefix",
                                                                                ),
                                                                                (
                                                                                    "$",
                                                                                    "&#x00028;",
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "mrow",
                                                                        MultiDict(
                                                                            [
                                                                                (
                                                                                    "msqrt",
                                                                                    {
                                                                                        "mrow": {
                                                                                            "mi": "x"
                                                                                        }
                                                                                    },
                                                                                ),
                                                                                (
                                                                                    "mo",
                                                                                    "&#x0002B;",
                                                                                ),
                                                                                (
                                                                                    "mn",
                                                                                    "5",
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "mo",
                                                                        MultiDict(
                                                                            [
                                                                                (
                                                                                    "@stretchy",
                                                                                    "true",
                                                                                ),
                                                                                (
                                                                                    "@fence",
                                                                                    "true",
                                                                                ),
                                                                                (
                                                                                    "@form",
                                                                                    "postfix",
                                                                                ),
                                                                                (
                                                                                    "$",
                                                                                    "&#x00029;",
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
                                            (
                                                "mrow",
                                                MultiDict(
                                                    [
                                                        ("mi", "x"),
                                                        ("mo", "&#x0002B;"),
                                                        ("mn", "4"),
                                                    ]
                                                ),
                                            ),
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
    ),
    (
        "issue #63",
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
                                                MultiDict(
                                                    [
                                                        ("@stretchy", "true"),
                                                        ("@fence", "true"),
                                                        ("@form", "prefix"),
                                                        ("$", "&#x00028;"),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "mrow",
                                                {
                                                    "msup": MultiDict(
                                                        [
                                                            ("mi", "x"),
                                                            ("mrow", {"mn": 3}),
                                                        ]
                                                    )
                                                },
                                            ),
                                            (
                                                "mo",
                                                MultiDict(
                                                    [
                                                        ("@stretchy", "true"),
                                                        ("@fence", "true"),
                                                        ("@form", "postfix"),
                                                        ("$", "&#x00029;"),
                                                    ]
                                                ),
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
    ),
    (r"empty subscript", r"1_{}", {"msub": MultiDict([("mn", "1"), ("mrow", {})])}),
    (
        r"\Bmatrix",
        r"\begin{Bmatrix}\end{Bmatrix}",
        MultiDict([("mo", "&#x0007B;"), ("mtable", {}), ("mo", "&#x0007D;")]),
    ),
    (
        r"\vmatrix",
        r"\begin{vmatrix}\end{vmatrix}",
        MultiDict([("mo", "&#x0007C;"), ("mtable", {}), ("mo", "&#x0007C;")]),
    ),
    (
        r"\Vmatrix",
        r"\begin{Vmatrix}\end{Vmatrix}",
        MultiDict([("mo", "&#x02016;"), ("mtable", {}), ("mo", "&#x02016;")]),
    ),
    (
        r"command inside matrix",
        r"\begin{matrix}1^2\end{matrix}",
        {"mtable": {"mtr": {"mtd": {"msup": MultiDict([("mn", "1"), ("mn", "2")])}}}},
    ),
    (r"\e", r"\e", {"mi": r"\e"}),
    (
        "issue #77",
        r"\left[\begin{matrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\0 & 0 & 1 & 0\\0 & 0 & 0 & 1\end{matrix}\right]",
        {
            "mrow": MultiDict(
                [
                    (
                        "mo",
                        MultiDict(
                            [
                                ("@stretchy", "true"),
                                ("@fence", "true"),
                                ("@form", "prefix"),
                                ("$", "["),
                            ]
                        ),
                    ),
                    (
                        "mrow",
                        {
                            "mtable": MultiDict(
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
                            )
                        },
                    ),
                    (
                        "mo",
                        MultiDict(
                            [
                                ("@stretchy", "true"),
                                ("@fence", "true"),
                                ("@form", "postfix"),
                                ("$", "]"),
                            ]
                        ),
                    ),
                ]
            )
        },
    ),
    (r"logarithm", r"\log{x}", MultiDict([("mi", "log"), ("mrow", {"mi": "x"})])),
    (
        r"logarithm with base",
        r"\log_2{x}",
        MultiDict(
            [("msub", MultiDict([("mi", "log"), ("mn", "2")])), ("mrow", {"mi": "x"})]
        ),
    ),
    (
        "exponent without base works",
        "^3",
        MultiDict([("msup", MultiDict([("mi", ""), ("mn", "3")]))]),
    ),
    (
        "limit at plus infinity",
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
                                    [
                                        ("mi", "x"),
                                        ("mo", "&#x02192;"),
                                        ("mo", "&#x0002B;"),
                                        ("mo", "&#x0221E;"),
                                    ]
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
    ),
    (
        "inf",
        r"\inf_{x > s}f(x)",
        MultiDict(
            [
                (
                    "munder",
                    MultiDict(
                        [
                            ("mo", "inf"),
                            (
                                "mrow",
                                MultiDict([("mi", "x"), ("mo", "&gt;"), ("mi", "s")]),
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
    ),
    (
        "issue #76",
        r"\int\limits_{0}^{\pi}",
        MultiDict(
            [
                (
                    "munderover",
                    MultiDict(
                        [
                            ("mo", "&#x0222B;"),
                            ("mrow", MultiDict([("mn", "0")])),
                            ("mrow", MultiDict([("mi", "&#x003C0;")])),
                        ]
                    ),
                ),
            ]
        ),
    ),
    (
        "issue #75 - 1 row",
        r"\substack{ \xi{2}=g{\left(x \right)}}",
        {
            "mstyle": {
                "@scriptlevel": "1",
                "mtable": {
                    "mtr": {
                        "mtd": MultiDict(
                            [
                                ("mi", "&#x003BE;"),
                                ("mn", "2"),
                                ("mo", "&#x0003D;"),
                                ("mi", "g"),
                                (
                                    "mrow",
                                    MultiDict(
                                        [
                                            (
                                                "mo",
                                                MultiDict(
                                                    [
                                                        ("@stretchy", "true"),
                                                        ("@fence", "true"),
                                                        ("@form", "prefix"),
                                                        ("$", "&#x00028;"),
                                                    ]
                                                ),
                                            ),
                                            ("mrow", {"mi": "x"}),
                                            (
                                                "mo",
                                                MultiDict(
                                                    [
                                                        ("@stretchy", "true"),
                                                        ("@fence", "true"),
                                                        ("@form", "postfix"),
                                                        ("$", "&#x00029;"),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        )
                    }
                },
            }
        },
    ),
    (
        "issue #75 - 2 rows",
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
                                            {
                                                "mtd": MultiDict(
                                                    [
                                                        ("mi", "i"),
                                                        ("mo", "&#x02260;"),
                                                        ("mi", "j"),
                                                    ]
                                                )
                                            },
                                        ),
                                    ]
                                ),
                            }
                        },
                    ),
                ]
            )
        },
    ),
    (
        "issue #91",
        r"\tan x + \sec x + \cos x + \sin x + \cot x + \csc x",
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
            ]
        ),
    ),
]


@pytest.mark.parametrize(
    "name, latex, json", ids=[x[0] for x in PARAMS], argvalues=PARAMS,
)
def test_converter(name: str, latex: str, json: MultiDict):
    parent = {
        "math": {
            "@xmlns": "http://www.w3.org/1998/Math/MathML",
            "@display": "inline",
            "mrow": json,
        }
    }
    bf = BadgerFish(dict_type=MultiDict)
    math = bf.etree(parent)
    assert convert(latex) == _convert(math[0])


@pytest.mark.skipif(
    sys.version_info < (3, 8), reason="xml.etree sorts attributes in 3.7 and below"
)
def test_attributes():
    assert (
        convert("1")
        == '<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><mrow><mn>1</mn></mrow></math>'
    )
    assert (
        convert("1", display="block")
        == '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mn>1</mn></mrow></math>'
    )
