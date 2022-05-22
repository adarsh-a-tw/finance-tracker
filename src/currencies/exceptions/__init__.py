class InvalidComparisonException(Exception):
    def __init__(self):
        super().__init__(
            "Cannot compare two different currencies due to fluctuating rates.")


class CoinbaseAPIException(Exception):
    def __init__(self):
        super().__init__("Coinbase API seems to be down.")
