import pandas as pd


from Trader.Periphery.constants import BASE_DATA_PATH


class Token:
    def __init__(self, symbol: str, chainId: int) -> None:

        self.token_data = TokenData()
        self.chainId = chainId
        self.address = self.token_data.get_token_address(symbol, chainId)
        self.decimals = self.token_data.get_token_decimals(symbol)


class TokenData:
    def __init__(self) -> None:

        self.tokens_path = f"{BASE_DATA_PATH}\\Tokens\\tokens.json"

    """---------------------------------"""

    def get_token_address(self, ticker: str, chainId: str):
        if type(chainId) != type(str):
            chainId = str(chainId)
        df = pd.read_json(self.tokens_path)
        token_address = df[ticker]["address"][chainId]
        return token_address

    """---------------------------------"""

    def get_token_decimals(self, ticker: str):
        df = pd.read_json(self.tokens_path)
        token_decimal = df[ticker]["decimals"]
        return token_decimal

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""
