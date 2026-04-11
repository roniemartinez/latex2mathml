from collections import OrderedDict, defaultdict
from typing import Optional

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
TRPRIME = r"\trprime"
QPRIME = r"\qprime"
PRIME_UPGRADE = {
    PRIME: DPRIME,
    DPRIME: TRPRIME,
    TRPRIME: QPRIME,
}

LEFT = r"\left"
MIDDLE = r"\middle"
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
GENFRAC = r"\genfrac"
OVER = r"\over"
TBINOM = r"\tbinom"
TFRAC = r"\tfrac"

ROOT = r"\root"
SQRT = r"\sqrt"

OVERSET = r"\overset"
STACKREL = r"\stackrel"
UNDERSET = r"\underset"

ACUTE = r"\acute"
BAR = r"\bar"
BREVE = r"\breve"
CHECK = r"\check"
DOT = r"\dot"
DDOT = r"\ddot"
DDDOT = r"\dddot"
DDDDOT = r"\ddddot"
GRAVE = r"\grave"
HAT = r"\hat"
MATHRING = r"\mathring"
OVERBRACE = r"\overbrace"
OVERBRACKET = r"\overbracket"
OVERLEFTARROW = r"\overleftarrow"
OVERLEFTRIGHTARROW = r"\overleftrightarrow"
OVERLINE = r"\overline"
OVERPAREN = r"\overparen"
OVERRIGHTARROW = r"\overrightarrow"
TILDE = r"\tilde"
UNDERBAR = r"\underbar"
UNDERBRACE = r"\underbrace"
UNDERBRACKET = r"\underbracket"
UNDERLEFTARROW = r"\underleftarrow"
UNDERLINE = r"\underline"
UNDERPAREN = r"\underparen"
UNDERRIGHTARROW = r"\underrightarrow"
UNDERLEFTRIGHTARROW = r"\underleftrightarrow"
VEC = r"\vec"
WIDECHECK = r"\widecheck"
WIDEHAT = r"\widehat"
WIDETILDE = r"\widetilde"
XLEFTARROW = r"\xleftarrow"
XLEFTHARPOONDOWN = r"\xleftharpoondown"
XLEFTHARPOONUP = r"\xleftharpoonup"
XLEFTRIGHTARROW = r"\xleftrightarrow"
XLEFTRIGHTHARPOONS = r"\xleftrightharpoons"
XLONGEQUAL = r"\xlongequal"
XMAPSTO = r"\xmapsto"
XRIGHTARROW = r"\xrightarrow"
XRIGHTHARPOONDOWN = r"\xrightharpoondown"
XRIGHTHARPOONUP = r"\xrightharpoonup"
XRIGHTLEFTHARPOONS = r"\xrightleftharpoons"
XTOFROM = r"\xtofrom"
XTWOHEADLEFTARROW = r"\xtwoheadleftarrow"
XTWOHEADRIGHTARROW = r"\xtwoheadrightarrow"
XHOOKLEFTARROW = r"\xhookleftarrow"
XHOOKRIGHTARROW = r"\xhookrightarrow"
XLEFTARROW_UPPER = r"\xLeftarrow"
XRIGHTARROW_UPPER = r"\xRightarrow"
XLEFTRIGHTARROW_UPPER = r"\xLeftrightarrow"

EXTENSIBLE_ARROWS: dict[str, str] = {
    XLEFTARROW: "&#x2190;",
    XLEFTHARPOONDOWN: "&#x21BD;",
    XLEFTHARPOONUP: "&#x21BC;",
    XLEFTRIGHTARROW: "&#x2194;",
    XLEFTRIGHTHARPOONS: "&#x21CB;",
    XLONGEQUAL: "&#x003D;",
    XMAPSTO: "&#x21A6;",
    XRIGHTARROW: "&#x2192;",
    XRIGHTHARPOONDOWN: "&#x21C1;",
    XRIGHTHARPOONUP: "&#x21C0;",
    XRIGHTLEFTHARPOONS: "&#x21CC;",
    XTOFROM: "&#x21C4;",
    XTWOHEADLEFTARROW: "&#x219E;",
    XTWOHEADRIGHTARROW: "&#x21A0;",
    XHOOKLEFTARROW: "&#x21A9;",
    XHOOKRIGHTARROW: "&#x21AA;",
    XLEFTARROW_UPPER: "&#x21D0;",
    XRIGHTARROW_UPPER: "&#x21D2;",
    XLEFTRIGHTARROW_UPPER: "&#x21D4;",
}

EMPH = r"\emph"
HREF = r"\href"
TEXT = r"\text"
TEXTBF = r"\textbf"
TEXTIT = r"\textit"
TEXTMD = r"\textmd"
TEXTNORMAL = r"\textnormal"
TEXTRM = r"\textrm"
TEXTSF = r"\textsf"
TEXTTT = r"\texttt"
TEXTUP = r"\textup"

BEGIN = r"\begin"
END = r"\end"

LIMITS = r"\limits"
NOLIMITS = r"\nolimits"
INTEGRAL = r"\int"
SUMMATION = r"\sum"
PRODUCT = r"\prod"
LIMIT = (r"\lim", r"\sup", r"\inf", r"\max", r"\min")

OPERATORNAME = r"\operatorname"
OPERATORNAMEWITHLIMITS = r"\operatornamewithlimits"

LBRACE = r"\{"

FUNCTIONS = (
    r"\arccos",
    r"\arcctg",
    r"\arcsin",
    r"\arctan",
    r"\arctg",
    r"\ch",
    r"\cos",
    r"\cosh",
    r"\cosec",
    r"\cot",
    r"\cotg",
    r"\coth",
    r"\csc",
    r"\ctg",
    r"\cth",
    r"\deg",
    r"\dim",
    r"\exp",
    r"\hom",
    r"\ker",
    r"\ln",
    r"\lg",
    r"\log",
    r"\sec",
    r"\sh",
    r"\sin",
    r"\sinh",
    r"\tan",
    r"\tanh",
    r"\tg",
    r"\th",
)
ARGMAX = r"\argmax"
ARGMIN = r"\argmin"
DETERMINANT = r"\det"
GCD = r"\gcd"
INTOP = r"\intop"
INJLIM = r"\injlim"
LIMINF = r"\liminf"
LIMSUP = r"\limsup"
PLIM = r"\plim"
PR = r"\Pr"
PROJLIM = r"\projlim"
VARINJLIM = r"\varinjlim"
VARLIMINF = r"\varliminf"
VARLIMSUP = r"\varlimsup"
VARPROJLIM = r"\varprojlim"
MOD = r"\mod"
PMOD = r"\pmod"
POD = r"\pod"
BMOD = r"\bmod"

HDASHLINE = r"\hdashline"
HLINE = r"\hline"
HFIL = r"\hfil"

CASES = r"\cases"
EQALIGN = r"\eqalign"
EQALIGNNO = r"\eqalignno"
DISPLAYLINES = r"\displaylines"
SMALLMATRIX = r"\smallmatrix"
SUBSTACK = r"\substack"
SPLIT = r"\split"
ALIGN = r"\align*"
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
    EQALIGN,
    EQALIGNNO,
    SMALLMATRIX,
    SPLIT,
    ALIGN,
)

BACKSLASH = "\\"
CARRIAGE_RETURN = r"\cr"

COLON = r"\:"
COMMA = r"\,"
DOUBLEBACKSLASH = r"\\"
ENSPACE = r"\enspace"
EXCLAMATION = r"\!"
GREATER_THAN = r"\>"
HSKIP = r"\hskip"
HSPACE = r"\hspace"
KERN = r"\kern"
MKERN = r"\mkern"
MSKIP = r"\mskip"
MSPACE = r"\mspace"
NEGTHINSPACE = r"\negthinspace"
NEGMEDSPACE = r"\negmedspace"
NEGTHICKSPACE = r"\negthickspace"
NOBREAKSPACE = r"\nobreakspace"
SPACE = r"\space"
SPACE_UPPER = r"\Space"
THICKSPACE = r"\thickspace"
THINSPACE = r"\thinspace"
QQUAD = r"\qquad"
QUAD = r"\quad"
SEMICOLON = r"\;"

BM = r"\bm"
BLACKBOARD_BOLD = r"\Bbb"
BOLD = r"\bold"
BOLD_SYMBOL = r"\boldsymbol"
MIT = r"\mit"
OLDSTYLE = r"\oldstyle"
PMB = r"\pmb"
SCR = r"\scr"
TT = r"\tt"

MATH = r"\math"
MATHBB = r"\mathbb"
MATHBF = r"\mathbf"
MATHCAL = r"\mathcal"
MATHFRAK = r"\mathfrak"
MATHIT = r"\mathit"
MATHRM = r"\mathrm"
MATHCHOICE = r"\mathchoice"
MATHBIN = r"\mathbin"
MATHCLOSE = r"\mathclose"
MATHINNER = r"\mathinner"
MATHNORMAL = r"\mathnormal"
MATHOP = r"\mathop"
MATHOPEN = r"\mathopen"
MATHORD = r"\mathord"
MATHPUNCT = r"\mathpunct"
MATHREL = r"\mathrel"
MATHSCR = r"\mathscr"
MATHSF = r"\mathsf"
MATHSFIT = r"\mathsfit"
MATHTT = r"\mathtt"

BRA = r"\bra"
BRAKET = r"\braket"
BCANCEL = r"\bcancel"
BOXED = r"\boxed"
CANCEL = r"\cancel"
CLASS = r"\class"
CLAP = r"\clap"
LLAP = r"\llap"
MATHCLAP = r"\mathclap"
MATHLLAP = r"\mathllap"
MATHRLAP = r"\mathrlap"
FBOX = r"\fbox"
HBOX = r"\hbox"
KET = r"\ket"
MBOX = r"\mbox"
RLAP = r"\rlap"

COLOR = r"\color"
COLORBOX = r"\colorbox"
FCOLORBOX = r"\fcolorbox"
TEXTCOLOR = r"\textcolor"
FOOTNOTESIZE = r"\footnotesize"
DISPLAYSTYLE = r"\displaystyle"
TEXTSTYLE = r"\textstyle"
SCRIPTSTYLE = r"\scriptstyle"
SCRIPTSCRIPTSTYLE = r"\scriptscriptstyle"
STYLE = r"\style"

HPHANTOM = r"\hphantom"
MATHSTRUT = r"\mathstrut"
PHANTOM = r"\phantom"
STRUT = r"\strut"
VCENTER = r"\vcenter"
VPHANTOM = r"\vphantom"

MATH_NON_FONT_COMMANDS = (
    MATHRING,
    MATHBIN,
    MATHCLOSE,
    MATHINNER,
    MATHOP,
    MATHOPEN,
    MATHORD,
    MATHPUNCT,
    MATHREL,
    MATHSTRUT,
)

IDOTSINT = r"\idotsint"
LATEX = r"\LaTeX"
TEX = r"\TeX"

LEFTROOT = r"\leftroot"
LOWER = r"\lower"
MOVELEFT = r"\moveleft"
MOVERIGHT = r"\moveright"
RAISE = r"\raise"
RULE = r"\rule"
SHOVELEFT = r"\shoveleft"
SHOVERIGHT = r"\shoveright"
SMASH = r"\smash"
SOUT = r"\sout"
SIDESET = r"\sideset"

SKEW = r"\skew"
TAG = r"\tag"
TAG_STAR = r"\tag*"
UNICODE = r"\unicode"
UPROOT = r"\uproot"
VERB = r"\verb"
XCANCEL = r"\xcancel"
NOT = r"\not"


def font_factory(default: Optional[str], replacement: dict[str, Optional[str]]) -> defaultdict[str, Optional[str]]:
    fonts = defaultdict(lambda: default, replacement)
    return fonts


LOCAL_FONTS: dict[str, defaultdict[str, Optional[str]]] = {
    BLACKBOARD_BOLD: font_factory("double-struck", {"fence": None}),
    BM: font_factory("bold-italic", {"fence": None}),
    BOLD: font_factory("bold", {"fence": None}),
    BOLD_SYMBOL: font_factory("bold", {"mi": "bold-italic", "mtext": None}),
    MATHBB: font_factory("double-struck", {"fence": None}),
    MATHBF: font_factory("bold", {"fence": None}),
    MATHCAL: font_factory("script", {"fence": None}),
    MATHFRAK: font_factory("fraktur", {"fence": None}),
    MATHIT: font_factory("italic", {"fence": None}),
    MATHRM: font_factory(None, {"mi": "normal"}),
    MATHSCR: font_factory("script", {"fence": None}),
    MATHSF: font_factory(None, {"mi": "sans-serif"}),
    MATHSFIT: font_factory(None, {"mi": "sans-serif-italic"}),
    MATHTT: font_factory("monospace", {"fence": None}),
    MATHNORMAL: font_factory(None, {"mi": "normal"}),
    MIT: font_factory("italic", {"fence": None, "mi": None}),
    OLDSTYLE: font_factory("normal", {"fence": None}),
    PMB: font_factory("bold", {"fence": None}),
    SCR: font_factory("script", {"fence": None}),
    TT: font_factory("monospace", {"fence": None}),
}

OLD_STYLE_FONTS: dict[str, defaultdict[str, Optional[str]]] = {
    r"\rm": font_factory(None, {"mi": "normal"}),
    r"\bf": font_factory(None, {"mi": "bold"}),
    r"\it": font_factory(None, {"mi": "italic"}),
    r"\sf": font_factory(None, {"mi": "sans-serif"}),
    r"\tt": font_factory(None, {"mi": "monospace"}),
}

GLOBAL_FONTS = {
    **OLD_STYLE_FONTS,
    r"\cal": font_factory("script", {"fence": None}),
    r"\frak": font_factory("fraktur", {"fence": None}),
}

COMMANDS_WITH_ONE_PARAMETER = (
    ACUTE,
    BAR,
    BCANCEL,
    BLACKBOARD_BOLD,
    BM,
    BOLD,
    BRA,
    BRAKET,
    BOLD_SYMBOL,
    BOXED,
    CANCEL,
    BREVE,
    CHECK,
    DOT,
    DDOT,
    DDDOT,
    DDDDOT,
    GRAVE,
    HAT,
    HPHANTOM,
    KET,
    MATHBIN,
    MATHCLAP,
    MATHCLOSE,
    MATHINNER,
    MATHLLAP,
    MATHOP,
    MATHOPEN,
    MATHORD,
    MATHPUNCT,
    MATHREL,
    MATHRLAP,
    MATHRING,
    MIT,
    MOD,
    OLDSTYLE,
    OVERBRACE,
    OVERBRACKET,
    OVERLEFTARROW,
    OVERLEFTRIGHTARROW,
    OVERLINE,
    OVERPAREN,
    OVERRIGHTARROW,
    PHANTOM,
    PMB,
    UNICODE,
    PMOD,
    POD,
    SCR,
    SHOVELEFT,
    SHOVERIGHT,
    SOUT,
    TILDE,
    TT,
    UNDERBAR,
    UNDERBRACE,
    UNDERBRACKET,
    UNDERLEFTARROW,
    UNDERLINE,
    UNDERPAREN,
    UNDERRIGHTARROW,
    UNDERLEFTRIGHTARROW,
    VEC,
    VCENTER,
    VPHANTOM,
    WIDECHECK,
    WIDEHAT,
    WIDETILDE,
    XCANCEL,
)
COMMANDS_WITH_TWO_PARAMETERS = (
    BINOM,
    CFRAC,
    DBINOM,
    DFRAC,
    FRAC,
    OVERSET,
    STACKREL,
    TBINOM,
    TFRAC,
    UNDERSET,
)

BIG: dict[str, tuple[str, dict]] = {
    # command: (mathml_equivalent, attributes)
    r"\Bigg": ("mo", OrderedDict([("minsize", "2.470em"), ("maxsize", "2.470em")])),
    r"\bigg": ("mo", OrderedDict([("minsize", "2.047em"), ("maxsize", "2.047em")])),
    r"\Big": ("mo", OrderedDict([("minsize", "1.623em"), ("maxsize", "1.623em")])),
    r"\big": ("mo", OrderedDict([("minsize", "1.2em"), ("maxsize", "1.2em")])),
}

BIG_OPEN_CLOSE = {
    command + postfix: (tag, OrderedDict([("stretchy", "true"), ("fence", "true"), *attrib.items()]))
    for command, (tag, attrib) in BIG.items()
    for postfix in "lmr"
}

MSTYLE_SIZES: dict[str, tuple[str, dict]] = {
    # command: (mathml_equivalent, attributes)
    r"\Huge": ("mstyle", {"mathsize": "2.49em"}),
    r"\huge": ("mstyle", {"mathsize": "2.07em"}),
    r"\LARGE": ("mstyle", {"mathsize": "1.73em"}),
    r"\Large": ("mstyle", {"mathsize": "1.44em"}),
    r"\large": ("mstyle", {"mathsize": "1.2em"}),
    FOOTNOTESIZE: ("mstyle", {"mathsize": "0.85em"}),
    r"\normalsize": ("mstyle", {"mathsize": "1em"}),
    r"\scriptsize": ("mstyle", {"mathsize": "0.7em"}),
    r"\small": ("mstyle", {"mathsize": "0.85em"}),
    r"\tiny": ("mstyle", {"mathsize": "0.5em"}),
    r"\Tiny": ("mstyle", {"mathsize": "0.6em"}),
}

STYLES: dict[str, tuple[str, dict]] = {
    DISPLAYSTYLE: ("mstyle", {"displaystyle": "true", "scriptlevel": "0"}),
    TEXTSTYLE: ("mstyle", {"displaystyle": "false", "scriptlevel": "0"}),
    SCRIPTSTYLE: ("mstyle", {"displaystyle": "false", "scriptlevel": "1"}),
    SCRIPTSCRIPTSTYLE: ("mstyle", {"displaystyle": "false", "scriptlevel": "2"}),
}

CONVERSION_MAP: dict[str, tuple[str, dict]] = {
    # command: (mathml_equivalent, attributes)
    # tables
    **{matrix: ("mtable", {}) for matrix in MATRICES},
    DISPLAYLINES: ("mtable", {"rowspacing": "0.5em", "columnspacing": "1em", "displaystyle": "true"}),
    EQALIGN: ("mtable", {"displaystyle": "true", "columnspacing": "0em"}),
    EQALIGNNO: ("mtable", {"displaystyle": "true", "columnspacing": "0em"}),
    SMALLMATRIX: ("mtable", {"rowspacing": "0.1em", "columnspacing": "0.2778em"}),
    SPLIT: (
        "mtable",
        {"displaystyle": "true", "columnspacing": "0em", "rowspacing": "3pt"},
    ),
    ALIGN: (
        "mtable",
        {"displaystyle": "true", "rowspacing": "3pt"},
    ),
    # subscripts/superscripts
    SUBSCRIPT: ("msub", {}),
    SUPERSCRIPT: ("msup", {}),
    SUBSUP: ("msubsup", {}),
    # fractions
    BINOM: ("mfrac", {"linethickness": "0"}),
    CFRAC: ("mfrac", {}),
    DBINOM: ("mfrac", {"linethickness": "0"}),
    DFRAC: ("mfrac", {}),
    FRAC: ("mfrac", {}),
    GENFRAC: ("mfrac", {}),
    TBINOM: ("mfrac", {"linethickness": "0"}),
    TFRAC: ("mfrac", {}),
    # over/under
    ACUTE: ("mover", {}),
    BAR: ("mover", {}),
    BREVE: ("mover", {}),
    CHECK: ("mover", {}),
    DOT: ("mover", {}),
    DDOT: ("mover", {}),
    DDDOT: ("mover", {}),
    DDDDOT: ("mover", {}),
    GRAVE: ("mover", {}),
    HAT: ("mover", {}),
    LIMITS: ("munderover", {}),
    MATHRING: ("mover", {}),
    OVERBRACE: ("mover", {}),
    OVERBRACKET: ("mover", {}),
    OVERLEFTARROW: ("mover", {}),
    OVERLEFTRIGHTARROW: ("mover", {}),
    OVERLINE: ("mover", {}),
    OVERPAREN: ("mover", {}),
    OVERRIGHTARROW: ("mover", {}),
    TILDE: ("mover", {}),
    OVERSET: ("mover", {}),
    STACKREL: ("mover", {}),
    UNDERBAR: ("munder", {}),
    UNDERBRACE: ("munder", {}),
    UNDERBRACKET: ("munder", {}),
    UNDERLEFTARROW: ("munder", {}),
    UNDERLINE: ("munder", {}),
    UNDERPAREN: ("munder", {}),
    UNDERRIGHTARROW: ("munder", {}),
    UNDERLEFTRIGHTARROW: ("munder", {}),
    UNDERSET: ("munder", {}),
    VEC: ("mover", {}),
    WIDECHECK: ("mover", {}),
    WIDEHAT: ("mover", {}),
    WIDETILDE: ("mover", {}),
    # spaces
    COLON: ("mspace", {"width": "0.222em"}),
    COMMA: ("mspace", {"width": "0.167em"}),
    DOUBLEBACKSLASH: ("mspace", {"linebreak": "newline"}),
    ENSPACE: ("mspace", {"width": "0.5em"}),
    EXCLAMATION: ("mspace", {"width": "negativethinmathspace"}),
    GREATER_THAN: ("mspace", {"width": "0.222em"}),
    HSKIP: ("mspace", {}),
    HSPACE: ("mspace", {}),
    KERN: ("mspace", {}),
    MKERN: ("mspace", {}),
    MSKIP: ("mspace", {}),
    MSPACE: ("mspace", {}),
    NEGTHINSPACE: ("mspace", {"width": "negativethinmathspace"}),
    NEGMEDSPACE: ("mspace", {"width": "negativemediummathspace"}),
    NEGTHICKSPACE: ("mspace", {"width": "negativethickmathspace"}),
    THICKSPACE: ("mspace", {"width": "thickmathspace"}),
    THINSPACE: ("mspace", {"width": "thinmathspace"}),
    QQUAD: ("mspace", {"width": "2em"}),
    QUAD: ("mspace", {"width": "1em"}),
    SEMICOLON: ("mspace", {"width": "0.278em"}),
    SPACE_UPPER: ("mspace", {"width": "0.5em"}),
    # overlap
    CLAP: ("mpadded", {"lspace": "-0.5width", "width": "0px"}),
    LLAP: ("mpadded", {"lspace": "-1width", "width": "0px"}),
    MATHCLAP: ("mpadded", {"lspace": "-0.5width", "width": "0px"}),
    MATHLLAP: ("mpadded", {"lspace": "-1width", "width": "0px"}),
    MATHRLAP: ("mpadded", {"width": "0px"}),
    RLAP: ("mpadded", {"width": "0px"}),
    SHOVELEFT: ("mpadded", {"lspace": "0"}),
    SHOVERIGHT: ("mpadded", {"lspace": "0", "width": "0"}),
    # enclose
    BCANCEL: ("menclose", {"notation": "downdiagonalstrike"}),
    BOXED: ("menclose", {"notation": "box"}),
    CANCEL: ("menclose", {"notation": "updiagonalstrike"}),
    FBOX: ("menclose", {"notation": "box"}),
    SOUT: ("menclose", {"notation": "horizontalstrike"}),
    XCANCEL: ("menclose", {"notation": "updiagonalstrike downdiagonalstrike"}),
    # operators
    **BIG,
    **BIG_OPEN_CLOSE,
    **MSTYLE_SIZES,
    **{limit: ("mo", {}) for limit in LIMIT},
    LEFT: ("mo", OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "prefix")])),
    MIDDLE: ("mo", OrderedDict([("stretchy", "true"), ("fence", "true"), ("lspace", "0.05em"), ("rspace", "0.05em")])),
    RIGHT: ("mo", OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "postfix")])),
    # styles
    COLOR: ("mstyle", {}),
    COLORBOX: ("mpadded", {}),
    FCOLORBOX: ("mpadded", {}),
    SMASH: ("mpadded", {}),
    **STYLES,
    # others
    SQRT: ("msqrt", {}),
    ROOT: ("mroot", {}),
    EMPH: ("mtext", {"mathvariant": "italic"}),
    HREF: ("mtext", {}),
    TEXT: ("mtext", {}),
    TEXTBF: ("mtext", {"mathvariant": "bold"}),
    TEXTIT: ("mtext", {"mathvariant": "italic"}),
    TEXTMD: ("mtext", {}),
    TEXTNORMAL: ("mtext", {}),
    TEXTRM: ("mtext", {}),
    TEXTSF: ("mtext", {"mathvariant": "sans-serif"}),
    TEXTTT: ("mtext", {"mathvariant": "monospace"}),
    TAG: ("mtext", {}),
    TAG_STAR: ("mtext", {}),
    TEXTUP: ("mtext", {}),
    VERB: ("mtext", {"mathvariant": "monospace"}),
    HBOX: ("mtext", {}),
    MBOX: ("mtext", {}),
    HPHANTOM: ("mphantom", {}),
    PHANTOM: ("mphantom", {}),
    LOWER: ("mpadded", {}),
    MATHBIN: ("mo", {"lspace": "0.22em", "rspace": "0.22em"}),
    MATHCLOSE: ("mo", {"stretchy": "false", "lspace": "0em", "rspace": "0em"}),
    MATHINNER: ("mpadded", {}),
    MATHOP: ("mo", {}),
    MATHOPEN: ("mo", {"stretchy": "false", "lspace": "0em", "rspace": "0em"}),
    MATHORD: ("mi", {}),
    MATHPUNCT: ("mo", {"separator": "true", "lspace": "0em", "rspace": "0.17em"}),
    MATHREL: ("mo", {}),
    MOVELEFT: ("mpadded", {}),
    MOVERIGHT: ("mpadded", {}),
    RAISE: ("mpadded", {}),
    VCENTER: ("mpadded", {}),
    VPHANTOM: ("mphantom", {}),
    BRA: ("mrow", {}),
    BRAKET: ("mrow", {}),
    KET: ("mrow", {}),
    SIDESET: ("mrow", {}),
    SKEW: ("mrow", {}),
    MOD: ("mi", {}),
    PMOD: ("mi", {}),
    POD: ("mi", {}),
    BMOD: ("mo", {}),
    **{arrow: ("mover", {}) for arrow in EXTENSIBLE_ARROWS},
}


DIACRITICS: dict[str, tuple[str, dict[str, str]]] = {
    ACUTE: ("&#x000B4;", {}),
    BAR: ("&#x000AF;", {"stretchy": "true"}),
    BREVE: ("&#x002D8;", {}),
    CHECK: ("&#x002C7;", {}),
    DOT: ("&#x002D9;", {}),
    DDOT: ("&#x000A8;", {}),
    DDDOT: ("&#x020DB;", {}),
    DDDDOT: ("&#x020DC;", {}),
    GRAVE: ("&#x00060;", {}),
    HAT: ("&#x0005E;", {"stretchy": "false"}),
    MATHRING: ("&#x002DA;", {}),
    OVERBRACE: ("&#x23DE;", {}),
    OVERBRACKET: ("&#x23B4;", {"stretchy": "true"}),
    OVERLEFTARROW: ("&#x02190;", {}),
    OVERLEFTRIGHTARROW: ("&#x02194;", {}),
    OVERLINE: ("&#x02015;", {"accent": "true"}),
    OVERPAREN: ("&#x023DC;", {}),
    OVERRIGHTARROW: ("&#x02192;", {}),
    TILDE: ("&#x0007E;", {"stretchy": "false"}),
    UNDERBAR: ("&#x02015;", {"stretchy": "true", "accent": "true"}),
    UNDERBRACE: ("&#x23DF;", {}),
    UNDERBRACKET: ("&#x23B5;", {"stretchy": "true"}),
    UNDERLEFTARROW: ("&#x02190;", {}),
    UNDERLEFTRIGHTARROW: ("&#x02194;", {}),
    UNDERLINE: ("&#x02015;", {"accent": "true"}),
    UNDERPAREN: ("&#x023DD;", {}),
    UNDERRIGHTARROW: ("&#x02192;", {}),
    VEC: ("&#x02192;", {"stretchy": "true"}),
    WIDECHECK: ("&#x002C7;", {"stretchy": "true"}),
    WIDEHAT: ("&#x0005E;", {}),
    WIDETILDE: ("&#x0007E;", {}),
}
