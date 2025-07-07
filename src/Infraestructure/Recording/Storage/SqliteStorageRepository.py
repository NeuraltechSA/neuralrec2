from src.Domain.Recording.Storage.Contracts.StorageRepositoryInterface import StorageRepositoryInterface
from src.Domain.Recording.Storage.Entities.Storage import Storage

class SqliteStorageRepository(StorageRepositoryInterface):
    
    def get_local_storage(self) -> Storage | None:
        return Storage(
            id="c32d8b45-92fe-44f6-8b61-42c2107dfe87",
            path="/app/videos"
        )
    
    def get_remote_storage(self) -> Storage | None:
        return Storage(
            id="c32d8b45-92fe-44f6-8b61-42c2107dfe87",
            path="/app/abc"
        )