#!/usr/bin/env python
import unittest
from latex2mathml import aggregator

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2016-2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Development"


class AggregatorTest(unittest.TestCase):
    def test_single_group(self):
        self.assertListEqual([['a']], aggregator.aggregate('{a}'))

    def test_multiple_groups(self):
        self.assertListEqual([['a'], ['b']], aggregator.aggregate('{a}{b}'))

    def test_inner_group(self):
        self.assertListEqual([['a', '+', ['b']]], aggregator.aggregate('{a+{b}}'))

    def test_subscript(self):
        self.assertListEqual(['_', 'a', 'b'], aggregator.aggregate('a_b'))

    def test_superscript(self):
        self.assertListEqual(['^', 'a', 'b'], aggregator.aggregate('a^b'))

    def test_subscript_and_superscript(self):
        self.assertListEqual(['_^', 'a', 'b', 'c'], aggregator.aggregate('a_b^c'))

    def test_root(self):
        self.assertListEqual([r'\root', ['2'], ['3']], aggregator.aggregate(r'\sqrt[3]{2}'))

    def test_matrix(self):
        self.assertListEqual([r'\matrix', [['a', 'b'], ['c', 'd']]],
                             list(aggregator.aggregate(r'\begin{matrix}a & b \\ c & d \end{matrix}')))

    def test_matrix_with_alignment(self):
        self.assertListEqual([r'\matrix*', 'r', [['a', 'b'], ['c', 'd']]],
                             list(aggregator.aggregate(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}')))

    def test_matrix_with_negative_sign(self):
        self.assertListEqual([r'\matrix', [[['-', 'a'], 'b'], ['c', 'd']]],
                             list(aggregator.aggregate(r'\begin{matrix}-a & b \\ c & d \end{matrix}')))

    def test_complex_matrix(self):
        self.assertListEqual(['\\matrix', [['_', 'a', ['1'], '_', 'b', ['2']], ['_', 'c', ['3'], '_', 'd', ['4']]]],
                             list(aggregator.aggregate(r'\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}')))

    def test_simple_array(self):
        self.assertListEqual([r'\array', 'cc', [['1', '2'], ['3', '4']]],
                             list(aggregator.aggregate(r'\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}''')))


if __name__ == '__main__':
    unittest.main(verbosity=2)
