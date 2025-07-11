from src.Domain.Recording.Storage.Contracts.StorageRepositoryInterface import StorageRepositoryInterface
from src.Domain.Recording.Storage.Entities.Storage import Storage
import os

class StorageRepository(StorageRepositoryInterface):
    
    def get_local_storage(self) -> Storage:
        return Storage(
            path=os.getenv("LOCAL_STORAGE_PATH","")
        )
    
    def get_remote_storage(self) -> Storage:
        return Storage(
            path=os.getenv("REMOTE_STORAGE_PATH","")
        )