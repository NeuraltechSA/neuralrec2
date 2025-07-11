from abc import ABC, abstractmethod
from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath

class RemoteStorageHandlerInterface(ABC):
    @abstractmethod
    async def upload(self, src: StorageFilePath, dst: StorageFilePath) -> None:
        pass
    
    @abstractmethod
    async def exists(self, src: StorageFilePath) -> bool:
        pass