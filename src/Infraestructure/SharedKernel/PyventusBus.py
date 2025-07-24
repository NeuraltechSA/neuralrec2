from src.Domain.SharedKernel.EventBusInterface import EventBusInterface
from src.Domain.SharedKernel.DomainEvent import DomainEvent
from pyventus.events import AsyncIOEventEmitter

class PyventusBus(EventBusInterface):
    def __init__(self):
        self.__event_emitter = AsyncIOEventEmitter()

    def publish(self, event: DomainEvent):
        self.__event_emitter.emit(event.event_name, event)