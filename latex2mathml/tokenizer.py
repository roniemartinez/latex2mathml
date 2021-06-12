import re
from typing import Iterator

from latex2mathml import commands
from latex2mathml.symbols_parser import convert_symbol

UNITS = ("in", "mm", "cm", "pt", "em", "ex", "pc", "bp", "dd", "cc", "sp")

PATTERN = re.compile(
    rf"""
    %[^\n]+ |  # comment
    [a-zA-Z] |  # letter
    \d+(\.\d+)?(\s*({'|'.join(UNITS)}))? |  # integer/decimal/dimension
    \. |  # dot
    \\(
        [\\\[\]{{}}\s!,:>;|_%#$&] |  # escaped characters
        (begin|end|operatorname){{[a-zA-Z]+\*?}} |  # begin, end or operatorname
        # FIXME: curly braces is tricky on these commands
        (color|fbox|href|text)\s*{{([^}}]*)}} |  # color, fbox, href, text
        math[a-z]+{{[a-zA-Z]}} |  # commands starting with math
        [a-zA-Z]+  # other commands
    )? |
    \S  # non-space character
    """,
    re.VERBOSE,
)


def tokenize(data: str) -> Iterator[str]:
    for match in PATTERN.finditer(data):
        first_match = match.group(0)
        if first_match.startswith(commands.MATH):
            yield from _tokenize_math(first_match)
        elif first_match.startswith((commands.COLOR, commands.FBOX, commands.HREF, commands.TEXT)):
            index = first_match.index(commands.OPENING_BRACE)
            yield first_match[:index].strip()
            yield match.group(7)
        elif first_match.startswith("%"):
            continue
        elif first_match[0].isdigit() and first_match.endswith(UNITS):
            yield first_match.replace(" ", "")
        else:
            yield first_match


def _tokenize_math(match: str) -> Iterator[str]:
    symbol = convert_symbol(match)
    if symbol:
        yield f"&#x{symbol};"
        return
    try:
        index = match.index(commands.OPENING_BRACE)
        yield match[:index]
        yield match[index]
        yield match[index + 1 : -1]
        yield match[-1]
    except ValueError:
        yield match
