#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2018, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
# __status__ = "Production"
import string

import TexSoup


class Latex2MathMLError(Exception):
    pass


def group(iterable):
    g = []
    for i in iterable:
        if i == '{':
            g.append(group(iterable))
        elif i == '}':
            return g
        else:
            try:
                g[-1] += i
            except IndexError:
                g.append(i)
    if len(g):
        return aggregate(g)


def tokenize(text):
    if '\\\\' in text:
        for item in text.split('\\\\'):
            row = list(tokenize(item))
            yield row
    elif '&' in text:
        for item in text.split('&'):
            yield from tokenize(item)
    elif text.startswith('-'):
        yield ['-'] + list(tokenize(text[1:]))
    elif '_' in text:
        items = iter(text.split('_'))
        try:
            yield from tokenize(next(items))
            while True:
                i = next(items)
                yield '_'
                yield from tokenize(i)
        except StopIteration:
            return
    elif '^' in text:
        items = iter(text.split('^'))
        try:
            yield from tokenize(next(items))
            while True:
                i = next(items)
                yield '^'
                yield from tokenize(i)
        except StopIteration:
            return
    else:
        buffer = ''
        iterable = iter(text.strip())
        for char in iterable:
            if char.isdigit():
                if len(buffer) and not buffer[-1].isdigit():
                    yield buffer
                    buffer = ''
                buffer += char
                try:
                    while True:
                        char = next(iterable)
                        if char.isdigit() or char == '.':
                            buffer += char
                        else:
                            if len(buffer):
                                yield buffer
                                buffer = ''
                            if char != ' ':
                                yield char
                            break
                except StopIteration:
                    if len(buffer):
                        yield buffer
                        buffer = ''
            elif char == ' ':
                if len(buffer):
                    yield buffer
                    buffer = ''
            elif buffer.startswith('\\'):
                if char == '\\' or char.isalpha():
                    buffer += char
                elif char in '(){}.':
                    buffer += char
                    yield buffer
                    buffer = ''
                else:
                    if len(buffer):
                        yield buffer
                        buffer = ''
                    yield char
            elif char == '\\':
                buffer += char
            else:
                if len(buffer):
                    yield buffer
                    buffer = ''
                yield char


def aggregate(tex_tree):
    tree = []
    iterable = iter(tex_tree)
    for i in iterable:
        if isinstance(i, list):
            tree.append(i)
        elif isinstance(i, str):
            text = i.strip()
            if text in '{':
                g = group(iterable)
                tree.append(g)
            elif len(text):
                tokens = list(tokenize(text))
                for token in tokens:
                    tree.append(token)
        elif isinstance(i, TexSoup.RArg):
            if not len(i.exprs):
                tree += ['{', '}']
            else:
                tree.append(aggregate(TexSoup.TexSoup(i.value)))
        elif isinstance(i, TexSoup.OArg):
            if not len(i.exprs):
                tree += ['[', ']']
            else:
                raise Latex2MathMLError()
        elif isinstance(i, TexSoup.TexNode):
            if isinstance(i.expr, TexSoup.TexCmd):
                try:
                    first = i.args(0)
                except IndexError:
                    first = None
                if i.name == 'sqrt' and isinstance(first, TexSoup.OArg):
                    tree.append(r'\root')
                    tree.append(aggregate(i.args[1:]))
                    tree.append(aggregate(first))
                elif i.name == 'over':
                    tree.insert(-1, r'\frac')
                    tree[-1] = [tree[-1]]
                    tree.append([i.extra])
                elif i.name == 'frac' and len(i.extra):
                    tree.append(r'\frac')
                    for token in tokenize(i.extra):
                        tree.append(token)
                elif (i.name != 'left' and i.name.startswith('left')) or \
                        (i.name != 'right' and i.name.startswith('right')):
                    tokens = list(tokenize('\\' + i.name))
                    for token in tokens:
                        tree.append(token)
                else:
                    if any([x in i.name for x in string.digits]):
                        # noinspection PyTypeChecker
                        soup = TexSoup.TexSoup(' '.join(tokenize('\\' + i.name)))
                        tree = aggregate(soup)
                    else:
                        tree.append('\\' + i.name)
                        for arg in i.args:
                            tree.append(aggregate(arg))
            elif isinstance(i.expr, TexSoup.TexEnv):
                tree.append('\\' + i.name)
                try:
                    tree.append(i.args[0])
                except IndexError:
                    pass
                if len(list(i.contents)) > 1:
                    content = []
                    row = []
                    for item in i.contents:
                        if isinstance(item, str):
                            item = item.strip()
                            if item == '\\':
                                content.append(row)
                                row = []
                                continue
                            elif item.startswith('\\\\'):
                                content.append(row)
                                item = item[2:].strip()
                                row = []
                            elif item.startswith('&'):
                                item = item[1:].strip()

                            if not len(item):
                                continue
                            elif item.endswith('_'):
                                row += ['_', item[:-1]]
                            else:
                                for token in tokenize(item):
                                    if isinstance(token, list) and len(token) == 0:
                                        continue
                                    content.append(token)
                        elif isinstance(item, TexSoup.RArg):
                            row_ = aggregate(item)
                            if all([x in 'lcr' for x in row_]):
                                tree.append(row_)
                            else:
                                row.append(aggregate(item.exprs))
                        elif isinstance(item, TexSoup.TexNode):
                            item = item.expr
                            row = []
                            if isinstance(item, TexSoup.TexCmd):
                                row.append('\\' + item.name)
                                for token in tokenize(item.extra):
                                    row.append(token)
                            else:
                                raise Latex2MathMLError
                        else:
                            row.append(aggregate(item))
                    content.append(row)
                else:
                    content = aggregate(i.contents)
                tree.append(content)
        else:
            raise Latex2MathMLError
    # fix superscripts and subscripts arrangements
    length = len(tree)
    if (length == 3 or length == 5) and ('_' in tree[1::2] or '^' in tree[1::2]):
        operators = ''.join(tree[1::2])
        operands = tree[::2]
        if operators == '^_':
            operators = '_^'
            a, b, c = operands
            operands = [a, c, b]
        return [operators] + operands
    return tree
