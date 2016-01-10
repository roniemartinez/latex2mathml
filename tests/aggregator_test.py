#!/usr/bin/python
import unittest
from pprint import pprint

import latex2mathml

__author__ = 'Ronie Martinez'


class AggregatorTest(unittest.TestCase):
    def test_single_group(self):
        self.assertListEqual([['a']], latex2mathml.aggregate('{a}'))

    def test_multiple_groups(self):
        self.assertListEqual([['a'], ['b']], latex2mathml.aggregate('{a}{b}'))

    def test_inner_group(self):
        self.assertListEqual([['a', '+', ['b']]], latex2mathml.aggregate('{a+{b}}'))

    def test_subscript(self):
        self.assertListEqual(['_', 'a', 'b'], latex2mathml.aggregate('a_b'))

    def test_superscript(self):
        self.assertListEqual(['^', 'a', 'b'], latex2mathml.aggregate('a^b'))

    def test_subscript_and_superscript(self):
        self.assertListEqual(['_^', 'a', 'b', 'c'], latex2mathml.aggregate('a_b^c'))

    def test_root(self):
        self.assertListEqual([r'\root', ['2'], ['3']], latex2mathml.aggregate(r'\sqrt[3]{2}'))

    def test_matrix(self):
        self.assertListEqual([r'\matrix', [['a', 'b'], ['c', 'd']]],
                             list(latex2mathml.aggregate(r'\begin{matrix}a & b \\ c & d \end{matrix}')))

    def test_matrix_with_alignment(self):
        self.assertListEqual([r'\matrix*', 'r', [['a', 'b'], ['c', 'd']]],
                             list(latex2mathml.aggregate(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}')))

    def test_matrix_with_negative_sign(self):
        self.assertListEqual([r'\matrix', [[['-', 'a'], 'b'], ['c', 'd']]],
                             list(latex2mathml.aggregate(r'\begin{matrix}-a & b \\ c & d \end{matrix}')))

    def test_complex_matrix(self):
        self.assertListEqual(['\\matrix', [['_', 'a', ['1'], '_', 'b', ['2']], ['_', 'c', ['3'], '_', 'd', ['4']]]],
                             list(latex2mathml.aggregate(r'\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}')))

if __name__ == '__main__':
    unittest.main()
