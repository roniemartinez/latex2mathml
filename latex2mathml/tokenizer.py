#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2018-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from typing import Iterator

from latex2mathml.symbols_parser import convert_symbol


def tokenize(data) -> Iterator[str]:
    iterable = iter(data)
    buffer = ""
    while True:
        try:
            char = next(iterable)
            if char == "\\":
                if buffer == "\\":
                    yield buffer + char
                    buffer = ""
                    continue
                elif len(buffer):
                    yield buffer
                buffer = char
                try:
                    buffer += next(iterable)
                    if buffer == r"\\":
                        yield buffer
                        buffer = ""
                except StopIteration:
                    break
            elif char.isalpha():
                if len(buffer):
                    if buffer.endswith("}"):
                        yield buffer
                        yield char
                        buffer = ""
                    elif buffer.startswith("\\"):
                        buffer += char
                else:
                    yield char
            elif char.isdigit():
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
                        if char == "\\":
                            buffer = char
                        else:
                            yield char
                        break
            elif char.isspace():
                if len(buffer):
                    yield buffer
                    buffer = ""
            elif char in "{}*":
                # FIXME: Anything that starts with '\math' passes. There is a huge list of math symbols in
                #  unimathsymbols.txt and hard-coding all of them is inefficient.
                if (
                    buffer.startswith(r"\begin")
                    or buffer.startswith(r"\end")
                    or buffer.startswith(r"\math")
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
