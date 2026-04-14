import re
from typing import Iterator

from latex2mathml import commands
from latex2mathml.symbols_parser import convert_symbol

UNITS = ("in", "mm", "cm", "pt", "em", "ex", "pc", "bp", "dd", "cc", "sp", "mu")

PATTERN = re.compile(
    rf"""
    (?P<comment>%[^\n]+) |
    (?P<letter>[a-zA-Z]) |
    (?P<subsup_operator>[_^])(?P<subsup_digit>\d) |
    (?P<dimension>-?\d+(?:\.\d+)?\s*(?:{"|".join(UNITS)})) |
    (?P<number>\d+(?:\.\d+)?) |
    (?P<dot_decimal>\.\d*) |
    (?P<escaped>\\[\\\[\]{{}}\s!,:>;|_%#$&]) |
    (?P<begin_end>\\(?:begin|end)\s*{{[a-zA-Z]+\*?}}) |
    (?P<operatorname>\\operatorname(?:withlimits|\*)?\s*{{[a-zA-Z\s*]+\*?\s*}}) |
    (?P<text_cmd>\\(?:cla(?:p|ss)|color(?!box)|emph|fbox|hbox|href|llap|mbox|rlap|style
        |tag\*?|text(?:bf|color|it|md|normal|rm|sf|tt|up)?|underbar))\s*{{(?P<text_content>[^}}]*)}} |
    (?P<frac_cmd>\\[cdt]?frac)\s*(?P<frac_arg1>[.\d])\s*(?P<frac_arg2>[.\d])? |
    (?P<math_font>\\math(?!ring|bin|close|inner|op|open|ord|punct|rel|strut)
        [a-z]+)(?P<math_open>{{)(?P<math_arg>[a-zA-Z])(?P<math_close>}}) |
    (?P<verb>\\verb(?P<verb_delim>.)(?P<verb_content>.*?)(?P=verb_delim)) |
    (?P<command>\\[a-zA-Z]+) |
    (?P<char>\S)
    """,
    re.VERBOSE,
)


def tokenize(latex_string: str, skip_comments: bool = True) -> Iterator[str]:
    """
    Converts Latex string into tokens.

    :param latex_string: Latex string.
    :param skip_comments: Flag to skip comments (default=True).
    """
    for match in PATTERN.finditer(latex_string):
        tokens = tuple(filter(lambda x: x is not None, match.groups()))
        if tokens[0].startswith(commands.VERB):
            yield commands.VERB
            yield tokens[2]  # verb_content
            continue
        if tokens[0].startswith(commands.MATH) and tokens[0] not in commands.MATH_NON_FONT_COMMANDS:
            full_math = "".join(tokens)
            symbol = convert_symbol(full_math)
            if symbol:
                yield f"&#x{symbol};"
                continue
        for captured in tokens:
            if skip_comments and captured.startswith("%"):
                break
            if captured.endswith(UNITS) and captured[0:1].isdigit():
                yield captured.replace(" ", "")
                continue
            if captured.startswith((commands.BEGIN, commands.END, commands.OPERATORNAME)):
                yield "".join(captured.split(" "))
                continue
            yield captured
