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
    r"\substack",
    r"\cases",
)

SPACES = (r"\,", r"\:", r"\;", r"\\", r"\quad", r"\qquad")

COMMANDS: Dict[str, Tuple[int, str, dict]] = {
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
    r"\limits": (3, "munderover", {}),
    r"\overrightarrow": (1, "mover", {}),
    r"\vec": (1, "mover", {}),
    r"\dot": (1, "mover", {}),
    r"\text": (1, "mtext", {}),
}

LIMIT = (r"\lim", r"\sup", r"\inf", r"\max", r"\min")

for space in SPACES:
    COMMANDS[space] = (0, "mspace", {"width": "0.167em"})

for matrix in MATRICES:
    COMMANDS[matrix] = (1, "mtable", {})

for limit in LIMIT:
    COMMANDS[limit] = (1, "mo", {})
