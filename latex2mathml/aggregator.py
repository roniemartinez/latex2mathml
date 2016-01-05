#!/usr/bin/python
from tokenizer import tokenize

__author__ = 'Ronie Martinez'


def aggregate(latex):
    aggregation = []
    subgroups = [aggregation]
    insert_before_last_item = False
    environment = None
    for token in tokenize(latex):
        if token == r'\matrix':
            environment = r'\matrix'
        if token in '{([':
            try:
                a = subgroups[-1][-1]
                if a != r'\left':
                    raise IndexError
            except IndexError:
                n = []
                if insert_before_last_item:
                    subgroups[-1].insert(-1, n)
                    insert_before_last_item = False
                else:
                    subgroups[-1].append(n)
                subgroups.append(n)
            if environment and environment == r'\matrix':
                n = []
                subgroups[-1].append(n)
                subgroups.append(n)
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
        elif token == '&' and environment and environment == r'\matrix':
            pass
        elif token == r'\\' and environment and environment == r'\matrix':
            subgroups.pop()
            n = []
            subgroups[-1].append(n)
            subgroups.append(n)
        else:
            if insert_before_last_item:
                subgroups[-1].insert(-1, token)
                insert_before_last_item = False
            else:
                subgroups[-1].append(token)
    return aggregation