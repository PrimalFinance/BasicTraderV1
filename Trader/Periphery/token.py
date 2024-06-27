import pandas as pd


from Trader.Periphery.Constants.constants import BASE_DATA_PATH


class Token:
    def __init__(self, symbol: str, chain_id: int) -> None:

        self.token_data = TokenData()
        self.symbol = symbol.upper()
        self.chain_id = chain_id
        self.address = self.token_data.get_token_address(self.symbol, chain_id)
        self.decimals = self.token_data.get_token_decimals(self.symbol)

    def __str__(self) -> str:
        return f"""Symbol: {self.symbol}\nAddress: {self.address}\nDecimals: {self.decimals}"""


class TokenData:
    def __init__(self) -> None:

        self.tokens_path = f"{BASE_DATA_PATH}\\Tokens\\tokens.json"

    """---------------------------------"""

    def get_token_address(self, ticker: str, chain_id: str):
        if type(chain_id) != type(str):
            chain_id = str(chain_id)
        df = pd.read_json(self.tokens_path)
        token_address = df[ticker]["address"][chain_id]
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
