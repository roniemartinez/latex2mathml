#!/usr/bin/env python

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2016-2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Development"


def tokenize(string):
    _buffer = ''
    environments = []
    iterable = iter(range(len(string)))
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
                environment = _get_environment(iterable, string)
                _buffer = ''
                environments.append(environment)
                yield '\\{}'.format(environment)
                if environment.endswith('*'):
                    for _ in range(2):
                        i = next(iterable)
                    _char = string[i]
                    _buffer = ''
                    while _char != ']':
                        _buffer += _char
                        i = next(iterable)
                        _char = string[i]
                    yield _buffer
                    _buffer = ''
                elif environment == 'array':
                    for _ in range(2):
                        i = next(iterable)
                    _char = string[i]
                    _buffer = ''
                    while _char != '}':
                        _buffer += _char
                        i = next(iterable)
                        _char = string[i]
                    yield _buffer
                    _buffer = ''
                yield '{'
            elif _buffer.startswith(r'\end') and char == '{':
                environment = _get_environment(iterable, string)
                _buffer = ''
                if environments[-1] == environment:
                    yield '}'
                    environments.pop()
                else:
                    pass  # TODO should raise error
            else:
                if len(_buffer):
                    yield _buffer
                _buffer = '' if char.isspace() else char
    if len(_buffer):
        yield _buffer


def _get_environment(iterable, string):
    i = next(iterable)
    _char = string[i]
    environment = ''
    while _char != '}':
        environment += _char
        i = next(iterable)
        _char = string[i]
    return environment
