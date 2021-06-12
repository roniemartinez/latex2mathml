import codecs
import os
import re
from typing import Dict, Optional, Union

SYMBOLS_FILE: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "unimathsymbols.txt")
SYMBOLS: Optional[Dict[str, str]] = None


def convert_symbol(symbol: str) -> Union[str, None]:
    global SYMBOLS
    if not SYMBOLS:
        SYMBOLS = parse_symbols()
    return SYMBOLS.get(symbol, None)


def parse_symbols() -> Dict[str, str]:
    _symbols: Dict[str, str] = {}
    with codecs.open(SYMBOLS_FILE, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            columns = line.strip().split("^")
            _unicode = columns[0]
            latex = columns[2]
            unicode_math = columns[3]
            if latex and latex not in _symbols:
                _symbols[latex] = _unicode
            if unicode_math and unicode_math not in _symbols:
                _symbols[unicode_math] = _unicode
            for equivalent in re.findall(r"[=#]\s*(\\[^,^ ]+),?", columns[-1]):
                if equivalent not in _symbols:
                    _symbols[equivalent] = _unicode
    _symbols.update(
        {
            r"\bigcirc": _symbols[r"\lgwhtcircle"],
            r"\Box": _symbols[r"\square"],
            r"\circledS": "024C8",
            r"\diagdown": "02572",
            r"\diagup": "02571",
            r"\dots": "02026",
            r"\dotsb": "022EF",
            r"\dotsc": "02026",
            r"\dotsi": "022EF",
            r"\dotsm": "022EF",
            r"\dotso": "02026",
            r"\emptyset": "02205",
        }
    )
    return _symbols
