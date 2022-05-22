import requests

from currencies.exceptions import CoinbaseAPIException


def fetch_data_from_coinbase(base_currency, to_currency):
    api_url = f"https://api.coinbase.com/v2/exchange-rates?currency={base_currency}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['data']['rates'][to_currency]

    raise CoinbaseAPIException
