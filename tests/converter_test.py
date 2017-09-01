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


class ConverterTest(unittest.TestCase):

    def setUp(self):
        self.math = eTree.Element('math')
        self.row = eTree.SubElement(self.math, 'mrow')

    def test_single_identifier(self):
        mi = eTree.SubElement(self.row, 'mi')
        mi.text = 'x'
        self.assertEqual(eTree.tostring(self.math), converter.convert('x'))

    def test_multiple_identifiers(self):
        mi = eTree.SubElement(self.row, 'mi')
        mi.text = 'x'
        mi = eTree.SubElement(self.row, 'mi')
        mi.text = 'y'
        mi = eTree.SubElement(self.row, 'mi')
        mi.text = 'z'
        self.assertEqual(eTree.tostring(self.math), converter.convert('xyz'))

    def test_single_number(self):
        mn = eTree.SubElement(self.row, 'mn')
        mn.text = '3'
        self.assertEqual(eTree.tostring(self.math), converter.convert('3'))

    def test_multiple_numbers(self):
        mn = eTree.SubElement(self.row, 'mn')
        mn.text = '333'
        self.assertEqual(eTree.tostring(self.math), converter.convert('333'))

    def test_decimal_numbers(self):
        mn = eTree.SubElement(self.row, 'mn')
        mn.text = '12.34'
        self.assertEqual(eTree.tostring(self.math), converter.convert('12.34'))

    def test_numbers_and_identifiers(self):
        mn = eTree.SubElement(self.row, 'mn')
        mn.text = '12'
        mi = eTree.SubElement(self.row, 'mi')
        mi.text = 'x'
        self.assertEqual(eTree.tostring(self.math), converter.convert('12x'))

    def test_single_operator(self):
        mo = eTree.SubElement(self.row, 'mo')
        mo.text = '&#x0002B;'
        self.assertEqual(eTree.tostring(self.math), converter.convert('+'))

    def test_numbers_and_operators(self):
        mn = eTree.SubElement(self.row, 'mn')
        mn.text = '3'
        mo = eTree.SubElement(self.row, 'mo')
        mo.text = '&#x02212;'
        mn = eTree.SubElement(self.row, 'mn')
        mn.text = '2'
        self.assertEqual(eTree.tostring(self.math), converter.convert('3-2'))

    def test_numbers_and_identifiers_and_operators(self):
        mn = eTree.SubElement(self.row, 'mn')
        mn.text = '3'
        mi = eTree.SubElement(self.row, 'mi')
        mi.text = 'x'
        mo = eTree.SubElement(self.row, 'mo')
        mo.text = '&#x0002A;'
        mn = eTree.SubElement(self.row, 'mn')
        mn.text = '2'
        self.assertEqual(eTree.tostring(self.math), converter.convert('3x*2'))

    def test_single_group(self):
        mrow = eTree.SubElement(self.row, 'mrow')
        mi = eTree.SubElement(mrow, 'mi')
        mi.text = 'a'
        self.assertEqual(eTree.tostring(self.math), converter.convert('{a}'))

    def test_multiple_groups(self):
        mrow = eTree.SubElement(self.row, 'mrow')
        mi = eTree.SubElement(mrow, 'mi')
        mi.text = 'a'
        mrow = eTree.SubElement(self.row, 'mrow')
        mi = eTree.SubElement(mrow, 'mi')
        mi.text = 'b'
        self.assertEqual(eTree.tostring(self.math), converter.convert('{a}{b}'))

    def test_inner_group(self):
        mrow = eTree.SubElement(self.row, 'mrow')
        mi = eTree.SubElement(mrow, 'mi')
        mi.text = 'a'
        mo = eTree.SubElement(mrow, 'mo')
        mo.text = '&#x0002B;'
        mrow = eTree.SubElement(mrow, 'mrow')
        mi = eTree.SubElement(mrow, 'mi')
        mi.text = 'b'
        self.assertEqual(eTree.tostring(self.math), converter.convert('{a+{b}}'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
