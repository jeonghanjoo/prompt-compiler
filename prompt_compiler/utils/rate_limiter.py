from typing import Callable

from functools import wraps
from datetime import datetime, timedelta
from ..exceptions import RateLimitError


class RateLimiter:
    """Rate limiter for API calls."""

    def __init__(self, calls: int, period: int):
        """
        Initialize rate limiter.

        Args:
            calls: Number of calls allowed
            period: Time period in seconds
        """
        self.calls = calls
        self.period = period
        self.timestamps = []

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.now()

            # Remove timestamps older than the period
            self.timestamps = [
                ts
                for ts in self.timestamps
                if now - ts < timedelta(seconds=self.period)
            ]

            if len(self.timestamps) >= self.calls:
                oldest = min(self.timestamps)
                retry_after = self.period - (now - oldest).seconds
                raise RateLimitError(model=args[0].model, retry_after=retry_after)

            self.timestamps.append(now)
            return func(*args, **kwargs)

        return wrapper
