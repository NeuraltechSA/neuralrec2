from abc import ABC, abstractmethod
from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath

class LocalStorageHandlerInterface(ABC):
    @abstractmethod
    def remove(self, src: StorageFilePath) -> None:
        pass

    @abstractmethod
    def exists(self, src: StorageFilePath) -> bool:
        pass
    
    @abstractmethod
    def get_all_files(self, path:str) -> list[StorageFilePath]:
        pass