import copy
import re
from collections import OrderedDict
from typing import Iterable, Iterator, Optional, Tuple
from xml.etree.cElementTree import Element, SubElement, tostring
from xml.sax.saxutils import unescape

from latex2mathml import commands
from latex2mathml.symbols_parser import convert_symbol
from latex2mathml.walker import Node, walk

COLUMN_ALIGNMENT_MAP = {"r": "right", "l": "left", "c": "center"}


def convert(latex: str, xmlns: str = "http://www.w3.org/1998/Math/MathML", display: str = "inline") -> str:
    math = Element("math", xmlns=xmlns, display=display)
    row = SubElement(math, "mrow")
    _convert_group(iter(walk(latex)), row)
    return _convert(math)


def _convert(tree: Element) -> str:
    return unescape(tostring(tree, encoding="unicode"))


def _convert_matrix(nodes: Iterator[Node], parent: Element, alignment: Optional[str] = None) -> None:
    row = None
    cell = None

    col_index = 0
    col_alignment = None

    row_index = 0
    row_lines = []

    for node in nodes:
        if row is None:
            row = SubElement(parent, "mtr")

        if cell is None:
            col_alignment, col_index = _get_column_alignment(alignment, col_alignment, col_index)
            cell = _make_matrix_cell(row, col_alignment)

        if node.token == commands.BRACES:
            _convert_group(iter([node]), cell)
            continue

        if node.token == "&":
            col_alignment, col_index = _get_column_alignment(alignment, col_alignment, col_index)
            cell = _make_matrix_cell(row, col_alignment)
            continue
        elif node.token == commands.DOUBLEBACKSLASH:
            row_index += 1
            col_index = 0
            col_alignment, col_index = _get_column_alignment(alignment, col_alignment, col_index)
            row = SubElement(parent, "mtr")
            cell = _make_matrix_cell(row, col_alignment)
            continue
        elif node.token == commands.HLINE:
            row_lines.append("solid")
            continue

        if row_index > len(row_lines):
            row_lines.append("none")

        _convert_group(iter([node]), cell)

    if any(r == "solid" for r in row_lines):
        parent.set("rowlines", " ".join(row_lines))


def _get_column_alignment(
    alignment: Optional[str], column_alignment: Optional[str], column_index: int
) -> Tuple[Optional[str], int]:
    if alignment:
        try:
            column_alignment = COLUMN_ALIGNMENT_MAP.get(alignment[column_index])
            column_index += 1
        except IndexError:
            pass
    return column_alignment, column_index


def _make_matrix_cell(row: Element, column_alignment: Optional[str]) -> Element:
    if column_alignment:
        return SubElement(row, "mtd", columnalign=column_alignment)
    return SubElement(row, "mtd")


def _convert_group(
    nodes: Iterable[Node], parent: Element, is_math_mode: bool = False, font: Optional[str] = None
) -> None:
    _font = font
    for node in nodes:
        token = node.token
        if token in commands.CONVERSION_MAP:
            _convert_command(node, parent, is_math_mode, _font)
        elif token.startswith(r"\math"):
            is_math_mode = True
        elif token in commands.OLD_STYLE_FONTS.keys():
            _font = commands.OLD_STYLE_FONTS.get(token)
        elif node.children is None:
            _convert_symbol(node, parent, is_math_mode, _font)
        elif node.children is not None:
            _row = SubElement(parent, "mrow")
            if token == "()":  # TODO: other pairs
                _convert_symbol(Node(token=token[0]), _row, is_math_mode, _font)
            _convert_group(iter(node.children), _row, is_math_mode)
            if token == "()":  # TODO: other pairs
                _convert_symbol(Node(token=token[1]), _row, is_math_mode, _font)


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


def _convert_command(node: Node, parent: Element, is_math_mode: bool = False, font: Optional[str] = None) -> None:
    command = node.token

    if command == commands.SUBSTACK:
        parent = SubElement(parent, "mstyle", scriptlevel="1")
    elif command == commands.CASES:
        lbrace = SubElement(parent, "mo", OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "prefix")]))
        lbrace.text = "&#x{};".format(convert_symbol(commands.LBRACE))

    tag, attributes = copy.deepcopy(commands.CONVERSION_MAP[command])

    if command == commands.LEFT:
        parent = SubElement(parent, "mrow")

    _append_prefix_element(command, parent)

    alignment, column_lines = _get_alignment_and_column_lines(node.alignment)

    if column_lines:
        attributes["columnlines"] = column_lines
    if (
        command == commands.SUBSCRIPT
        and node.children is not None
        and len(node.children[0])
        and node.children[0].token in (*commands.LIMIT, commands.SUMMATION)
    ):
        tag = "munder"

    element = SubElement(parent, tag, attributes)

    if command in commands.LIMIT:
        element.text = command[1:]
    elif node.text is not None:
        element.text = node.text
    elif node.delimiter is not None:
        if node.delimiter != ".":
            symbol = convert_symbol(node.delimiter)
            element.text = node.delimiter if symbol is None else "&#x{};".format(symbol)

    if node.children is not None:
        _parent = element
        if command == commands.LEFT:
            _parent = parent
        if command in commands.MATRICES:
            if command == commands.CASES:
                alignment = "l"
            _convert_matrix(iter(node.children), _parent, alignment=alignment)
        elif command == commands.MATHOP:
            _convert_group(iter(node.children), _parent, is_math_mode, font)
        elif command == commands.HSPACE:
            element.attrib["width"] = node.children[0].token
        else:
            _convert_group(iter(node.children), _parent, is_math_mode, font)

    _append_postfix_element(command, parent)

    if command in (commands.OVERLINE, commands.BAR):
        mo = SubElement(element, "mo", stretchy="true")
        mo.text = "&#x000AF;"
    elif command == commands.UNDERLINE:
        mo = SubElement(element, "mo", stretchy="true")
        mo.text = "&#x00332;"
    elif command in (commands.OVERRIGHTARROW, commands.VEC):
        mo = SubElement(element, "mo", stretchy="true")
        mo.text = "&#x02192;"
    elif command == commands.DOT:
        mo = SubElement(element, "mo")
        mo.text = "&#x002D9;"


def _convert_and_append_command(command: str, parent: Element) -> None:
    code_point = convert_symbol(command)
    mo = SubElement(parent, "mo")
    mo.text = "&#x{};".format(code_point)


def _append_prefix_element(command: str, parent: Element) -> None:
    if command in (commands.BINOM, r"\pmatrix"):
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
    if command in (commands.BINOM, r"\pmatrix"):
        _convert_and_append_command(r"\rparen", parent)
    elif command == r"\bmatrix":
        _convert_and_append_command(r"\rbrack", parent)
    elif command == r"\Bmatrix":
        _convert_and_append_command(r"\rbrace", parent)
    elif command == r"\vmatrix":
        _convert_and_append_command(r"\vert", parent)
    elif command == r"\Vmatrix":
        _convert_and_append_command(r"\Vert", parent)


def _convert_symbol(node: Node, parent: Element, is_math_mode: bool = False, font: Optional[str] = None) -> None:
    token = node.token
    symbol = convert_symbol(token)
    if re.match(r"\d+(.\d+)?", token):
        mn = SubElement(parent, "mn")
        mn.text = token
    elif len(token) and token in "<>&":
        mo = SubElement(parent, "mo")
        mo.text = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}[token]
    elif len(token) and token in ("+", "-", "*", "/", "(", ")", "=", ",", "?", "[", "]", "|", r"\|"):
        mo = SubElement(parent, "mo")
        mo.text = token if symbol is None else "&#x{};".format(symbol)
        if token == r"\|":
            mo.attrib["fence"] = "false"
        if token in ("(", ")", "[", "]", "|", r"\|"):
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
    elif token == r"\ ":
        mtext = SubElement(parent, "mtext")
        mtext.text = "&#x000A0;"
    elif token.startswith(commands.BACKSLASH):
        element = SubElement(parent, "mo" if is_math_mode else "mi")
        if element.tag == "mi" and font is not None:
            element.attrib["mathvariant"] = font
        if symbol:
            element.text = "&#x{};".format(symbol)
        elif token in commands.FUNCTIONS:
            element.text = token[1:]
        elif token.startswith(commands.OPERATORNAME):
            element.text = token[14:-1]
        else:
            element.text = token
    else:
        element = SubElement(parent, "mo" if is_math_mode else "mi")
        if element.tag == "mi" and font is not None:
            element.attrib["mathvariant"] = font
        element.text = token


def main() -> None:  # pragma: no cover
    import argparse

    import pkg_resources

    parser = argparse.ArgumentParser(description="Pure Python library for LaTeX to MathML conversion")
    parser.add_argument("-V", "--version", dest="version", action="store_true", required=False, help="Show version")
    parser.add_argument("-b", "--block", dest="block", action="store_true", required=False, help="Display block")

    required = parser.add_argument_group("required arguments")

    group = required.add_mutually_exclusive_group(required=False)
    group.add_argument("-t", "--text", dest="text", type=str, required=False, help="Text")
    group.add_argument("-f", "--file", dest="file", type=str, required=False, help="File")

    arguments = parser.parse_args()
    display = "block" if arguments.block else "inline"

    if arguments.version:
        version = pkg_resources.get_distribution("latex2mathml").version
        print("latex2mathml", version)
    elif arguments.text:
        print(convert(arguments.text, display=display))
    elif arguments.file:
        with open(arguments.file) as f:
            print(convert(f.read(), display=display))


if __name__ == "__main__":  # pragma: no cover
    main()
