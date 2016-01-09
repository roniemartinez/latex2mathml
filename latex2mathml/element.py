#!/usr/bin/python

__author__ = 'Ronie Martinez'


class Element(object):

    def __init__(self, tag, text=None, **attributes):
        self._tag = tag
        self._text = text
        self._attributes = attributes
        self._children = []
        self._pretty = False
        self._level = 0

    def __str__(self):
        spaces, end, attributes = '', '', ''
        if self.pretty:
            spaces = ' ' * (self._level * 4)
            end = '\n'
        if len(self._attributes):
            attributes = ' ' + ' '.join(("{}='{}'".format(key, value) for key, value in self._attributes.items()))
        if self._text or len(self._children):
            output = '{}<{}{}>{}'.format(spaces, self._tag, attributes, end)
            if self._text:
                _spaces = '' if not self.pretty else ' ' * ((self._level + 1) * 4)
                output += '{}{}{}'.format(_spaces, str(self._text), end)
            for child in self._children:
                child.pretty = self.pretty
                child._level = self._level + 1
                output += '{}{}'.format(str(child), end)
            output += '{}</{}>'.format(spaces, self._tag)
            return output
        return '{}<{}{}/>'.format(spaces, self._tag, attributes)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def pretty(self):
        return self._pretty

    @pretty.setter
    def pretty(self, value):
        self._pretty = value

    def append_child(self, *args, **attributes):
        child = args[0] if isinstance(args[0], Element) else Element(*args, **attributes)
        self._children.append(child)
        return child
