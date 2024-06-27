import ccxt
from Trader.Periphery.Constants.edge_cases import cex_edge_cases
from Trader.Periphery.Exchanges.dex import Dex
from Trader.Periphery.Exchanges.cex import Cex
from Trader.Periphery.Utils.dates import Dates

import pandas as pd
import datetime as dt


class TradingEnvironment:
    def __init__(self, base_token, quote_token, dex: Dex, chain_id: int) -> None:
        self.base_token = base_token
        self.quote_token = quote_token
        self.base_symbol = base_token.symbol
        self.quote_symbol = quote_token.symbol
        self.dex = dex
        self.cex = Cex(ccxt.coinbaseadvanced())
        self.chain_id = chain_id
        self.dates = Dates()

    def start_trading(self):

        running = True
        # self.dates.wait_until_next_minute()
        while running:
            self.on_trading_iteration()
            self.dates.wait_until_next_minute()

    def on_trading_iteration(self):
        self.get_candles()

    def get_candles(self):
        base_path = f"Trader\\Periphery\\Candles\\DexMemory\\{self.base_symbol}/{self.quote_symbol}.csv"
        quote_path = f"Trader\\Periphery\\Candles\\DexMemory\\{self.quote_symbol}/{self.base_symbol}.csv"

        base_price = self.dex.get_price(self.base_token, self.quote_token)
        alt_price = self.dex.get_price(self.quote_token, self.base_token)

        try:
            current_timestamp = dt.datetime.now(tz=dt.tzinfo.utcoffset)
            current_timestamp = current_timestamp.tz_convert("America/Los_Angeles")

            base_file = pd.read_csv(base_path)
            quote_file = pd.read_csv(quote_path)

        except FileNotFoundError:
            if self.base_symbol in cex_edge_cases:
                _base_symbol = cex_edge_cases[self.base_symbol]
            else:
                _base_symbol = self.base_symbol
            print(f"Base Symbol: {_base_symbol}")
            base_candles = self.cex.get_OHLCV(_base_symbol)
            base_candles = base_candles[["close"]]
            print(f"Base: {base_candles}")

            quote_candles = base_candles
            print(f"Quote1: {quote_candles}")
            quote_candles["close"] = 1 / quote_candles["close"]
            print(f"Quote: {quote_candles}")
            exit()
            base_candles.to_csv(base_path)
            quote_candles.to_csv(quote_path)
