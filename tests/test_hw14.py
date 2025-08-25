import pytest
from conftest import config

try:
    from homeworks.hw14.date_and_time.between_dates import calculate_days_between
    from homeworks.hw14.date_and_time.future_or_past import is_future
    from homeworks.hw14.regex.check_password import check_password
    from homeworks.hw14.regex.correct_duplicates import fix_duplicates
    from homeworks.hw14.regex.find_dates_file import find_dates_in_file
    from homeworks.hw14.parse_file.from_xml import calculate_total_cost
    from homeworks.hw14.parse_file.from_json import get_club_with_most_wins
    from homeworks.hw14.parse_file.from_yaml import add_book, save_books, read_books
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw14", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("date1,date2,expected", [
    ("2024-02-21", "2024-02-21", 0),
    ("2024-02-20", "2024-02-21", 1),
    ("2000-01-01", "2024-02-21", 8817),
    ("2024-02-21", "2024-02-20", 1),
    ("2024-02-21", "2024-02-20", 1),
])
def test_days_between(date1, date2, expected):
    assert calculate_days_between(date1, date2) == expected, f"Expected {expected} days, between {date1} and {date2}"


@pytest.mark.parametrize("date1,date2,expected", [
    ("21-02-2024", "2024-02-21", "Wrong datetime format or incorrect date"),
    ("2024-02-21", "21-02-2024", "Wrong datetime format or incorrect date"),
    ("2024-02-30", "2024-02-21", "Wrong datetime format or incorrect date"),
])
def test_days_between_negative(date1, date2, expected):
    assert calculate_days_between(date1, date2) == expected, f"Expected {expected} error"


@pytest.mark.parametrize("date1,expected", [
    ("2030-01-01", True),
    ("2025-01-01", False),
    # ("2025-02-23", None), before run tests -> change to current date
])
def test_is_future(date1, expected):
    assert is_future(date1) == expected, f"Expected {date1} day in future={expected}"


@pytest.mark.parametrize("date1,expected", [
    ("2024-02-30", "Wrong datetime format or incorrect date"),
    ("21-02-2024", "Wrong datetime format or incorrect date"),
])
def test_is_future_negative(date1, expected):
    assert is_future(date1) == expected, f"Expected {expected} error"


@pytest.mark.parametrize("password,expected", [
    ("StrongPass1", True),
    ("Short1", False),
    ("weakpassword1", False),
    ("WEAKPASSWORD1", False),
    ("NoDigitsHere", False),
    ("", False),
])
def test_check_password(password, expected):
    assert check_password(password) == expected, f"Expected {expected} for password {password}"


@pytest.mark.parametrize("sentence,expected", [
    ("Test automation automation in Python is funny", "Test automation in Python is funny"),
    ("London is a a capital of of GB GB", "London is a capital of GB"),
])
def test_fix_duplicates(sentence, expected):
    assert fix_duplicates(sentence) == expected, f"Expected '{expected}' after fixing duplications"


def test_find_dates_in_file_with_mock_data(mocker):
    mock_data = mocker.mock_open(read_data="Test data in file\n01.01.2025")
    mocker.patch("builtins.open", mock_data)
    assert find_dates_in_file("example.txt"), "Expected to read date in files"


def test_find_dates_in_file_with_mock_data_negative(mocker):
    mock_data = mocker.mock_open(read_data="Test data in file\nTest automation")
    mocker.patch("builtins.open", mock_data)
    assert not find_dates_in_file("example.txt"), "Expected to read date in files"


@pytest.mark.parametrize("xml_content,expected", [
    ("""<items>
        <item>
            <name>Product1</name>
            <price>10.5</price>
            <quantity>2</quantity>
        </item>
        <item>
            <name>Product2</name>
            <price>5.0</price>
            <quantity>4</quantity>
        </item>
    </items>""", 41.0),
    ("""<items>
        <item>
            <name>Laptop</name>
            <price>1000</price>
            <quantity>2</quantity>
        </item>
        <item>
            <name>Mouse</name>
            <price>50</price>
            <quantity>5</quantity>
        </item>
        <item>
            <name>Keyboard</name>
            <price>80</price>
            <quantity>3</quantity>
        </item>
    </items>""", 2490.0),
])
def test_calculate_total_cost(xml_content, expected, mocker):
    mock_data = mocker.mock_open(read_data=xml_content)
    mocker.patch("builtins.open", mock_data)
    assert calculate_total_cost("test.xml") == expected, f"Expected {expected} in total from XML file"


@pytest.mark.parametrize("json_content,expected", [
    ("""[
         {"name": "Real Madrid", "country": "Spain", "wins": 95},
         {"name": "Manchester United", "country": "England", "wins": 85},
         {"name": "Bayern Munich", "country": "Germany", "wins": 90}
     ]""", [{"name": "Real Madrid", "country": "Spain", "wins": 95}]),
    ("""[
         {"name": "Real Madrid", "country": "Spain", "wins": 85},
         {"name": "Manchester United", "country": "England", "wins": 85},
         {"name": "Bayern Munich", "country": "Germany", "wins": 60}
     ]""", [{"name": "Real Madrid", "country": "Spain", "wins": 85},
            {"name": "Manchester United", "country": "England", "wins": 85}]),
])
def test_get_club_with_most_wins(json_content, expected, mocker):
    mock_data = mocker.mock_open(read_data=json_content)
    mocker.patch("builtins.open", mock_data)
    assert get_club_with_most_wins("clubs.json") == expected, f"Expected to find {expected} in the JSON file"


@pytest.mark.parametrize("yaml_content,expected", [
    ("""books:
        - author: Yukihiro Matsumoto
          title: Ruby in a Nutshell
          year: 1998
        - author: Zed A. Shaw
          title: Learn Ruby The Hard Way
          year: 1932""",
     [{'author': 'Yukihiro Matsumoto', 'title': 'Ruby in a Nutshell', 'year': 1998},
      {'author': 'Zed A. Shaw', 'title': 'Learn Ruby The Hard Way', 'year': 1932}]),
])
def test_get_books(yaml_content, expected, mocker):
    filename = "books.yaml"
    mock_data = mocker.mock_open(read_data=yaml_content)
    mocker.patch("builtins.open", mock_data)
    assert read_books(filename) == expected, f"Expected to find {expected} in the YAML file"


@pytest.mark.parametrize("title,author,year,content1,content2,expected", [
    ("Fluent Python", "Luciano Ramalho", 2015,
     """{'books': [{'author': 'Yukihiro Matsumoto', 'title': 'Ruby in a Nutshell', 'year': 1998},
               {'author': 'Zed A. Shaw', 'title': 'Learn Ruby The Hard Way', 'year': 1932}]}""",
     """{'books': [{'author': 'Yukihiro Matsumoto', 'title': 'Ruby in a Nutshell', 'year': 1998},
               {'author': 'Zed A. Shaw', 'title': 'Learn Ruby The Hard Way', 'year': 1932},
               {'author': 'Luciano Ramalho', 'title': 'Fluent Python', 'year': 2015}]}""",
     [{'author': 'Yukihiro Matsumoto', 'title': 'Ruby in a Nutshell', 'year': 1998},
      {'author': 'Zed A. Shaw', 'title': 'Learn Ruby The Hard Way', 'year': 1932},
      {'author': 'Luciano Ramalho', 'title': 'Fluent Python', 'year': 2015}]
     ),
])
def test_add_new_book(title, author, year, content1, content2, expected, mocker):
    filename = "books.yaml"
    mock_data = mocker.mock_open(read_data=content1)
    mocker.patch("builtins.open", mock_data)
    add_book(title, author, year, filename)
    mock_data = mocker.mock_open(read_data=content2)
    mocker.patch("builtins.open", mock_data)
    assert read_books(filename) == expected, f"Expected to find {expected} in the YAML file"
