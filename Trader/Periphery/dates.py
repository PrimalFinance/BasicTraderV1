import time
import datetime as dt
from dateutil.relativedelta import relativedelta


class Dates:
    def __init__(self) -> None:

        self.minute_params = [
            "Minutes",
            "minutes",
            "Minute",
            "minute",
            "Min",
            "min",
            "Mi",
            "mi",
            "m",
        ]
        self.hour_params = ["Hour", "hour", "Hour", "hour", "H", "h"]
        self.day_params = ["Days", "days", "Day", "day", "D", "d"]
        self.week_params = ["Weeks", "weeks", "Week", "week", "W", "w"]
        self.month_params = ["Months", "months", "Month", "month", "Mo", "mo"]

    """---------------------------------"""

    def outdated(
        self, timestamp, expiration_interval: int = 1, expiration_unit: str = "m"
    ) -> bool:
        """
        Determine if a given timestamp is outdated based on the specified expiration interval and unit.

        Args:
            timestamp (datetime): The timestamp to check.
            expiration_interval (int, optional): The interval for expiration. Default is 1.
            expiration_unit (str, optional): The unit of time for the expiration interval.
                                            Valid units are 's' (seconds), 'm' (minutes),
                                            'h' (hours), and 'd' (days). Default is 'm'.

        Returns:
            bool: True if the timestamp is outdated, False otherwise.
        """
        if type(timestamp) == str:
            timestamp = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S%z")

        timestamp = timestamp.replace(tzinfo=None)
        delta = self._create_time_delta(expiration_interval, expiration_unit)
        timestamp_sum = timestamp + delta
        current_time = dt.datetime.now()
        if current_time > timestamp_sum:
            return True
        else:
            return False

    """---------------------------------"""

    def _create_time_delta(self, interval: int, unit: str):
        """
        Create a delta to allow further calculations with a datetime object.

        Args:
            interval (int): The interval for the delta. Default is 1.
            unit (str): The unit of time for the interval.
                                            Valid units are 's' (seconds), 'm' (minutes),
                                            'h' (hours), and 'd' (days). Default is 'm'.

        Returns:
            bool: True if the timestamp is outdated, False otherwise.
        """
        if unit in self.minute_params:
            delta = dt.timedelta(minutes=interval)
        elif unit in self.hour_params:
            delta = dt.timedelta(hours=interval)
        elif unit in self.day_params:
            delta = dt.timedelta(days=interval)
        elif unit in self.week_params:
            delta = dt.timedelta(weeks=interval)
        elif unit in self.month_params:
            delta = dt.timedelta(days=(interval * 30))
        return delta

    """---------------------------------"""

    def add(self, base_datetime, value, timeunit: str):
        if timeunit == "S":
            d = self.add_seconds(base_datetime, value)
        elif timeunit == "M":
            d = self.add_minutes(base_datetime, value)
        elif timeunit == "H":
            d = self.add_hours(base_datetime, value)
        elif timeunit == "D":
            d = self.add_days(base_datetime, value)
        return d

    def subtract(self, base_datetime, value, timeunit: str):
        if timeunit == "S":
            d = self.sub_seconds(base_datetime, value)
        elif timeunit == "M":
            d = self.sub_minutes(base_datetime, value)
        elif timeunit == "H":
            d = self.sub_hours(base_datetime, value)
        elif timeunit == "D":
            d = self.sub_days(base_datetime, value)
        return d

    def add_years(self, base_datetime, years: int = 5):
        new_datetime = base_datetime + relativedelta(years=years)
        return new_datetime

    def sub_years(self, base_datetime, years: int = 5):
        new_datetime = base_datetime - relativedelta(years=years)
        return new_datetime

    def add_days(self, base_datetime, days: int = 5):
        new_datetime = base_datetime + dt.timedelta(days=days)
        return new_datetime

    def sub_days(self, base_datetime, days: int = 5):
        new_datetime = base_datetime - dt.timedelta(days=days)
        return new_datetime

    def add_hours(self, base_datetime, hours: int = 5):
        new_datetime = base_datetime + dt.timedelta(hours=hours)
        return new_datetime

    def sub_hours(self, base_datetime, hours: int = 5):
        new_datetime = base_datetime - dt.timedelta(hours=hours)
        return new_datetime

    def add_minutes(self, base_datetime, minutes: int = 5):
        new_datetime = base_datetime + dt.timedelta(minutes=minutes)
        return new_datetime

    def sub_minutes(self, base_datetime, minutes: int = 5):
        new_datetime = base_datetime - dt.timedelta(minutes=minutes)
        return new_datetime

    def add_seconds(self, base_datetime, seconds: int = 5):
        new_datetime = base_datetime + dt.timedelta(seconds=seconds)
        return new_datetime

    def sub_seconds(self, base_datetime, seconds: int = 5):
        new_datetime = base_datetime - dt.timedelta(seconds=seconds)
        return new_datetime

    def round_dates(self, base_datetime, timeunit: str, round_to: int):
        """
        Round a date.

        Ex: 07:16:02 -> 07:16:00

        """
        if timeunit == "S":
            rounded_second = self.round_to_nearest(
                value=base_datetime.second, nearest=round_to
            )
            if rounded_second >= 60:
                base_datetime = base_datetime.replace(
                    second=0, microsecond=0
                ) + dt.timedelta(minutes=1)
            else:
                base_datetime = base_datetime.replace(
                    second=rounded_second, microsecond=0
                )

        elif timeunit == "M":
            rounded_minute = self.round_to_nearest(
                value=base_datetime.minute, nearest=round_to
            )

            if rounded_minute >= 60:
                base_datetime = base_datetime.replace(
                    minute=0, second=0, microsecond=0
                ) + dt.timedelta(hours=1)
            else:
                base_datetime = base_datetime.replace(
                    minute=rounded_minute, second=0, microsecond=0
                )

        elif timeunit == "H":
            rounded_hour = self.round_to_nearest(
                value=base_datetime.hour, nearest=round_to
            )
            if rounded_hour >= 24:
                base_datetime = base_datetime.replace(
                    hour=0, minute=0, second=0, microsecond=0
                ) + dt.timedelta(days=1)
            else:
                base_datetime = base_datetime.replace(
                    hour=rounded_hour, minute=0, second=0, microsecond=0
                )
        return base_datetime

    def round_to_nearest(self, value, nearest=5):
        """
        Rounds a given number to the nearest specified value.

        Parameters:
        value (int or float): The number to be rounded.
        nearest (int): The value to which the number should be rounded. Default is 5.

        Returns:
        int: The rounded number.
        """
        return int(round(value / nearest) * nearest)

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""
    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""
    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""
