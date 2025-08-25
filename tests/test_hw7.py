import pytest
from conftest import config

try:
    from homeworks.hw7.bulls_and_cows.hw7_solution import check_guess, generate_secret_number
    from homeworks.hw7.statues.hw7_solution import missing_statues
    from homeworks.hw7.infinity_loop.hw7_solution import infinity_loop
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw7", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("bulls,cows,expected", [
    ('3219', '3219', (4, 0)),
    ('3219', '2310', (1, 2)),
    ('3219', '7654', (0, 0)),
    ('1234', '4321', (0, 4)),
    ('9876', '9870', (3, 0)),
    ('5678', '5768', (2, 2)),
])
def test_cow_bulls(bulls, cows, expected):
    assert check_guess(bulls, cows) == expected, f"Expected '{expected[0]} bulls, {expected[1]} cows'"


@pytest.mark.parametrize("expected", [
    4,
])
def test_cow_bulls_len(expected):
    assert len(generate_secret_number()) == expected, \
        f"Expected that secret code should be generated with '{expected}' digits"


@pytest.mark.parametrize("expected", [
    True,
])
def test_cow_bulls_generate_digit(expected):
    assert generate_secret_number().isdigit() == expected, \
        "Expected that secret code should be generated with '4' digits"


@pytest.mark.parametrize("arr,expected", [
    ([6, 2, 3, 8], 3),
    ([1, 2, 3, 4, 5], 0),
    ([10], 0),
    ([3, 4, 5, 6, 7], 0),
    ([1, 10], 8),
    ([8, 3, 6, 2], 3),
    ([5, 3, 3, 7], 2),
    ([], 0),
])
def test_missing_statues(arr, expected):
    assert missing_statues(arr) == expected, f"Expected '{expected}' missing statues, from {arr}"


@pytest.mark.parametrize("left,right,expected", [
    (2, 6, False),
    (2, 3, True),
    (5, 5, False),
    (-3, -1, False),
    (-2, 2, False),
    (10, 11, True),
])
def test_infinity_loop(left, right, expected):
    assert infinity_loop(left, right) == expected, \
        f"Expected infinity-loop={expected} for numbers from {left} to {right} "
