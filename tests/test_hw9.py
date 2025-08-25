import pytest
from conftest import config

try:
    from homeworks.hw9.candles.hw9_solution import count_candles
    from homeworks.hw9.count_characters.hw9_solution import count_char
    from homeworks.hw9.remove_prev_symbol.hw9_solution import remove_previous_symbol
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw9", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("candles,leftover,expected", [
    (5, 2, 9),
    (1, 2, 1),
    (15, 5, 18),
    (12, 2, 23),
    (6, 4, 7),
    (13, 5, 16),
    (2, 3, 2),
])
def test_count_candles(candles, leftover, expected):
    assert count_candles(candles, leftover) == expected, \
        f"Expected that from {candles} candles, you can make {expected}"


@pytest.mark.parametrize("raw_str,expected", [
    ("a#bc#d", "bd"),
    ("abc#d##c", "ac"),
    ("abc##d######", ""),
    ("#######", ""),
    ("", ""),
])
def test_remove_previous_symbol(raw_str, expected):
    assert remove_previous_symbol(raw_str) == expected, f"Expected from {raw_str} you get {expected}"


@pytest.mark.parametrize("raw_str,expected", [
    ("cccbba", "c3b2a"),
    ("abeehhhhhccced", "abe2h5c3ed"),
    ("aaabbceedd", "a3b2ce2d2"),
    ("abcde", "abcde"),
    ("aaabbdefffff", "a3b2def5"),
])
def test_count_char(raw_str, expected):
    assert count_char(raw_str) == expected, f"Expected from {raw_str} you get {expected}"
