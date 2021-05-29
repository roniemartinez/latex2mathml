from collections import OrderedDict
from typing import Dict, Tuple

OPENING_BRACES = "{"
CLOSING_BRACES = "}"
BRACES = "{}"

OPENING_BRACKET = "["
CLOSING_BRACKET = "]"
BRACKETS = "[]"

OPENING_PARENTHESIS = "("
CLOSING_PARENTHESIS = ")"
PARENTHESES = "()"

SUBSUP = "_^"
SUBSCRIPT = "_"
SUPERSCRIPT = "^"

LEFT = r"\left"
RIGHT = r"\right"
OVER = r"\over"
FRAC = r"\frac"
BINOM = r"\binom"
ROOT = r"\root"
SQRT = r"\sqrt"

OVERSET = r"\overset"
UNDERSET = r"\underset"

OVERLINE = r"\overline"
BAR = r"\bar"
UNDERLINE = r"\underline"
OVERRIGHTARROW = r"\overrightarrow"
VEC = r"\vec"
DOT = r"\dot"
TEXT = r"\text"
MATHOP = r"\mathop"

BEGIN = r"\begin"
END = r"\end"

LIMITS = r"\limits"
INTEGRAL = r"\int"
SUMMATION = r"\sum"
LIMIT = (r"\lim", r"\sup", r"\inf", r"\max", r"\min")

OPERATORNAME = r"\operatorname"

LBRACE = r"\{"

FUNCTIONS = (r"\log", r"\ln", r"\tan", r"\sec", r"\cos", r"\sin", r"\cot", r"\csc")

HLINE = r"\hline"

CASES = r"\cases"
SUBSTACK = r"\substack"
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
    SUBSTACK,
    CASES,
)

BACKSLASH = "\\"
DOUBLEBACKSLASH = r"\\"

QUAD = r"\quad"
QQUAD = r"\qquad"
HSPACE = r"\hspace"

SPACES = (r"\,", r"\:", r"\;", r"\\")

COMMANDS_WITH_ONE_PARAMETER = (OVERLINE, BAR, UNDERLINE, OVERRIGHTARROW, VEC, DOT, MATHOP, HSPACE)
COMMANDS_WITH_TWO_PARAMETERS = (FRAC, BINOM, OVERSET, UNDERSET)

CONVERSION_MAP: Dict[str, Tuple[str, dict]] = {
    # command: (mathml_equivalent, attributes)
    SUBSCRIPT: ("msub", {}),
    SUPERSCRIPT: ("msup", {}),
    SUBSUP: ("msubsup", {}),
    FRAC: ("mfrac", {}),
    SQRT: ("msqrt", {}),
    ROOT: ("mroot", {}),
    BINOM: ("mfrac", {"linethickness": "0"}),
    LEFT: ("mo", OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "prefix")])),
    RIGHT: ("mo", OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "postfix")])),
    OVERLINE: ("mover", {}),
    BAR: ("mover", {}),
    UNDERLINE: ("munder", {}),
    LIMITS: ("munderover", {}),
    OVERRIGHTARROW: ("mover", {}),
    VEC: ("mover", {}),
    DOT: ("mover", {}),
    OVERSET: ("mover", {}),
    UNDERSET: ("munder", {}),
    TEXT: ("mtext", {}),
    MATHOP: ("mrow", {}),
    QUAD: ("mspace", {"width": "1em"}),
    QQUAD: ("mspace", {"width": "2em"}),
    HSPACE: ("mspace", {}),
}

for space in SPACES:
    CONVERSION_MAP[space] = ("mspace", {"width": "0.167em"})

for matrix in MATRICES:
    CONVERSION_MAP[matrix] = ("mtable", {})

for limit in LIMIT:
    CONVERSION_MAP[limit] = ("mo", {})
