import time
import ccxt

from Trader.trader import Trader
from Trader.Periphery.cex import Cex
from Trader.Periphery.graphs import Graphs


if __name__ == "__main__":
    chainId = 42161
    start = time.time()
    g = Graphs()
    c = Cex(ccxt.coinbaseadvanced())
    df = c.get_OHLCV("BTC", check_expiration=True)
    # g.plot_graph(df)
    end = time.time()
    elapse = end - start
    elapse = "{:.2f}".format(elapse)
    print(f"Elapse: {elapse} seconds")


"""
0.02 seconds without expiration check, and without plotting. 
1.97 seconds *with* expiration chekc, and without plotting. 
"""
