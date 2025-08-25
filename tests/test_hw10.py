import pytest
from conftest import config

try:
    from homeworks.hw10.positive_func_args.hw10_solution import sum_positive
    from homeworks.hw10.return_number.hw10_solution import concat_str, arguments_summary
    from homeworks.hw10.type_decorator.hw10_solution import add_str, add_float, add_int
    from homeworks.hw10.cache_function.hw10_solution import cache_function
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw10", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("args,kwargs,expected", [
    ((1, 1, 1, 1), {"a": 1, "b": 1}, 6),
    ((), {"c": 2, "b": 3}, 5),
    ((5,), {"c": 2}, 7),
    ((1, 1), {}, 2),
    ((), {}, 0),
])
def test_sum_positive(args, kwargs, expected):
    assert sum_positive(*args, **kwargs) == expected, f"Expected {expected} for the arguments {args}"


@pytest.mark.parametrize("args,kwargs,expected", [
    ((0,), {"a": 1}, 0),
    ((1,), {"a": 0}, 0),
    ((-1,), {"a": 1}, -1),
    ((1,), {"a": -1}, -1),
])
def test_sum_negative(args, kwargs, expected):
    with pytest.raises(ValueError) as excinfo:
        sum_positive(*args, **kwargs)
    assert str(excinfo.value) == f"{expected} is not a positive", \
        "Expected an error if arguments less then 1"


@pytest.mark.parametrize("args,kwargs,expected", [
    ((-1, 2), {}, 1),
    ((), {"a": 1, "b": 0}, 1),
])
def test_arguments_summary(args, kwargs, expected):
    assert arguments_summary(*args, **kwargs) == expected, \
        f"Expected '{expected}' as summary of arguments arg1={args}, arg2={kwargs}"


@pytest.mark.parametrize("args,kwargs,expected", [
    (('foo', 'bar'), {}, "Arguments should be a number"),
    ((), {"a": "foo", "b": "bar"}, "Arguments should be a number"),
])
def test_arguments_concatenate_negative(args, kwargs, expected):
    with pytest.raises(ValueError) as excinfo:
        concat_str(*args, **kwargs)
    assert str(excinfo.value) == expected, f"Expected to have an error {expected}"


@pytest.mark.parametrize("args,expected", [
    (("3", 5), "35"),
    ((5, 5), "55"),
    (("a", "b"), 'ab'),
])
def test_typed_decorator_to_str(args, expected):
    assert add_str(*args) == expected, f"Expected '{expected}', as summary of arguments={args}"


@pytest.mark.parametrize("args,expected", [
    ((3, 5), 8),
    ((5, 5), 10),
    ((5, "6", 7), 18),
])
def test_typed_decorator_to_int(args, expected):
    assert add_int(*args) == expected, f"Expected '{expected}', as summary of arguments={args}"


@pytest.mark.parametrize("args,expected", [
    ((0.1, 0.2, 0.4), 0.7000000000000001),
    ((0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1), 0.9999999999999999),
])
def test_typed_decorator_to_float(args, expected):
    assert add_float(*args) == expected, f"Expected '{expected}', as summary of arguments={args}"


# TODO 10*
@pytest.mark.parametrize("args,expected", [
    (7, 13),
    (10, 55),
    (55, 139583862445),
])
def test_cache_function(args, expected):
    assert cache_function(args) == expected, f"Expected '{expected}', as fibonacci for {args}"
