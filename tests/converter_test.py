#!/usr/bin/python
import unittest

import latex2mathml

__author__ = 'Ronie Martinez'


class ConverterTest(unittest.TestCase):

    def test_single_identifier(self):
        self.assertEqual('<{0}><{1}><{2}>{3}</{2}></{1}></{0}>'.format('math', 'mrow', 'mi', 'x'),
                         latex2mathml.convert('x'))

    def test_multiple_identifiers(self):
        self.assertEqual('<{0}><{1}><{2}>{3}</{2}><{2}>{4}</{2}><{2}>{5}</{2}></{1}></{0}>'.format('math', 'mrow', 'mi', 'x', 'y', 'z'),
                         latex2mathml.convert('xyz'))

    def test_single_number(self):
        self.assertEqual('<{0}><{1}><{2}>{3}</{2}></{1}></{0}>'.format('math', 'mrow', 'mn', '3'),
                         latex2mathml.convert('3'))

    def test_multiple_numbers(self):
        self.assertEqual('<{0}><{1}><{2}>{3}</{2}></{1}></{0}>'.format('math', 'mrow', 'mn', '333'),
                         latex2mathml.convert('333'))

    def test_decimal_numbers(self):
        self.assertEqual('<{0}><{1}><{2}>{3}</{2}></{1}></{0}>'.format('math', 'mrow', 'mn', '12.34'),
                         latex2mathml.convert('12.34'))

    def test_numbers_and_identifiers(self):
        self.assertEqual('<{0}><{1}><{2}>{4}</{2}><{3}>{5}</{3}></{1}></{0}>'.format(
                'math', 'mrow', 'mn', 'mi', '12', 'x'), latex2mathml.convert('12x'))

    def test_single_operator(self):
        self.assertEqual('<{0}><{1}><{2}>{3}</{2}></{1}></{0}>'.format('math', 'mrow', 'mo', '&#x0002B;'),
                         latex2mathml.convert('+'))

    def test_numbers_and_operators(self):
        self.assertEqual('<{0}><{1}><{2}>{4}</{2}><{3}>{5}</{3}><{2}>{6}</{2}></{1}></{0}>'.format(
                'math', 'mrow', 'mn', 'mo', '3', '&#x02212;', '2'), latex2mathml.convert('3 - 2'))

    def test_numbers_and_identifiers_and_operators(self):
        self.assertEqual('<{0}><{1}><{2}>{5}</{2}><{3}>{6}</{3}><{4}>{7}</{4}><{2}>{8}</{2}></{1}></{0}>'.format(
                'math', 'mrow', 'mn', 'mi', 'mo', '3', 'x', '&#x0002A;', '2'), latex2mathml.convert('3x * 2'))

    def test_single_group(self):
        self.assertEqual('<{0}><{1}><{1}><{2}>{3}</{2}></{1}></{1}></{0}>'.format('math', 'mrow', 'mi', 'a'),
                         latex2mathml.convert('{a}'))

    def test_multiple_groups(self):
        self.assertEqual('<{0}><{1}><{1}><{2}>{3}</{2}></{1}><{1}><{2}>{4}</{2}></{1}></{1}></{0}>'.format(
                'math', 'mrow', 'mi', 'a', 'b'), latex2mathml.convert('{a}{b}'))

    def test_inner_group(self):
        self.assertEqual('<{0}><{1}><{1}><{2}>{4}</{2}><{3}>{5}</{3}><{1}><{2}>{6}</{2}></{1}></{1}></{1}></{0}>'
                         .format('math', 'mrow', 'mi', 'mo', 'a', '&#x0002B;', 'b'), latex2mathml.convert('{a+{b}}'))


if __name__ == '__main__':
    unittest.main()
