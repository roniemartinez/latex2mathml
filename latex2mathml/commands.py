#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from collections import OrderedDict
from typing import Dict, Tuple

MATRICES = (
    r"\matrix",
    r"\matrix*",
    r"\pmatrix",
    r"\pmatrix*",
    r"\bmatrix",
    r"\bmatrix*",
    r"\Bmatrix",
    r"\Bmatrix*",
    r"\vmatrix",
    r"\vmatrix*",
    r"\Vmatrix",
    r"\Vmatrix*",
    r"\array",
)

SPACES = (r"\,", r"\:", r"\;", r"\\", r"\quad", r"\qquad")

COMMANDS = {
    # command: (params_count, mathml_equivalent, attributes)
    "_": (2, "msub", {}),
    "^": (2, "msup", {}),
    "_^": (3, "msubsup", {}),
    r"\frac": (2, "mfrac", {}),
    r"\sqrt": (1, "msqrt", {}),
    r"\root": (2, "mroot", {}),
    r"\binom": (2, "mfrac", {"linethickness": "0"}),
    r"\left": (
        1,
        "mo",
        OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "prefix")]),
    ),
    r"\right": (
        1,
        "mo",
        OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "postfix")]),
    ),
    r"\overline": (1, "mover", {}),
    r"\bar": (1, "mover", {}),
    r"\underline": (1, "munder", {}),
}  # type: Dict[str, Tuple[int, str, dict]]

for space in SPACES:
    COMMANDS[space] = (0, "mspace", {"width": "0.167em"})

for matrix in MATRICES:
    COMMANDS[matrix] = (1, "mtable", {})
