#!/usr/bin/env python
import unittest
import xml.etree.cElementTree as eTree
from latex2mathml import converter

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2016-2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Development"


class CommandTest(unittest.TestCase):

    def setUp(self):
        self.math = eTree.Element('math')
        self.row = eTree.SubElement(self.math, 'mrow')

    def test_subscript(self):
        sub = eTree.SubElement(self.row, 'msub')
        mi = eTree.SubElement(sub, 'mi')
        mi.text = 'a'
        mi = eTree.SubElement(sub, 'mi')
        mi.text = 'b'
        self.assertEqual(eTree.tostring(self.math), converter.convert('a_b'))

    def test_superscript(self):
        sup = eTree.SubElement(self.row, 'msup')
        mi = eTree.SubElement(sup, 'mi')
        mi.text = 'a'
        mi = eTree.SubElement(sup, 'mi')
        mi.text = 'b'
        self.assertEqual(eTree.tostring(self.math), converter.convert('a^b'))

    def test_subscript_and_superscript(self):
        subsup = eTree.SubElement(self.row, 'msubsup')
        mi = eTree.SubElement(subsup, 'mi')
        mi.text = 'a'
        mi = eTree.SubElement(subsup, 'mi')
        mi.text = 'b'
        mi = eTree.SubElement(subsup, 'mi')
        mi.text = 'c'
        self.assertEqual(eTree.tostring(self.math), converter.convert('a_b^c'))

    def test_superscript_and_subscript(self):
        subsup = eTree.SubElement(self.row, 'msubsup')
        mi = eTree.SubElement(subsup, 'mi')
        mi.text = 'a'
        mi = eTree.SubElement(subsup, 'mi')
        mi.text = 'c'
        mi = eTree.SubElement(subsup, 'mi')
        mi.text = 'b'
        self.assertEqual(eTree.tostring(self.math), converter.convert('a^b_c'))

    def test_subscript_within_curly_braces(self):
        row = eTree.SubElement(self.row, 'mrow')
        sub = eTree.SubElement(row, 'msub')
        mi = eTree.SubElement(sub, 'mi')
        mi.text = 'a'
        mi = eTree.SubElement(sub, 'mi')
        mi.text = 'b'
        self.assertEqual(eTree.tostring(self.math), converter.convert('{a_b}'))

    def test_superscript_within_curly_braces(self):
        row = eTree.SubElement(self.row, 'mrow')
        sup = eTree.SubElement(row, 'msup')
        mi = eTree.SubElement(sup, 'mi')
        mi.text = 'a'
        mi = eTree.SubElement(sup, 'mi')
        mi.text = 'b'
        self.assertEqual(eTree.tostring(self.math), converter.convert('{a^b}'))

    def test_superscript_with_curly_braces(self):
        subsup = eTree.SubElement(self.row, 'msubsup')
        mi = eTree.SubElement(subsup, 'mi')
        mi.text = 'a'
        mn = eTree.SubElement(subsup, 'mn')
        mn.text = '3'
        row = eTree.SubElement(subsup, 'mrow')
        mi = eTree.SubElement(row, 'mi')
        mi.text = 'i'
        mo = eTree.SubElement(row, 'mo')
        mo.text = '&#x0002B;'
        mn = eTree.SubElement(row, 'mn')
        mn.text = '1'
        self.assertEqual(eTree.tostring(self.math), converter.convert('a^{i+1}_3'))

    def test_simple_fraction(self):
        frac = eTree.SubElement(self.row, 'mfrac')
        row = eTree.SubElement(frac, 'mrow')
        mn = eTree.SubElement(row, 'mn')
        mn.text = '1'
        row = eTree.SubElement(frac, 'mrow')
        mn = eTree.SubElement(row, 'mn')
        mn.text = '2'
        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\frac{1}{2}'))

    def test_square_root(self):
        sqrt = eTree.SubElement(self.row, 'msqrt')
        row = eTree.SubElement(sqrt, 'mrow')
        mn = eTree.SubElement(row, 'mn')
        mn.text = '2'
        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\sqrt{2}'))

    def test_root(self):
        root = eTree.SubElement(self.row, 'mroot')
        row = eTree.SubElement(root, 'mrow')
        mn = eTree.SubElement(row, 'mn')
        mn.text = '2'
        row = eTree.SubElement(root, 'mrow')
        mn = eTree.SubElement(row, 'mn')
        mn.text = '3'
        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\sqrt[3]{2}'))

    def test_binomial(self):
        mo = eTree.SubElement(self.row, 'mo')
        mo.text = '&#x00028;'
        frac = eTree.SubElement(self.row, 'mfrac', linethickness="0")
        row = eTree.SubElement(frac, 'mrow')
        mn = eTree.SubElement(row, 'mn')
        mn.text = '2'
        row = eTree.SubElement(frac, 'mrow')
        mn = eTree.SubElement(row, 'mn')
        mn.text = '3'
        mo = eTree.SubElement(self.row, 'mo')
        mo.text = '&#x00029;'
        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\binom{2}{3}'))

    def test_left_and_right(self):
        mo = eTree.SubElement(self.row, 'mo', stretchy='true', form='prefix', fence='true')
        mo.text = '&#x00028;'
        mi = eTree.SubElement(self.row, 'mi')
        mi.text = 'x'
        mo = eTree.SubElement(self.row, 'mo', stretchy='true', form='postfix', fence='true')
        mo.text = '&#x00029;'
        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\left(x\right)'))

    def test_space(self):
        eTree.SubElement(self.row, 'mspace', width='0.167em')
        self.assertEqual(eTree.tostring(self.math), converter.convert('\,'))

    def test_overline(self):
        over = eTree.SubElement(self.row, 'mover')
        row = eTree.SubElement(over, 'mrow')
        mi = eTree.SubElement(row, 'mi')
        mi.text = 'a'
        mo = eTree.SubElement(over, 'mo', stretchy='true')
        mo.text = '&#x000AF;'
        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\overline{a}'))

    def test_underline(self):
        under = eTree.SubElement(self.row, 'munder')
        mrow = eTree.SubElement(under, 'mrow')
        mi = eTree.SubElement(mrow, 'mi')
        mi.text = 'a'
        mo = eTree.SubElement(under, 'mo', stretchy='true')
        mo.text = '&#x00332;'
        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\underline{a}'))

    def test_matrix(self):
        table = eTree.SubElement(self.row, 'mtable')

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'a'
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'b'

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'c'
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'd'
        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\begin{matrix}a & b \\ c & d \end{matrix}'))

    def test_matrix_without_begin_and_end(self):  # taken from MathJax
        table = eTree.SubElement(self.row, 'mtable')

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'a'
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'b'

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'c'
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'd'

        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\matrix{a & b \\ c & d}'))

    def test_matrix_with_alignment(self):
        table = eTree.SubElement(self.row, 'mtable')

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'a'
        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'b'

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'c'
        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'd'

        self.assertEqual(eTree.tostring(self.math),
                         converter.convert(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}'))

    def test_matrix_with_negative_sign(self):
        table = eTree.SubElement(self.row, 'mtable')

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd')
        mo = eTree.SubElement(td, 'mo')
        mo.text = '&#x02212;'
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'a'
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'b'

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'c'
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'd'

        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\begin{matrix}-a & b \\ c & d \end{matrix}'))

    def test_pmatrix(self):
        mo = eTree.SubElement(self.row, 'mo')
        mo.text = '&#x00028;'
        table = eTree.SubElement(self.row, 'mtable')

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'a'
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'b'

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'c'
        td = eTree.SubElement(tr, 'mtd')
        mi = eTree.SubElement(td, 'mi')
        mi.text = 'd'

        mo = eTree.SubElement(self.row, 'mo')
        mo.text = '&#x00029;'
        self.assertEqual(eTree.tostring(self.math), converter.convert(r'\begin{pmatrix}a & b \\ c & d \end{pmatrix}'))

    def test_simple_array(self):
        table = eTree.SubElement(self.row, 'mtable')

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd', columnalign='center')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '1'
        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '2'

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd', columnalign='center')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '3'
        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '4'

        self.assertEqual(eTree.tostring(self.math),
                         converter.convert(r'\begin{array}{cr} 1 & 2 \\ 3 & 4 \end{array}'''))

    def test_array_with_vertical_bars(self):
        table = eTree.SubElement(self.row, 'mtable', columnlines='solid none')
        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd', columnalign='center')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '1'
        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '2'
        td = eTree.SubElement(tr, 'mtd', columnalign='left')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '3'

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd', columnalign='center')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '4'
        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '5'
        td = eTree.SubElement(tr, 'mtd', columnalign='left')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '6'

        self.assertEqual(eTree.tostring(self.math),
                         converter.convert(r'\begin{array}{c|rl} 1 & 2 & 3 \\ 4 & 5 & 6 \end{array}'''))

    def test_array_with_horizontal_lines(self):
        table = eTree.SubElement(self.row, 'mtable', rowlines="none solid")

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd', columnalign='center')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '1'

        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '2'

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd', columnalign='center')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '3'

        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '4'

        tr = eTree.SubElement(table, 'mtr')
        td = eTree.SubElement(tr, 'mtd', columnalign='center')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '5'

        td = eTree.SubElement(tr, 'mtd', columnalign='right')
        mn = eTree.SubElement(td, 'mn')
        mn.text = '6'
        self.assertEqual(eTree.tostring(self.math),
                         converter.convert(r'\begin{array}{cr} 1 & 2 \\ 3 & 4 \\ \hline 5 & 6 \end{array}'''))

if __name__ == '__main__':
    unittest.main(verbosity=2)
