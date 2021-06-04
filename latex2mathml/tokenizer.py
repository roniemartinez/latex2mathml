from typing import Iterator, Union

from latex2mathml import commands
from latex2mathml.symbols_parser import convert_symbol

ESCAPED_CHARACTERS = (r"\\", r"\[", r"\]", r"\{", r"\}", r"\ ", r"\!", r"\,", r"\:", r"\>", r"\;", r"\|", r"\_")
LENGTHS = ("in", "mm", "cm", "pt", "em", "ex", "pc", "bp", "dd", "cc", "sp")


def dimension(iterable: Iterator[str]) -> str:
    dim = ""
    for char in iterable:
        if char.isspace():
            continue
        elif char.isdigit() or char.isalpha() or char == ".":
            dim += char
        if dim.endswith(LENGTHS):
            break
    return dim.strip()


def tokenize(data: str) -> Iterator[Union[str, list]]:
    iterable = iter(data)
    buffer = ""
    while True:
        try:
            char = next(iterable)
            if char == commands.BACKSLASH:
                if buffer == commands.BACKSLASH:
                    yield buffer + char
                    buffer = ""
                    continue
                elif len(buffer):
                    yield buffer
                buffer = char
                try:
                    buffer += next(iterable)
                    if buffer in ESCAPED_CHARACTERS:
                        yield buffer
                        buffer = ""
                except StopIteration:
                    break
            elif char == "%":
                if buffer == commands.BACKSLASH:
                    yield buffer + char
                    buffer = ""
                    continue
                elif len(buffer):
                    yield buffer
                    buffer = ""
                for char in iterable:
                    if char == "\n":
                        break
            elif char.isalpha():
                if len(buffer):
                    if buffer.endswith(commands.CLOSING_BRACE):
                        yield buffer
                        yield char
                        buffer = ""
                    elif buffer.startswith(commands.BACKSLASH):
                        buffer += char
                else:
                    yield char
            elif char.isdigit():
                if buffer.startswith((commands.HSPACE, commands.ABOVE)):
                    yield buffer
                    yield char + dimension(iterable)
                    buffer = ""
                    continue
                if len(buffer):
                    yield buffer
                buffer = char
                while True:
                    try:
                        char = next(iterable)
                    except StopIteration:
                        break
                    if char.isspace():
                        yield buffer
                        buffer = ""
                        break
                    elif char.isdigit() or char == ".":
                        buffer += char
                    elif char == "%":
                        for char in iterable:
                            if char == "\n":
                                break
                    else:
                        if buffer.endswith("."):
                            yield buffer[:-1]
                            yield buffer[-1]
                        else:
                            yield buffer
                        buffer = ""
                        if char == commands.BACKSLASH:
                            buffer = char
                        else:
                            yield char
                        break
            elif char.isspace():
                if buffer.startswith(commands.TEXT):
                    buffer += char
                elif buffer.startswith((commands.HSPACE, commands.ABOVE)):
                    pass
                elif len(buffer):
                    yield buffer
                    buffer = ""
            elif char in "{}*":
                # FIXME: Anything that starts with '\math' passes. There is a huge list of math symbols in
                #  unimathsymbols.txt and hard-coding all of them is inefficient.
                if buffer.startswith(
                    (
                        commands.BEGIN,
                        commands.END,
                        commands.OPERATORNAME,
                        commands.TEXT,
                        commands.HSPACE,
                        commands.ABOVE,
                        r"\math",
                    )
                ):
                    if buffer.endswith(commands.CLOSING_BRACE):
                        yield buffer
                        yield char
                        buffer = ""
                    elif buffer.startswith(r"\math") and char == commands.CLOSING_BRACE:
                        symbol = convert_symbol(buffer + char)
                        if symbol:
                            yield "&#x{};".format(symbol)
                            buffer = ""
                            continue
                        index = buffer.index(commands.OPENING_BRACE)
                        yield buffer[:index]
                        yield buffer[index]
                        yield from tokenize(buffer[index + 1 :])
                        yield char
                        buffer = ""
                    elif buffer.startswith(commands.TEXT) and char == commands.CLOSING_BRACE:
                        yield commands.TEXT
                        yield buffer[6:]
                        buffer = ""
                    elif buffer.startswith((commands.HSPACE, commands.ABOVE)) and char == commands.CLOSING_BRACE:
                        index = buffer.index(commands.OPENING_BRACE)
                        yield buffer[:index]
                        yield buffer[index]
                        yield buffer[index + 1 :]
                        yield char
                        buffer = ""
                    elif buffer in (commands.HSPACE, commands.ABOVE) and char == commands.OPENING_BRACE:
                        yield buffer
                        yield char
                        yield dimension(iterable)
                        buffer = ""
                    else:
                        buffer += char
                else:
                    if len(buffer):
                        yield buffer
                        buffer = ""
                    yield char
            else:
                if len(buffer):
                    if buffer.startswith(r"\math"):
                        yield buffer[:-1]
                        yield buffer[-1]
                    elif buffer.startswith(commands.TEXT):
                        buffer += char
                        continue
                    else:
                        yield buffer
                    buffer = ""
                if len(char):
                    yield char
        except StopIteration:
            break
    if len(buffer):
        yield buffer
