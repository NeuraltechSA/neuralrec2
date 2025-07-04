from abc import ABC, abstractmethod
from src.Domain.Recording.Storage.Entities.Storage import Storage

class StorageRepositoryInterface(ABC):
    #TODO: idea: grabar en varios almacenamientos, 
    # ej: carpeta remota en la oficina y local en el dispositivo
    @abstractmethod
    def get_local_storage(self) -> Storage | None:
        pass
    
    @abstractmethod
    def get_remote_storage(self) -> Storage | None:
        pass