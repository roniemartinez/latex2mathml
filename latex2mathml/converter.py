import copy
import enum
import re
from collections import OrderedDict
from typing import Iterable, Iterator, Optional
from xml.etree.cElementTree import Element, SubElement, tostring
from xml.sax.saxutils import unescape

from latex2mathml import commands
from latex2mathml.symbols_parser import convert_symbol
from latex2mathml.walker import MULTIPRIMES, Node, walk

COLUMN_ALIGNMENT_MAP = {"r": "right", "l": "left", "c": "center"}
OPERATORS = frozenset(
    (
        "+",
        "-",
        "*",
        "/",
        "(",
        ")",
        "=",
        ",",
        "?",
        "[",
        "]",
        "|",
        r"\|",
        "!",
        r"\{",
        r"\}",
        r">",
        r"<",
        r".",
        r"\ast",
        r"\bigotimes",
        r"\cdot",
        r"\centerdot",
        r"\div",
        r"\dots",
        r"\dotsc",
        r"\dotso",
        r"\gt",
        r"\ldotp",
        r"\lt",
        r"\lvert",
        r"\lVert",
        r"\lvertneqq",
        r"\ngeqq",
        r"\omicron",
        r"\rvert",
        r"\rVert",
        r"\S",
        r"\smallfrown",
        r"\smallint",
        r"\smallsmile",
        r"\surd",
        r"\times",
        r"\varsubsetneqq",
        r"\varsupsetneqq",
    )
)
MATH_MODE_PATTERN = re.compile(r"\\\$|\$|\\?[^\\$]+")
NUMBER_PATTERN = re.compile(r"\d+(\.\d+)?")
MOVABLE_LIMIT_TEXTS = {
    commands.ARGMAX: "arg&#x02009;max",
    commands.ARGMIN: "arg&#x02009;min",
    commands.INJLIM: "inj&#x02006;lim",
    commands.INTOP: "&#x0222B;",
    commands.LIMINF: "lim&#x02006;inf",
    commands.LIMSUP: "lim&#x02006;sup",
    commands.PROJLIM: "proj&#x02006;lim",
    commands.VARINJLIM: "inj&#x02006;lim",
    commands.VARLIMINF: "lim&#x02006;inf",
    commands.VARLIMSUP: "lim&#x02006;sup",
    commands.VARPROJLIM: "proj&#x02006;lim",
}


class Mode(enum.Enum):
    TEXT = enum.auto()
    MATH = enum.auto()


class Converter:
    def __init__(self, xmlns: str = "http://www.w3.org/1998/Math/MathML", display: str = "inline") -> None:
        self.xmlns = xmlns
        self.display = display
        self.equation_counter = 0
        self.macros: dict[str, tuple[list[str], int]] = {}

    def convert(self, latex: str, parent: Optional[Element] = None) -> str:
        return self._convert(self.convert_to_element(latex, parent))

    def convert_to_element(self, latex: str, parent: Optional[Element] = None) -> Element:
        tag = "math"
        attrib = {"xmlns": self.xmlns, "display": self.display}
        math = Element(tag, attrib) if parent is None else SubElement(parent, tag, attrib)
        row = SubElement(math, "mrow")
        self._convert_group(iter(walk(latex, self.display, macros=self.macros)), row)
        return math

    def reset(self) -> None:
        self.equation_counter = 0
        self.macros = {}

    @staticmethod
    def _convert(tree: Element) -> str:
        return unescape(tostring(tree, encoding="unicode"))

    def _convert_matrix(
        self, nodes: Iterator[Node], parent: Element, command: str, alignment: Optional[str] = None
    ) -> None:
        row = None
        cell = None

        col_index = 0
        col_alignment = None

        max_col_size = 0

        row_index = 0
        row_lines: list[str] = []

        hfil_indexes: list[bool] = []

        for node in nodes:
            if row is None:
                row = SubElement(parent, "mtr")

            if cell is None:
                col_alignment, col_index = _get_column_alignment(alignment, col_alignment, col_index)
                cell = _make_matrix_cell(row, col_alignment)

            if node.token == commands.BRACES:
                self._convert_group(iter([node]), cell)
            elif node.token == "&":
                _set_cell_alignment(cell, hfil_indexes)
                hfil_indexes = []
                col_alignment, col_index = _get_column_alignment(alignment, col_alignment, col_index)
                cell = _make_matrix_cell(row, col_alignment)
                if command in (commands.SPLIT, commands.ALIGN) and col_index % 2 == 0:
                    SubElement(cell, "mi")
            elif node.token in (commands.DOUBLEBACKSLASH, commands.CARRIAGERETURN):
                _set_cell_alignment(cell, hfil_indexes)
                hfil_indexes = []
                row_index += 1
                if col_index > max_col_size:
                    max_col_size = col_index
                col_index = 0
                col_alignment, col_index = _get_column_alignment(alignment, col_alignment, col_index)
                row = SubElement(parent, "mtr")
                cell = _make_matrix_cell(row, col_alignment)
            elif node.token == commands.HLINE:
                row_lines.append("solid")
            elif node.token == commands.HDASHLINE:
                row_lines.append("dashed")
            elif node.token == commands.HFIL:
                hfil_indexes.append(True)
            else:
                if row_index > len(row_lines):
                    row_lines.append("none")
                hfil_indexes.append(False)
                self._convert_group(iter([node]), cell)

        if col_index > max_col_size:
            max_col_size = col_index

        if any(r == "solid" for r in row_lines):
            parent.set("rowlines", " ".join(row_lines))

        if row is not None and cell is not None and len(cell) == 0:
            parent.remove(row)

        if max_col_size and command == commands.ALIGN:
            spacing = ("0em", "2em")
            multiplier = max_col_size // len(spacing)
            parent.set("columnspacing", " ".join(spacing * multiplier))

    def _convert_group(
        self, nodes: Iterable[Node], parent: Element, font: Optional[dict[str, Optional[str]]] = None
    ) -> None:
        _font = font
        for node in nodes:
            token = node.token
            if token in (*commands.MSTYLE_SIZES, *commands.STYLES):
                node = Node(token=token, children=tuple(n for n in nodes))
                self._convert_command(node, parent, _font)
            elif token == commands.UNICODE:
                arg = node.children[0] if node.children else None
                if arg and arg.children:
                    code = "".join(c.token for c in arg.children)
                elif arg:
                    code = arg.token
                else:
                    code = ""
                element = SubElement(parent, "mi")
                element.text = f"&#x{code.lstrip('x')};"
            elif token == commands.RULE:
                attrs = node.attributes or {}
                SubElement(parent, "mspace", mathbackground="black", width=attrs["width"], height=attrs["height"])
            elif token in commands.CONVERSION_MAP or token in (commands.MOD, commands.PMOD, commands.POD):
                self._convert_command(node, parent, _font)
            elif token in commands.LOCAL_FONTS and node.children is not None:
                self._convert_group(iter(node.children), parent, commands.LOCAL_FONTS[token])
            elif token.startswith(commands.MATH) and node.children is not None:
                self._convert_group(iter(node.children), parent, _font)
            elif token in commands.GLOBAL_FONTS.keys():
                _font = commands.GLOBAL_FONTS.get(token)
            elif node.children is None:
                self._convert_symbol(node, parent, _font)
            else:
                attributes = node.attributes or {}
                _row = SubElement(parent, "mrow", attrib=attributes)
                self._convert_group(iter(node.children), _row, _font)

    def _convert_command(self, node: Node, parent: Element, font: Optional[dict[str, Optional[str]]] = None) -> None:
        command = node.token
        modifier = node.modifier

        if command in (commands.SUBSTACK, commands.SMALLMATRIX):
            parent = SubElement(parent, "mstyle", scriptlevel="1")
        elif command == commands.CASES:
            parent = SubElement(parent, "mrow")
            lbrace = SubElement(
                parent, "mo", OrderedDict([("stretchy", "true"), ("fence", "true"), ("form", "prefix")])
            )
            lbrace.text = "&#x{};".format(convert_symbol(commands.LBRACE))
        elif command in (commands.DBINOM, commands.DFRAC):
            parent = SubElement(parent, "mstyle", displaystyle="true", scriptlevel="0")
        elif command == commands.HPHANTOM:
            parent = SubElement(parent, "mpadded", height="0", depth="0")
        elif command == commands.VPHANTOM:
            parent = SubElement(parent, "mpadded", width="0")
        elif command in (commands.TBINOM, commands.HBOX, commands.MBOX, commands.TFRAC):
            parent = SubElement(parent, "mstyle", displaystyle="false", scriptlevel="0")
        elif command in (commands.MOD, commands.PMOD, commands.POD):
            SubElement(parent, "mspace", width="1em")

        tag, attributes = copy.deepcopy(commands.CONVERSION_MAP[command])

        if node.attributes is not None and node.token != commands.SKEW:
            attributes.update(node.attributes)

        if command == commands.LEFT:
            parent = SubElement(parent, "mrow")

        self._append_delimiter_element(node, parent, is_prefix=True)

        alignment, column_lines = _get_alignment_and_column_lines(node.alignment)

        if column_lines:
            attributes["columnlines"] = column_lines

        if command == commands.SUBSUP and node.children is not None and node.children[0].token == commands.GCD:
            tag = "munderover"
        elif command == commands.SUPERSCRIPT and modifier in (commands.LIMITS, commands.OVERBRACE):
            tag = "mover"
        elif command == commands.SUBSCRIPT and modifier in (commands.LIMITS, commands.UNDERBRACE):
            tag = "munder"
        elif command == commands.SUBSUP and modifier in (commands.LIMITS, commands.OVERBRACE, commands.UNDERBRACE):
            tag = "munderover"
        elif command in commands.EXTENSIBLE_ARROWS and node.children is not None and len(node.children) == 2:
            tag = "munderover"

        element = SubElement(parent, tag, attributes)

        if command in commands.LIMIT:
            element.text = command[1:]
        elif command in (commands.MOD, commands.PMOD):
            element.text = "mod"
            SubElement(parent, "mspace", width="0.333em")
        elif command == commands.POD:
            pass
        elif command == commands.BMOD:
            element.text = "mod"
        elif command in commands.EXTENSIBLE_ARROWS:
            style = SubElement(element, "mstyle", scriptlevel="0")
            arrow = SubElement(style, "mo")
            arrow.text = commands.EXTENSIBLE_ARROWS[command]
        elif command == commands.BRA:
            SubElement(element, "mo", stretchy="false").text = "&#x27E8;"
        elif command == commands.KET:
            SubElement(element, "mo").text = "&#x2223;"
        elif command == commands.BRAKET:
            SubElement(element, "mo", stretchy="false").text = "&#x27E8;"
        elif node.text is not None:
            if command == commands.MIDDLE:
                element.text = "&#x{};".format(convert_symbol(node.text))
            elif command == commands.HBOX:
                mtext: Optional[Element] = element
                for text, mode in _separate_by_mode(node.text):
                    if mode == Mode.TEXT:
                        if mtext is None:
                            mtext = SubElement(parent, tag, attributes)
                        mtext.text = text.replace(" ", "&#x000A0;")
                        self._set_font(mtext, "mtext", font)
                        mtext = None
                    else:
                        _row = SubElement(parent, "mrow")
                        self._convert_group(iter(walk(text)), _row)
            else:
                if command in (
                    commands.FBOX,
                    commands.LLAP,
                    commands.RLAP,
                    commands.CLAP,
                    commands.COLORBOX,
                    commands.FCOLORBOX,
                ):
                    element = SubElement(element, "mtext")
                if command == commands.TAG:
                    element.text = f"({node.text})"
                elif command == commands.TAGSTAR:
                    element.text = node.text
                else:
                    element.text = node.text.replace(" ", "&#x000A0;")
                self._set_font(element, "mtext", font)
        elif node.delimiter is not None and command not in (commands.FRAC, commands.GENFRAC):
            if node.delimiter != ".":
                symbol = convert_symbol(node.delimiter)
                element.text = node.delimiter if symbol is None else "&#x{};".format(symbol)

        if node.children is not None:
            _parent = element
            if command in (commands.LEFT, commands.MOD, commands.PMOD, commands.POD):
                _parent = parent
            if command in commands.MATRICES:
                if command == commands.CASES:
                    alignment = "l"
                elif command in (commands.SPLIT, commands.ALIGN):
                    alignment = "rl"
                self._convert_matrix(iter(node.children), _parent, command, alignment=alignment)
            elif command == commands.CFRAC:
                for child in node.children:
                    p = SubElement(_parent, "mstyle", displaystyle="false", scriptlevel="0")
                    self._convert_group(iter([child]), p, font)
            elif command == commands.SIDESET:
                left, right = node.children
                self._convert_group(iter([left]), _parent, font)
                fill = SubElement(_parent, "mstyle", scriptlevel="0")
                SubElement(fill, "mspace", width="-0.167em")
                self._convert_group(iter([right]), _parent, font)
            elif command == commands.SKEW:
                child = node.children[0]
                new_node = Node(
                    token=child.token,
                    children=(
                        Node(
                            token=commands.BRACES,
                            children=(*child.children, Node(token=commands.MKERN, attributes=node.attributes)),
                        ),
                    ),
                )
                self._convert_group(iter([new_node]), _parent, font)
            elif command in commands.EXTENSIBLE_ARROWS:
                for child in node.children:
                    padded = SubElement(
                        _parent,
                        "mpadded",
                        OrderedDict(
                            [("width", "+0.833em"), ("lspace", "0.556em"), ("voffset", "-.2em"), ("height", "-.2em")]
                        ),
                    )
                    self._convert_group(iter([child]), padded, font)
                    SubElement(padded, "mspace", depth=".25em")
            else:
                self._convert_group(iter(node.children), _parent, font)

        _add_diacritic(command, element)

        if command == commands.BRA:
            SubElement(element, "mo").text = "&#x2223;"
        elif command == commands.KET:
            SubElement(element, "mo", stretchy="false").text = "&#x27E9;"
        elif command == commands.BRAKET:
            SubElement(element, "mo", stretchy="false").text = "&#x27E9;"

        self._append_delimiter_element(node, parent, is_prefix=False)

    @staticmethod
    def _append_delimiter_element(node: Node, parent: Element, is_prefix: bool) -> None:
        delimiter_index = 0 if is_prefix else 1
        size = "2.047em"
        if parent.attrib.get("displaystyle") == "false" or node.token == commands.TBINOM:
            size = "1.2em"
        if node.token in (r"\pmatrix", commands.PMOD, commands.POD):
            _convert_and_append_command(r"\lparen" if is_prefix else r"\rparen", parent)
        elif node.token in (commands.BINOM, commands.DBINOM, commands.TBINOM):
            _convert_and_append_command(
                r"\lparen" if is_prefix else r"\rparen", parent, {"minsize": size, "maxsize": size}
            )
        elif node.token == r"\bmatrix":
            _convert_and_append_command(r"\lbrack" if is_prefix else r"\rbrack", parent)
        elif node.token == r"\Bmatrix":
            _convert_and_append_command(r"\lbrace" if is_prefix else r"\rbrace", parent)
        elif node.token == r"\vmatrix":
            _convert_and_append_command(r"\vert", parent)
        elif node.token == r"\Vmatrix":
            _convert_and_append_command(r"\Vert", parent)
        elif (
            node.token in (commands.FRAC, commands.GENFRAC)
            and node.delimiter is not None
            and node.delimiter[delimiter_index] != "."
        ):
            _convert_and_append_command(node.delimiter[delimiter_index], parent, {"minsize": size, "maxsize": size})
        elif not is_prefix and node.token == commands.SKEW and node.attributes is not None:
            SubElement(parent, "mspace", width="-" + node.attributes["width"])

    def _convert_symbol(self, node: Node, parent: Element, font: Optional[dict[str, Optional[str]]] = None) -> None:
        token = node.token
        attributes = node.attributes or {}
        symbol = convert_symbol(token)
        if token == MULTIPRIMES:
            count = int(node.text or "0")
            element = SubElement(parent, "mi", attrib=attributes)
            element.text = "&#x02032;" * count
            return
        if NUMBER_PATTERN.match(token):
            element = SubElement(parent, "mn", attrib=attributes)
            element.text = token
            self._set_font(element, element.tag, font)
        elif token in OPERATORS:
            element = SubElement(parent, "mo", attrib=attributes)
            element.text = token if symbol is None else "&#x{};".format(symbol)
            if token == r"\|":
                element.attrib["fence"] = "false"
            if token == r"\smallint":
                element.attrib["largeop"] = "false"
            if token in ("(", ")", "[", "]", "|", r"\|", r"\{", r"\}", r"\surd"):
                element.attrib["stretchy"] = "false"
                self._set_font(element, "fence", font)
            else:
                self._set_font(element, element.tag, font)
        elif (
            symbol
            and (
                int(symbol, 16) in range(int("2200", 16), int("22FF", 16) + 1)
                or int(symbol, 16) in range(int("2190", 16), int("21FF", 16) + 1)
            )
            or symbol == "."
        ):
            element = SubElement(parent, "mo", attrib=attributes)
            element.text = "&#x{};".format(symbol)
            self._set_font(element, element.tag, font)
        elif token in (r"\ ", "~", commands.NOBREAKSPACE, commands.SPACE):
            element = SubElement(parent, "mtext", attrib=attributes)
            element.text = "&#x000A0;"
            self._set_font(element, "mtext", font)
        elif token == commands.NOT:
            mpadded = SubElement(parent, "mpadded", width="0")
            element = SubElement(mpadded, "mtext")
            element.text = "&#x029F8;"
        elif token in (
            commands.ARGMAX,
            commands.ARGMIN,
            commands.DETERMINANT,
            commands.GCD,
            commands.INTOP,
            commands.INJLIM,
            commands.LIMINF,
            commands.LIMSUP,
            commands.PLIM,
            commands.PR,
            commands.PROJLIM,
            commands.VARINJLIM,
            commands.VARLIMINF,
            commands.VARLIMSUP,
            commands.VARPROJLIM,
        ):
            element = SubElement(parent, "mo", attrib={"movablelimits": "true", **attributes})
            element.text = MOVABLE_LIMIT_TEXTS.get(token, token[1:])
            self._set_font(element, element.tag, font)
        elif token in (commands.MATHSTRUT, commands.STRUT):
            mpadded = SubElement(parent, "mpadded", width="0px")
            mphantom = SubElement(mpadded, "mphantom")
            SubElement(mphantom, "mo", stretchy="false").text = "&#x00028;"
        elif token == commands.IDOTSINT:
            _parent = SubElement(parent, "mrow", attrib=attributes)
            for s in ("&#x0222B;", "&#x022EF;", "&#x0222B;"):
                element = SubElement(_parent, "mo")
                element.text = s
        elif token in (commands.LATEX, commands.TEX):
            _parent = SubElement(parent, "mrow", attrib=attributes)
            if token == commands.LATEX:
                mi_l = SubElement(_parent, "mi")
                mi_l.text = "L"
                SubElement(_parent, "mspace", width="-.325em")
                mpadded = SubElement(_parent, "mpadded", height="+.21ex", depth="-.21ex", voffset="+.21ex")
                mstyle = SubElement(mpadded, "mstyle", displaystyle="false", scriptlevel="1")
                mrow = SubElement(mstyle, "mrow")
                mi_a = SubElement(mrow, "mi")
                mi_a.text = "A"
                SubElement(_parent, "mspace", width="-.17em")
                self._set_font(mi_l, mi_l.tag, font)
                self._set_font(mi_a, mi_a.tag, font)
            mi_t = SubElement(_parent, "mi")
            mi_t.text = "T"
            SubElement(_parent, "mspace", width="-.14em")
            mpadded = SubElement(_parent, "mpadded", height="-.5ex", depth="+.5ex", voffset="-.5ex")
            mrow = SubElement(mpadded, "mrow")
            mi_e = SubElement(mrow, "mi")
            mi_e.text = "E"
            SubElement(_parent, "mspace", width="-.115em")
            mi_x = SubElement(_parent, "mi")
            mi_x.text = "X"
            self._set_font(mi_t, mi_t.tag, font)
            self._set_font(mi_e, mi_e.tag, font)
            self._set_font(mi_x, mi_x.tag, font)
        elif token.startswith(commands.OPERATORNAMEWITHLIMITS):
            element = SubElement(parent, "mo", attrib={"movablelimits": "true", **attributes})
            element.text = token[len(commands.OPERATORNAMEWITHLIMITS) + 1 : -1]
        elif token.startswith(commands.OPERATORNAMESTAR):
            element = SubElement(parent, "mo", attrib={"movablelimits": "true", **attributes})
            element.text = token[len(commands.OPERATORNAMESTAR) + 1 : -1]
        elif token.startswith(commands.OPERATORNAME):
            element = SubElement(parent, "mo", attrib=attributes)
            element.text = token[14:-1]
        elif token.startswith(commands.BACKSLASH):
            element = SubElement(parent, "mi", attrib=attributes)
            if symbol:
                element.text = "&#x{};".format(symbol)
            elif token in commands.FUNCTIONS:
                element.text = token[1:]
            else:
                element.text = token
            self._set_font(element, element.tag, font)
        else:
            element = SubElement(parent, "mi", attrib=attributes)
            element.text = token
            self._set_font(element, element.tag, font)

    @staticmethod
    def _set_font(element: Element, key: str, font: Optional[dict[str, Optional[str]]]) -> None:
        if font is None:
            return
        _font = font[key]
        if _font is not None:
            element.attrib["mathvariant"] = _font


def _set_cell_alignment(cell: Element, hfil_indexes: list[bool]) -> None:
    if cell is not None and any(hfil_indexes) and len(hfil_indexes) > 1:
        if hfil_indexes[0] and not hfil_indexes[-1]:
            cell.attrib["columnalign"] = "right"
        elif not hfil_indexes[0] and hfil_indexes[-1]:
            cell.attrib["columnalign"] = "left"


def _get_column_alignment(
    alignment: Optional[str], column_alignment: Optional[str], column_index: int
) -> tuple[Optional[str], int]:
    if alignment:
        try:
            column_alignment = COLUMN_ALIGNMENT_MAP.get(alignment[column_index])
        except IndexError:
            column_alignment = COLUMN_ALIGNMENT_MAP.get(alignment[column_index % len(alignment)])
        column_index += 1
    return column_alignment, column_index


def _make_matrix_cell(row: Element, column_alignment: Optional[str]) -> Element:
    if column_alignment:
        return SubElement(row, "mtd", columnalign=column_alignment)
    return SubElement(row, "mtd")


def _get_alignment_and_column_lines(alignment: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
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


def _separate_by_mode(text: str) -> Iterator[tuple[str, Mode]]:
    string = ""
    is_math_mode = False
    for match in MATH_MODE_PATTERN.findall(text):
        if match == "$":
            yield string, Mode.MATH if is_math_mode else Mode.TEXT
            string = ""
            is_math_mode = not is_math_mode
        else:
            string += match
    if len(string):
        yield string, Mode.MATH if is_math_mode else Mode.TEXT


def _add_diacritic(command: str, parent: Element) -> None:
    if command in commands.DIACRITICS:
        text, attributes = copy.deepcopy(commands.DIACRITICS[command])
        element = SubElement(parent, "mo", attributes)
        element.text = text


def _convert_and_append_command(command: str, parent: Element, attributes: Optional[dict[str, str]] = None) -> None:
    code_point = convert_symbol(command)
    mo = SubElement(parent, "mo", attributes if attributes is not None else {})
    mo.text = "&#x{};".format(code_point) if code_point else command


def convert(
    latex: str,
    xmlns: str = "http://www.w3.org/1998/Math/MathML",
    display: str = "inline",
    parent: Optional[Element] = None,
) -> str:
    return Converter(xmlns=xmlns, display=display).convert(latex, parent=parent)


def convert_to_element(
    latex: str,
    xmlns: str = "http://www.w3.org/1998/Math/MathML",
    display: str = "inline",
    parent: Optional[Element] = None,
) -> Element:
    return Converter(xmlns=xmlns, display=display).convert_to_element(latex, parent=parent)


def main() -> None:  # pragma: no cover
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Pure Python library for LaTeX to MathML conversion")
    parser.add_argument("-V", "--version", dest="version", action="store_true", required=False, help="Show version")
    parser.add_argument("-b", "--block", dest="block", action="store_true", required=False, help="Display block")

    required = parser.add_argument_group("required arguments")

    group = required.add_mutually_exclusive_group(required=False)
    group.add_argument("-t", "--text", dest="text", type=str, required=False, help="Text")
    group.add_argument("-f", "--file", dest="file", type=str, required=False, help="File")
    group.add_argument("-s", "--stdin", dest="stdin", action="store_true", required=False, help="Stdin")

    arguments = parser.parse_args()
    display = "block" if arguments.block else "inline"

    if arguments.version:
        import latex2mathml

        print("latex2mathml", latex2mathml.__version__)
    elif arguments.text:
        print(convert(arguments.text, display=display))
    elif arguments.file:
        with open(arguments.file) as f:
            print(convert(f.read(), display=display))
    elif arguments.stdin:
        print(convert(sys.stdin.read(), display=display))


if __name__ == "__main__":  # pragma: no cover
    main()
