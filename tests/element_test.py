#!/usr/bin/python
import unittest
from latex2mathml import element

__author__ = 'Ronie Martinez'


class ElementTest(unittest.TestCase):
    def test_empty_element(self):
        self.assertEqual('<{}/>'.format('empty'), str(element.Element('empty')))

    def test_element_with_text(self):
        expected = '<{0}>{1}</{0}>'.format('element', 'text')
        self.assertEqual(expected, str(element.Element('element', 'text')))

        _element = element.Element('element')
        _element.text = 'text'
        self.assertEqual(expected, str(_element))

    def test_empty_element_with_empty_child(self):
        root = element.Element('root')
        root.append_child('child')
        self.assertEqual('<{0}><{1}/></{0}>'.format('root', 'child'), str(root))

        root = element.Element('root')
        child = element.Element('child')
        root.append_child(child)
        self.assertEqual('<{0}><{1}/></{0}>'.format('root', 'child'), str(root))

    def test_element_with_text_and_empty_child(self):
        root = element.Element('root')
        root.append_child('child')
        root.text = 'root'
        self.assertEqual('<{0}>{0}<{1}/></{0}>'.format('root', 'child'), str(root))

    def test_empty_element_with_child_with_text(self):
        root = element.Element('root')
        child = root.append_child('child')
        child.text = 'child'
        self.assertEqual('<{0}><{1}>{1}</{1}></{0}>'.format('root', 'child'), str(root))

        root = element.Element('root')
        root.append_child('child', 'child')
        self.assertEqual('<{0}><{1}>{1}</{1}></{0}>'.format('root', 'child'), str(root))

    def test_empty_element_with_attributes(self):
        _element = element.Element('element', width='10')
        self.assertEqual("<{} {}='{}'/>".format('element', 'width', '10'), str(_element))

    def test_element_with_text_and_attributes(self):
        _element = element.Element('element', 'text', width='10')
        self.assertEqual("<{0} {2}='{3}'>{1}</{0}>".format('element', 'text', 'width', '10'), str(_element))

    def test_empty_element_with_empty_child_and_attributes(self):
        root = element.Element('root')
        root.append_child('child', width='10')
        self.assertEqual("<{0}><{1} {2}='{3}'/></{0}>".format('root', 'child', 'width', '10'), str(root))


class PrettyElementTest(unittest.TestCase):
    def test_empty_element_with_empty_child(self):
        root = element.Element('root')
        root.pretty = True
        root.append_child('child')
        self.assertEqual('<{0}>\n    <{1}/>\n</{0}>'.format('root', 'child'), str(root))

        root = element.Element('root')
        root.pretty = True
        child = element.Element('child')
        root.append_child(child)
        self.assertEqual('<{0}>\n    <{1}/>\n</{0}>'.format('root', 'child'), str(root))


if __name__ == '__main__':
    unittest.main()
