from src.Domain.Recording.Storage.Entities.Storage import Storage
from tests.Domain.Recording.Storage.mothers.StoragePathMother import StoragePathMother

class StorageMother:
    @staticmethod
    def create(path: str | None = None) -> Storage:
        return Storage(
            path=StoragePathMother.create(path).value
        )