import ccxt
import pandas as pd
import pytz
import datetime as dt

import Trader.Periphery.Utils.dates

import Trader.Periphery.ta

import Trader.Periphery.Constants.enums


class Cex:
    def __init__(self, exchange: ccxt, timezone: str = "PST") -> None:
        self.exchange = exchange
        self.timezone = timezone
        self.candles_path = "Trader\\Periphery\\Candles"
        self.dates = Trader.Periphery.Utils.dates.Dates()
        self.ta = Trader.Periphery.ta.TechnicalAnalysis()

    """---------------------------------"""

    def get_OHLCV(
        self,
        ticker: str,
        market: str = "USD",
        time_interval: int = 1,
        time_unit: str = "m",
        check_expiration: bool = True,
        apply_indicators: bool = True,
    ):
        symbol = f"{ticker.upper()}/{market.upper()}"
        path = f"{self.candles_path}\\{ticker.upper()}.csv"
        try:
            df = pd.read_csv(path).set_index("timestamp")

            if check_expiration:

                # state = self._get_candle_state()

                if self.dates.outdated(df.index[-1], 1, time_unit):
                    # Convert index to datetime so they can be compared with the datetimes of the external data.
                    df.index = pd.to_datetime(df.index)
                    new_df = self._fetch_externally(symbol, time_interval, time_unit)
                    merged_df = pd.concat([df, new_df])
                    merged_df = merged_df.loc[~merged_df.index.duplicated(keep="first")]
                    merged_df.to_csv(path)

                    if apply_indicators:
                        merged_df = self.ta.apply_indicators(merged_df)
                    return merged_df

                else:
                    df.index = pd.to_datetime(df.index)
                    if apply_indicators:
                        df = self.ta.apply_indicators(df)
                    return df
            else:
                df.index = pd.to_datetime(df.index)
                if apply_indicators:
                    df = self.ta.apply_indicators(df)
                return df

        except FileNotFoundError:
            df = self._fetch_externally(symbol, time_interval, time_unit)
            df.to_csv(path)
            if apply_indicators:
                df = self.ta.apply_indicators(df)
            return df

    """---------------------------------"""

    def _fetch_externally(
        self, symbol: str, time_interval: int, time_unit: str
    ) -> pd.DataFrame:
        timeframe = self.create_timeframe(time_interval, time_unit)
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe)

        # Convert the data to a DataFrame for easier manipulation
        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        # Convert timestamp to datetime
        # By default datetime's are in UTC.
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        # Logic to convert from UTC to local timezone, if user specified one in class initialization.
        if self.timezone == "PST":
            pst = pytz.timezone("America/Los_Angeles")
            df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert(pst)
        elif self.timezone == "EST":
            est = pytz.timezone("America/New_York")
            df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert(est)

        df = df.set_index("timestamp")
        return df

    """---------------------------------"""

    def _get_candle_state(
        self, df: pd.DataFrame, interval: int, unit: str, MAX_EXPIRATION: int = 300
    ):

        timestamp = df.index[-1]

        if type(timestamp) == str:
            timestamp = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S%z")

        curr_diff = self._get_current_time_difference(timestamp)

        curr_diff = self.dates.convert_delta(curr_diff, "h")

        print(f"Curr: {curr_diff}    {type(curr_diff)}")
        # timestamp = timestamp.replace(tzinfo=None)
        # delta = self.dates._create_time_delta(interval, unit)
        # timestamp_sum = timestamp + delta
        # current_time = dt.datetime.now()

        # change = current_time - timestamp
        # change = self.dates.convert_to_minutes(change)

        # print(f"CHange: {change}")

    """---------------------------------"""

    def _get_current_time_difference(self, timestamp):
        """
        Compare the current time, with the last recorded candle.
        """
        if type(timestamp) == str:
            timestamp = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S%z")
        current_time = dt.datetime.now()
        try:
            change = current_time - timestamp
        except TypeError:
            timestamp = timestamp.replace(tzinfo=None)
            change = current_time - timestamp
        return change

    """---------------------------------"""

    def create_timeframe(self, time_interval: int, time_unit: str):
        if time_unit in self.dates.minute_params:
            timeframe = f"{time_interval}m"
        elif time_unit in self.dates.hour_params:
            timeframe = f"{time_interval}h"
        elif time_unit in self.dates.day_params:
            timeframe = f"{time_interval}d"
        elif time_unit in self.dates.week_params:
            timeframe = f"{time_interval}w"
        elif time_unit in self.dates.month_params:
            timeframe = f"{time_interval}M"
        return timeframe

    """---------------------------------"""
