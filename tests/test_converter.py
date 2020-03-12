#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"

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
    ("numbers and identifiers", "12x", {"mn": "12", "mi": "x"}),
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
                                                "msub": {
                                                    "mi": "a",
                                                    "mrow": MultiDict(
                                                        [
                                                            ("mn", "1"),
                                                            ("mi", ","),
                                                            ("mn", "1"),
                                                        ]
                                                    ),
                                                }
                                            },
                                        ),
                                        (
                                            "mtd",
                                            {
                                                "msub": {
                                                    "mi": "a",
                                                    "mrow": MultiDict(
                                                        [
                                                            ("mn", "1"),
                                                            ("mi", ","),
                                                            ("mn", "2"),
                                                        ]
                                                    ),
                                                }
                                            },
                                        ),
                                        ("mtd", {"mo": "&#x022EF;"}),
                                        (
                                            "mtd",
                                            {
                                                "msub": {
                                                    "mi": "a",
                                                    "mrow": MultiDict(
                                                        [
                                                            ("mn", "1"),
                                                            ("mi", ","),
                                                            ("mi", "n"),
                                                        ]
                                                    ),
                                                }
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
                                                "msub": {
                                                    "mi": "a",
                                                    "mrow": MultiDict(
                                                        [
                                                            ("mn", "2"),
                                                            ("mi", ","),
                                                            ("mn", "1"),
                                                        ]
                                                    ),
                                                }
                                            },
                                        ),
                                        (
                                            "mtd",
                                            {
                                                "msub": {
                                                    "mi": "a",
                                                    "mrow": MultiDict(
                                                        [
                                                            ("mn", "2"),
                                                            ("mi", ","),
                                                            ("mn", "2"),
                                                        ]
                                                    ),
                                                }
                                            },
                                        ),
                                        ("mtd", {"mo": "&#x022EF;"}),
                                        (
                                            "mtd",
                                            {
                                                "msub": {
                                                    "mi": "a",
                                                    "mrow": MultiDict(
                                                        [
                                                            ("mn", "2"),
                                                            ("mi", ","),
                                                            ("mi", "n"),
                                                        ]
                                                    ),
                                                }
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
                                                "msub": {
                                                    "mi": "a",
                                                    "mrow": MultiDict(
                                                        [
                                                            ("mi", "m"),
                                                            ("mi", ","),
                                                            ("mn", "1"),
                                                        ]
                                                    ),
                                                }
                                            },
                                        ),
                                        (
                                            "mtd",
                                            {
                                                "msub": {
                                                    "mi": "a",
                                                    "mrow": MultiDict(
                                                        [
                                                            ("mi", "m"),
                                                            ("mi", ","),
                                                            ("mn", "2"),
                                                        ]
                                                    ),
                                                }
                                            },
                                        ),
                                        ("mtd", {"mo": "&#x022EF;"}),
                                        (
                                            "mtd",
                                            {
                                                "msub": {
                                                    "mi": "a",
                                                    "mrow": MultiDict(
                                                        [
                                                            ("mi", "m"),
                                                            ("mi", ","),
                                                            ("mi", "n"),
                                                        ]
                                                    ),
                                                }
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
    # (
    #     "issue #42",
    #     r"\sqrt { ( - 25 ) ^ { 2 } } = \pm 25",
    #     MultiDict(
    #         [
    #             (
    #                 "msqrt",
    #                 {
    #                     "mrow": MultiDict(
    #                         [
    #                             ("mo", {"$": "&#x00028;"}),
    #                             ("mo", {"$": "&#x02212;"}),
    #                             ("mn", {"$": "25"}),
    #                             (
    #                                 "msup",
    #                                 {
    #                                     "mo": {"$": "&#x00029;"},
    #                                     "mrow": {"mn": {"$": "2"}},
    #                                 },
    #                             ),
    #                         ]
    #                     )
    #                 },
    #             ),
    #             ("mo", {"$": "&#x0003D;"}),
    #             ("mi", {"$": "&#x000B1;"}),
    #             ("mn", {"$": "25"}),
    #         ]
    #     ),
    # ),
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
                                                            {
                                                                "mi": "x",
                                                                "mrow": {"mn": "3"},
                                                            },
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
            )
        },
    ),
    ("issue #51", r"\mathbb{R}", {"mi": "&#x0211D;"}),
    (
        "issue #60-1",
        r"\mathrm{...}",
        {"mrow": MultiDict([("mo", "."), ("mo", "."), ("mo", ".")])},
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
                    ("mrow", {"mi": "x", "mo": "&#x0002B;", "mn": "4"}),
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
                                                {
                                                    "mn": "123",
                                                    "mrow": MultiDict(
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
                                                                {
                                                                    "msqrt": {
                                                                        "mrow": {
                                                                            "mi": "x"
                                                                        }
                                                                    },
                                                                    "mo": "&#x0002B;",
                                                                    "mn": "5",
                                                                },
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
                                                },
                                            ),
                                            (
                                                "mrow",
                                                {
                                                    "mi": "x",
                                                    "mo": "&#x0002B;",
                                                    "mn": "4",
                                                },
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
                        "mrow": {
                            "mrow": MultiDict(
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
                                    ("mrow", {"msup": {"mi": "x", "mrow": {"mn": 3}}}),
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
                                    ("mo", "&#x0002B;"),
                                    ("mi", "v"),
                                ]
                            )
                        }
                    }
                }
            }
        },
    ),
]


@pytest.mark.parametrize(
    "name, latex, json", ids=[x[0] for x in PARAMS], argvalues=PARAMS,
)
def test_converter(name: str, latex: str, json: MultiDict):
    parent = {"math": {"@xmlns": "http://www.w3.org/1998/Math/MathML", "mrow": json}}
    bf = BadgerFish(dict_type=MultiDict)
    math = bf.etree(parent)
    assert _convert(math[0]) == convert(latex), name
