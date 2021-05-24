from typing import Any, Iterator, List, NamedTuple, Optional, Tuple

from latex2mathml.commands import MATRICES
from latex2mathml.exceptions import (
    DenominatorNotFoundError,
    ExtraLeftOrMissingRight,
    MissingSuperScriptOrSubscript,
    NumeratorNotFoundError,
)
from latex2mathml.tokenizer import tokenize

OPENING_BRACES = "{"
CLOSING_BRACES = "}"
BRACES = "{}"

OPENING_BRACKET = "["
CLOSING_BRACKET = "]"
BRACKETS = "[]"

OPENING_PARENTHESIS = "("
CLOSING_PARENTHESIS = ")"
PARENTHESES = "()"

SUB_SUP = "_^"
SUBSCRIPT = "_"
SUPERSCRIPT = "^"

LEFT = r"\left"
RIGHT = r"\right"
OVER = r"\over"
FRAC = r"\frac"
BINOM = r"\binom"
ROOT = r"\root"
SQRT = r"\sqrt"

OVERLINE = r"\overline"
BAR = r"\bar"
UNDERLINE = r"\underline"
OVERRIGHTARROW = r"\overrightarrow"
VEC = r"\vec"
DOT = r"\dot"
TEXT = r"\text"

COMMANDS_WITH_ONE_PARAMETER = (OVERLINE, BAR, UNDERLINE, OVERRIGHTARROW, VEC, DOT)

BEGIN = r"\begin"
END = r"\end"


class Node(NamedTuple):
    token: str
    children: Optional[Tuple[Any, ...]] = None
    delimiter: Optional[str] = None
    alignment: Optional[str] = None
    text: Optional[str] = None


def _aggregate(tokens: Iterator, terminator: str = None, limit: int = 0) -> List[Node]:
    aggregated: List[Node] = []
    token: str
    for token in tokens:
        if token == terminator:
            if terminator == RIGHT:
                delimiter = next(tokens)
                node = Node(token=token, delimiter=delimiter)
                aggregated.append(node)
            break
        elif token == RIGHT != terminator:
            raise ExtraLeftOrMissingRight
        elif token == LEFT:
            delimiter = next(tokens)
            children = tuple(_aggregate(tokens, terminator=RIGHT))  # make \right as a child of \left
            if len(children) == 0 or children[-1].token != RIGHT:
                raise ExtraLeftOrMissingRight
            node = Node(token=token, children=children if len(children) else None, delimiter=delimiter)
        elif token == OPENING_BRACES:
            children = tuple(_aggregate(tokens, terminator=CLOSING_BRACES))
            node = Node(token=BRACES, children=children)
        elif token == OPENING_PARENTHESIS:
            children = tuple(_aggregate(tokens, terminator=CLOSING_PARENTHESIS))
            if len(children):
                node = Node(token=PARENTHESES, children=children)
            else:
                aggregated.append(Node(token=token))
                aggregated.append(Node(token=CLOSING_PARENTHESIS))
                continue
        elif token == OPENING_BRACKET:
            children = tuple(_aggregate(tokens, terminator=CLOSING_BRACKET))
            if len(children) or (terminator is not None and terminator.startswith(END)):
                node = Node(token=BRACKETS, children=children)
            else:
                aggregated.append(Node(token=token))
                aggregated.append(Node(token=CLOSING_BRACKET))
                continue
        elif token == SUBSCRIPT or token == SUPERSCRIPT:
            try:
                previous = aggregated.pop()
            except IndexError:
                previous = Node(token="")
            if token == SUBSCRIPT and previous.token == SUPERSCRIPT and previous.children is not None:
                node = Node(
                    token=SUB_SUP,
                    children=(
                        previous.children[0],
                        *_aggregate(tokens, terminator=terminator, limit=1),
                        previous.children[1],
                    ),
                )
            elif token == SUPERSCRIPT and previous.token == SUBSCRIPT and previous.children is not None:
                node = Node(
                    token=SUB_SUP,
                    children=(*previous.children, *_aggregate(tokens, terminator=terminator, limit=1)),
                )
            elif token == previous.token:
                pass  # TODO: Raise error
            else:
                next_nodes = tuple(_aggregate(tokens, terminator=terminator, limit=1))
                if len(next_nodes) == 0:
                    raise MissingSuperScriptOrSubscript
                node = Node(token=token, children=(previous, *next_nodes))
        elif token == FRAC or token == BINOM:
            node = Node(token=token, children=tuple(_aggregate(tokens, terminator=terminator, limit=2)))
        elif token in COMMANDS_WITH_ONE_PARAMETER:
            node = Node(token=token, children=tuple(_aggregate(tokens, terminator=terminator, limit=1)))
        elif token == TEXT:
            node = Node(token=token, text=next(tokens))
        elif token == OVER:
            denominator = tuple(_aggregate(tokens, terminator=terminator))
            if len(denominator) > 1:
                denominator = (Node(token=BRACES, children=denominator),)
            if len(denominator) == 0:
                raise DenominatorNotFoundError
            try:
                node = Node(token=FRAC, children=(aggregated.pop(), *denominator))
            except IndexError:
                raise NumeratorNotFoundError
        elif token == SQRT:
            root = None
            next_node = tuple(_aggregate(tokens, limit=1))
            if next_node[0].token == BRACKETS and next_node[0].children is not None:
                root = next_node[0].children[0]
                next_node = tuple(_aggregate(tokens, limit=1))
            if root:
                node = Node(token=ROOT, children=(*next_node[-1:], root))
            else:
                node = Node(token=token, children=next_node[-1:])
        elif token.startswith(BEGIN):
            # TODO: support non-matrix environments
            matrix = token[token.index("{") + 1 : -1]
            children = tuple(_aggregate(tokens, terminator=rf"{END}{{{matrix}}}"))
            alignment = ""
            try:
                if (
                    len(children) > 1
                    and children[0] is not None
                    and children[0].children is not None
                    and (children[0].token == BRACES or (matrix.endswith("*") and children[0].token == BRACKETS))
                    and all(c.token in "lcr|" for c in children[0].children)
                ):
                    alignment = "".join(c.token for c in children[0].children)
                    children = children[1:]
            except IndexError:  # TODO: refactor
                children = children[1:]
            node = Node(token=rf"\{matrix}", children=children, alignment=alignment)
        elif token in MATRICES:
            children = tuple(_aggregate(tokens, terminator=terminator))
            if len(children) == 1 and children[0].token == BRACES:
                children = children[0].children
            node = Node(token=token, children=children, alignment="")
        else:
            node = Node(token=token)
        aggregated.append(node)
        if limit and len(aggregated) >= limit:
            break
    return aggregated


def aggregate(data: str) -> List[Node]:
    tokens = tokenize(data)
    return _aggregate(tokens)
