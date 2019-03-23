#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import xml.etree.cElementTree as eTree

# noinspection PyPackageRequirements
import pytest

# noinspection PyProtectedMember
from latex2mathml.converter import convert, _convert


@pytest.fixture
def math_and_row():
    math = eTree.Element('math')
    row = eTree.SubElement(math, 'mrow')
    yield math, row


def test_issue_42(math_and_row):
    math, row = math_and_row
    msqrt = eTree.SubElement(row, 'msqrt')
    mrow = eTree.SubElement(msqrt, 'mrow')
    mo = eTree.SubElement(mrow, 'mo')
    mo.text = '&#x00028;'
    mo = eTree.SubElement(mrow, 'mo')
    mo.text = '&#x02212;'
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '25'

    msup = eTree.SubElement(mrow, 'msup')
    mo = eTree.SubElement(msup, 'mo')
    mo.text = '&#x00029;'
    mrow2 = eTree.SubElement(msup, 'mrow')
    mn = eTree.SubElement(mrow2, 'mn')
    mn.text = '2'

    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x0003D;'
    mi = eTree.SubElement(row, 'mi')
    mi.text = '&#x000B1;'
    mn = eTree.SubElement(row, 'mn')
    mn.text = '25'

    assert _convert(math) == convert(r'\sqrt { ( - 25 ) ^ { 2 } } = \pm 25')


def test_issue_45_lt(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&lt;'
    mn = eTree.SubElement(row, 'mn')
    mn.text = '5'
    assert _convert(math) == convert('2 < 5')


def test_issue_45_gt(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&gt;'
    mn = eTree.SubElement(row, 'mn')
    mn.text = '5'
    assert _convert(math) == convert('2 > 5')


def test_issue_45_amp(math_and_row):
    math, row = math_and_row
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&amp;'
    assert _convert(math) == convert('&')


def test_issue_44(math_and_row):
    math, row = math_and_row
    msup = eTree.SubElement(row, 'msup')
    mrow = eTree.SubElement(msup, 'mrow')
    mo = eTree.SubElement(mrow, 'mo', fence='true', form='prefix', stretchy='true')
    mo.text = '&#x00028;'
    mrow = eTree.SubElement(msup, 'mrow')
    mo = eTree.SubElement(mrow, 'mo')
    mo.text = '&#x02212;'
    msup2 = eTree.SubElement(row, 'msup')
    mi = eTree.SubElement(msup2, 'mi')
    mi.text = 'x'
    mrow = eTree.SubElement(msup2, 'mrow')
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '3'

    mo = eTree.SubElement(mrow, 'mo')
    mo.text = '&#x0002B;'
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '5'

    mo = eTree.SubElement(mrow, 'mo', fence='true', form='postfix', stretchy='true')
    mo.text = '&#x00029;'

    mrow = eTree.SubElement(msup, 'mrow')
    mn = eTree.SubElement(mrow, 'mn')
    mn.text = '5'
