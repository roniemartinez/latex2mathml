#!/usr/bin/python
import unittest

import latex2mathml

__author__ = 'Ronie Martinez'


class ElementTest(unittest.TestCase):

    def test_empty_element(self):
        self.assertEqual('<{}/>'.format('empty'), str(latex2mathml.Element('empty')))

    def test_element_with_text(self):
        expected = '<{0}>{1}</{0}>'.format('element', 'text')
        self.assertEqual(expected, str(latex2mathml.Element('element', 'text')))

        element = latex2mathml.Element('element')
        element.text = 'text'
        self.assertEqual(expected, str(element))

    def test_empty_element_with_empty_child(self):
        root = latex2mathml.Element('root')
        root.append_child('child')
        self.assertEqual('<{0}><{1}/></{0}>'.format('root', 'child'), str(root))

        root = latex2mathml.Element('root')
        child = latex2mathml.Element('child')
        root.append_child(child)
        self.assertEqual('<{0}><{1}/></{0}>'.format('root', 'child'), str(root))

    def test_element_with_text_and_empty_child(self):
        root = latex2mathml.Element('root')
        root.append_child('child')
        root.text = 'root'
        self.assertEqual('<{0}>{0}<{1}/></{0}>'.format('root', 'child'), str(root))

    def test_empty_element_with_child_with_text(self):
        root = latex2mathml.Element('root')
        child = root.append_child('child')
        child.text = 'child'
        self.assertEqual('<{0}><{1}>{1}</{1}></{0}>'.format('root', 'child'), str(root))

        root = latex2mathml.Element('root')
        child = root.append_child('child', 'child')
        self.assertEqual('<{0}><{1}>{1}</{1}></{0}>'.format('root', 'child'), str(root))

    def test_empty_element_with_attributes(self):
        element = latex2mathml.Element('element', width='10')
        self.assertEqual("<{} {}='{}'/>".format('element', 'width', '10'), str(element))

    def test_element_with_text_and_attributes(self):
        element = latex2mathml.Element('element', 'text', width='10')
        self.assertEqual("<{0} {2}='{3}'>{1}</{0}>".format('element', 'text', 'width', '10'), str(element))

    def test_empty_element_with_empty_child_and_attributes(self):
        root = latex2mathml.Element('root')
        root.append_child('child', width='10')
        self.assertEqual("<{0}><{1} {2}='{3}'/></{0}>".format('root', 'child', 'width', '10'), str(root))

if __name__ == '__main__':
    unittest.main()