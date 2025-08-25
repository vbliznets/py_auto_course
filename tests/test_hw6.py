import pytest
from conftest import config

try:
    from homeworks.hw6.hw6_solution import (level_up,
                                            motor_time,
                                            time_converter)
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw6", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("experience,threshold,reward,expected", [
    (10, 15, 5, True),
    (10, 15, 4, False),
    (10, 10, 0, True),
    (1000, 1500, 600, True),
    (1000, 1500, 499, False),
    (20, 50, 0, False),
    (50, 50, 10, True),
])
def test_level_up(experience, threshold, reward, expected):
    assert level_up(experience, threshold, reward) == expected, \
        f"Expected with input parameters experience={experience}', threshold={threshold} and reward={reward}'" \
        f"should be {expected}"


@pytest.mark.parametrize("motor_h,expected", [
    (240, 4),
    (808, 14),
    (0, 0),
    (60, 1),
    (1439, 19),
])
def test_motor_time(motor_h, expected):
    assert motor_time(motor_h) == expected, f"Expected '{expected}' for motor hour {motor_h}"


@pytest.mark.parametrize("hours_string,expected", [
    ('12:30', '12:30 p.m.'),
    ('09:00', '9:00 a.m.'),
    ('23:59', '11:59 p.m.'),
    ('00:00', '12:00 a.m.'),
    ('06:45', '6:45 a.m.'),
    ('12:00', '12:00 p.m.'),
    ('00:01', '12:01 a.m.'),
])
def test_time_converter(hours_string, expected):
    assert time_converter(hours_string) == expected, \
        f"Expected '{expected}' in 12h format from {hours_string} in 24h format"
