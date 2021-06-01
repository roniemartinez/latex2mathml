from typing import Iterator, Union

from latex2mathml import commands
from latex2mathml.symbols_parser import convert_symbol

LENGTHS = (
    "in",
    "mm",
    "cm",
    "pt",
    "em",
    "ex",
    "pc",
    "bp",
    "dd",
    "cc",
    "sp",
)


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
                    if buffer in (r"\\", r"\[", r"\]", r"\{", r"\}", r"\ ", r"\!", r"\,", r"\:", r"\>", r"\;", r"\|"):
                        yield buffer
                        buffer = ""
                except StopIteration:
                    break
            elif char.isalpha():
                if buffer.startswith(commands.HSPACE):
                    buffer += char
                    if "{" not in buffer and (buffer + char).endswith(LENGTHS):
                        yield commands.HSPACE
                        yield buffer[7:]
                        buffer = ""
                    continue
                if len(buffer):
                    if buffer.endswith("}"):
                        yield buffer
                        yield char
                        buffer = ""
                    elif buffer.startswith(commands.BACKSLASH):
                        buffer += char
                else:
                    yield char
            elif char.isdigit():
                if buffer.startswith(commands.HSPACE):
                    buffer += char
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
                    continue
                if len(buffer):
                    yield buffer
                    buffer = ""
            elif char in "{}*":
                # FIXME: Anything that starts with '\math' passes. There is a huge list of math symbols in
                #  unimathsymbols.txt and hard-coding all of them is inefficient.
                if buffer.startswith(
                    (commands.BEGIN, commands.END, commands.OPERATORNAME, commands.TEXT, commands.HSPACE, r"\math")
                ):
                    if buffer.endswith("}"):
                        yield buffer
                        yield char
                        buffer = ""
                        continue
                    elif buffer.startswith(r"\math") and char == "}":
                        symbol = convert_symbol(buffer + char)
                        if symbol:
                            yield "&#x{};".format(symbol)
                            buffer = ""
                            continue
                        else:
                            index = buffer.index("{")
                            yield buffer[:index]
                            yield buffer[index]
                            yield from tokenize(buffer[index + 1 :])
                            yield char
                            buffer = ""
                            continue
                    elif buffer.startswith(commands.TEXT) and char == "}":
                        yield buffer[:5]
                        yield buffer[6:]
                        buffer = ""
                        continue
                    elif buffer.startswith(commands.HSPACE) and char == "}":
                        index = buffer.index("{")
                        yield buffer[:index]
                        yield buffer[index]
                        yield buffer[index + 1 :]
                        yield char
                        buffer = ""
                        continue
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
                    else:
                        yield buffer
                    buffer = ""
                if len(char):
                    yield char
        except StopIteration:
            break
    if len(buffer):
        yield buffer
