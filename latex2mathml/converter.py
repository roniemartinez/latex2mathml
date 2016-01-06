#!/usr/bin/python
import re

from element import Element
from aggregator import aggregate
from symbols_parser import convert_symbol

__author__ = 'Ronie Martinez'

mspace = (0, 'mspace', {'width': '0.167em'})

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
    r'\,': mspace,
    r'\:': mspace,
    r'\;': mspace,
    '\\': mspace,
    r'\quad': mspace,
    r'\qquad': mspace,
    r'\overline': (1, 'mover', {}),
    r'\underline': (1, 'munder', {}),
}

matrix_commands = (
    r'\matrix',
    r'\matrix*',
    r'\pmatrix',
    r'\pmatrix*',
    r'\bmatrix',
    r'\bmatrix*',
    r'\Bmatrix',
    r'\Bmatrix*',
    r'\vmatrix',
    r'\vmatrix*',
    r'\Vmatrix',
    r'\Vmatrix*')

for command in matrix_commands:
    commands[command] =  (1, 'mtable', {})


def convert(latex):
    math = Element('math')
    mrow = math.append_child('mrow')
    _classify_subgroup(aggregate(latex), mrow)
    return str(math)


def _convert_matrix_content(param, parent, alignment=None):
    for row in param:
        mtr = parent.append_child('mtr')
        for element in row:
            if alignment:
                if alignment == 'r':
                    mtd = mtr.append_child('mtd', None, columnalign='right')
                elif alignment == 'l':
                    mtd = mtr.append_child('mtd', None, columnalign='left')
                elif alignment == 'c':
                    mtd = mtr.append_child('mtd', None, columnalign='center')
            else:
                mtd = mtr.append_child('mtd')
            if isinstance(element, list):
                _classify_subgroup(element, mtd)
            else:
                _classify(element, mtd)


def _classify_subgroup(elements, row):
    iterable = iter(xrange(len(elements)))
    for i in iterable:
        element = elements[i]
        if isinstance(element, list):
            _row = row.append_child('mrow')
            _classify_subgroup(element, _row)
        elif element in commands:
            if element in (r'\binom', r'\pmatrix'):
                symbol = convert_symbol(r'\lparen')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            elif element == r'\bmatrix':
                symbol = convert_symbol(r'\lbrack')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            elif element == r'\Bmatrix':
                symbol = convert_symbol(r'\lbrace')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            elif element == r'\vmatrix':
                symbol = convert_symbol(r'\vert')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            elif element == r'\Vmatrix':
                symbol = convert_symbol(r'\Vert')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            params, tag, attributes = commands[element]
            parent = row.append_child(tag, None, **attributes)
            alignment = None
            if element in matrix_commands and element.endswith('*'):
                i += 1
                alignment = elements[i]
                iterable.next()
            for j in range(params):
                i += 1
                param = elements[i]
                if element == r'\left' or element == r'\right':
                    symbol = convert_symbol(param)
                    parent.text = param if symbol is None else '&#x{};'.format(symbol)
                elif element in matrix_commands:
                    _convert_matrix_content(param, parent, alignment)
                else:
                    if isinstance(param, list):
                        _parent = parent.append_child('mrow')
                        _classify_subgroup(param, _parent)
                    else:
                        _classify(param, parent)
            if element in (r'\binom', r'\pmatrix'):
                symbol = convert_symbol(r'\rparen')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            elif element == r'\bmatrix':
                symbol = convert_symbol(r'\rbrack')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            elif element == r'\Bmatrix':
                symbol = convert_symbol(r'\rbrace')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            elif element == r'\vmatrix':
                symbol = convert_symbol(r'\vert')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            elif element == r'\Vmatrix':
                symbol = convert_symbol(r'\Vert')
                row.append_child(Element('mo', '&#x{};'.format(symbol)))
            elif element == r'\overline':
                parent.append_child(Element('mo', '&#x000AF;', stretchy='true'))
            elif element == r'\underline':
                parent.append_child(Element('mo', '&#x00332;', stretchy='true'))
            [iterable.next() for j in xrange(params)]
        else:
            _classify(element, row)


def _classify(_element, parent):
    symbol = convert_symbol(_element)
    if re.match('\d+(.\d+)?', _element):
        parent.append_child(Element('mn', _element))
    elif _element in '+-*/()=':
        parent.append_child(Element('mo', _element if symbol is None else '&#x{};'.format(symbol)))
    elif symbol and (int(symbol, 16) in xrange(int('2200', 16), int('22FF', 16)+1) or
                           int(symbol, 16) in xrange(int('2190', 16), int('21FF', 16)+1)):
        parent.append_child(Element('mo', '&#x{};'.format(symbol)))
    elif _element.startswith('\\'):
        if symbol is not None:
            parent.append_child(Element('mi', '&#x{};'.format(symbol)))
        else:
            e = _element.lstrip('\\')
            parent.append_child(Element('mi', e))
    else:
        parent.append_child(Element('mi', _element))

