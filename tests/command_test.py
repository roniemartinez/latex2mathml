#!/usr/bin/env python
import unittest
from latex2mathml import element, converter

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2016-2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Development"


class CommandTest(unittest.TestCase):

    def setUp(self):
        self.math = element.Element('math')
        self.math.pretty = True
        self.row = self.math.append_child('mrow')

    def test_subscript(self):
        sub = self.row.append_child('msub')
        sub.append_child('mi', 'a')
        sub.append_child('mi', 'b')
        self.assertEqual(str(self.math), converter.convert('a_b'))

    def test_superscript(self):
        sub = self.row.append_child('msup')
        sub.append_child('mi', 'a')
        sub.append_child('mi', 'b')
        self.assertEqual(str(self.math), converter.convert('a^b'))

    def test_subscript_and_superscript(self):
        sup = self.row.append_child('msubsup')
        sup.append_child('mi', 'a')
        sup.append_child('mi', 'b')
        sup.append_child('mi', 'c')
        self.assertEqual(str(self.math), converter.convert('a_b^c'))

    def test_superscript_and_subscript(self):
        subsup = self.row.append_child('msubsup')
        subsup.append_child('mi', 'a')
        subsup.append_child('mi', 'c')
        subsup.append_child('mi', 'b')
        self.assertEqual(str(self.math), converter.convert('a^b_c'))

    def test_subscript_within_curly_braces(self):
        row = self.row.append_child('mrow')
        sub = row.append_child('msub')
        sub.append_child('mi', 'a')
        sub.append_child('mi', 'b')
        self.assertEqual(str(self.math), converter.convert('{a_b}'))

    def test_superscript_within_curly_braces(self):
        row = self.row.append_child('mrow')
        sup = row.append_child('msup')
        sup.append_child('mi', 'a')
        sup.append_child('mi', 'b')
        self.assertEqual(str(self.math), converter.convert('{a^b}'))

    def test_superscript_with_curly_braces(self):
        subsup = self.row.append_child('msubsup')
        subsup.append_child('mi', 'a')
        subsup.append_child('mn', 3)
        row = subsup.append_child('mrow')
        row.append_child('mi', 'i')
        row.append_child('mo', '&#x0002B;')
        row.append_child('mn', 1)
        self.assertEqual(str(self.math), converter.convert('a^{i+1}_3'))

    def test_simple_fraction(self):
        frac = self.row.append_child('mfrac')
        frac.append_child('mrow').append_child('mn', 1)
        frac.append_child('mrow').append_child('mn', 2)
        self.assertEqual(str(self.math), converter.convert(r'\frac{1}{2}'))

    def test_square_root(self):
        sqrt = self.row.append_child('msqrt')
        sqrt.append_child('mrow').append_child('mn', 2)
        self.assertEqual(str(self.math), converter.convert(r'\sqrt{2}'))

    def test_root(self):
        root = self.row.append_child('mroot')
        root.append_child('mrow').append_child('mn', 2)
        root.append_child('mrow').append_child('mn', 3)
        self.assertEqual(str(self.math), converter.convert(r'\sqrt[3]{2}'))

    def test_binomial(self):
        self.row.append_child('mo', '&#x00028;')
        frac = self.row.append_child('mfrac', None, linethickness=0)
        frac.append_child('mrow').append_child('mn', 2)
        frac.append_child('mrow').append_child('mn', 3)
        self.row.append_child('mo', '&#x00029;')
        self.assertEqual(str(self.math), converter.convert(r'\binom{2}{3}'))

    def test_left_and_right(self):
        self.row.append_child('mo', '&#x00028;', stretchy='true', form='prefix', fence='true')
        self.row.append_child('mi', 'x')
        self.row.append_child('mo', '&#x00029;', stretchy='true', form='postfix', fence='true')
        self.assertEqual(str(self.math), converter.convert(r'\left(x\right)'))

    def test_space(self):
        self.row.append_child('mspace', None, width='0.167em')
        self.assertEqual(str(self.math), converter.convert('\,'))

    def test_overline(self):
        over = self.row.append_child('mover')
        over.append_child('mrow').append_child('mi', 'a')
        over.append_child('mo', '&#x000AF;', stretchy='true')
        self.assertEqual(str(self.math), converter.convert(r'\overline{a}'))

    def test_underline(self):
        under = self.row.append_child('munder')
        under.append_child('mrow').append_child('mi', 'a')
        under.append_child('mo', '&#x00332;', stretchy='true')
        self.assertEqual(str(self.math), converter.convert(r'\underline{a}'))

    def test_matrix(self):
        table = self.row.append_child('mtable')
        tr = table.append_child('mtr')
        tr.append_child('mtd').append_child('mi', 'a')
        tr.append_child('mtd').append_child('mi', 'b')
        tr = table.append_child('mtr')
        tr.append_child('mtd').append_child('mi', 'c')
        tr.append_child('mtd').append_child('mi', 'd')
        self.assertEqual(str(self.math), converter.convert(r'\begin{matrix}a & b \\ c & d \end{matrix}'))

    def test_matrix_without_begin_and_end(self):  # taken from MathJax
        table = self.row.append_child('mtable')
        tr = table.append_child('mtr')
        tr.append_child('mtd').append_child('mi', 'a')
        tr.append_child('mtd').append_child('mi', 'b')
        tr = table.append_child('mtr')
        tr.append_child('mtd').append_child('mi', 'c')
        tr.append_child('mtd').append_child('mi', 'd')
        self.assertEqual(str(self.math), converter.convert(r'\matrix{a & b \\ c & d}'))

    def test_matrix_with_alignment(self):
        table = self.row.append_child('mtable')
        tr = table.append_child('mtr')
        tr.append_child('mtd', None, columnalign='right').append_child('mi', 'a')
        tr.append_child('mtd', None, columnalign='right').append_child('mi', 'b')
        tr = table.append_child('mtr')
        tr.append_child('mtd', None, columnalign='right').append_child('mi', 'c')
        tr.append_child('mtd', None, columnalign='right').append_child('mi', 'd')
        self.assertEqual(str(self.math), converter.convert(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}'))

    def test_matrix_with_negative_sign(self):
        table = self.row.append_child('mtable')
        tr = table.append_child('mtr')
        mtd = tr.append_child('mtd')
        mtd.append_child('mo', '&#x02212;')
        mtd.append_child('mi', 'a')
        tr.append_child('mtd').append_child('mi', 'b')
        tr = table.append_child('mtr')
        tr.append_child('mtd').append_child('mi', 'c')
        tr.append_child('mtd').append_child('mi', 'd')
        self.assertEqual(str(self.math), converter.convert(r'\begin{matrix}-a & b \\ c & d \end{matrix}'))

    def test_pmatrix(self):
        self.row.append_child('mo', '&#x00028;')
        table = self.row.append_child('mtable')
        tr = table.append_child('mtr')
        tr.append_child('mtd').append_child('mi', 'a')
        tr.append_child('mtd').append_child('mi', 'b')
        tr = table.append_child('mtr')
        tr.append_child('mtd').append_child('mi', 'c')
        tr.append_child('mtd').append_child('mi', 'd')
        self.row.append_child('mo', '&#x00029;')
        self.assertEqual(str(self.math),
                         converter.convert(r'\begin{pmatrix}a & b \\ c & d \end{pmatrix}'))

    def test_simple_array(self):
        table = self.row.append_child('mtable')
        tr = table.append_child('mtr')
        tr.append_child('mtd', None, columnalign='center').append_child('mn', '1')
        tr.append_child('mtd', None, columnalign='right').append_child('mn', '2')
        tr = table.append_child('mtr')
        tr.append_child('mtd', None, columnalign='center').append_child('mn', '3')
        tr.append_child('mtd', None, columnalign='right').append_child('mn', '4')
        self.assertEqual(str(self.math), converter.convert(r'\begin{array}{cr} 1 & 2 \\ 3 & 4 \end{array}'''))

    def test_array_with_vertical_bars(self):
        table = self.row.append_child('mtable', None, columnlines='solid none')
        tr = table.append_child('mtr')
        tr.append_child('mtd', None, columnalign='center').append_child('mn', '1')
        tr.append_child('mtd', None, columnalign='right').append_child('mn', '2')
        tr.append_child('mtd', None, columnalign='left').append_child('mn', '3')
        tr = table.append_child('mtr')
        tr.append_child('mtd', None, columnalign='center').append_child('mn', '4')
        tr.append_child('mtd', None, columnalign='right').append_child('mn', '5')
        tr.append_child('mtd', None, columnalign='left').append_child('mn', '6')
        self.assertEqual(str(self.math),
                         converter.convert(r'\begin{array}{c|rl} 1 & 2 & 3 \\ 4 & 5 & 6 \end{array}'''))

    def test_array_with_horizontal_lines(self):
        table = self.row.append_child('mtable', None, rowlines="none solid")
        tr = table.append_child('mtr')
        tr.append_child('mtd', None, columnalign='center').append_child('mn', '1')
        tr.append_child('mtd', None, columnalign='right').append_child('mn', '2')
        tr = table.append_child('mtr')
        tr.append_child('mtd', None, columnalign='center').append_child('mn', '3')
        tr.append_child('mtd', None, columnalign='right').append_child('mn', '4')
        tr = table.append_child('mtr')
        tr.append_child('mtd', None, columnalign='center').append_child('mn', '5')
        tr.append_child('mtd', None, columnalign='right').append_child('mn', '6')
        self.assertEqual(str(self.math),
                         converter.convert(r'\begin{array}{cr} 1 & 2 \\ 3 & 4 \\ \hline 5 & 6 \end{array}'''))

if __name__ == '__main__':
    unittest.main(verbosity=2)
