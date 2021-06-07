import re
from typing import Iterator, Union

from latex2mathml import commands
from latex2mathml.symbols_parser import convert_symbol

UNITS = ("in", "mm", "cm", "pt", "em", "ex", "pc", "bp", "dd", "cc", "sp")

PATTERN = re.compile(
    r"%[^\n]+|"  # comment
    r"[a-zA-Z]|"  # letter
    rf"\d+(\.\d+)?(\s*({'|'.join(UNITS)}))?|"  # integer/decimal/dimension
    r"\.|"  # dot
    r"\\([\\\[\]{} !,:>;|_%#$&]|"  # escaped character
    r"(begin|end|operatorname){[a-zA-Z]+\*?}|(text|color)\s*{([^{^}]*)}|math[a-z]+{[a-zA-Z]}|[a-zA-Z]+)?|"  # command
    r"\S"  # non-space character
)


def tokenize(data: str) -> Iterator[Union[str, list]]:
    for match in PATTERN.finditer(data):
        first_match = match.group(0)
        if first_match.startswith(commands.MATH):
            yield from _tokenize_math(first_match)
        elif first_match.startswith((commands.COLOR, commands.TEXT)):
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
