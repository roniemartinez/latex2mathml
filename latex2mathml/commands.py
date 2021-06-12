from collections import OrderedDict, defaultdict
from typing import DefaultDict, Dict, Optional, Tuple

OPENING_BRACE = "{"
CLOSING_BRACE = "}"
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
APOSTROPHE = "'"
PRIME = r"\prime"
DPRIME = r"\dprime"

LEFT = r"\left"
RIGHT = r"\right"

ABOVE = r"\above"
ABOVEWITHDELIMS = r"\abovewithdelims"
ATOP = r"\atop"
ATOPWITHDELIMS = r"\atopwithdelims"
BINOM = r"\binom"
BRACE = r"\brace"
BRACK = r"\brack"
CFRAC = r"\cfrac"
CHOOSE = r"\choose"
DBINOM = r"\dbinom"
DFRAC = r"\dfrac"
FRAC = r"\frac"
OVER = r"\over"

ROOT = r"\root"
SQRT = r"\sqrt"

OVERSET = r"\overset"
UNDERSET = r"\underset"

ACUTE = r"\acute"
BAR = r"\bar"
BREVE = r"\breve"
CHECK = r"\check"
DOT = r"\dot"
DDOT = r"\ddot"
DDDOT = r"\dddot"
DDDDOT = r"\ddddot"
OVERLINE = r"\overline"
OVERRIGHTARROW = r"\overrightarrow"
UNDERLINE = r"\underline"
VEC = r"\vec"

TEXT = r"\text"

MATH = r"\math"
MATHOP = r"\mathop"

BEGIN = r"\begin"
END = r"\end"

LIMITS = r"\limits"
INTEGRAL = r"\int"
SUMMATION = r"\sum"
LIMIT = (r"\lim", r"\sup", r"\inf", r"\max", r"\min")

OPERATORNAME = r"\operatorname"

LBRACE = r"\{"

FUNCTIONS = (
    r"\arccos",
    r"\arcsin",
    r"\arctan",
    r"\cos",
    r"\cosh",
    r"\cot",
    r"\coth",
    r"\csc",
    r"\deg",
    r"\dim",
    r"\exp",
    r"\ln",
    r"\log",
    r"\sec",
    r"\sin",
    r"\tan",
)
DETERMINANT = r"\det"

HLINE = r"\hline"

CASES = r"\cases"
DISPLAYLINES = r"\displaylines"
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
    DISPLAYLINES,
)

BACKSLASH = "\\"
CARRIAGE_RETURN = r"\cr"

COLON = r"\:"
COMMA = r"\,"
DOUBLEBACKSLASH = r"\\"
ENSPACE = r"\enspace"
EXCLAMATION = r"\!"
GREATER_THAN = r"\>"
HSPACE = r"\hspace"
QQUAD = r"\qquad"
QUAD = r"\quad"
SEMICOLON = r"\;"

BLACKBOARD_BOLD = r"\Bbb"
BOLD_SYMBOL = r"\boldsymbol"

BOXED = r"\boxed"

COLOR = r"\color"
DISPLAYSTYLE = r"\displaystyle"


def font_factory(default: Optional[str], replacement: Dict[str, Optional[str]]) -> DefaultDict[str, Optional[str]]:
    fonts = defaultdict(lambda: default, replacement)
    return fonts


LOCAL_FONTS: Dict[str, DefaultDict[str, Optional[str]]] = {
    BLACKBOARD_BOLD: font_factory("double-struck", {"fence": None}),
    BOLD_SYMBOL: font_factory("bold", {"mi": "bold-italic", "mtext": None}),
}

OLD_STYLE_FONTS: Dict[str, DefaultDict[str, Optional[str]]] = {
    r"\rm": font_factory(None, {"mi": "normal"}),
    r"\bf": font_factory(None, {"mi": "bold"}),
    r"\it": font_factory(None, {"mi": "italic"}),
    r"\sf": font_factory(None, {"mi": "sans-serif"}),
    r"\tt": font_factory(None, {"mi": "monospace"}),
}

GLOBAL_FONTS = {
    **OLD_STYLE_FONTS,
    r"\cal": font_factory("script", {"fence": None}),
}

COMMANDS_WITH_ONE_PARAMETER = (
    ACUTE,
    BAR,
    BLACKBOARD_BOLD,
    BOLD_SYMBOL,
    BOXED,
    BREVE,
    CHECK,
    DOT,
    DDOT,
    DDDOT,
    DDDDOT,
    MATHOP,
    OVERLINE,
    OVERRIGHTARROW,
    UNDERLINE,
    VEC,
)
COMMANDS_WITH_TWO_PARAMETERS = (
    BINOM,
    CFRAC,
    DBINOM,
    DFRAC,
    FRAC,
    OVERSET,
    UNDERSET,
)

BIG: Dict[str, Tuple[str, dict]] = {
    # command: (mathml_equivalent, attributes)
    r"\Bigg": ("mo", OrderedDict([("minsize", "2.470em"), ("maxsize", "2.470em")])),
    r"\bigg": ("mo", OrderedDict([("minsize", "2.047em"), ("maxsize", "2.047em")])),
    r"\Big": ("mo", OrderedDict([("minsize", "1.623em"), ("maxsize", "1.623em")])),
    r"\big": ("mo", OrderedDict([("minsize", "1.2em"), ("maxsize", "1.2em")])),
}

CONVERSION_MAP: Dict[str, Tuple[str, dict]] = {
    # command: (mathml_equivalent, attributes)
    # tables
    **{matrix: ("mtable", {}) for matrix in MATRICES},
    DISPLAYLINES: ("mtable", {"rowspacing": "0.5em", "columnspacing": "1em", "displaystyle": "true"}),
    # subscripts/superscripts
    SUBSCRIPT: ("msub", {}),
    SUPERSCRIPT: ("msup", {}),
    SUBSUP: ("msubsup", {}),
    # fractions
    FRAC: ("mfrac", {}),
    BINOM: ("mfrac", {"linethickness": "0"}),
    CFRAC: ("mfrac", {}),
    DBINOM: ("mfrac", {"linethickness": "0"}),
    DFRAC: ("mfrac", {}),
    # over/under
    ACUTE: ("mover", {}),
    BAR: ("mover", {}),
    BREVE: ("mover", {}),
    CHECK: ("mover", {}),
    DOT: ("mover", {}),
    DDOT: ("mover", {}),
    DDDOT: ("mover", {}),
    DDDDOT: ("mover", {}),
    LIMITS: ("munderover", {}),
    OVERLINE: ("mover", {}),
    OVERRIGHTARROW: ("mover", {}),
    OVERSET: ("mover", {}),
    UNDERLINE: ("munder", {}),
    UNDERSET: ("munder", {}),
    VEC: ("mover", {}),
    # spaces
    COLON: ("mspace", {"width": "0.222em"}),
    COMMA: ("mspace", {"width": "0.167em"}),
    DOUBLEBACKSLASH: ("mspace", {"linebreak": "newline"}),
    ENSPACE: ("mspace", {"width": "0.5em"}),
    EXCLAMATION: ("mspace", {"width": "negativethinmathspace"}),
    GREATER_THAN: ("mspace", {"width": "0.222em"}),
    HSPACE: ("mspace", {}),
    QQUAD: ("mspace", {"width": "2em"}),
    QUAD: ("mspace", {"width": "1em"}),
    SEMICOLON: ("mspace", {"width": "0.278em"}),
    # enclose
    BOXED: ("menclose", {"notation": "box"}),
    # operators
    **BIG,
    **{limit: ("mo", {}) for limit in LIMIT},
    LEFT: ("mo", OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "prefix")])),
    RIGHT: ("mo", OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "postfix")])),
    # styles
    COLOR: ("mstyle", {}),
    DISPLAYSTYLE: ("mstyle", {"displaystyle": "true", "scriptlevel": "0"}),
    # others
    SQRT: ("msqrt", {}),
    ROOT: ("mroot", {}),
    TEXT: ("mtext", {}),
    MATHOP: ("mrow", {}),
}

DIACRITICS: Dict[str, Tuple[str, Dict[str, str]]] = {
    OVERLINE: ("&#x000AF;", {"stretchy": "true"}),
    BAR: ("&#x000AF;", {"stretchy": "true"}),
    UNDERLINE: ("&#x00332;", {"stretchy": "true"}),
    OVERRIGHTARROW: ("&#x02192;", {"stretchy": "true"}),
    VEC: ("&#x02192;", {"stretchy": "true"}),
    ACUTE: ("&#x000B4;", {}),
    BREVE: ("&#x002D8;", {}),
    CHECK: ("&#x002C7;", {}),
    DOT: ("&#x002D9;", {}),
    DDOT: ("&#x000A8;", {}),
    DDDOT: ("&#x020DB;", {}),
    DDDDOT: ("&#x020DC;", {}),
}
