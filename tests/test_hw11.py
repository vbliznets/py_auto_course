import pytest
from conftest import config

try:
    from homeworks.hw11.bank_deposit.bank import Bank
    from homeworks.hw11.library.book import Book
    from homeworks.hw11.library.reader import Reader
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw11", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("client_id,name,balance,year,expected", [
    ("001", "James Bond", 1000, 1, 1104.71),
    ("002", "Guy Ritchie", 10000, 5, 16453.09),
    ("003", "J. R. R. Tolkien", 100000, 10, 270704.15),
])
def test_user_can_open_bank_deposit(client_id, name, balance, year, expected):
    bank = Bank()
    assert bank.register_client(client_id=client_id, name=name), "Expected new customer can open bank account"
    assert bank.open_deposit_account(client_id=client_id, start_balance=balance, years=year), \
        "Expected that customer can open a deposit in bank "
    assert bank.calc_interest_rate(client_id=client_id) == expected, \
        f"Expected to have '{expected}' after {year} year"
    assert bank.close_deposit(client_id=client_id) == expected, "Expected that existing customer can close deposit"


@pytest.mark.parametrize("client_id,name,expected", [
    ("007", "James Bond", False),
])
def test_user_cannot_open_2_bank_deposits(client_id, name, expected):
    bank = Bank()
    assert bank.register_client(client_id=client_id, name=name), "Expected new customer can open bank account"
    assert bank.register_client(client_id=client_id, name=name) == expected, \
        "Expected that same customer can not register twice in the same bank"


@pytest.mark.parametrize("client_id,balance,year,expected", [
    ("001", 1000, 1, False),
    ("002", 100, 2, False),
    ("003", 100, 5, False),
])
def test_unregister_user_cannot_open_deposits(client_id, balance, year, expected):
    bank = Bank()
    assert bank.open_deposit_account(client_id=client_id, start_balance=balance, years=year) == expected, \
        "Expected new customer can open bank account"


@pytest.mark.parametrize("client_id,expected", [
    ("007", False),
])
def test_unregister_user_cannot_calc_interest_rate(client_id, expected):
    bank = Bank()
    assert bank.calc_interest_rate(client_id=client_id) == expected, \
        "Expected unregister user cannot calculate interest rate"


@pytest.mark.parametrize("client_id,name,expected", [
    ("007", "James Bond", False),
])
def test_user_without_deposit_cannot_calc_interest_rate(client_id, name, expected):
    bank = Bank()
    assert bank.register_client(client_id=client_id, name=name), "Expected new customer can open bank account"
    assert bank.calc_interest_rate(client_id=client_id) == expected, \
        "Expected unregister user cannot calculate interest rate"


@pytest.mark.parametrize("client_id,expected", [
    ("007", False),
])
def test_unknown_user_cannot_close_deposit(client_id, expected):
    bank = Bank()
    assert bank.close_deposit(client_id=client_id) == expected, \
        "Expected that unknown user can not close a deposit account"


@pytest.mark.parametrize("client_id,name,expected", [
    ("007", "James Bond", False),
])
def test_user_without_deposit_cannot_close_it(client_id, name, expected):
    bank = Bank()
    assert bank.register_client(client_id=client_id, name=name), "Expected new customer can open bank account"
    assert bank.close_deposit(client_id=client_id) == expected, \
        "Expected that unknown user can not close a deposit account"


@pytest.mark.parametrize("book_name,author,num_pages,isbn,reader_name,expected", [
    ("The Hobbit", "J. R. R. Tolkien", 310, "0345339681", "James Bond", True),
])
def test_user_use_library(book_name, author, num_pages, isbn, reader_name, expected):
    book = Book(book_name, author, num_pages, isbn)
    james_bond = Reader(reader_name)
    assert james_bond.reserve_book(book) == expected, "New reader can reserve free book"
    assert james_bond.cancel_reserve(book) == expected, "Reader can cancel existing reservation"
    assert james_bond.get_book(book) == expected, "Reader can get book, if he reserve it"
    assert james_bond.return_book(book) == expected, "Reader can return a book"


@pytest.mark.parametrize("book_name,author,num_pages,isbn,reader_name1,reader_name2,expected", [
    ("The Hobbit", "J. R. R. Tolkien", 310, "0345339681", "James Bond", "Guy Ritchie", False),
])
def test_user_cannot_reserve_already_reserved_book(book_name, author, num_pages, isbn, reader_name1, reader_name2,
                                                   expected):
    book = Book(book_name, author, num_pages, isbn)
    james_bond = Reader(reader_name1)
    guy_ritchie = Reader(reader_name2)
    assert james_bond.reserve_book(book), "New reader can reserve free book"
    assert guy_ritchie.reserve_book(book) == expected, "Same user can not reserve a book twice"


@pytest.mark.parametrize("book_name,author,num_pages,isbn,reader_name1,reader_name2,expected", [
    ("The Hobbit", "J. R. R. Tolkien", 310, "0345339681", "James Bond", "Guy Ritchie", False),
])
def test_user_cannot_cancel_someone_else_reservation(book_name, author, num_pages, isbn, reader_name1, reader_name2,
                                                     expected):
    book = Book(book_name, author, num_pages, isbn)
    james_bond = Reader(reader_name1)
    guy_ritchie = Reader(reader_name2)
    assert james_bond.reserve_book(book), "New reader can reserve free book"
    assert guy_ritchie.cancel_reserve(book) == expected, "Same user can not reserve a book twice"


@pytest.mark.parametrize("book_name,author,num_pages,isbn,reader_name1,reader_name2,expected", [
    ("The Hobbit", "J. R. R. Tolkien", 310, "0345339681", "James Bond", "Guy Ritchie", False),
])
def test_user_cannot_get_someone_else_book(book_name, author, num_pages, isbn, reader_name1, reader_name2,
                                           expected):
    book = Book(book_name, author, num_pages, isbn)
    james_bond = Reader(reader_name1)
    guy_ritchie = Reader(reader_name2)
    assert james_bond.reserve_book(book), "New reader can reserve free book"
    assert guy_ritchie.get_book(book) == expected, "Another user can not get a book if someone else reserved it"


@pytest.mark.parametrize("book_name,author,num_pages,isbn,reader_name1,reader_name2,expected", [
    ("The Hobbit", "J. R. R. Tolkien", 310, "0345339681", "James Bond", "Guy Ritchie", False),
])
def test_user_cannot_return_someone_else_book(book_name, author, num_pages, isbn, reader_name1, reader_name2,
                                              expected):
    book = Book(book_name, author, num_pages, isbn)
    james_bond = Reader(reader_name1)
    guy_ritchie = Reader(reader_name2)
    assert james_bond.reserve_book(book), "New reader can reserve free book"
    assert james_bond.get_book(book), "Reader can get book, if he reserve it"
    assert guy_ritchie.return_book(book) == expected, "Another user can not get a book if someone else reserved it"


@pytest.mark.parametrize("book_name,author,num_pages,isbn,reader_name1,reader_name2,expected", [
    ("The Hobbit", "J. R. R. Tolkien", 310, "0345339681", "James Bond", "Guy Ritchie", True),
])
def test_multiple_users_uses_book(book_name, author, num_pages, isbn, reader_name1, reader_name2,
                                  expected):
    book = Book(book_name, author, num_pages, isbn)
    james_bond = Reader(reader_name1)
    guy_ritchie = Reader(reader_name2)
    assert james_bond.reserve_book(book) == expected, "New reader can reserve free book"
    assert james_bond.cancel_reserve(book) == expected, "New reader can reserve free book"
    assert guy_ritchie.reserve_book(book) == expected, "New reader can reserve free book"
    assert guy_ritchie.get_book(book) == expected, "Reader can get book, if he reserve it"
    assert guy_ritchie.return_book(book) == expected, "Reader can get book, if he reserve it"
    assert james_bond.reserve_book(book) == expected, "Another user can not get a book if someone else reserved it"
    assert james_bond.get_book(book) == expected, "Reader can get book, if he reserve it"
    assert james_bond.return_book(book) == expected, "Reader can get book, if he reserve it"
