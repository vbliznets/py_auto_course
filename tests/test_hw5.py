import pytest
from conftest import config

try:
    from homeworks.hw5.hw5_solution import (change_symbol, add_ing,
                                            change_order, clean_string,
                                            to_capitalize, to_list,
                                            formatting, to_string,
                                            insert_to_list, delete_from_list)
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw5", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("string,expected", [
    ('www.my_site.com#about', 'www.my_site.com/about'),
    ('Test#me', 'Test/me'),
    ('my#first#string', 'my/first/string'),
])
def test_change_symbol(string, expected):
    assert change_symbol(string) == expected, f"Expected '{expected}' string"


@pytest.mark.parametrize("string,expected", [
    ('Word', 'Wording'),
    ('Hello', 'Helloing'),
    ('Python', 'Pythoning')
])
def test_add_ing(string, expected):
    assert add_ing(string) == expected, f"Expected '{expected}' for adding 'ing' to '{string}'"


@pytest.mark.parametrize("string,expected", [
    ('Ivan Ivanov', 'Ivanov Ivan'),
    ('Petya Petrov', 'Petrov Petya'),
    ('Test String', 'String Test'),
])
def test_change_order(string, expected):
    assert change_order(string) == expected, f"Expected '{expected}', from {string}"


@pytest.mark.parametrize("string,expected", [
    (' Python ', 'Python'),
    (' Hello World', 'Hello World'),
    ('Test String ', 'Test String'),
])
def test_clean_string(string, expected):
    assert clean_string(string) == expected, f"Expected to have'{expected}', from input {string}"


@pytest.mark.parametrize("string,expected", [
    ('pARiS', 'Paris'),
    ('paris', 'Paris'),
    ('PARIS', 'Paris'),
])
def test_to_capitalize(string, expected):
    assert to_capitalize(string) == expected, f"Expected '{expected}', from input '{string}'"


@pytest.mark.parametrize("string,expected", [
    ("Robin Singh", ["Robin", "Singh"]),
    ("Test String", ["Test", "String"]),
    ("I love arrays they are my favorite", ["I", "love", "arrays", "they", "are", "my", "favorite"]),
])
def test_to_list(string, expected):
    assert to_list(string) == expected, f"Expected a list {expected}, from input {string}"


@pytest.mark.parametrize("arr,s1,s2,expected", [
    (["Robin", "Singh"], "Welcome", "airport", "Hello, Robin Singh! Welcome to airport"),
])
def test_formatting(arr, s1, s2, expected):
    assert formatting(arr, s1, s2) == expected, f"Expected {expected}, from input: {arr}, {s1}, {s2}"


@pytest.mark.parametrize("arr,expected", [
    (["I", "love", "arrays", "they", "are", "my", "favorite"], "I love arrays they are my favorite"),
])
def test_to_string(arr, expected):
    assert to_string(arr) == expected, f"Expected to have a string {expected}"


@pytest.mark.parametrize("arr,item,place,expected", [
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], "new", 3, [1, 2, 3, "new", 4, 5, 6, 7, 8, 9]),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], 10, 1, [1, 10, 2, 3, 4, 5, 6, 7, 8, 9]),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], 10, 10, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
])
def test_insert_to_list(arr, item, place, expected):
    assert insert_to_list(arr, item, place) == expected, f"Expected to get a list {expected}"


@pytest.mark.parametrize("arr,place,expected", [
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], 3, [1, 2, 3, 5, 6, 7, 8, 9]),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9], 0, [2, 3, 4, 5, 6, 7, 8, 9]),
])
def test_delete_from_list(arr, place, expected):
    assert delete_from_list(arr, place) == expected, f"Expected to have a list {expected}"
