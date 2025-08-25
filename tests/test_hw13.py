import os
import pytest
from conftest import config

try:
    from homeworks.hw13.files.hw13_solution import StudentManager
    from homeworks.hw13.engineering_calculator.hw13_solution import (evaluate_expression,
                                                                     validate_expression)
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw13", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("students_content,expected", [
    ("""John Doe, Group 1, 85\nJane Smith, Group 2, 90\nAlice Johnson, Group 1, 78\nBob Brown, Group 2, 88\n""",
     ([('John Doe', 'Group 1', 85), ('Jane Smith', 'Group 2', 90),
       ('Alice Johnson', 'Group 1', 78), ('Bob Brown', 'Group 2', 88)],
      {'Group 1': {'count': 2, 'total_grade': 163}, 'Group 2': {'count': 2, 'total_grade': 178}})),
])
def test_read_students_from_file(students_content, expected, mocker):
    sm = StudentManager("students.txt")
    mock_file = mocker.mock_open(read_data=students_content)
    mocker.patch("builtins.open", mock_file)
    assert sm.read_students_file() == expected, f"Expected to get {expected} information from file"


@pytest.mark.parametrize("students_content,expected", [
    ("""John Doe, Group 1, 85\nJane Smith, Group 2, 90\nAlice Johnson, Group 1, 78\nBob Brown, Group 2, 88\n""",
     ({'Group 1': {'count': 2, 'avg_grade': 81.5}, 'Group 2': {'count': 2, 'avg_grade': 89.0}})),
])
def test_get_summary_from_file(students_content, expected, mocker):
    sm = StudentManager("students.txt")
    mock_file = mocker.mock_open(read_data=students_content)
    mocker.patch("builtins.open", mock_file)
    sm.read_students_file()
    assert sm.get_summary() == expected, f"Expected to get {expected} information from file"


@pytest.mark.parametrize("students_content,expected", [
    ("""John Doe, Group 1, 85\nJane Smith, Group 2, 90\n""",
     """John Doe, Group 1, 85\nJane Smith, Group 2, 90\n"""),
])
def test_create_students_from_file(students_content, expected, mocker):
    sm = StudentManager("students.txt")
    # Check that file doesn't exist
    assert not os.path.isfile(sm.filename)
    # Mock the 'open' function call to return a file object.
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)
    sm.create_students_file(students_content)
    # Assert that the 'open' function was called with the expected arguments.
    mock_file.assert_called_once_with(sm.filename, "w")
    # Assert that the file was written to with the expected text.
    mock_file().write.assert_called_once_with(expected)


@pytest.mark.parametrize("students_content,expected", [
    ("""John Doe, Group 1, 85\nJane Smith, Group 2, 90\n""",
     """\nTotal students: 0\n"""),
])
def test_write_to_file(students_content, expected, mocker):
    sm = StudentManager("students.txt")
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)
    sm.write_summary_to_file()
    mock_file.assert_called_once_with(sm.filename, "a")
    mock_file().write.assert_called_once_with(expected)


@pytest.mark.parametrize("expression,expected", [
    ("2+3", 5),
    ("10-2", 8),
    ("2*3", 6),
    ("8/4", 2),
    ("10//3", 3),
    ("10%3", 1),
    ("2**3", 8),
    ("2+3*4", 14),
    ("2*3+4", 10),
    ("2+(3*4)-2", 12),
    ("(2+3)*4", 20),
    ("1/0", "Division by zero."),
    ("2+*3", "Syntax error in the expression."),
    ("2 + abc", "Invalid char --> a"),
])
def test_engineering_calculator(expression, expected):
    assert evaluate_expression(expression) == expected, \
        f"Expression={expected}, expected result {expected}"


@pytest.mark.parametrize("expression,expected", [
    ("1234567890", (True, None)),
    ("+-*/()%", (True, None)),
    ("'", (False, "'")),
    ("~", (False, "~")),
    ("_", (False, "_")),
    ("{", (False, "{")),
    ("}", (False, "}")),
    ("[", (False, "[")),
    ("]", (False, "]")),
    ("=", (False, "=")),
])
def test_engineering_calculator_negative(expression, expected):
    assert validate_expression(expression) == expected, \
        f"Expression={expected}, expected result {expected}"
