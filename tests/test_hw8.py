import pytest
from conftest import config

try:
    from homeworks.hw8.sequence.hw8_solution import ascending_sequence
    from homeworks.hw8.number_opposite.hw8_solution import number_opposite
    from homeworks.hw8.payment_card_validation.hw8_solution import is_card_number_valid
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw8", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("arr,expected", [
    ([1, 2, 3], True),
    ([1, 2, 1, 2], False),
    ([1, 3, 2, 1], False),
    ([1, 2, 3, 4, 5, 3, 5, 6], False),
    ([40, 50, 60, 10, 20, 30], False),
])
def test_ascending_sequence(arr, expected):
    assert ascending_sequence(arr) == expected, f"Expected ascending-sequence={expected} for {arr}"


@pytest.mark.parametrize("n,f_number,expected", [
    (10, 6, 1),
    (10, 2, 7),
    (10, 4, 9),
    (6, 0, 3),
    (8, 4, 0),
    (100, 25, 75),
    (12, 0, 6),
    (14, 13, 6),
])
def test_number_opposite(n, f_number, expected):
    assert number_opposite(n, f_number) == expected, f"Expected '{expected}' is opposite to '{f_number}'"


@pytest.mark.parametrize("numer,expected", [
    (4561261212345464, False),
    (4561261212345467, True),
    (123, False),
    (123, False),
    ("abcd1234", False),
    ("", False),
    (79927398713, True),
    (378282246310005, True),
    (378734493671000, True),
    (4222222222222, True),
    (4222222222222, True),
    (5555555555554444, True),
    (5105105105105100, True),
])
def test_is_card_number_valid(numer, expected):
    assert is_card_number_valid(numer) == expected, \
        f"Expected that card with number '{numer}' is valid={expected}"
