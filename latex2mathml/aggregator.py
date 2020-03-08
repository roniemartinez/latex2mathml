#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from itertools import tee

from latex2mathml.commands import MATRICES
from latex2mathml.exceptions import EmptyGroupError, NumeratorNotFoundError, DenominatorNotFoundError, \
    ExtraLeftOrMissingRight
from latex2mathml.tokenizer import tokenize


def group(tokens, opening='{', closing='}', delimiter=None):
    g = []
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
                    g += [opening, closing]
            elif token == r'\right':
                g.append(token)
                g.append(next(tokens))
                try:
                    t, _ = tee(tokens)
                    while True:
                        token = next(t)
                        if token == opening:
                            g.append(group(t))
                        elif token != closing:
                            g.append(token)
                        else:
                            break
                except StopIteration:
                    pass
                break
            else:
                g.append(token)
        except StopIteration:
            break
    if delimiter:
        try:
            right = g.index(r'\right')
            content = g[2:right]
            if len(content):
                return g[0:2] + [_aggregate(iter(content))] + g[right:]
            return g
        except ValueError:
            raise ExtraLeftOrMissingRight
    return _aggregate(iter(g))


def process_row(tokens):
    row = []
    content = []
    for token in tokens:
        if token == '&':
            pass
        elif token == r'\\':
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


def environment(begin, tokens):
    if begin.startswith(r'\begin'):
        env = begin[7:-1]
    else:
        env = begin[1:]
    alignment = None
    content = []
    row = []
    has_rowline = False
    while True:
        try:
            token = next_item_or_group(tokens)
            if isinstance(token, list):
                if env == 'array' and all(x in 'lcr|' for x in token):
                    alignment = token
                else:
                    row.append(process_row(token))
            elif token == r'\end{{{}}}'.format(env):
                break
            elif token == '&':
                row.append(token)
            elif token == r'\\':
                if '&' in row:
                    row = group_columns(row)
                if has_rowline:
                    row.insert(0, r'\hline')
                content.append(row)
                row = []
                has_rowline = False
            elif token == r'\hline':
                has_rowline = True
            elif token == '[' and not len(content):
                try:
                    alignment = group(tokens, '[', ']')
                except EmptyGroupError:
                    pass
            elif token == '-':
                try:
                    next_token = next(tokens)
                    row.append([token, next_token])
                except StopIteration:
                    row.append(token)
            elif token in '_^':
                process_sub_sup(row, token, tokens)
            else:
                row.append(token)
        except EmptyGroupError:
            row += ['{', '}']
            continue
        except StopIteration:
            break
    if len(row):
        if '&' in row:
            row = group_columns(row)
        if has_rowline:
            row.insert(0, r'\hline')
        content.append(row)
    while len(content) == 1 and isinstance(content[0], list):
        content = content.pop()
    if alignment:
        return r'\{}'.format(env), ''.join(alignment), content
    return r'\{}'.format(env), content


def group_columns(row):
    grouped = [[]]
    for item in row:
        if item == '&':
            grouped.append([])
        else:
            grouped[-1].append(item)
    return [item if len(item) > 1 else item.pop() for item in grouped]


def next_item_or_group(tokens):
    token = next(tokens)
    if token == '{':
        return group(tokens)
    elif token == r'\left':
        return group(tokens, delimiter=token)
    return token


def _aggregate(tokens):
    aggregated = []
    while True:
        try:
            token = next_item_or_group(tokens)
            if isinstance(token, list):
                aggregated.append(token)
            elif token == '[':
                try:
                    g = group(tokens, '[', ']')
                    if len(aggregated):
                        previous = aggregated[-1]
                        if previous == r'\sqrt':
                            root = next(tokens)
                            if root == '{':
                                try:
                                    root = group(tokens)
                                except EmptyGroupError:
                                    root = ''
                            aggregated[-1] = r'\root'
                            aggregated.append(root)
                        else:
                            pass  # FIXME: possible issues
                    aggregated.append(g)
                except EmptyGroupError:
                    aggregated += ['[', ']']
            elif token in '_^':
                process_sub_sup(aggregated, token, tokens)
            elif token.startswith(r'\begin') or token in MATRICES:
                aggregated += environment(token, tokens)
            elif token == r'\over':
                try:
                    numerator = aggregated.pop()
                    aggregated.append(r'\frac')
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
            aggregated += ['{', '}']
            continue
        except StopIteration:
            break
    return aggregated


def aggregate(data):
    tokens = tokenize(data)
    return _aggregate(tokens)


def process_sub_sup(aggregated, token, tokens):
    try:
        previous = aggregated.pop()
        if isinstance(previous, str) and previous in '+-*/=[]_^{}':
            aggregated += [previous, token]
            return
        try:
            next_token = next_item_or_group(tokens)
            if len(aggregated) >= 2:
                if aggregated[-2] == '_' and token == '^':
                    aggregated[-2] = '_^'
                    aggregated += [previous, next_token]
                elif aggregated[-2] == '^' and token == '_':
                    aggregated[-2] = '_^'
                    aggregated += [next_token, previous]
                else:
                    aggregated += [token, previous, next_token]
            else:
                aggregated += [token, previous, next_token]
        except EmptyGroupError:
            aggregated += [previous, token, '{', '}']
        except StopIteration:
            return
    except IndexError:
        aggregated.append(token)
