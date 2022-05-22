from currencies.domain.currency_type import CurrencyType


def mock_coinbase_api(base_currency, to_currency):
    if base_currency == CurrencyType.DOLLAR and to_currency == CurrencyType.RUPEE:
        return 77
    if base_currency == CurrencyType.RUPEE and to_currency == CurrencyType.DOLLAR:
        return 1 / 77
    raise NotImplementedError
