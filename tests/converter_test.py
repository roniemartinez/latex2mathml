#!/usr/bin/python
import unittest

import latex2mathml

__author__ = 'Ronie Martinez'


class ConverterTest(unittest.TestCase):

    def setUp(self):
        self.math = latex2mathml.Element('math')
        self.row = self.math.append_child('mrow')

    def test_single_identifier(self):
        self.row.append_child('mi', 'x')
        self.assertEqual(str(self.math), latex2mathml.convert('x'))

    def test_multiple_identifiers(self):
        self.row.append_child('mi', 'x')
        self.row.append_child('mi', 'y')
        self.row.append_child('mi', 'z')
        self.assertEqual(str(self.math), latex2mathml.convert('xyz'))

    def test_single_number(self):
        self.row.append_child('mn', 3)
        self.assertEqual(str(self.math), latex2mathml.convert('3'))

    def test_multiple_numbers(self):
        self.row.append_child('mn', 333)
        self.assertEqual(str(self.math), latex2mathml.convert('333'))

    def test_decimal_numbers(self):
        self.row.append_child('mn', 12.34)
        self.assertEqual(str(self.math), latex2mathml.convert('12.34'))

    def test_numbers_and_identifiers(self):
        self.row.append_child('mn', 12)
        self.row.append_child('mi', 'x')
        self.assertEqual(str(self.math), latex2mathml.convert('12x'))

    def test_single_operator(self):
        self.row.append_child('mo', '&#x0002B;')
        self.assertEqual(str(self.math), latex2mathml.convert('+'))

    def test_numbers_and_operators(self):
        self.row.append_child('mn', 3)
        self.row.append_child('mo', '&#x02212;')
        self.row.append_child('mn', 2)
        self.assertEqual(str(self.math), latex2mathml.convert('3-2'))

    def test_numbers_and_identifiers_and_operators(self):
        self.row.append_child('mn', 3)
        self.row.append_child('mi', 'x')
        self.row.append_child('mo', '&#x0002A;')
        self.row.append_child('mn', 2)
        self.assertEqual(str(self.math), latex2mathml.convert('3x*2'))

    def test_single_group(self):
        self.row.append_child('mrow').append_child('mi', 'a')
        self.assertEqual(str(self.math), latex2mathml.convert('{a}'))

    def test_multiple_groups(self):
        self.row.append_child('mrow').append_child('mi', 'a')
        self.row.append_child('mrow').append_child('mi', 'b')
        self.assertEqual(str(self.math), latex2mathml.convert('{a}{b}'))

    def test_inner_group(self):
        row = self.row.append_child('mrow')
        row.append_child('mi', 'a')
        row.append_child('mo', '&#x0002B;')
        row.append_child('mrow').append_child('mi', 'b')
        self.assertEqual(str(self.math), latex2mathml.convert('{a+{b}}'))


if __name__ == '__main__':
    unittest.main()
