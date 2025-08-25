import pytest
from conftest import config

try:
    from homeworks.hw11.bank_deposit.bank import Bank
    from homeworks.hw11.bank_deposit.currency import CurrencyConverter
    from homeworks.hw12.card_desk.cards_deck import CardsDeck
except ImportError:
    pytest.skip("Module(s) does not exist or have incorrect path", allow_module_level=True)

pytestmark = pytest.mark.skipif(not config.get("hw12", False), reason="HW disabled in the config file!")


@pytest.mark.parametrize("from_curr,to_curr,amount,expected", [
    ("USD", "BYN", 1000, (3267.7, "BYN")),
    ("EUR", "BYN", 1000, (3399, "BYN")),
    ("BYN", "USD", 1000, (306.3, "USD")),
    ("BYN", "EUR", 1000, (294.2, "USD")),
    ("USD", "EUR", 1000, (951.8, "EUR")),
    ("EUR", "USD", 1000, (1050.6, "USD")),
])
def test_bank_currency_converter(from_curr, to_curr, amount, expected, mocker):
    cc = CurrencyConverter()
    mocker.patch.object(cc, "convert", return_value=expected)
    assert cc.convert(from_curr=from_curr, amount=amount, to_curr=to_curr) == expected, \
        f"Expected to get {expected} from {amount}{from_curr}"


@pytest.mark.parametrize("from_curr,to_curr,amount,expected", [
    ("USD", "BYYN", 1000, "Unsupported currency: {curr}"),
    ("BYN", "USDD", 1000, "Unsupported currency: {curr}"),
    ("BYN", "EEUR", 1000, "Unsupported currency: {curr}"),
])
def test_bank_currency_converter_incorrect_to_currency(from_curr, to_curr, amount, expected):
    bank = Bank()
    with pytest.raises(ValueError) as excinfo:
        assert bank.exchange_currency(from_curr=from_curr, amount=amount, to_curr=to_curr)
    assert str(excinfo.value) == expected.format(curr=to_curr), \
        f"Expected to get an error {expected.format(curr=from_curr)}"


@pytest.mark.parametrize("from_curr,to_curr,amount,expected", [
    ("BYNN", "USD", 1000, "Unsupported currency: {curr}"),
    ("USSD", "BYN", 1000, "Unsupported currency: {curr}"),
    ("EEUR", "BYN", 1000, "Unsupported currency: {curr}"),
])
def test_bank_currency_converter_incorrect_from_currency(from_curr, to_curr, amount, expected):
    bank = Bank()
    with pytest.raises(ValueError) as excinfo:
        assert bank.exchange_currency(from_curr=from_curr, amount=amount, to_curr=to_curr)
    assert str(excinfo.value) == expected.format(curr=from_curr), \
        f"Expected to get an error {expected.format(curr=from_curr)}"


def test_initialize_card_deck(expected=54):
    deck = CardsDeck()
    deck.shuffle()
    assert len(deck.get_remaining_cards()) == expected, \
        f"Expected to have {expected} cards in deck"


@pytest.mark.parametrize("card_number,expected", [
    (1, 51),
    (5, 51),
    (51, 51),
])
def test_get_cards_from_card_deck(card_number, expected):
    deck = CardsDeck()
    deck.shuffle()
    deck.get_card(card_number)
    deck.get_card(card_number)
    deck.get_card(card_number)
    assert len(deck.get_remaining_cards()) == expected, \
        f"Expected to have {expected} cards in deck"


@pytest.mark.parametrize("card_number,expected1,expected2", [
    (2, 54, 53),
    (10, 54, 53),
    (51, 54, 53),
])
def test_shuffle_card_deck(card_number, expected1, expected2):
    deck = CardsDeck()
    deck.shuffle()
    assert len(deck.get_remaining_cards()) == expected1, \
        f"Expected to have {expected1} cards in deck"
    deck.get_card(card_number)
    deck.shuffle()
    assert len(deck.get_remaining_cards()) == expected2, \
        f"Expected to have {expected2} cards in deck"


@pytest.mark.parametrize("card_number,expected", [
    (12, 12),
    (25, 25),
    (53, 53),
])
def test_validate_card(card_number, expected):
    deck = CardsDeck()
    assert deck._card_validator(card_number) == expected, f"Expected, {expected} card is valid"


@pytest.mark.parametrize("card_number", [
    55,
    100,
    "Test",
    "12",
])
def test_validate_card_negative(card_number):
    deck = CardsDeck()
    with pytest.raises(ValueError) as excinfo:
        assert deck._card_validator(card_number)
    assert str(excinfo.value) == "Error: enter a card number from 1 to 54"
