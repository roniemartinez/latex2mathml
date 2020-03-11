#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import xml.etree.cElementTree as eTree

import pytest
from multidict import MultiDict
from xmljson import BadgerFish

# noinspection PyProtectedMember
from latex2mathml.converter import convert, _convert


@pytest.fixture
def math_and_row():
    math = eTree.Element('math')
    math.set('xmlns', 'http://www.w3.org/1998/Math/MathML')
    row = eTree.SubElement(math, 'mrow')
    yield math, row


@pytest.mark.parametrize(
    'latex,json',
    ids=[
        'issue #42',
        'issue #45 lt',
        'issue #45 gt',
        'issue #45 amp',
        'issue #44',
    ],
    argvalues=[
        (
                r'\sqrt { ( - 25 ) ^ { 2 } } = \pm 25',
                MultiDict([
                    ('msqrt', {
                        'mrow':
                            MultiDict([
                                ('mo', {'$': '&#x00028;'}),
                                ('mo', {'$': '&#x02212;'}),
                                ('mn', {'$': '25'}),
                                ('msup', {
                                    'mo': {'$': '&#x00029;'},
                                    'mrow': {'mn': {'$': '2'}}
                                })
                            ])
                    }),
                    ('mo', {'$': '&#x0003D;'}),
                    ('mi', {'$': '&#x000B1;'}),
                    ('mn', {'$': '25'}),
                ])
        ),
        (
                '2 < 5',
                MultiDict([
                    ('mn', {'$': '2'}),
                    ('mo', {'$': '&lt;'}),
                    ('mn', {'$': '5'}),
                ])
        ),
        (
                '2 > 5',
                MultiDict([
                    ('mn', {'$': '2'}),
                    ('mo', {'$': '&gt;'}),
                    ('mn', {'$': '5'}),
                ])
        ),
        (
                '&',
                {
                    'mo': '&amp;'
                }
        ),
        (
                r'\left(- x^{3} + 5\right)^{5}',
                {
                    'msup': MultiDict([
                        ('mrow', MultiDict([
                        ])),
                        ('mrow', {'mn': {'$': '5'}})
                    ])
                }
        ),
    ]

)
def test_converter(latex, json):
    parent = {
        'math': {
            '@xmlns': 'http://www.w3.org/1998/Math/MathML',
            'mrow': json
        }
    }
    badgerfish = BadgerFish(dict_type=MultiDict)
    math = badgerfish.etree(parent)
    assert _convert(math[0]) == convert(latex)
