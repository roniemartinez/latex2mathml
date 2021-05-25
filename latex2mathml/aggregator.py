from typing import Any, Iterator, List, NamedTuple, Optional, Tuple

from latex2mathml import commands
from latex2mathml.exceptions import (
    DenominatorNotFoundError,
    DoubleSubscriptsError,
    DoubleSuperscriptsError,
    ExtraLeftOrMissingRight,
    MissingSuperScriptOrSubscript,
    NumeratorNotFoundError,
)
from latex2mathml.tokenizer import tokenize


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
            if terminator == commands.RIGHT:
                delimiter = next(tokens)
                node = Node(token=token, delimiter=delimiter)
                aggregated.append(node)
            break
        elif token == commands.RIGHT != terminator:
            raise ExtraLeftOrMissingRight
        elif token == commands.LEFT:
            delimiter = next(tokens)
            children = tuple(_aggregate(tokens, terminator=commands.RIGHT))  # make \right as a child of \left
            if len(children) == 0 or children[-1].token != commands.RIGHT:
                raise ExtraLeftOrMissingRight
            node = Node(token=token, children=children if len(children) else None, delimiter=delimiter)
        elif token == commands.OPENING_BRACES:
            children = tuple(_aggregate(tokens, terminator=commands.CLOSING_BRACES))
            node = Node(token=commands.BRACES, children=children)
        elif token == commands.OPENING_PARENTHESIS:
            children = tuple(_aggregate(tokens, terminator=commands.CLOSING_PARENTHESIS))
            if len(children):
                node = Node(token=commands.PARENTHESES, children=children)
            else:
                aggregated.extend([Node(token=token), Node(token=commands.CLOSING_PARENTHESIS)])
                continue
        elif token == commands.OPENING_BRACKET:
            children = tuple(_aggregate(tokens, terminator=commands.CLOSING_BRACKET))
            if len(children) or (terminator is not None and terminator.startswith(commands.END)):
                node = Node(token=commands.BRACKETS, children=children)
            else:
                aggregated.extend([Node(token=token), Node(token=commands.CLOSING_BRACKET)])
                continue
        elif token == commands.SUBSCRIPT or token == commands.SUPERSCRIPT:
            try:
                previous = aggregated.pop()
            except IndexError:
                previous = Node(token="")
            if token == commands.SUBSCRIPT and previous.token == commands.SUPERSCRIPT and previous.children is not None:
                node = Node(
                    token=commands.SUBSUP,
                    children=(
                        previous.children[0],
                        *_aggregate(tokens, terminator=terminator, limit=1),
                        previous.children[1],
                    ),
                )
            elif (
                token == commands.SUPERSCRIPT and previous.token == commands.SUBSCRIPT and previous.children is not None
            ):
                next_children = _aggregate(tokens, terminator=terminator, limit=1)
                if previous.children[0].token == commands.LIMITS and aggregated[-1].token == commands.INTEGRAL:
                    node = Node(commands.LIMITS, children=(aggregated.pop(), *previous.children[1:], *next_children))
                else:
                    node = Node(token=commands.SUBSUP, children=(*previous.children, *next_children))
            elif token == previous.token == commands.SUBSCRIPT:
                raise DoubleSubscriptsError
            elif token == previous.token == commands.SUPERSCRIPT:
                raise DoubleSuperscriptsError
            else:
                next_nodes = _aggregate(tokens, terminator=terminator, limit=1)
                if len(next_nodes) == 0:
                    raise MissingSuperScriptOrSubscript
                node = Node(token=token, children=(previous, *next_nodes))
        elif token == commands.FRAC or token == commands.BINOM:
            node = Node(token=token, children=tuple(_aggregate(tokens, terminator=terminator, limit=2)))
        elif token in commands.COMMANDS_WITH_ONE_PARAMETER:
            node = Node(token=token, children=tuple(_aggregate(tokens, terminator=terminator, limit=1)))
        elif token == commands.TEXT:
            node = Node(token=token, text=next(tokens))
        elif token == commands.OVER:
            denominator = tuple(_aggregate(tokens, terminator=terminator))
            if len(denominator) > 1:
                denominator = (Node(token=commands.BRACES, children=denominator),)
            if len(denominator) == 0:
                raise DenominatorNotFoundError
            if len(aggregated) == 0:
                raise NumeratorNotFoundError
            elif len(aggregated) == 1:
                children = (*aggregated, *denominator)
            else:
                children = (Node(token=commands.BRACES, children=tuple(aggregated)), *denominator)
            aggregated = [Node(token=commands.FRAC, children=children)]
            continue
        elif token == commands.SQRT:
            root = None
            next_node = tuple(_aggregate(tokens, limit=1))
            if next_node[0].token == commands.BRACKETS and next_node[0].children is not None:
                root = next_node[0].children[0]
                next_node = tuple(_aggregate(tokens, limit=1))
            if root:
                node = Node(token=commands.ROOT, children=(*next_node[-1:], root))
            else:
                node = Node(token=token, children=next_node[-1:])
        elif token.startswith(commands.BEGIN):
            # TODO: support non-matrix environments
            matrix = token[token.index("{") + 1 : -1]
            children = tuple(_aggregate(tokens, terminator=rf"{commands.END}{{{matrix}}}"))
            alignment = ""
            try:
                if (
                    len(children) > 1
                    and children[0] is not None
                    and children[0].children is not None
                    and (
                        children[0].token == commands.BRACES
                        or (matrix.endswith("*") and children[0].token == commands.BRACKETS)
                    )
                    and all(c.token in "lcr|" for c in children[0].children)
                ):
                    alignment = "".join(c.token for c in children[0].children)
                    children = children[1:]
            except IndexError:  # TODO: refactor
                children = children[1:]
            node = Node(token=rf"\{matrix}", children=children, alignment=alignment)
        elif token in commands.MATRICES:
            children = tuple(_aggregate(tokens, terminator=terminator))
            if len(children) == 1 and children[0].token == commands.BRACES and children[0].children:
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
