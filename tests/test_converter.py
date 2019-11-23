#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import xml.etree.cElementTree as eTree

# noinspection PyPackageRequirements
from collections import OrderedDict

import pytest

# noinspection PyProtectedMember
from latex2mathml.converter import convert, _convert


@pytest.fixture
def math_and_row():
    math = eTree.Element('math')
    math.set('xmlns', 'http://www.w3.org/1998/Math/MathML')
    row = eTree.SubElement(math, 'mrow')
    yield math, row


def test_single_identifier(math_and_row):
    math, row = math_and_row
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    assert _convert(math) == convert('x')


def test_multiple_identifiers(math_and_row):
    math, row = math_and_row
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'y'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'z'
    assert _convert(math) == convert('xyz')


def test_single_number(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '3'
    assert _convert(math) == convert('3')


def test_multiple_numbers(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '333'
    assert _convert(math) == convert('333')


def test_decimal_numbers(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '12.34'
    assert _convert(math) == convert('12.34')


def test_numbers_and_identifiers(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '12'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    assert _convert(math) == convert('12x')


def test_single_operator(math_and_row):
    math, row = math_and_row
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x0002B;'
    assert _convert(math) == convert('+')


def test_numbers_and_operators(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '3'
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x02212;'
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    assert _convert(math) == convert('3-2')


def test_numbers_and_identifiers_and_operators(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '3'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x0002A;'
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    assert _convert(math) == convert('3x*2')


def test_single_group(math_and_row):
    math, row = math_and_row
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'a'
    assert _convert(math) == convert('{a}')


def test_multiple_groups(math_and_row):
    math, row = math_and_row
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'b'
    assert _convert(math) == convert('{a}{b}')


def test_inner_group(math_and_row):
    math, row = math_and_row
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'a'
    mo = eTree.SubElement(mrow, 'mo')
    mo.text = '&#x0002B;'
    mrow = eTree.SubElement(mrow, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'b'
    assert _convert(math) == convert('{a+{b}}')


def test_over(math_and_row):
    math, row = math_and_row
    frac = eTree.SubElement(row, 'mfrac')
    row = eTree.SubElement(frac, 'mrow')
    mn = eTree.SubElement(row, 'mn')
    mn.text = '1'
    row = eTree.SubElement(frac, 'mrow')
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    assert _convert(math) == convert(r'1 \over 2')


def test_over_inside_braces(math_and_row):
    math, row = math_and_row
    row = eTree.SubElement(row, 'mrow')
    frac = eTree.SubElement(row, 'mfrac')
    row = eTree.SubElement(frac, 'mrow')
    mn = eTree.SubElement(row, 'mn')
    mn.text = '1'
    row = eTree.SubElement(frac, 'mrow')
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    assert _convert(math) == convert(r'{1 \over 2}')


def test_complex_matrix(math_and_row):
    math, row = math_and_row
    mtable = eTree.SubElement(row, 'mtable')

    mtr = eTree.SubElement(mtable, 'mtr')
    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '1'

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'b'
    mrow = eTree.SubElement(msub, 'mrow')
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '2'

    mtr = eTree.SubElement(mtable, 'mtr')

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'c'
    mrow = eTree.SubElement(msub, 'mrow')
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '3'

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'd'
    mrow = eTree.SubElement(msub, 'mrow')
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '4'

    latex = r'\begin{matrix}a_{1} & b_{2} \\ c_{3} & d_{4} \end{matrix}'
    assert _convert(math) == convert(latex)


def test_null_delimiter(math_and_row):
    math, row = math_and_row
    mrow = eTree.SubElement(row, 'mrow')
    left = eTree.SubElement(mrow, 'mo', OrderedDict([('stretchy', 'true'), ('fence', 'true'), ('form', 'prefix')]))
    left.text = '&#x0007B;'

    mrow2 = eTree.SubElement(mrow, 'mrow')
    table = eTree.SubElement(mrow2, 'mtable')
    eTree.SubElement(mrow, 'mo', OrderedDict([('stretchy', 'true'), ('fence', 'true'), ('form', 'postfix')]))

    mtr = eTree.SubElement(table, 'mtr')
    mtd = eTree.SubElement(mtr, 'mtd', columnalign='left')
    mn = eTree.SubElement(mtd, 'mn')
    mn.text = '3'
    mi = eTree.SubElement(mtd, 'mi')
    mi.text = 'x'
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x02212;'
    mn = eTree.SubElement(mtd, 'mn')
    mn.text = '5'
    mi = eTree.SubElement(mtd, 'mi')
    mi.text = 'y'
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x0002B;'
    mn = eTree.SubElement(mtd, 'mn')
    mn.text = '4'
    mi = eTree.SubElement(mtd, 'mi')
    mi.text = 'z'
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x0003D;'
    mn = eTree.SubElement(mtd, 'mn')
    mn.text = '0'

    mtr = eTree.SubElement(table, 'mtr')
    mtd = eTree.SubElement(mtr, 'mtd', columnalign='left')
    mi = eTree.SubElement(mtd, 'mi')
    mi.text = 'x'
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x02212;'
    mi = eTree.SubElement(mtd, 'mi')
    mi.text = 'y'
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x0002B;'
    mn = eTree.SubElement(mtd, 'mn')
    mn.text = '8'
    mi = eTree.SubElement(mtd, 'mi')
    mi.text = 'z'
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x0003D;'
    mn = eTree.SubElement(mtd, 'mn')
    mn.text = '0'

    mtr = eTree.SubElement(table, 'mtr')
    mtd = eTree.SubElement(mtr, 'mtd', columnalign='left')
    mn = eTree.SubElement(mtd, 'mn')
    mn.text = '2'
    mi = eTree.SubElement(mtd, 'mi')
    mi.text = 'x'
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x02212;'
    mn = eTree.SubElement(mtd, 'mn')
    mn.text = '6'
    mi = eTree.SubElement(mtd, 'mi')
    mi.text = 'y'
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x0002B;'
    mi = eTree.SubElement(mtd, 'mi')
    mi.text = 'z'
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x0003D;'
    mn = eTree.SubElement(mtd, 'mn')
    mn.text = '0'

    latex = r'\left\{ \begin{array} { l } { 3x - 5y + 4z = 0} \\ { x - y + 8z = 0} \\ { 2x - 6y + z = 0} \end{array} ' \
            r'\right.'
    assert _convert(math) == convert(latex)


def test_issue_33(math_and_row):
    latex = r'''\begin{bmatrix}
     a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
     a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
     \vdots  & \vdots  & \ddots & \vdots  \\
     a_{m,1} & a_{m,2} & \cdots & a_{m,n}
    \end{bmatrix}'''
    math, row = math_and_row
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x0005B;'

    mtable = eTree.SubElement(row, 'mtable')

    # 1st row
    mtr = eTree.SubElement(mtable, 'mtr')

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mi = eTree.SubElement(mrow, 'mn')
    mi.text = '1'
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = ','
    mi = eTree.SubElement(mrow, 'mn')
    mi.text = '1'

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mi = eTree.SubElement(mrow, 'mn')
    mi.text = '1'
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = ','
    mi = eTree.SubElement(mrow, 'mn')
    mi.text = '2'

    mtd = eTree.SubElement(mtr, 'mtd')
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x022EF;'

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mi = eTree.SubElement(mrow, 'mn')
    mi.text = '1'
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = ','
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'n'

    # 2nd row
    mtr = eTree.SubElement(mtable, 'mtr')

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mi = eTree.SubElement(mrow, 'mn')
    mi.text = '2'
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = ','
    mi = eTree.SubElement(mrow, 'mn')
    mi.text = '1'

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mi = eTree.SubElement(mrow, 'mn')
    mi.text = '2'
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = ','
    mi = eTree.SubElement(mrow, 'mn')
    mi.text = '2'

    mtd = eTree.SubElement(mtr, 'mtd')
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x022EF;'

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '2'
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = ','
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'n'

    # 3rd row
    mtr = eTree.SubElement(mtable, 'mtr')
    mtd = eTree.SubElement(mtr, 'mtd')
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x022EE;'
    mtd = eTree.SubElement(mtr, 'mtd')
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x022EE;'
    mtd = eTree.SubElement(mtr, 'mtd')
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x022F1;'
    mtd = eTree.SubElement(mtr, 'mtd')
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x022EE;'

    # 4th row
    mtr = eTree.SubElement(mtable, 'mtr')

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'm'
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = ','
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '1'

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'm'
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = ','
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '2'

    mtd = eTree.SubElement(mtr, 'mtd')
    mo = eTree.SubElement(mtd, 'mo')
    mo.text = '&#x022EF;'

    mtd = eTree.SubElement(mtr, 'mtd')
    msub = eTree.SubElement(mtd, 'msub')
    mi = eTree.SubElement(msub, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(msub, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'm'
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = ','
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'n'

    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x0005D;'
    assert _convert(math) == convert(latex)


def test_issue_51(math_and_row):
    math, row = math_and_row
    mi = eTree.SubElement(row, 'mi')
    mi.text = '&#x0211D;'
    assert _convert(math) == convert(r'\mathbb{R}')
