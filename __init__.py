import time
import ccxt
import pandas as pd

from Trader.trader import Trader
from Trader.Periphery.Utils.dates import Dates
from Trader.Periphery.Exchanges.cex import Cex

from Trader.Periphery.Exchanges.dex import Dex
from Trader.Periphery.Graphs.graphs import Graphs
from Trader.Periphery.token import Token


from TradingEnvironment.trading_environment import TradingEnvironment


# def on_trading_iteration():
#     chain_id = 42161
#     ticker = "BTC"
#     d = Dates()
#     cex = Cex(ccxt.coinbaseadvanced())
#     trader = Trader(chain_id)
#     running = True
#     while running:

#         candles = cex.get_OHLCV(ticker)
#         w = 10
#         close = trader.trailing_values(candles["close"], window=w)
#         macd = trader.trailing_values(candles["macd"], window=w)
#         signal = trader.trailing_values(candles["signal"], window=w)

#         print(
#             f"""
#          Close: {close}
#          Macd: {macd}
#          Signal: {signal}
#           """
#         )

#         d.wait_until_next_minute()


if __name__ == "__main__":
    chain_id = 42161
    start = time.time()

    baseToken = Token("ARB", chain_id)
    quoteToken = Token("USDC", chain_id)
    dex = Dex("uniswap", "V3", chain_id)

    trading_env = TradingEnvironment(baseToken, quoteToken, dex, chain_id)
    trading_env.start_trading()

    end = time.time()
    elapse = end - start
    elapse = "{:.2f}".format(elapse)
    print(f"Elapse: {elapse} seconds")


"""
0.02 seconds without expiration check, and without plotting. 
1.97 seconds *with* expiration chekc, and without plotting. 
"""
