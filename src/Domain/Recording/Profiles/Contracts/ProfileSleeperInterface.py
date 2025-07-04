from abc import ABC, abstractmethod

class ProfileSleeperInterface(ABC):
    @abstractmethod
    def sleep(self, seconds: int) -> None:
        pass