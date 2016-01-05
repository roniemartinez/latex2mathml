#!/usr/bin/python

__author__ = 'Ronie Martinez'


def tokenize(string):
    _buffer = ''
    environment = ''
    iterable = iter(xrange(len(string)))
    for i in iterable:
        char = string[i]
        if char.isdigit() or char == '.':
            if len(_buffer) and not _buffer[0].isdigit():
                yield _buffer
                _buffer = ''
            _buffer += char
        elif char.isalpha() and _buffer.startswith('\\'):
            _buffer += char
        elif char in r'\,:;' and _buffer == '\\':
            _buffer += char
            yield _buffer
            _buffer = ''
        else:
            if _buffer.startswith(r'\begin') and char == '{':
                i = iterable.next()
                _char = string[i]
                while _char != '}':
                    environment += _char
                    i = iterable.next()
                    _char = string[i]
                _buffer = ''
                yield '\\{}'.format(environment)
                yield '{'
            elif _buffer.startswith(r'\end') and char == '{':
                i = iterable.next()
                _char = string[i]
                _environment = ''
                while _char != '}':
                    _environment += _char
                    i = iterable.next()
                    _char = string[i]
                _buffer = ''
                if environment == _environment:
                    yield '}'
                    environment = ''
            else:
                if len(_buffer):
                    yield _buffer
                _buffer = '' if char.isspace() else char
    if len(_buffer):
        yield _buffer