#!/usr/bin/python
import unittest

import latex2mathml

__author__ = 'Ronie Martinez'


class CommandTest(unittest.TestCase):

    def test_subscript(self):
        self.assertEqual('<{0}><{1}><{2}><{3}>{4}</{3}><{3}>{5}</{3}></{2}></{1}></{0}>'.format(
                'math', 'mrow', 'msub', 'mi', 'a', 'b'), latex2mathml.convert('a_b'))

    def test_superscript(self):
        self.assertEqual('<{0}><{1}><{2}><{3}>{4}</{3}><{3}>{5}</{3}></{2}></{1}></{0}>'.format(
                'math', 'mrow', 'msup', 'mi', 'a', 'b'), latex2mathml.convert('a^b'))

    def test_subscript_and_superscript(self):
        self.assertEqual('<{0}><{1}><{2}><{3}>{4}</{3}><{3}>{5}</{3}><{3}>{6}</{3}></{2}></{1}></{0}>'.format(
                'math', 'mrow', 'msubsup', 'mi', 'a', 'b', 'c'), latex2mathml.convert('a_b^c'))

    def test_superscript_and_subscript(self):
        self.assertEqual('<{0}><{1}><{2}><{3}>{4}</{3}><{3}>{5}</{3}><{3}>{6}</{3}></{2}></{1}></{0}>'.format(
                'math', 'mrow', 'msubsup', 'mi', 'a', 'c', 'b'), latex2mathml.convert('a^b_c'))

    def test_subscript_within_curly_braces(self):
        self.assertEqual('<{0}><{1}><{1}><{2}><{3}>{4}</{3}><{3}>{5}</{3}></{2}></{1}></{1}></{0}>'.format(
                'math', 'mrow', 'msub', 'mi', 'a', 'b'), latex2mathml.convert('{a_b}'))

    def test_superscript_within_curly_braces(self):
        self.assertEqual('<{0}><{1}><{1}><{2}><{3}>{4}</{3}><{3}>{5}</{3}></{2}></{1}></{1}></{0}>'.format(
                'math', 'mrow', 'msup', 'mi', 'a', 'b'), latex2mathml.convert('{a^b}'))

    def test_superscript_with_curly_braces(self):
        self.assertEqual('<{0}><{1}><{2}><{3}>{6}</{3}><{4}>{10}</{4}><{1}><{3}>{7}</{3}><{5}>{8}</{5}><{4}>{9}</{4}>'
                         '</{1}></{2}></{1}></{0}>'.format( 'math', 'mrow', 'msubsup', 'mi', 'mn', 'mo', 'a', 'i',
                                                            '&#x0002B;', '1', '3'), latex2mathml.convert('a^{i+1}_3'))

    def test_simple_fraction(self):
        self.assertEqual('<{0}><{1}><{2}><{1}><{3}>{4}</{3}></{1}><{1}><{3}>{5}</{3}></{1}></{2}></{1}></{0}>'.format(
                'math', 'mrow', 'mfrac', 'mn', '1', '2'), latex2mathml.convert(r'\frac{1}{2}'))

    def test_square_root(self):
        self.assertEqual('<{0}><{1}><{2}><{1}><{3}>{4}</{3}></{1}></{2}></{1}></{0}>'.format(
                'math', 'mrow', 'msqrt', 'mn', '2'), latex2mathml.convert(r'\sqrt{2}'))

    def test_root(self):
        self.assertEqual('<{0}><{1}><{2}><{1}><{3}>{4}</{3}></{1}><{1}><{3}>{5}</{3}></{1}></{2}></{1}></{0}>'.format(
                'math', 'mrow', 'mroot', 'mn', '2', '3'), latex2mathml.convert(r'\sqrt[3]{2}'))

    def test_binomial(self):
        self.assertEqual(
                "<{0}><{1}><{2}>{5}</{2}><{3} {9}='{10}'><{1}><{4}>{6}</{4}></{1}><{1}><{4}>{7}</{4}></{1}></{3}>"
                "<{2}>{8}</{2}></{1}></{0}>".format(
                        'math', 'mrow', 'mo', 'mfrac', 'mn', '&#x00028;', 2, 3, '&#x00029;', 'linethickness', 0),
                latex2mathml.convert(r'\binom{2}{3}'))

    def test_left_and_right(self):
        self.assertEqual("<{0}><{1}><{2} stretchy='true' form='prefix' fence='true'>{4}</{2}><{3}>{5}</{3}><{2} "
                         "stretchy='true' form='postfix' fence='true'>{6}</{2}></{1}></{0}>".format(
                'math', 'mrow', 'mo', 'mi', '&#x00028;', 'x', '&#x00029;'), latex2mathml.convert(r'\left(x\right)'))

    def test_space(self):
        self.assertEqual("<{0}><{1}><{2} {3}='{4}'/></{1}></{0}>".format('math', 'mrow', 'mspace', 'width', '0.167em'),
                         latex2mathml.convert('\,'))

    def test_overline(self):
        self.assertEqual("<{0}><{1}><{2}><{1}><{3}>{5}</{3}></{1}><{4} {7}='{8}'>{6}</{4}></{2}></{1}></{0}>".format(
                'math', 'mrow', 'mover', 'mi', 'mo', 'a', '&#x000AF;', 'stretchy', 'true'),
                latex2mathml.convert(r'\overline{a}'))

    def test_underline(self):
        self.assertEqual("<{0}><{1}><{2}><{1}><{3}>{5}</{3}></{1}><{4} {7}='{8}'>{6}</{4}></{2}></{1}></{0}>".format(
                'math', 'mrow', 'munder', 'mi', 'mo', 'a', '&#x00332;', 'stretchy', 'true'),
                latex2mathml.convert(r'\underline{a}'))

    def test_matrix(self):
        self.assertEqual('<{0}><{1}><{2}><{3}><{4}><{5}>{6}</{5}></{4}><{4}><{5}>{7}</{5}></{4}></{3}>'
                         '<{3}><{4}><{5}>{8}</{5}></{4}><{4}><{5}>{9}</{5}></{4}></{3}></{2}></{1}></{0}>'.format(
                'math', 'mrow', 'mtable', 'mtr', 'mtd', 'mi', 'a', 'b', 'c', 'd'),
                latex2mathml.convert(r'\begin{matrix}a & b \\ c & d \end{matrix}'))

    def test_matrix_without_begin_and_end(self):  # taken from MathJax
        self.assertEqual('<{0}><{1}><{2}><{3}><{4}><{5}>{6}</{5}></{4}><{4}><{5}>{7}</{5}></{4}></{3}>'
                         '<{3}><{4}><{5}>{8}</{5}></{4}><{4}><{5}>{9}</{5}></{4}></{3}></{2}></{1}></{0}>'.format(
                'math', 'mrow', 'mtable', 'mtr', 'mtd', 'mi', 'a', 'b', 'c', 'd'),
                latex2mathml.convert(r'\matrix{a & b \\ c & d}'))

if __name__ == '__main__':
    unittest.main()
