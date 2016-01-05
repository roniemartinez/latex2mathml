#!/usr/bin/python

__author__ = 'Ronie Martinez'


class Element(object):

    def __init__(self, tag, text=None, **attributes):
        self._tag = tag
        self._text = text
        self._attributes = attributes
        self._children = []

    def __str__(self):
        if self._text or len(self._children):
            if len(self._attributes):
                output = '<{} {}>'.format(self._tag, ' '.join(
                        ("{}='{}'".format(key, value) for key, value in self._attributes.items())))
            else:
                output = '<{}>'.format(self._tag)
            if self._text:
                output += self._text
            for child in self._children:
                output += str(child)
            output += '</{}>'.format(self._tag)
            return output
        if len(self._attributes):
            return '<{} {}/>'.format(self._tag, ' '.join(
                    ("{}='{}'".format(key, value) for key, value in self._attributes.items())))
        else:
            return '<{}/>'.format(self._tag)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def append_child(self, *args, **attributes):
        child = args[0] if isinstance(args[0], Element) else Element(*args, **attributes)
        self._children.append(child)
        return child