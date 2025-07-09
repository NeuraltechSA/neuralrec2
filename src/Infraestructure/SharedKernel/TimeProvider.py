import datetime
import os

from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface

class TimeProvider(TimeProviderInterface):
    def now_utc(self) -> datetime.datetime:
        return datetime.datetime.now()
    
    def now_local(self) -> datetime.datetime:
        tz_offset = int(os.getenv("TZ_OFFSET", "0"))
        return datetime.datetime.now() + datetime.timedelta(hours=tz_offset)