#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import re
from typing import Iterator, Optional, Union
from xml.etree.cElementTree import Element, SubElement, tostring
from xml.sax.saxutils import unescape

from latex2mathml.aggregator import aggregate
from latex2mathml.commands import COMMANDS, MATRICES
from latex2mathml.symbols_parser import convert_symbol


def convert(latex: str, xmlns: str = "http://www.w3.org/1998/Math/MathML") -> str:
    math = Element("math")
    math.attrib["xmlns"] = xmlns
    row = SubElement(math, "mrow")
    _classify_subgroup(aggregate(latex), row)
    return _convert(math)


def _convert(tree: Element) -> str:
    return unescape(tostring(tree, encoding="unicode"))


def _convert_matrix_content(
    param: list, parent: Element, alignment: Union[str, None] = None
) -> None:
    if not len(param):
        return
    has_list = False
    for i in param:
        if isinstance(i, list):
            has_list = True
            break
    if has_list:
        for row in param:
            _convert_matrix_row(row, parent, alignment)
    else:
        _convert_matrix_row(param, parent, alignment)


def _convert_matrix_row(row: list, parent: Element, alignment: Optional[str]):
    mtr = SubElement(parent, "mtr")
    iterable = iter(range(len(row)))  # type: Iterator[int]
    for i in iterable:
        element = row[i]
        if alignment:
            column_align = {"r": "right", "l": "left", "c": "center"}.get(
                alignment, ""
            )  # type: str
            mtd = SubElement(mtr, "mtd", columnalign=column_align)
        else:
            mtd = SubElement(mtr, "mtd")
        if isinstance(element, list):
            _classify_subgroup(element, mtd)
        elif element in COMMANDS:
            _convert_command(element, row, i, iterable, mtd)
        else:
            _classify(element, mtd)


def _convert_array_content(param: list, parent: Element, alignment: str = "") -> None:
    if alignment and "|" in alignment:
        _alignment, column_lines = [], []
        for j in alignment:
            if j == "|":
                column_lines.append("solid")
            else:
                _alignment.append(j)
            if len(_alignment) - len(column_lines) == 2:
                column_lines.append("none")
        parent.attrib["columnlines"] = " ".join(column_lines)
    else:
        _alignment = list(alignment)
    row_lines = []
    row_count = 0
    for row in param:
        row_count += 1
        mtr = SubElement(parent, "mtr")
        iterable = iter(range(len(row)))  # type: Iterator[int]
        index = 0
        has_row_line = False
        for i in iterable:
            element = row[i]
            if element == r"\hline" and row_count > 1:
                row_lines.append("solid")
                has_row_line = True
                continue
            align = None  # type: Union[str, None]
            try:
                align = _alignment[index]
            except IndexError:
                pass
            if align:
                column_align = {"r": "right", "l": "left", "c": "center"}.get(
                    align, ""
                )  # type: str
                mtd = SubElement(mtr, "mtd", columnalign=column_align)
            else:
                mtd = SubElement(mtr, "mtd")
            if isinstance(element, list):
                _classify_subgroup(element, mtd)
            elif element in COMMANDS:
                _convert_command(element, row, i, iterable, mtd)
            else:
                _classify(element, mtd)
            index += 1
        if not has_row_line and row_count > 1:
            row_lines.append("none")
    if "solid" in row_lines:
        parent.set("rowlines", " ".join(row_lines))


def _classify_subgroup(
    elements: list, row: Element, is_math_mode: bool = False
) -> None:
    iterable = iter(range(len(elements)))
    for i in iterable:
        element = elements[i]
        if isinstance(element, list):
            _row = SubElement(row, "mrow")
            _classify_subgroup(element, _row, is_math_mode)
            is_math_mode = False
        elif element in COMMANDS:
            _convert_command(element, elements, i, iterable, row)
        elif element.startswith(r"\math"):
            is_math_mode = True
        else:
            _classify(element, row, is_math_mode)


def _convert_command(
    element, elements, index: int, iterable: Iterator[int], parent: Element
):
    _get_prefix_element(element, parent)
    params, tag, attributes = COMMANDS[element]
    new_parent = SubElement(parent, tag, attributes)
    alignment = ""
    if element in MATRICES and (element.endswith("*") or element == r"\array"):
        index += 1
        alignment = elements[index]
        next(iterable)
    for j in range(params):
        index += 1
        param = elements[index]
        if element == r"\left" or element == r"\right":
            if param == ".":
                pass
            else:
                symbol = convert_symbol(param)
                new_parent.text = param if symbol is None else "&#x{};".format(symbol)
        elif element == r"\array":
            _convert_array_content(param, new_parent, alignment)
        elif element in MATRICES:
            _convert_matrix_content(param, new_parent, alignment)
        else:
            if isinstance(param, list):
                _parent = SubElement(new_parent, "mrow")
                _classify_subgroup(param, _parent)
            else:
                _classify(param, new_parent)
    _get_postfix_element(element, parent)
    if element in (r"\overline", r"\bar"):
        mo = SubElement(new_parent, "mo", stretchy="true")
        mo.text = "&#x000AF;"
    elif element == r"\underline":
        mo = SubElement(new_parent, "mo", stretchy="true")
        mo.text = "&#x00332;"
    [next(iterable) for _ in range(params)]


def _convert_and_append_operator(symbol: str, parent: Element) -> None:
    converted = convert_symbol(symbol)
    mo = SubElement(parent, "mo")
    mo.text = "&#x{};".format(converted)


def _get_postfix_element(element: str, row: Element) -> None:
    if element in (r"\binom", r"\pmatrix"):
        _convert_and_append_operator(r"\rparen", row)
    elif element == r"\bmatrix":
        _convert_and_append_operator(r"\rbrack", row)
    elif element == r"\Bmatrix":
        _convert_and_append_operator(r"\rbrace", row)
    elif element == r"\vmatrix":
        _convert_and_append_operator(r"\vert", row)
    elif element == r"\Vmatrix":
        _convert_and_append_operator(r"\Vert", row)


def _get_prefix_element(element: str, row: Element) -> None:
    if element in (r"\binom", r"\pmatrix"):
        _convert_and_append_operator(r"\lparen", row)
    elif element == r"\bmatrix":
        _convert_and_append_operator(r"\lbrack", row)
    elif element == r"\Bmatrix":
        _convert_and_append_operator(r"\lbrace", row)
    elif element == r"\vmatrix":
        _convert_and_append_operator(r"\vert", row)
    elif element == r"\Vmatrix":
        _convert_and_append_operator(r"\Vert", row)


def _classify(_element: str, parent: Element, is_math_mode: bool = False) -> None:
    symbol = convert_symbol(_element)
    if re.match(r"\d+(.\d+)?", _element):
        mn = SubElement(parent, "mn")
        mn.text = _element
    elif _element in "<>&":
        mo = SubElement(parent, "mo")
        mo.text = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}[_element]
    elif _element in "+-*/()=":
        mo = SubElement(parent, "mo")
        mo.text = _element if symbol is None else "&#x{};".format(symbol)
    elif (
        symbol
        and (
            int(symbol, 16) in range(int("2200", 16), int("22FF", 16) + 1)
            or int(symbol, 16) in range(int("2190", 16), int("21FF", 16) + 1)
        )
        or symbol == "."
    ):
        mo = SubElement(parent, "mo")
        mo.text = "&#x{};".format(symbol)
    elif _element.startswith("\\"):
        tag = SubElement(parent, "mo" if is_math_mode else "mi")
        if symbol:
            tag.text = "&#x{};".format(symbol)
        else:
            tag.text = _element
    else:
        tag = SubElement(parent, "mo" if is_math_mode else "mi")
        tag.text = _element


def main() -> None:  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(
        description="Pure Python library for LaTeX to MathML conversion"
    )
    required = parser.add_argument_group("required arguments")
    group = required.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-t", "--text", dest="text", type=str, required=False, help="Text",
    )
    group.add_argument(
        "-f", "--file", dest="file", type=str, required=False, help="File",
    )
    arguments = parser.parse_args()

    if arguments.text:
        print(convert(arguments.text))
    elif arguments.file:
        with open(arguments.file) as f:
            print(convert(f.read()))


if __name__ == "__main__":  # pragma: no cover
    main()
