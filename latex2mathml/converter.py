#!/usr/bin/env python
import re
from latex2mathml.aggregator import aggregate
from latex2mathml.element import Element
from latex2mathml.commands import MATRICES, SPACES
from latex2mathml.symbols_parser import convert_symbol

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2016-2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Development"

commands = {
    # command: (params_count, mathml_equivalent, attributes)
    '_': (2, 'msub', {}),
    '^': (2, 'msup', {}),
    '_^': (3, 'msubsup', {}),
    r'\frac': (2, 'mfrac', {}),
    r'\sqrt': (1, 'msqrt', {}),
    r'\root': (2, 'mroot', {}),
    r'\binom': (2, 'mfrac', {'linethickness': 0}),
    r'\left': (1, 'mo', {'stretchy': 'true', 'fence': 'true', 'form': 'prefix'}),
    r'\right': (1, 'mo', {'stretchy': 'true', 'fence': 'true', 'form': 'postfix'}),
    r'\overline': (1, 'mover', {}),
    r'\underline': (1, 'munder', {}),
}

for space in SPACES:
    commands[space] = (0, 'mspace', {'width': '0.167em'})

for matrix in MATRICES:
    commands[matrix] = (1, 'mtable', {})


def convert(latex):
    math = Element('math')
    math.pretty = True
    row = math.append_child('mrow')
    _classify_subgroup(aggregate(latex), row)
    return str(math)


def _convert_matrix_content(param, parent, alignment=None):
    for row in param:
        mtr = parent.append_child('mtr')
        iterable = iter(range(len(row)))
        for i in iterable:
            element = row[i]
            if alignment:
                column_align = {'r': 'right', 'l': 'left', 'c': 'center'}.get(alignment)
                mtd = mtr.append_child('mtd', None, columnalign=column_align)
            else:
                mtd = mtr.append_child('mtd')
            if isinstance(element, list):
                _classify_subgroup(element, mtd)
            elif element in commands:
                _convert_command(element, row, i, iterable, mtd)
            else:
                _classify(element, mtd)


def _convert_array_content(param, parent, alignment=None):
    if '|' in alignment:
        _alignment, columnlines = [], []
        for i in alignment:
            if i == '|':
                columnlines.append('solid')
            else:
                _alignment.append(i)
            if len(_alignment) - len(columnlines) == 2:
                columnlines.append('none')
        parent._attributes['columnlines'] = ' '.join(columnlines)
    else:
        _alignment = list(alignment)
    rowlines = []
    row_count = 0
    for row in param:
        row_count += 1
        mtr = parent.append_child('mtr')
        iterable = iter(range(len(row)))
        index = 0
        has_rowline = False
        for i in iterable:
            element = row[i]
            if element == r'\hline' and row_count > 1:
                rowlines.append('solid')
                has_rowline = True
                continue
            __alignment = _alignment[index]
            if __alignment:
                column_align = {'r': 'right', 'l': 'left', 'c': 'center'}.get(__alignment)
                mtd = mtr.append_child('mtd', None, columnalign=column_align)
            else:
                mtd = mtr.append_child('mtd')
            if isinstance(element, list):
                _classify_subgroup(element, mtd)
            elif element in commands:
                _convert_command(element, row, i, iterable, mtd)
            else:
                _classify(element, mtd)
            index += 1
        if not has_rowline and row_count > 1:
            rowlines.append('none')
    if 'solid' in rowlines:
        parent._attributes['rowlines'] = ' '.join(rowlines)


def _classify_subgroup(elements, row):
    iterable = iter(range(len(elements)))
    for i in iterable:
        element = elements[i]
        if isinstance(element, list):
            _row = row.append_child('mrow')
            _classify_subgroup(element, _row)
        elif element in commands:
            _convert_command(element, elements, i, iterable, row)
        else:
            _classify(element, row)


def _convert_command(element, elements, index, iterable, parent):
    _get_prefix_element(element, parent)
    params, tag, attributes = commands[element]
    new_parent = parent.append_child(tag, None, **attributes)
    alignment = None
    if element in MATRICES and (element.endswith('*') or element == r'\array'):
        index += 1
        alignment = elements[index]
        next(iterable)
    for j in range(params):
        index += 1
        param = elements[index]
        if element == r'\left' or element == r'\right':
            symbol = convert_symbol(param)
            new_parent.text = param if symbol is None else '&#x{};'.format(symbol)
        elif element == r'\array':
            _convert_array_content(param, new_parent, alignment)
        elif element in MATRICES:
            _convert_matrix_content(param, new_parent, alignment)
        else:
            if isinstance(param, list):
                _parent = new_parent.append_child('mrow')
                _classify_subgroup(param, _parent)
            else:
                _classify(param, new_parent)
    _get_postfix_element(element, parent)
    if element == r'\overline':
        new_parent.append_child(Element('mo', '&#x000AF;', stretchy='true'))
    elif element == r'\underline':
        new_parent.append_child(Element('mo', '&#x00332;', stretchy='true'))
    [next(iterable) for _ in range(params)]


def _convert_and_append_operator(symbol, parent):
    symbol = convert_symbol(symbol)
    parent.append_child(Element('mo', '&#x{};'.format(symbol)))


def _get_postfix_element(element, row):
    if element in (r'\binom', r'\pmatrix'):
        _convert_and_append_operator(r'\rparen', row)
    elif element == r'\bmatrix':
        _convert_and_append_operator(r'\rbrack', row)
    elif element == r'\Bmatrix':
        _convert_and_append_operator(r'\rbrace', row)
    elif element == r'\vmatrix':
        _convert_and_append_operator(r'\vert', row)
    elif element == r'\Vmatrix':
        _convert_and_append_operator(r'\Vert', row)


def _get_prefix_element(element, row):
    if element in (r'\binom', r'\pmatrix'):
        _convert_and_append_operator(r'\lparen', row)
    elif element == r'\bmatrix':
        _convert_and_append_operator(r'\lbrack', row)
    elif element == r'\Bmatrix':
        _convert_and_append_operator(r'\lbrace', row)
    elif element == r'\vmatrix':
        _convert_and_append_operator(r'\vert', row)
    elif element == r'\Vmatrix':
        _convert_and_append_operator(r'\Vert', row)


def _classify(_element, parent):
    symbol = convert_symbol(_element)
    if re.match('\d+(.\d+)?', _element):
        parent.append_child(Element('mn', _element))
    elif _element in '+-*/()=':
        parent.append_child(Element('mo', _element if symbol is None else '&#x{};'.format(symbol)))
    elif symbol and (int(symbol, 16) in range(int('2200', 16), int('22FF', 16) + 1) or
                             int(symbol, 16) in range(int('2190', 16), int('21FF', 16) + 1)):
        parent.append_child(Element('mo', '&#x{};'.format(symbol)))
    elif _element.startswith('\\'):
        if symbol is not None:
            parent.append_child(Element('mi', '&#x{};'.format(symbol)))
        else:
            e = _element.lstrip('\\')
            parent.append_child(Element('mi', e))
    else:
        parent.append_child(Element('mi', _element))
