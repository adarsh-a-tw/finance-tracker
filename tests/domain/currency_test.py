import pytest

from mocks import mock_coinbase_api

from currencies.domain.currency import Currency
from currencies.domain.currency_type import CurrencyType
from currencies.exceptions import InvalidComparisonException


def test_create_five_rupees():
    five_rupees = Currency(5, CurrencyType.RUPEE)

    assert five_rupees is not None


def test_create_ten_dollars():
    ten_dollars = Currency(10, CurrencyType.DOLLAR)

    assert ten_dollars is not None


def test_should_assert_that_ten_rupees_and_another_ten_rupees_are_equal():
    ten_rupees = Currency(10, CurrencyType.RUPEE)
    another_ten_rupees = Currency(10, CurrencyType.RUPEE)

    assert ten_rupees.__eq__(another_ten_rupees)


def test_should_not_compare_different_currencies():
    ten_rupees = Currency(10, CurrencyType.RUPEE)
    ten_dollars = Currency(10, CurrencyType.DOLLAR)

    with pytest.raises(InvalidComparisonException):
        ten_rupees.__eq__(ten_dollars)


def test_should_convert_ten_dollars_to_rupees():
    ten_dollars = Currency(10, CurrencyType.DOLLAR)

    converted_rupees = ten_dollars.convert(CurrencyType.RUPEE, api=mock_coinbase_api)

    seven_hundred_seventy_rupees = Currency(770, CurrencyType.RUPEE)
    assert converted_rupees == seven_hundred_seventy_rupees


def test_add_two_currencies():
    ten_dollars = Currency(10, CurrencyType.DOLLAR)
    two_hundred_thirty_rupees = Currency(230, CurrencyType.RUPEE)

    added_rupees = two_hundred_thirty_rupees.add(ten_dollars, conversion_api=mock_coinbase_api)

    thousand_rupees = Currency(1000, CurrencyType.RUPEE)
    assert added_rupees == thousand_rupees


def test_subtract_two_different_currencies():
    eleven_dollars = Currency(11, CurrencyType.DOLLAR)
    seventy_seven_rupees = Currency(77, CurrencyType.RUPEE)

    deducted_rupees = eleven_dollars.sub(seventy_seven_rupees, conversion_api=mock_coinbase_api)

    ten_dollars = Currency(10, CurrencyType.DOLLAR)
    assert deducted_rupees == ten_dollars
