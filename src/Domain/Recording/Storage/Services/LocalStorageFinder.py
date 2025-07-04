from src.Domain.Recording.Storage.Contracts.StorageRepositoryInterface import StorageRepositoryInterface
from src.Domain.Recording.Storage.Entities.Storage import Storage

class LocalStorageFinder:
    def __init__(self, storage_repository: StorageRepositoryInterface):
        self.storage_repository = storage_repository

    def find_local_storage(self) -> Storage:
        storage = self.storage_repository.get_local_storage()
        self.ensure_local_storage_exists(storage)
        assert storage is not None  # Type assertion for the type checker
        return storage
    
    def ensure_local_storage_exists(self, storage: Storage | None) -> None:
        if storage is None:
            raise Exception("Local storage not found")
            #TODO: create a custom exception