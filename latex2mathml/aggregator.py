#!/usr/bin/env python
from latex2mathml.commands import MATRICES
from latex2mathml.tokenizer import tokenize

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2016-2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Development"


def aggregate(latex):
    aggregation = []
    subgroups = [aggregation]
    insert_before_last_item = False
    environment = None
    has_negative_sign = False
    for token in tokenize(latex):
        if token in MATRICES:
            environment = token
            _insert_before_last_item(insert_before_last_item, token, subgroups)
        elif token in '{([':
            try:
                a = subgroups[-1][-1]
                if a != r'\left':
                    raise IndexError
            except IndexError:
                n = []
                _insert_before_last_item(insert_before_last_item, n, subgroups)
                subgroups.append(n)
            if environment and environment in MATRICES:
                if a and a in MATRICES:
                    _add_new_subgroup(subgroups)
                else:
                    try:
                        b = subgroups[-2][-3]
                        if b in MATRICES:
                            _add_new_subgroup(subgroups)
                    except IndexError:
                        pass
            elif token == '[' and subgroups[-2][-2] == r'\sqrt':
                subgroups[-2][-2] = r'\root'  # change name from \sqrt to \root - not a latex command!
            elif token != '{':
                subgroups[-1].append(token)
        elif token in '})]':
            try:
                a = subgroups[-1][-1]
            except IndexError:
                pass
            if token == ']' and subgroups[-2][-2] == r'\root':
                insert_before_last_item = True
            elif token != '}':
                subgroups[-1].append(token)
            if a and a == r'\right':
                pass
            else:
                subgroups.pop()
        elif token in '_^':
            try:
                a = subgroups[-1][-3]
                if a == '_' and token == '^':
                    subgroups[-1][-3] = '_^'
                elif a == '^' and token == '_':
                    subgroups[-1][-3] = '_^'
                    insert_before_last_item = True
                else:
                    subgroups[-1].insert(-1, token)
            except IndexError:
                subgroups[-1].insert(-1, token)
        elif token == '-' and environment and environment in MATRICES:
            _add_new_subgroup(subgroups)
            _insert_before_last_item(insert_before_last_item, token, subgroups)
            has_negative_sign = True
        elif token == '&' and environment and environment in MATRICES:
            if has_negative_sign:
                subgroups.pop()
                has_negative_sign = False
        elif (token == r'\\' or token == r'\cr') and environment and environment in MATRICES:
            if has_negative_sign:
                subgroups.pop()
                has_negative_sign = False
            subgroups.pop()
            _add_new_subgroup(subgroups)
        else:
            _insert_before_last_item(insert_before_last_item, token, subgroups)
    return aggregation


def _insert_before_last_item(insert_before_last_item, n, subgroups):
    if insert_before_last_item:
        subgroups[-1].insert(-1, n)
        insert_before_last_item = False
    else:
        subgroups[-1].append(n)


def _add_new_subgroup(subgroups):
    n = []
    subgroups[-1].append(n)
    subgroups.append(n)
