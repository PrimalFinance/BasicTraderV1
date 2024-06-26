import pandas as pd
import mplfinance as mpf


class Graphs:
    def __init__(self):
        self.colors = ["red", "orange", "yellow", "purple"]

    def plot_graph(
        self,
        df: pd.DataFrame,
        ema: bool = True,
        rsi: bool = True,
        macd: bool = True,
        ma_ranges=[9, 10, 20, 50, 100, 200],
    ):

        # Number of panels
        panel_num = 2
        add_plots = []
        df.index = pd.to_datetime(df.index, utc=True)

        ohlcv = df[["open", "high", "low", "close", "volume"]]

        if rsi:
            rsi_plot = mpf.make_addplot(df["rsi"], panel=panel_num, color="blue")
            panel_num += 1
            add_plots.append(rsi_plot)

        if macd:
            macd_plot = mpf.make_addplot(df["macd"], panel=panel_num, color="purple")
            signal_plot = mpf.make_addplot(
                df["signal"], panel=panel_num, color="orange"
            )
            histogram_plot = mpf.make_addplot(
                df["histogram"],
                type="bar",
                panel=panel_num,
                color=self._get_color_array(df["histogram"]),
                alpha=0.5,
            )
            panel_num += 1
            add_plots.append(macd_plot)
            add_plots.append(signal_plot)
            add_plots.append(histogram_plot)

        # if sma:
        #     index = 0
        #     for i in self.ma_ranges:
        #         column = f"sma_{i}"
        #         sma = df[column]
        #         p = mpf.make_addplot(sma, panel=0, color=self.colors[index])
        #         add_plots.append(p)
        #         index += 1

        if ema:
            index = 0
            for i in ma_ranges:
                column = f"ema_{i}"
                try:
                    ema = df[column]
                    p = mpf.make_addplot(ema, panel=0, color=self.colors[index])
                    add_plots.append(p)
                    index += 1
                except KeyError:
                    pass

        # ohlc.set
        mpf.plot(
            ohlcv,
            type="candle",
            style="yahoo",
            title="OHLC with Indicators",
            ylabel="Price",
            addplot=add_plots,
            volume=True,
        )

    def _get_color_array(self, df: pd.Series):
        colors = ["green" if value >= 0 else "red" for value in df]
        return colors
