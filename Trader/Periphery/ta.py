import pandas as pd


class TechnicalAnalysis:
    def __init__(self) -> None:
        pass

    def apply_indicators(self, df: pd.DataFrame):
        df = self.apply_EMA(df, period=9)
        df = self.apply_EMA(df, period=20)
        df = self.apply_EMA(df, period=200)
        df = self.apply_RSI(df)
        df = self.apply_MACD(df)

        return df

    def apply_RSI(self, df: pd.DataFrame, period: int = 14):
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        df["rsi"] = rsi
        return df

    def apply_MACD(
        self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9
    ):
        short_ema = df["close"].ewm(span=fast, adjust=False).mean()
        long_ema = df["close"].ewm(span=slow, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        historgram = macd_line - signal_line
        df["macd"] = macd_line
        df["signal"] = signal_line
        df["histogram"] = historgram
        return df

    def apply_EMA(self, df: pd.DataFrame, period: int):
        df[f"ema_{period}"] = df["close"].ewm(span=period, adjust=False).mean()
        return df
