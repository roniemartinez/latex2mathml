import re
from collections import OrderedDict
from typing import Any, Iterator, List, Optional, Union
from xml.etree.cElementTree import Element, SubElement, tostring  # nosec
from xml.sax.saxutils import unescape  # nosec

import pkg_resources

from latex2mathml.aggregator import aggregate
from latex2mathml.commands import COMMANDS, MATRICES
from latex2mathml.symbols_parser import convert_symbol


def convert(
    latex: str,
    xmlns: str = "http://www.w3.org/1998/Math/MathML",
    display: str = "inline",
) -> str:
    math = Element("math", xmlns=xmlns, display=display)
    row = SubElement(math, "mrow")
    _classify_subgroup(aggregate(latex), row)
    return _convert(math)


def _convert(tree: Element) -> str:
    return unescape(tostring(tree, encoding="unicode"))


def _convert_matrix_content(
    param: list,
    parent: Element,
    alignment: Union[str, None] = None,
    single_mtd: bool = True,
) -> None:
    if not len(param):
        return
    all_are_list = all(isinstance(i, list) for i in param)
    if all_are_list:
        for row in param:
            _convert_matrix_row(row, parent, alignment, single_mtd)
    else:
        _convert_matrix_row(param, parent, alignment, single_mtd)


def _convert_matrix_row(row: list, parent: Element, alignment: Optional[str], single_mtd: bool) -> None:
    mtr = SubElement(parent, "mtr")
    iterable: Iterator[int] = iter(range(len(row)))
    if single_mtd:
        mtd = SubElement(mtr, "mtd")
    for i in iterable:
        element = row[i]
        if alignment:
            column_align: str = {"r": "right", "l": "left", "c": "center"}.get(alignment, "")
            mtd = SubElement(mtr, "mtd", columnalign=column_align)
        elif not single_mtd:
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
        iterable: Iterator[int] = iter(range(len(row)))
        index = 0
        has_row_line = False
        for i in iterable:
            element = row[i]
            if element == r"\hline" and row_count > 1:
                row_lines.append("solid")
                has_row_line = True
                continue
            align: Union[str, None] = None
            try:
                align = _alignment[index]
            except IndexError:  # pragma: no cover
                pass
            if align:
                column_align: str = {"r": "right", "l": "left", "c": "center"}.get(align, "")
                mtd = SubElement(mtr, "mtd", columnalign=column_align)
            # else:
            #     mtd = SubElement(mtr, "mtd")
            if isinstance(element, list):
                _classify_subgroup(element, mtd)
            # elif element in COMMANDS:
            #     _convert_command(element, row, i, iterable, mtd)
            else:
                _classify(element, mtd)
            index += 1
        if not has_row_line and row_count > 1:
            row_lines.append("none")
    if "solid" in row_lines:
        parent.set("rowlines", " ".join(row_lines))


def _classify_subgroup(elements: list, row: Element, is_math_mode: bool = False) -> None:
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
    element: str,
    elements: List[Any],
    index: int,
    iterable: Iterator[int],
    parent: Element,
) -> None:
    _get_prefix_element(element, parent)
    if element == r"\substack":
        parent = SubElement(parent, "mstyle", scriptlevel="1")
    elif element == r"\cases":
        lbrace = SubElement(
            parent,
            "mo",
            OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "prefix")]),
        )
        lbrace.text = "&#x{};".format(convert_symbol(r"\{"))
    params, tag, attributes = COMMANDS[element]
    if len(elements) - 1 < params:
        mo = SubElement(parent, "mo")
        mo.text = element[1:]
        return
    new_parent = SubElement(parent, tag, attributes)
    alignment = ""
    if element in MATRICES:
        if element.endswith("*") or element == r"\array":
            index += 1
            alignment = elements[index]
            next(iterable)
        elif element == r"\cases":
            alignment = "l"
    if element in (r"\lim", r"\inf", r"\sup", r"\max", r"\min"):
        limit = SubElement(new_parent, "mo")
        limit.text = element[1:]
    for j in range(params):
        index += 1
        param = elements[index]
        if element == "_" and index == 1 and param == r"\sum":
            new_parent.tag = "munder"
            _classify(param, new_parent)
        elif element == r"\left" or element == r"\right":
            if param == ".":
                pass
            else:
                symbol = convert_symbol(param)
                new_parent.text = param if symbol is None else "&#x{};".format(symbol)
        elif element == r"\array":
            _convert_array_content(param, new_parent, alignment)
        elif element in MATRICES:
            _convert_matrix_content(param, new_parent, alignment, element == r"\substack")
        else:
            if isinstance(param, list):
                _parent = SubElement(new_parent, "mrow")
                _classify_subgroup(param, _parent)
            elif element == r"\text":
                new_parent.text = param
            else:
                _classify(param, new_parent)
    _get_postfix_element(element, parent)
    if element in (r"\overline", r"\bar"):
        mo = SubElement(new_parent, "mo", stretchy="true")
        mo.text = "&#x000AF;"
    elif element == r"\underline":
        mo = SubElement(new_parent, "mo", stretchy="true")
        mo.text = "&#x00332;"
    elif element in (r"\overrightarrow", r"\vec"):
        mo = SubElement(new_parent, "mo", stretchy="true")
        mo.text = "&#x02192;"
    elif element == r"\dot":
        mo = SubElement(new_parent, "mo")
        mo.text = "&#x002D9;"
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
    elif len(_element) and _element in "<>&":
        mo = SubElement(parent, "mo")
        mo.text = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}[_element]
    elif len(_element) and _element in "+-*/()=,":
        mo = SubElement(parent, "mo")
        mo.text = _element if symbol is None else "&#x{};".format(symbol)
        if _element in "()":
            mo.attrib["stretchy"] = "false"
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
    elif _element == r"\ ":
        tag = SubElement(parent, "mtext")
        tag.text = "&#x000A0;"
    elif _element.startswith("\\"):
        tag = SubElement(parent, "mo" if is_math_mode else "mi")
        if symbol:
            tag.text = "&#x{};".format(symbol)
        elif _element in (
            r"\log",
            r"\ln",
            r"\tan",
            r"\sec",
            r"\cos",
            r"\sin",
            r"\cot",
            r"\csc",
        ):
            tag.text = _element[1:]
        elif _element.startswith(r"\operatorname"):
            tag.text = _element[14:-1]
        else:
            tag.text = _element
    else:
        tag = SubElement(parent, "mo" if is_math_mode else "mi")
        tag.text = _element


def main() -> None:  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(description="Pure Python library for LaTeX to MathML conversion")
    parser.add_argument(
        "-V",
        "--version",
        dest="version",
        action="store_true",
        required=False,
        help="Show version",
    )
    required = parser.add_argument_group("required arguments")
    group = required.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-t",
        "--text",
        dest="text",
        type=str,
        required=False,
        help="Text",
    )
    group.add_argument(
        "-f",
        "--file",
        dest="file",
        type=str,
        required=False,
        help="File",
    )
    arguments = parser.parse_args()

    if arguments.version:
        version = pkg_resources.get_distribution("latex2mathml").version
        print("latex2mathml", version)
    elif arguments.text:
        print(convert(arguments.text))
    elif arguments.file:
        with open(arguments.file) as f:
            print(convert(f.read()))


if __name__ == "__main__":  # pragma: no cover
    main()
