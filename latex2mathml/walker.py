from typing import Any, Iterator, NamedTuple, Optional

from latex2mathml import commands
from latex2mathml.exceptions import (
    DenominatorNotFoundError,
    DoubleSubscriptsError,
    DoubleSuperscriptsError,
    ExtraLeftOrMissingRightError,
    InvalidAlignmentError,
    InvalidStyleForGenfracError,
    InvalidWidthError,
    LimitsMustFollowMathOperatorError,
    MissingEndError,
    MissingSuperScriptOrSubscriptError,
    NoAvailableTokensError,
    NumeratorNotFoundError,
)
from latex2mathml.symbols_parser import convert_symbol
from latex2mathml.tokenizer import tokenize

MULTIPRIMES = "multiprimes"
MAX_MACRO_DEPTH = 100


class Node(NamedTuple):
    token: str
    children: Optional[tuple[Any, ...]] = None
    delimiter: Optional[str] = None
    alignment: Optional[str] = None
    text: Optional[str] = None
    attributes: Optional[dict[str, str]] = None
    modifier: Optional[str] = None


def walk(data: str, display: str = "inline", macros: Optional[dict[str, tuple[list[str], int]]] = None) -> list[Node]:
    tokens = tokenize(data)
    block = display == "block"
    return _walk(tokens, block=block, macros={} if macros is None else macros)


def _walk(
    tokens: Iterator[str],
    terminator: Optional[str] = None,
    limit: int = 0,
    block: bool = False,
    macros: Optional[dict[str, tuple[list[str], int]]] = None,
    depth: int = 0,
) -> list[Node]:
    _macros = {} if macros is None else macros
    group: list[Node] = []
    token: str
    has_available_tokens = False
    for token in tokens:
        has_available_tokens = True
        if token == terminator:
            delimiter = None
            if terminator == commands.RIGHT:
                delimiter = next(tokens)
            group.append(Node(token=token, delimiter=delimiter))
            break
        elif (token == commands.RIGHT != terminator) or (token == commands.MIDDLE and terminator != commands.RIGHT):
            raise ExtraLeftOrMissingRightError
        elif token == commands.LEFT:
            delimiter = next(tokens)
            children = tuple(
                _walk(tokens, terminator=commands.RIGHT, macros=_macros)
            )  # make \right as a child of \left
            if len(children) == 0 or children[-1].token != commands.RIGHT:
                raise ExtraLeftOrMissingRightError
            node = Node(token=token, children=children if len(children) else None, delimiter=delimiter)
        elif token == commands.OPENING_BRACE:
            children = tuple(_walk(tokens, terminator=commands.CLOSING_BRACE, macros=_macros))
            if len(children) and children[-1].token == commands.CLOSING_BRACE:
                children = children[:-1]
            node = Node(token=commands.BRACES, children=children)
        elif token in (commands.SUBSCRIPT, commands.SUPERSCRIPT):
            try:
                previous = group.pop()
            except IndexError:
                previous = Node(token="")  # left operand can be empty if not present

            if token == previous.token == commands.SUBSCRIPT:
                raise DoubleSubscriptsError
            if (token == previous.token == commands.SUPERSCRIPT) and (
                previous.children is not None
                and len(previous.children) >= 2
                and previous.children[1].token != commands.PRIME
            ):
                raise DoubleSuperscriptsError

            modifier = None
            if previous.token in (commands.LIMITS, commands.NOLIMITS):
                modifier = previous.token
                try:
                    previous = group.pop()
                    if not previous.token.startswith("\\"):  # TODO: Complete list of operators
                        raise LimitsMustFollowMathOperatorError
                except IndexError:
                    raise LimitsMustFollowMathOperatorError
            elif block and previous.token in (commands.SUMMATION, commands.PRODUCT):
                # block summation and product should result in limited sub/sup
                modifier = commands.LIMITS

            if token == commands.SUBSCRIPT and previous.token == commands.SUPERSCRIPT and previous.children is not None:
                children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
                node = Node(
                    token=commands.SUBSUP,
                    children=(previous.children[0], *children, previous.children[1]),
                    modifier=previous.modifier,
                )
            elif (
                token == commands.SUPERSCRIPT and previous.token == commands.SUBSCRIPT and previous.children is not None
            ):
                children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
                node = Node(token=commands.SUBSUP, children=(*previous.children, *children), modifier=previous.modifier)
            elif (
                token == commands.SUPERSCRIPT
                and previous.token == commands.SUPERSCRIPT
                and previous.children is not None
                and previous.children[1].token == commands.PRIME
            ):
                children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))

                node = Node(
                    token=commands.SUPERSCRIPT,
                    children=(
                        previous.children[0],
                        Node(token=commands.BRACES, children=(previous.children[1], *children)),
                    ),
                    modifier=previous.modifier,
                )
            else:
                try:
                    children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
                except NoAvailableTokensError:
                    raise MissingSuperScriptOrSubscriptError
                if previous.token in (commands.OVERBRACE, commands.UNDERBRACE):
                    modifier = previous.token
                node = Node(token=token, children=(previous, *children), modifier=modifier)
        elif token == commands.APOSTROPHE:
            try:
                previous = group.pop()
            except IndexError:
                previous = Node(token="")  # left operand can be empty if not present

            prev_is_super_with_children = (
                previous.token == commands.SUPERSCRIPT and previous.children is not None and len(previous.children) >= 2
            )
            prev_prime = previous.children[1] if prev_is_super_with_children and previous.children else None
            prev_is_prime_token = prev_prime is not None and (
                prev_prime.token in commands.PRIME_UPGRADE
                or prev_prime.token == commands.QPRIME
                or prev_prime.token == MULTIPRIMES
            )

            if prev_is_super_with_children and not prev_is_prime_token:
                raise DoubleSuperscriptsError

            if prev_is_prime_token and previous.children is not None and prev_prime is not None:
                if prev_prime.token in commands.PRIME_UPGRADE:
                    new_prime = Node(token=commands.PRIME_UPGRADE[prev_prime.token])
                elif prev_prime.token == commands.QPRIME:
                    new_prime = Node(token=MULTIPRIMES, text="5")
                else:
                    new_prime = Node(token=MULTIPRIMES, text=str(int(prev_prime.text or "0") + 1))
                node = Node(token=commands.SUPERSCRIPT, children=(previous.children[0], new_prime))
            elif previous.token == commands.SUBSCRIPT and previous.children is not None:
                node = Node(
                    token=commands.SUBSUP,
                    children=(*previous.children, Node(token=commands.PRIME)),
                    modifier=previous.modifier,
                )
            else:
                node = Node(token=commands.SUPERSCRIPT, children=(previous, Node(token=commands.PRIME)))
        elif token in commands.COMMANDS_WITH_TWO_PARAMETERS:
            attributes = None
            children = tuple(_walk(tokens, terminator=terminator, limit=2, macros=_macros))
            if token in (commands.OVERSET, commands.STACKREL, commands.UNDERSET):
                children = children[::-1]
            node = Node(token=token, children=children, attributes=attributes)
        elif token in commands.COMMANDS_WITH_ONE_PARAMETER or (
            token.startswith(commands.MATH) and token not in (commands.MATHSTRUT, commands.MATHCHOICE)
        ):
            children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            node = Node(token=token, children=children)
        elif token == commands.NOT:
            try:
                next_node = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))[0]
                if next_node.token.startswith("\\"):
                    negated_symbol = r"\n" + next_node.token[1:]
                    symbol = convert_symbol(negated_symbol)
                    if symbol:
                        node = Node(token=negated_symbol)
                        group.append(node)
                        continue
                node = Node(token=token)
                group.extend((node, next_node))
                continue
            except NoAvailableTokensError:
                node = Node(token=token)
        elif token in commands.EXTENSIBLE_ARROWS:
            children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            if children[0].token == commands.OPENING_BRACKET:
                children = (
                    Node(
                        token=commands.BRACES,
                        children=tuple(_walk(tokens, terminator=commands.CLOSING_BRACKET, macros=_macros))[:-1],
                    ),
                    *tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros)),
                )
            node = Node(token=token, children=children)
        elif token in (commands.HSKIP, commands.HSPACE, commands.KERN, commands.MKERN, commands.MSKIP, commands.MSPACE):
            children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            if children[0].token == commands.BRACES and children[0].children is not None:
                children = children[0].children
            node = Node(token=token, attributes={"width": children[0].token})
        elif token in (commands.RAISE, commands.LOWER, commands.MOVELEFT, commands.MOVERIGHT):
            dim_children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            dim = dim_children[0].token if dim_children else "0"
            if dim_children[0].token == commands.BRACES and dim_children[0].children:
                dim = dim_children[0].children[0].token
            children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            if token == commands.RAISE:
                attributes = {"voffset": dim, "height": f"+{dim}", "depth": f"-{dim}"}
            elif token == commands.LOWER:
                attributes = {"voffset": f"-{dim}", "height": f"-{dim}", "depth": f"+{dim}"}
            elif token == commands.MOVELEFT:
                attributes = {"lspace": f"-{dim}"}
            else:
                attributes = {"lspace": dim}
            node = Node(token=token, children=children, attributes=attributes)
        elif token == commands.RULE:
            dims = []
            for _ in range(2):
                arg = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))[0]
                if arg.token == commands.BRACES and arg.children:
                    dims.append(arg.children[0].token)
                else:
                    dims.append(arg.token)
            node = Node(token=token, attributes={"width": dims[0], "height": dims[1]})
        elif token == commands.SMASH:
            children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            attributes = {"height": "0px", "depth": "0px"}
            if children[0].token == commands.OPENING_BRACKET:
                opt = tuple(_walk(tokens, terminator=commands.CLOSING_BRACKET, macros=_macros))[:-1]
                if opt and opt[0].token == "b":
                    attributes = {"depth": "0px"}
                elif opt and opt[0].token == "t":
                    attributes = {"height": "0px"}
                children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            node = Node(token=token, children=children, attributes=attributes)
        elif token == commands.TEXTCOLOR:
            color = next(tokens)
            children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            node = Node(token=commands.COLOR, children=children, attributes={"mathcolor": color})
        elif token in (commands.COLORBOX, commands.FCOLORBOX):
            arg_count = 3 if token == commands.FCOLORBOX else 2
            args = []
            for _ in range(arg_count):
                arg_node = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))[0]
                args.append("".join(c.token for c in arg_node.children) if arg_node.children else "")
            if token == commands.FCOLORBOX:
                attributes = {"mathbackground": args[1], "border-color": args[0]}
            else:
                attributes = {"mathbackground": args[0]}
            node = Node(token=token, text=args[-1], attributes=attributes)
        elif token == commands.COLOR:
            attributes = {"mathcolor": next(tokens)}
            children = tuple(_walk(tokens, terminator=terminator, macros=_macros))
            sibling = None
            if len(children) and children[-1].token == terminator:
                children, sibling = children[:-1], children[-1]
            group.append(Node(token=token, children=children, attributes=attributes))
            if sibling:
                group.append(sibling)
            break
        elif token in (commands.LEFTROOT, commands.UPROOT):
            # Consume the numeric argument but discard — MathML has no root index positioning
            tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            continue
        elif token == commands.MATHCHOICE:
            choices = tuple(_walk(tokens, terminator=terminator, limit=4, macros=_macros))
            # In block (display) mode use arg 0, in inline (text) mode use arg 1
            choice = choices[0] if block else choices[1]
            if choice.children:
                for child in choice.children:
                    group.append(child)
            else:
                group.append(choice)
            continue
        elif token == commands.CLASS:
            attributes = {"class": next(tokens)}
            next_node = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))[0]
            node = next_node._replace(attributes=attributes)
        elif token == commands.STYLE:
            attributes = {"style": next(tokens)}
            next_node = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))[0]
            node = next_node._replace(attributes=attributes)
        elif token in (
            *commands.BIG.keys(),
            *commands.BIG_OPEN_CLOSE.keys(),
            commands.CLAP,
            commands.EMPH,
            commands.FBOX,
            commands.HBOX,
            commands.LLAP,
            commands.MBOX,
            commands.MIDDLE,
            commands.RLAP,
            commands.TAG,
            commands.TAGSTAR,
            commands.TEXT,
            commands.TEXTBF,
            commands.TEXTIT,
            commands.TEXTMD,
            commands.TEXTNORMAL,
            commands.TEXTRM,
            commands.TEXTSF,
            commands.TEXTTT,
            commands.TEXTUP,
            commands.VERB,
        ):
            node = Node(token=token, text=next(tokens))
        elif token == commands.HREF:
            attributes = {"href": next(tokens)}
            children = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))
            node = Node(token=token, children=children, attributes=attributes)
        elif token in (
            commands.ABOVE,
            commands.ATOP,
            commands.ABOVEWITHDELIMS,
            commands.ATOPWITHDELIMS,
            commands.BRACE,
            commands.BRACK,
            commands.CHOOSE,
            commands.OVER,
        ):
            attributes = None
            delimiter = None

            if token == commands.ABOVEWITHDELIMS:
                delimiter = next(tokens).lstrip("\\") + next(tokens).lstrip("\\")
            elif token == commands.ATOPWITHDELIMS:
                attributes = {"linethickness": "0"}
                delimiter = next(tokens).lstrip("\\") + next(tokens).lstrip("\\")
            elif token == commands.BRACE:
                delimiter = "{}"
            elif token == commands.BRACK:
                delimiter = "[]"
            elif token == commands.CHOOSE:
                delimiter = "()"

            if token in (commands.ABOVE, commands.ABOVEWITHDELIMS):
                dimension_node = tuple(_walk(tokens, terminator=terminator, limit=1, macros=_macros))[0]
                dimension = _get_dimension(dimension_node)
                attributes = {"linethickness": dimension}
            elif token in (commands.ATOP, commands.BRACE, commands.BRACK, commands.CHOOSE):
                attributes = {"linethickness": "0"}

            denominator = tuple(_walk(tokens, terminator=terminator, macros=_macros))

            sibling = None
            if len(denominator) and denominator[-1].token == terminator:
                denominator, sibling = denominator[:-1], denominator[-1]

            if len(denominator) == 0:
                if token in (commands.BRACE, commands.BRACK):
                    denominator = (Node(token=commands.BRACES, children=()),)
                else:
                    raise DenominatorNotFoundError
            if len(group) == 0:
                if token in (commands.BRACE, commands.BRACK):
                    group = [Node(token=commands.BRACES, children=())]
                else:
                    raise NumeratorNotFoundError
            if len(denominator) > 1:
                denominator = (Node(token=commands.BRACES, children=denominator),)

            if len(group) == 1:
                children = (*group, *denominator)
            else:
                children = (Node(token=commands.BRACES, children=tuple(group)), *denominator)
            group = [Node(token=commands.FRAC, children=children, attributes=attributes, delimiter=delimiter)]
            if sibling is not None:
                group.append(sibling)
            break
        elif token == commands.SQRT:
            root_nodes = None
            next_node = tuple(_walk(tokens, limit=1, macros=_macros))[0]
            if next_node.token == commands.OPENING_BRACKET:
                root_nodes = tuple(_walk(tokens, terminator=commands.CLOSING_BRACKET, macros=_macros))[:-1]
                next_node = tuple(_walk(tokens, limit=1, macros=_macros))[0]
                if len(root_nodes) > 1:
                    root_nodes = (Node(token=commands.BRACES, children=root_nodes),)

            if root_nodes:
                node = Node(token=commands.ROOT, children=(next_node, *root_nodes))
            else:
                node = Node(token=token, children=(next_node,))
        elif token == commands.ROOT:
            root_nodes = tuple(_walk(tokens, terminator=r"\of", macros=_macros))[:-1]
            next_node = tuple(_walk(tokens, limit=1, macros=_macros))[0]
            if len(root_nodes) > 1:
                root_nodes = (Node(token=commands.BRACES, children=root_nodes),)
            if root_nodes:
                node = Node(token=token, children=(next_node, *root_nodes))
            else:
                node = Node(token=token, children=(next_node, Node(token=commands.BRACES, children=())))
        elif token in commands.MATRICES:
            children = tuple(_walk(tokens, terminator=terminator, macros=_macros))
            sibling = None
            if len(children) and children[-1].token == terminator:
                children, sibling = children[:-1], children[-1]
            if len(children) == 1 and children[0].token == commands.BRACES and children[0].children:
                children = children[0].children
            if sibling is not None:
                group.extend([Node(token=token, children=children, alignment=""), sibling])
                break
            else:
                node = Node(token=token, children=children, alignment="")
        elif token == commands.GENFRAC:
            delimiter = next(tokens).lstrip("\\") + next(tokens).lstrip("\\")
            dimension_node, style_node = tuple(_walk(tokens, terminator=terminator, limit=2, macros=_macros))
            dimension = _get_dimension(dimension_node)
            style = _get_style(style_node)
            attributes = {"linethickness": dimension}
            children = tuple(_walk(tokens, terminator=terminator, limit=2, macros=_macros))
            group.extend(
                [Node(token=style), Node(token=token, children=children, delimiter=delimiter, attributes=attributes)]
            )
            break
        elif token == commands.SIDESET:
            left, right, operator = tuple(_walk(tokens, terminator=terminator, limit=3, macros=_macros))
            left_token, left_children = _make_subsup(left)
            right_token, right_children = _make_subsup(right)
            attributes = {"movablelimits": "false"}
            node = Node(
                token=token,
                children=(
                    Node(
                        token=left_token,
                        children=(
                            Node(
                                token=commands.VPHANTOM,
                                children=(
                                    Node(token=operator.token, children=operator.children, attributes=attributes),
                                ),
                            ),
                            *left_children,
                        ),
                    ),
                    Node(
                        token=right_token,
                        children=(
                            Node(token=operator.token, children=operator.children, attributes=attributes),
                            *right_children,
                        ),
                    ),
                ),
            )
        elif token == commands.SKEW:
            width_node, child = tuple(_walk(tokens, terminator=terminator, limit=2, macros=_macros))
            width = width_node.token
            if width == commands.BRACES:
                if width_node.children is None or len(width_node.children) == 0:
                    raise InvalidWidthError
                width = width_node.children[0].token
            if not width.isdigit():
                raise InvalidWidthError
            node = Node(token=token, children=(child,), attributes={"width": f"{0.0555 * int(width):.3f}em"})
        elif token.startswith(commands.BEGIN):
            node = _get_environment_node(token, tokens, macros=_macros)
        elif token == commands.NEWCOMMAND:
            _parse_newcommand(tokens, _macros)
            continue
        elif token == commands.DEF:
            _parse_def(tokens, _macros)
            continue
        elif token == commands.DECLAREMATHOPERATOR:
            _parse_declare_math_operator(tokens, _macros)
            continue
        elif token == commands.NEWENVIRONMENT:
            _parse_newenvironment(tokens, _macros)
            continue
        elif token in _macros:
            if depth >= MAX_MACRO_DEPTH:
                raise RecursionError(f"Maximum macro expansion depth ({MAX_MACRO_DEPTH}) exceeded")
            expanded_tokens = _expand_macro(token, tokens, _macros)
            group.extend(_walk(iter(expanded_tokens), terminator=None, block=block, macros=_macros, depth=depth + 1))
            continue
        else:
            node = Node(token=token)

        group.append(node)

        if limit and len(group) >= limit:
            break
    if not has_available_tokens:
        raise NoAvailableTokensError
    return group


def _make_subsup(node: Node) -> tuple[str, tuple[Node, ...]]:
    if node.token != commands.BRACES:
        raise MissingSuperScriptOrSubscriptError
    if (
        node.children is not None
        and len(node.children) > 0
        and node.children[0].children is not None
        and 2 <= len(node.children[0].children) <= 3
        and node.children[0].token
        in (
            commands.SUBSUP,
            commands.SUBSCRIPT,
            commands.SUPERSCRIPT,
        )
    ):
        token = node.children[0].token
        children = node.children[0].children[1:]
        return token, children
    return "", ()


def _get_dimension(node: Node) -> str:
    dimension = node.token
    if node.token == commands.BRACES and node.children is not None:
        dimension = node.children[0].token
    return dimension


def _get_style(node: Node) -> str:
    style = node.token
    if node.token == commands.BRACES and node.children is not None:
        style = node.children[0].token
    if style == "0":
        return commands.DISPLAYSTYLE
    if style == "1":
        return commands.TEXTSTYLE
    if style == "2":
        return commands.SCRIPTSTYLE
    if style == "3":
        return commands.SCRIPTSCRIPTSTYLE
    raise InvalidStyleForGenfracError


def _get_environment_node(
    token: str, tokens: Iterator[str], macros: Optional[dict[str, tuple[list[str], int]]] = None
) -> Node:
    _macros = {} if macros is None else macros
    start_index = token.index("{") + 1
    environment = token[start_index:-1]
    env_key = f"\\begin{{{environment}}}"
    if env_key in _macros:
        begin_body, _ = _macros[env_key]
        end_body, _ = _macros.get(f"\\end{{{environment}}}", ([], 0))
        terminator = rf"{commands.END}{{{environment}}}"
        content_nodes = tuple(_walk(tokens, terminator=terminator, macros=_macros))
        if len(content_nodes) and content_nodes[-1].token == terminator:
            content_nodes = content_nodes[:-1]
        content_tokens: list[str] = []
        for node in content_nodes:
            content_tokens.append(node.token)
        expanded = [*begin_body, *content_tokens, *end_body]
        result = _walk(iter(expanded), macros=_macros)
        if len(result) == 1:
            return result[0]
        return Node(token=commands.BRACES, children=tuple(result))
    terminator = rf"{commands.END}{{{environment}}}"
    children = tuple(_walk(tokens, terminator=terminator, macros=macros))
    if len(children) and children[-1].token != terminator:
        raise MissingEndError
    children = children[:-1]
    alignment = ""

    if len(children) and children[0].token == commands.OPENING_BRACKET:
        children_iter = iter(children)
        next(children_iter)  # remove BRACKET
        for c in children_iter:
            if c.token == commands.CLOSING_BRACKET:
                break
            elif c.token not in "lcr|":
                raise InvalidAlignmentError
            alignment += c.token
        children = tuple(children_iter)
    elif (
        len(children)
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


def _consume_brace_arg(tokens: Iterator[str]) -> list[str]:
    token = next(tokens)
    if token == "{":
        return _read_until_close_brace(tokens)
    return [token]


def _parse_newcommand(tokens: Iterator[str], macros: dict[str, tuple[list[str], int]]) -> None:
    name_tokens = _consume_brace_arg(tokens)
    name = name_tokens[0] if name_tokens else ""
    nargs = 0
    peek = next(tokens)
    if peek == "[":
        nargs_str = ""
        for t in tokens:
            if t == "]":
                break
            nargs_str += t
        nargs = int(nargs_str)
        body = _consume_brace_arg(tokens)
    else:
        body = _read_until_close_brace(tokens)
    macros[name] = (body, nargs)


def _read_until_close_brace(tokens: Iterator[str]) -> list[str]:
    depth = 1
    content: list[str] = []
    for t in tokens:
        if t == "{":
            depth += 1
            content.append(t)
        elif t == "}":
            depth -= 1
            if depth == 0:
                return content
            content.append(t)
        else:
            content.append(t)
    return content


def _parse_newenvironment(tokens: Iterator[str], macros: dict[str, tuple[list[str], int]]) -> None:
    name_tokens = _consume_brace_arg(tokens)
    name = "".join(name_tokens)
    begin_body = _consume_brace_arg(tokens)
    end_body = _consume_brace_arg(tokens)
    macros[f"\\begin{{{name}}}"] = (begin_body, 0)
    macros[f"\\end{{{name}}}"] = (end_body, 0)


def _parse_def(tokens: Iterator[str], macros: dict[str, tuple[list[str], int]]) -> None:
    name = next(tokens)
    body = _consume_brace_arg(tokens)
    macros[name] = (body, 0)


def _parse_declare_math_operator(tokens: Iterator[str], macros: dict[str, tuple[list[str], int]]) -> None:
    name_tokens = _consume_brace_arg(tokens)
    name = name_tokens[0] if name_tokens else ""
    text_tokens = _consume_brace_arg(tokens)
    text = "".join(text_tokens)
    macros[name] = ([rf"\operatorname{{{text}}}"], 0)


def _expand_macro(token: str, tokens: Iterator[str], macros: dict[str, tuple[list[str], int]]) -> list[str]:
    body, nargs = macros[token]
    if nargs == 0:
        return list(body)
    args: list[list[str]] = []
    for _ in range(nargs):
        args.append(_consume_brace_arg(tokens))
    expanded: list[str] = []
    body_iter = iter(body)
    for tok in body_iter:
        if tok == "#":
            param_num = next(body_iter, "")
            if param_num.isdigit() and 1 <= int(param_num) <= len(args):
                expanded.extend(args[int(param_num) - 1])
            else:
                expanded.append(tok)
                if param_num:
                    expanded.append(param_num)
        else:
            expanded.append(tok)
    return expanded
