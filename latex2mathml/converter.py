import re
from typing import Iterable, Iterator, Optional, Tuple, Union
from xml.etree.cElementTree import Element, SubElement, tostring  # nosec
from xml.sax.saxutils import unescape  # nosec

import pkg_resources

from latex2mathml.aggregator import BAR, BRACES, DOT, LEFT, OVERLINE, OVERRIGHTARROW, UNDERLINE, VEC, Node, aggregate
from latex2mathml.commands import COMMANDS, MATRICES
from latex2mathml.symbols_parser import convert_symbol


def convert(latex: str, xmlns: str = "http://www.w3.org/1998/Math/MathML", display: str = "inline") -> str:
    math = Element("math", xmlns=xmlns, display=display)
    row = SubElement(math, "mrow")
    _convert_group(iter(aggregate(latex)), row)
    return _convert(math)


def _convert(tree: Element) -> str:
    return unescape(tostring(tree, encoding="unicode"))


def _convert_matrix_content(
    param: list, parent: Element, alignment: Union[str, None] = None, single_mtd: bool = True
) -> None:
    if not len(param):
        return
    all_are_list = all(isinstance(i, list) for i in param)
    if all_are_list:
        for row in param:
            _convert_matrix_row(row, parent, alignment, single_mtd)
    else:
        _convert_matrix_row(param, parent, alignment, single_mtd)


def _get_column_lines(alignment):
    pass


def _convert_matrix(nodes: Iterator[Node], parent: Element, alignment: Optional[str] = None) -> None:
    row = None
    cell = None
    index = 0
    column_align = {"r": "right", "l": "left", "c": "center"}
    column_alignment = None
    for node in nodes:
        if row is None:
            row = SubElement(parent, "mtr")

        if cell is None:
            if alignment:
                try:
                    column_alignment = column_align.get(alignment[index])
                    index += 1
                except IndexError:
                    pass

            cell = _make_matrix_cell(row, column_alignment)

        if node.token == BRACES:
            _convert_group(iter([node]), cell)
            continue

        if node.token == "&":
            if alignment:
                try:
                    column_alignment = column_align.get(alignment[index])
                    index += 1
                except IndexError:
                    pass

            cell = _make_matrix_cell(row, column_alignment)
            continue
        elif node.token == r"\\":
            index = 0
            if alignment:
                try:
                    column_alignment = column_align.get(alignment[index])
                    index += 1
                except IndexError:
                    pass
            row = SubElement(parent, "mtr")
            cell = _make_matrix_cell(row, column_alignment)
            continue

        _convert_group(iter([node]), cell)


def _make_matrix_cell(row: Element, column_alignment: Optional[str]) -> Element:
    if column_alignment:
        return SubElement(row, "mtd", columnalign=column_alignment)
    return SubElement(row, "mtd")


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
            _convert_group(element, mtd)
        elif element in COMMANDS:
            _convert_command(element, row, i, iterable, mtd)
        else:
            _convert_symbol(element, mtd)


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
                _convert_group(element, mtd)
            # elif element in COMMANDS:
            #     _convert_command(element, row, i, iterable, mtd)
            else:
                _convert_symbol(element, mtd)
            index += 1
        if not has_row_line and row_count > 1:
            row_lines.append("none")
    if "solid" in row_lines:
        parent.set("rowlines", " ".join(row_lines))


def _convert_group(nodes: Iterable[Node], parent: Element, is_math_mode: bool = False) -> None:
    for node in nodes:
        token = node.token
        if token in COMMANDS:
            _convert_command(node, parent)
        elif token.startswith(r"\math"):
            is_math_mode = True
        elif node.children is None:
            _convert_symbol(node, parent, is_math_mode)
        elif node.children is not None:
            _row = SubElement(parent, "mrow")
            if token == "()":  # TODO: other pairs
                _convert_symbol(Node(token=token[0]), _row, is_math_mode)
            _convert_group(iter(node.children), _row, is_math_mode)
            if token == "()":  # TODO: other pairs
                _convert_symbol(Node(token=token[1]), _row, is_math_mode)
    # for i in iterable:
    #     element = nodes[i]
    #     if isinstance(element, list):
    #         _row = SubElement(row, "mrow")
    #         _classify_subgroup(element, _row, is_math_mode)
    #         is_math_mode = False
    #     elif element in COMMANDS:
    #         _convert_command(element, nodes, i, iterable, row)
    #     elif element.startswith(r"\math"):
    #         is_math_mode = True
    #     else:
    #         _classify(element, row, is_math_mode)


def _get_alignment_and_column_lines(alignment: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    if alignment is None:
        return None, None
    if "|" not in alignment:
        return alignment, None
    _alignment = ""
    column_lines = []
    for c in alignment:
        if c == "|":
            column_lines.append("solid")
        else:
            _alignment += c
        if len(_alignment) - len(column_lines) == 2:
            column_lines.append("none")
    return _alignment, " ".join(column_lines)


def _convert_command(node: Node, parent: Element) -> None:
    command = node.token
    _, tag, attributes = COMMANDS[command]

    if command == LEFT:
        parent = SubElement(parent, "mrow")

    _append_prefix_element(command, parent)

    alignment = None

    if command in (r"\lim", r"\inf", r"\sup", r"\max", r"\min"):
        element = SubElement(parent, "mo")
        element.text = command[1:]
    else:
        alignment, column_lines = _get_alignment_and_column_lines(node.alignment)
        if column_lines:
            attributes["columnlines"] = column_lines
        element = SubElement(parent, tag, attributes)

    if node.text is not None:
        element.text = node.text
    elif node.delimiter is not None:
        if node.delimiter != ".":
            symbol = convert_symbol(node.delimiter)
            element.text = node.delimiter if symbol is None else "&#x{};".format(symbol)

    if node.children is not None:
        _parent = element
        if command == LEFT:
            _parent = parent
        if command in MATRICES:
            _convert_matrix(iter(node.children), _parent, alignment=alignment)
        else:
            _convert_group(iter(node.children), _parent)

    _append_postfix_element(command, parent)

    # if element == r"\substack":
    #     parent = SubElement(parent, "mstyle", scriptlevel="1")
    # elif element == r"\cases":
    #     lbrace = SubElement(
    #         parent,
    #         "mo",
    #         OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "prefix")]),
    #     )
    #     lbrace.text = "&#x{};".format(convert_symbol(r"\{"))
    # params, tag, attributes = COMMANDS[element]
    # if len(elements) - 1 < params:
    #     mo = SubElement(parent, "mo")
    #     mo.text = element[1:]
    #     return
    # new_parent = SubElement(parent, tag, attributes)
    # alignment = ""
    # if element in MATRICES:
    #     if element.endswith("*") or element == r"\array":
    #         index += 1
    #         alignment = elements[index]
    #         next(iterable)
    #     elif element == r"\cases":
    #         alignment = "l"
    # for j in range(params):
    #     index += 1
    #     param = elements[index]
    #     if element == "_" and index == 1 and param == r"\sum":
    #         new_parent.tag = "munder"
    #         _classify(param, new_parent)
    #     elif element == r"\left" or element == r"\right":
    #         if param == ".":
    #             pass
    #         else:
    #             symbol = convert_symbol(param)
    #             new_parent.text = param if symbol is None else "&#x{};".format(symbol)
    #     elif element == r"\array":
    #         _convert_array_content(param, new_parent, alignment)
    #     elif element in MATRICES:
    #         _convert_matrix_content(param, new_parent, alignment, element == r"\substack")
    #     else:
    #         if isinstance(param, list):
    #             _parent = SubElement(new_parent, "mrow")
    #             _classify_subgroup(param, _parent)
    #         elif element == r"\text":
    #             new_parent.text = param
    #         else:
    #             _classify(param, new_parent)
    # _get_postfix_element(element, parent)
    if command in (OVERLINE, BAR):
        mo = SubElement(element, "mo", stretchy="true")
        mo.text = "&#x000AF;"
    elif command == UNDERLINE:
        mo = SubElement(element, "mo", stretchy="true")
        mo.text = "&#x00332;"
    elif command in (OVERRIGHTARROW, VEC):
        mo = SubElement(element, "mo", stretchy="true")
        mo.text = "&#x02192;"
    elif command == DOT:
        mo = SubElement(element, "mo")
        mo.text = "&#x002D9;"
    # [next(iterable) for _ in range(params)]


def _convert_and_append_command(command: str, parent: Element) -> None:
    code_point = convert_symbol(command)
    mo = SubElement(parent, "mo")
    mo.text = "&#x{};".format(code_point)


def _append_prefix_element(command: str, parent: Element) -> None:
    if command in (r"\binom", r"\pmatrix"):
        _convert_and_append_command(r"\lparen", parent)
    elif command == r"\bmatrix":
        _convert_and_append_command(r"\lbrack", parent)
    elif command == r"\Bmatrix":
        _convert_and_append_command(r"\lbrace", parent)
    elif command == r"\vmatrix":
        _convert_and_append_command(r"\vert", parent)
    elif command == r"\Vmatrix":
        _convert_and_append_command(r"\Vert", parent)


def _append_postfix_element(command: str, parent: Element) -> None:
    if command in (r"\binom", r"\pmatrix"):
        _convert_and_append_command(r"\rparen", parent)
    elif command == r"\bmatrix":
        _convert_and_append_command(r"\rbrack", parent)
    elif command == r"\Bmatrix":
        _convert_and_append_command(r"\rbrace", parent)
    elif command == r"\vmatrix":
        _convert_and_append_command(r"\vert", parent)
    elif command == r"\Vmatrix":
        _convert_and_append_command(r"\Vert", parent)


def _convert_symbol(node: Node, parent: Element, is_math_mode: bool = False) -> None:
    token = node.token
    symbol = convert_symbol(token)
    if re.match(r"\d+(.\d+)?", token):
        mn = SubElement(parent, "mn")
        mn.text = token
    elif len(token) and token in "<>&":
        mo = SubElement(parent, "mo")
        mo.text = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}[token]
    elif len(token) and token in "+-*/()=,":
        mo = SubElement(parent, "mo")
        mo.text = token if symbol is None else "&#x{};".format(symbol)
        if token in "()":
            mo.attrib["stretchy"] = "false"
    # elif (
    #     symbol
    #     and (
    #         int(symbol, 16) in range(int("2200", 16), int("22FF", 16) + 1)
    #         or int(symbol, 16) in range(int("2190", 16), int("21FF", 16) + 1)
    #     )
    #     or symbol == "."
    # ):
    #     mo = SubElement(parent, "mo")
    #     mo.text = "&#x{};".format(symbol)
    elif token == r"\ ":
        tag = SubElement(parent, "mtext")
        tag.text = "&#x000A0;"
    elif token.startswith("\\"):
        tag = SubElement(parent, "mo" if is_math_mode else "mi")
        if symbol:
            tag.text = "&#x{};".format(symbol)
        elif token in (
            r"\log",
            r"\ln",
            r"\tan",
            r"\sec",
            r"\cos",
            r"\sin",
            r"\cot",
            r"\csc",
        ):
            tag.text = token[1:]
        elif token.startswith(r"\operatorname"):
            tag.text = token[14:-1]
        else:
            tag.text = token
    else:
        tag = SubElement(parent, "mo" if is_math_mode else "mi")
        tag.text = token


def main() -> None:  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(description="Pure Python library for LaTeX to MathML conversion")
    parser.add_argument("-V", "--version", dest="version", action="store_true", required=False, help="Show version")

    required = parser.add_argument_group("required arguments")

    group = required.add_mutually_exclusive_group(required=False)
    group.add_argument("-t", "--text", dest="text", type=str, required=False, help="Text")
    group.add_argument("-f", "--file", dest="file", type=str, required=False, help="File")

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
