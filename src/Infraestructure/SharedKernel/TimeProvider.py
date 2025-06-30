import datetime

from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface

class TimeProvider(TimeProviderInterface):
    def now(self) -> datetime.datetime:
        return datetime.datetime.now()