from abc import ABC, abstractmethod
from src.Domain.SharedKernel.DomainEvent import DomainEvent

class EventBusInterface(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        pass