from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Tuple

from latex2mathml import commands
from latex2mathml.exceptions import (
    DenominatorNotFoundError,
    DoubleSubscriptsError,
    DoubleSuperscriptsError,
    ExtraLeftOrMissingRightError,
    MissingSuperScriptOrSubscriptError,
    NoAvailableTokensError,
    NumeratorNotFoundError,
)
from latex2mathml.tokenizer import tokenize


class Node(NamedTuple):
    token: str
    children: Optional[Tuple[Any, ...]] = None
    delimiter: Optional[str] = None
    alignment: Optional[str] = None
    text: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None


def walk(data: str) -> List[Node]:
    tokens = tokenize(data)
    return _walk(tokens)


def _walk(tokens: Iterator, terminator: str = None, limit: int = 0) -> List[Node]:
    group: List[Node] = []
    token: str
    has_available_tokens = False
    for token in tokens:
        has_available_tokens = True
        if token == terminator:
            if terminator == commands.RIGHT:
                group.append(Node(token=token, delimiter=next(tokens)))
            break
        elif token == commands.RIGHT != terminator:
            raise ExtraLeftOrMissingRightError
        elif token == commands.LEFT:
            delimiter = next(tokens)
            children = tuple(_walk(tokens, terminator=commands.RIGHT))  # make \right as a child of \left
            if len(children) == 0 or children[-1].token != commands.RIGHT:
                raise ExtraLeftOrMissingRightError
            node = Node(token=token, children=children if len(children) else None, delimiter=delimiter)
        elif token == commands.OPENING_BRACE:
            children = tuple(_walk(tokens, terminator=commands.CLOSING_BRACE))
            node = Node(token=commands.BRACES, children=children)
        elif token == commands.OPENING_PARENTHESIS:
            children = tuple(_walk(tokens, terminator=commands.CLOSING_PARENTHESIS))
            if len(children):
                node = Node(token=commands.PARENTHESES, children=children)
            else:
                group.extend([Node(token=token), Node(token=commands.CLOSING_PARENTHESIS)])
                continue
        elif token == commands.OPENING_BRACKET:
            try:
                children = tuple(_walk(tokens, terminator=commands.CLOSING_BRACKET))
                if len(children) or (terminator is not None and terminator.startswith(commands.END)):
                    node = Node(token=commands.BRACKETS, children=children)
                else:
                    group.extend([Node(token=token), Node(token=commands.CLOSING_BRACKET)])
                    continue
            except NoAvailableTokensError:
                node = Node(token=token)
        elif token in (commands.SUBSCRIPT, commands.SUPERSCRIPT):
            try:
                previous = group.pop()
            except IndexError:
                previous = Node(token="")  # left operand can be empty if not present

            if token == previous.token == commands.SUBSCRIPT:
                raise DoubleSubscriptsError
            if token == previous.token == commands.SUPERSCRIPT:
                raise DoubleSuperscriptsError

            if token == commands.SUBSCRIPT and previous.token == commands.SUPERSCRIPT and previous.children is not None:
                next_nodes = _walk(tokens, terminator=terminator, limit=1)
                node = Node(token=commands.SUBSUP, children=(previous.children[0], *next_nodes, previous.children[1]))
            elif (
                token == commands.SUPERSCRIPT and previous.token == commands.SUBSCRIPT and previous.children is not None
            ):
                next_nodes = _walk(tokens, terminator=terminator, limit=1)
                if previous.children[0].token == commands.LIMITS:
                    node = Node(token=commands.LIMITS, children=(group.pop(), *previous.children[1:], *next_nodes))
                else:
                    node = Node(token=commands.SUBSUP, children=(*previous.children, *next_nodes))
            else:
                try:
                    next_nodes = _walk(tokens, terminator=terminator, limit=1)
                except NoAvailableTokensError:
                    raise MissingSuperScriptOrSubscriptError
                node = Node(token=token, children=(previous, *next_nodes))
        elif token == commands.APOSTROPHE:
            try:
                previous = group.pop()
            except IndexError:
                previous = Node(token="")  # left operand can be empty if not present

            if (
                previous.token == commands.SUPERSCRIPT
                and previous.children is not None
                and len(previous.children) >= 2
                and previous.children[1].token == commands.PRIME
            ):
                node = Node(token=commands.SUPERSCRIPT, children=(previous.children[0], Node(token=commands.DPRIME)))
            else:
                node = Node(token=commands.SUPERSCRIPT, children=(previous, Node(token=commands.PRIME)))
        elif token in commands.COMMANDS_WITH_TWO_PARAMETERS:
            children = tuple(_walk(tokens, terminator=terminator, limit=2))
            if token in (commands.OVERSET, commands.UNDERSET):
                children = children[::-1]
            node = Node(token=token, children=children)
        elif token in commands.COMMANDS_WITH_ONE_PARAMETER:
            children = tuple(_walk(tokens, terminator=terminator, limit=1))
            node = Node(token=token, children=children)
        elif token == commands.HSPACE:
            children = tuple(_walk(tokens, terminator=terminator, limit=1))
            if children[0].token == commands.BRACES and children[0].children is not None:
                children = children[0].children
            node = Node(token=token, attributes={"width": children[0].token})
        elif token in commands.BIG.keys():
            node = Node(token=token, text=next(tokens))
        elif token == commands.TEXT:
            node = Node(token=token, text=next(tokens))
        elif token in (commands.OVER, commands.ABOVE):
            attributes = None
            denominator = tuple(_walk(tokens, terminator=terminator))

            if token == commands.ABOVE:
                attributes = {"linethickness": denominator[0].token}
                denominator = denominator[1:]

            if len(denominator) == 0:
                raise DenominatorNotFoundError
            if len(group) == 0:
                raise NumeratorNotFoundError

            if len(denominator) > 1:
                denominator = (Node(token=commands.BRACES, children=denominator),)

            if len(group) == 1:
                children = (*group, *denominator)
            else:
                children = (Node(token=commands.BRACES, children=tuple(group)), *denominator)
            group = [Node(token=commands.FRAC, children=children, attributes=attributes)]
            continue
        elif token == commands.SQRT:
            node = _get_root_node(token, tokens)
        elif token in commands.MATRICES:
            node = _get_matrix_node(token, tokens, terminator)
        elif token.startswith(commands.BEGIN):
            node = _get_environment_node(token, tokens)
        else:
            node = Node(token=token)

        group.append(node)

        if limit and len(group) >= limit:
            break
    if not has_available_tokens:
        raise NoAvailableTokensError
    return group


def _get_root_node(token: str, tokens: Iterator[str]) -> Node:
    root = None
    next_nodes = tuple(_walk(tokens, limit=1))
    if next_nodes[0].token == commands.BRACKETS and next_nodes[0].children is not None:
        root = next_nodes[0].children[0]
        next_nodes = tuple(_walk(tokens, limit=1))

    if root:
        return Node(token=commands.ROOT, children=(*next_nodes[-1:], root))
    return Node(token=token, children=next_nodes[-1:])


def _get_matrix_node(token: str, tokens: Iterator[str], terminator: Optional[str]) -> Node:
    next_nodes = tuple(_walk(tokens, terminator=terminator))
    if len(next_nodes) == 1 and next_nodes[0].token == commands.BRACES and next_nodes[0].children:
        next_nodes = next_nodes[0].children
    return Node(token=token, children=next_nodes, alignment="")


def _get_environment_node(token: str, tokens: Iterator[str]) -> Node:
    # TODO: support non-matrix environments
    start_index = token.index("{") + 1
    environment = token[start_index:-1]
    children = tuple(_walk(tokens, terminator=rf"{commands.END}{{{environment}}}"))
    alignment = ""
    if (
        len(children) > 1
        and children[0] is not None
        and children[0].children is not None
        and (
            children[0].token == commands.BRACES
            or (environment.endswith("*") and children[0].token == commands.BRACKETS)
        )
        and all(c.token in "lcr|" for c in children[0].children)
    ):
        alignment = "".join(c.token for c in children[0].children)
        children = children[1:]

    return Node(token=rf"\{environment}", children=children, alignment=alignment)
