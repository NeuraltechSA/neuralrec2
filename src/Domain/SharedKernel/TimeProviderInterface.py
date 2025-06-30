from abc import ABC, abstractmethod
import datetime

class TimeProviderInterface(ABC):
    @abstractmethod
    def now(self) -> datetime.datetime:
        pass

class TimeProvider(TimeProviderInterface):
    def now(self) -> datetime.datetime:
        return datetime.datetime.now()
