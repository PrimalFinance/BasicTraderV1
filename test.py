import time
import ccxt
import pandas as pd

import argparse

from Trader.trader import Trader
from Trader.Periphery.Exchanges.cex import Cex
from Trader.Periphery.Exchanges.dex import Dex
from Trader.Periphery.token import Token
from Trader.Periphery.Graphs.graphs import Graphs


def visualize_data():
    g = Graphs()
    c = Cex(ccxt.coinbaseadvanced())
    df = pd.read_csv("Trader\\Periphery\\Candles\\BTC.csv")
    df.set_index("timestamp", inplace=True)
    c._get_candle_state(df, 1, "m")
    df = c.get_OHLCV("BTC", check_expiration=True)
    g.plot_graph(df)


def test_trailing_values():
    chain_id = 42161
    t = Trader(chain_id)
    c = Cex(ccxt.coinbaseadvanced())
    df = c.get_OHLCV("BTC", check_expiration=True)

    w = 10
    close = t.trailing_values(df["close"], window=w)
    macd = t.trailing_values(df["macd"], window=w)
    signal = t.trailing_values(df["signal"], window=w)

    print(
        f"""
         Close: {close}
         Macd: {macd}
         Signal: {signal}  
          """
    )


def test_dex_pricing():
    chain_id = 42161
    baseToken = Token("WETH", chain_id)
    quoteToken = Token("USDC", chain_id)
    dex = Dex("uniswap", "V3", chain_id)

    price = dex.get_price(baseToken, quoteToken)
    print(f"Price: {price}")


if __name__ == "__main__":
    valid_args = ["visualize", "trailing", "dex_pricing"]
    start = time.time()
    parser = argparse.ArgumentParser(description="Inputs")
    parser.add_argument("function", type=str, help="Function to execute ['visualize']")
    market = "USD"
    args = parser.parse_args()
    arg = args.function
    if arg in valid_args:
        if arg == "visualize":
            visualize_data()
        elif arg == "trailing":
            test_trailing_values()
        elif arg == "dex_pricing":
            test_dex_pricing()

    end = time.time()
    elapse = end - start
    elapse = "{:.2f}".format(elapse)
    print(f"Elapse: {elapse} seconds")
