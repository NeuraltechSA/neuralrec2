from src.Domain.Recording.Storage.Contracts.StorageRepositoryInterface import StorageRepositoryInterface
from src.Domain.Recording.Storage.Entities.Storage import Storage

class SqliteStorageRepository(StorageRepositoryInterface):
    
    def get_local_storage(self) -> Storage | None:
        return Storage(
            id="local",
            path="/app/videos"
        )
    
    def get_remote_storage(self) -> Storage | None:
        return Storage(
            id="remote",
            path="/app/abc"
        )