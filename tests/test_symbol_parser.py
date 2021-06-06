import pytest

from latex2mathml.symbols_parser import convert_symbol


@pytest.mark.parametrize(
    "latex, expected",
    [pytest.param("+", "0002B", id="operator-plus"), pytest.param(r"\to", "02192", id="alias-command")],
)
def test_convert_symbol(latex: str, expected: str) -> None:
    assert convert_symbol(latex) == expected
    assert False  # make fail
