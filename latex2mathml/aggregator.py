#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from typing import Any, Iterator, List, Tuple, Union

from latex2mathml.commands import MATRICES
from latex2mathml.exceptions import (
    DenominatorNotFoundError,
    EmptyGroupError,
    ExtraLeftOrMissingRight,
    MissingSuperScriptOrSubscript,
    NumeratorNotFoundError,
)
from latex2mathml.tokenizer import tokenize

OPERATORS = "+-*/=[]_^{}()"

OPENING_BRACES = "{"
CLOSING_BRACES = "}"
OPENING_BRACKET = "["
CLOSING_BRACKET = "]"
OPENING_PARENTHESIS = "("
CLOSING_PARENTHESIS = ")"

BACKSLASH = r"\\"
AMPERSAND = "&"
DASH = "-"

SUB_SUP = "_^"
SUBSCRIPT = "_"
SUPERSCRIPT = "^"

LEFT = r"\left"
RIGHT = r"\right"
OVER = r"\over"
HLINE = r"\hline"
BEGIN = r"\begin"
FRAC = r"\frac"
ROOT = r"\root"
SQRT = r"\sqrt"


def group(
    tokens: Iterator,
    opening: str = OPENING_BRACES,
    closing: str = CLOSING_BRACES,
    delimiter: Union[str, None] = None,
) -> list:
    g = []  # type: List[Any]
    if delimiter:
        g.append(delimiter)
        g.append(next(tokens))
    while True:
        try:
            token = next(tokens)
            if token == closing and not delimiter:
                if len(g):
                    break
                raise EmptyGroupError
            elif token == opening:
                try:
                    g.append(group(tokens))
                except EmptyGroupError:
                    g += [[]]
            elif token == LEFT:
                g.append(group(tokens, delimiter=token))
            elif token == RIGHT:
                g.append(token)
                g.append(next(tokens))
                break
            else:
                g.append(token)
        except StopIteration:
            break
    if delimiter:
        try:
            right = g.index(RIGHT)
            content = g[2:right]
            g_ = g
            if len(content):
                g_ = g[0:2] + [_aggregate(iter(content))] + g[right:]
            return g_
        except ValueError:
            raise ExtraLeftOrMissingRight
    return _aggregate(iter(g))


def process_row(tokens: List[Any]) -> list:
    row = []  # type: List[Any]
    content = []
    for token in tokens:
        if token == AMPERSAND:
            pass
        elif token == BACKSLASH:
            if len(row):
                content.append(row)
            row = []
        else:
            row.append(token)
    if len(row):
        content.append(row)
    while len(content) == 1 and isinstance(content[0], list):
        content = content.pop()
    return content


def environment(
    begin: str, tokens: Iterator
) -> Union[Tuple[str, List[Any]], Tuple[str, str, List[List[Any]]]]:
    if begin.startswith(BEGIN):
        env = begin[7:-1]
    else:
        env = begin[1:]
    alignment = None
    content = []
    row = []  # type: List[Any]
    has_rowline = False
    while True:
        try:
            token = next_item_or_group(tokens)
            if isinstance(token, list):
                try:
                    if env == "array" and all(x in "lcr|" for x in token):
                        alignment = token
                    else:
                        row.append(process_row(token))
                except TypeError:
                    row.append(token)
            elif token == r"\end{{{}}}".format(env):
                break
            elif token == AMPERSAND:
                row.append(token)
            elif token == BACKSLASH:
                if AMPERSAND in row:
                    row = group_columns(row)
                if has_rowline:
                    row.insert(0, HLINE)
                content.append(row)
                row = []
                has_rowline = False
            elif token == HLINE:
                has_rowline = True
            elif token == OPENING_BRACKET and not len(content):
                try:
                    alignment = group(tokens, OPENING_BRACKET, CLOSING_BRACKET)
                except EmptyGroupError:
                    pass
            elif token == DASH:
                next_token = next(tokens)
                if next_token == r"\end{{{}}}".format(env):
                    row.append(token)
                else:
                    row.append([token, next_token])
            elif token in SUB_SUP:
                row = process_sub_sup(row, token, tokens)
            else:
                row.append(token)
        except EmptyGroupError:
            row.append([])
            continue
        except StopIteration:
            break
    if len(row):
        if AMPERSAND in row:
            row = group_columns(row)
        if has_rowline:
            row.insert(0, HLINE)
        content.append(row)
    while len(content) == 1 and isinstance(content[0], list):
        content = content.pop()
    if alignment:
        return r"\{}".format(env), "".join(alignment), content
    return r"\{}".format(env), content


def group_columns(row: list) -> list:
    grouped = [[]]  # type: List[Any]
    for item in row:
        if item == AMPERSAND:
            grouped.append([])
        else:
            grouped[-1].append(item)
    return [item if len(item) > 1 else item.pop() for item in grouped]


def next_item_or_group(tokens: Iterator) -> Union[str, list]:
    token = next(tokens)
    if token == OPENING_BRACES:
        return group(tokens)
    elif token == LEFT:
        return group(tokens, delimiter=token)
    return token


def _aggregate(tokens: Iterator) -> list:
    aggregated = []  # type: List[Any]
    while True:
        token = None
        try:
            token = next_item_or_group(tokens)
            if isinstance(token, list):
                aggregated.append(token)
            elif token == OPENING_BRACKET:
                previous = None
                if len(aggregated):
                    previous = aggregated[-1]
                try:
                    g = group(tokens, OPENING_BRACKET, CLOSING_BRACKET)
                    if previous == SQRT:
                        root = next(tokens)
                        if root == OPENING_BRACES:
                            try:
                                root = group(tokens)
                            except EmptyGroupError:
                                root = ""
                        aggregated[-1] = ROOT
                        aggregated.append(root)
                    else:
                        pass  # FIXME: possible issues
                    aggregated.append(g)
                except EmptyGroupError:
                    if previous == SQRT:
                        continue
                    aggregated += [OPENING_BRACKET, CLOSING_BRACKET]
            elif token in (r"\lim", r"\inf", r"\sup", r"\max", r"\min"):
                next(tokens)
                a = next_item_or_group(tokens)
                aggregated += [token, a]
            elif token == r"\limits":
                previous = aggregated.pop()
                next(tokens)
                a = next_item_or_group(tokens)
                next(tokens)
                b = next_item_or_group(tokens)
                aggregated += [token, previous, a, b]
            elif token in SUB_SUP:
                aggregated = process_sub_sup(aggregated, token, tokens)
            elif token.startswith(BEGIN) or token in MATRICES:
                aggregated += environment(token, tokens)
            elif token == OVER:
                try:
                    numerator = aggregated.pop()
                    aggregated.append(FRAC)
                    aggregated.append([numerator])
                    denominator = next_item_or_group(tokens)
                    aggregated.append([denominator])
                except IndexError:
                    raise NumeratorNotFoundError
                except (StopIteration, EmptyGroupError):
                    raise DenominatorNotFoundError
            else:
                aggregated.append(token)
        except EmptyGroupError:
            aggregated += [OPENING_BRACES, CLOSING_BRACES]
            continue
        except StopIteration:
            if token is not None:
                aggregated.append(token)
            break
    return aggregated


def aggregate(data: str):
    tokens = tokenize(data)
    return _aggregate(tokens)


def find_opening_parenthesis(tokens: List[Any]) -> int:
    closing = 0
    for index, token in reversed(list(enumerate(tokens))):
        if token == CLOSING_PARENTHESIS:
            closing += 1
        elif token == OPENING_PARENTHESIS:
            if closing == 0:
                return index
            else:
                closing -= 1
    raise ExtraLeftOrMissingRight


def process_sub_sup(aggregated: list, token: str, tokens: Iterator) -> list:
    try:
        previous = aggregated.pop()
        if isinstance(previous, str) and previous in OPERATORS:
            if previous == CLOSING_PARENTHESIS and OPENING_PARENTHESIS in aggregated:
                index = find_opening_parenthesis(aggregated)
                aggregated = (
                    aggregated[:index] + [token] + [aggregated[index:] + [previous]]
                )
            else:
                aggregated += [previous, token]
            return aggregated
        try:
            next_token = next_item_or_group(tokens)
            if len(aggregated) >= 2:
                if aggregated[-2] == SUBSCRIPT and token == SUPERSCRIPT:
                    aggregated[-2] = SUB_SUP
                    aggregated += [previous, next_token]
                elif aggregated[-2] == SUPERSCRIPT and token == SUBSCRIPT:
                    aggregated[-2] = SUB_SUP
                    aggregated += [next_token, previous]
                else:
                    aggregated += [token, previous, next_token]
            else:
                aggregated += [token, previous, next_token]
        except EmptyGroupError:
            aggregated += [token, previous, []]
        except StopIteration:
            raise MissingSuperScriptOrSubscript
    except IndexError:
        next_token = next_item_or_group(tokens)
        aggregated += [token, "", next_token]
    return aggregated
