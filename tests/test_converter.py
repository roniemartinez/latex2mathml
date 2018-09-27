#!/usr/bin/env python
import xml.etree.cElementTree as eTree
from xml.sax.saxutils import unescape

# noinspection PyPackageRequirements
import pytest

from latex2mathml.converter import convert

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2016-2018, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Development"


@pytest.fixture
def math_and_row():
    math = eTree.Element('math')
    row = eTree.SubElement(math, 'mrow')
    yield math, row


def test_single_identifier(math_and_row):
    math, row = math_and_row
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('x')


def test_multiple_identifiers(math_and_row):
    math, row = math_and_row
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'y'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'z'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('xyz')


def test_single_number(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '3'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('3')


def test_multiple_numbers(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '333'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('333')


def test_decimal_numbers(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '12.34'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('12.34')


def test_numbers_and_identifiers(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '12'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('12x')


def test_single_operator(math_and_row):
    math, row = math_and_row
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x0002B;'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('+')


def test_numbers_and_operators(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '3'
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x02212;'
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('3-2')


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
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('3x*2')


def test_single_group(math_and_row):
    math, row = math_and_row
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'a'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('{a}')


def test_multiple_groups(math_and_row):
    math, row = math_and_row
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'b'
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('{a}{b}')


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
    xml_string = eTree.tostring(math)
    try:
        expected = unescape(xml_string)
    except TypeError:  # pragma: nocover_py2
        expected = unescape(xml_string.decode('utf-8'))
    assert expected == convert('{a+{b}}')
