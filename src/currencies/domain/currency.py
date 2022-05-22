from dataclasses import dataclass

from currencies.domain.currency_type import CurrencyType
from currencies.exceptions import InvalidComparisonException
from currencies.services.coinbase_service import fetch_data_from_coinbase


@dataclass
class Currency:
    value: float
    type: CurrencyType

    def __init__(self, value: float, currency_type: CurrencyType):
        self.value = value
        self.type = currency_type

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.type != other.type:
                raise InvalidComparisonException
            return self.value == other.value
        return False

    def convert(self, to_currency_type, api=fetch_data_from_coinbase):
        if to_currency_type == self.type:
            return self
        rate = api(self.type, to_currency_type)
        return Currency(rate * self.value, to_currency_type)

    def add(self, currency, conversion_api=fetch_data_from_coinbase):
        converted_currency = currency.convert(self.type, api=conversion_api)
        return Currency(converted_currency.value + self.value, self.type)

    def sub(self, currency, conversion_api=fetch_data_from_coinbase):
        converted_currency = currency.convert(self.type, api=conversion_api)
        return Currency(self.value - converted_currency.value, self.type)
