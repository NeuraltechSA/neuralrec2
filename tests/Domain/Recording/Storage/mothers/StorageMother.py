from src.Domain.Recording.Storage.Entities.Storage import Storage
from tests.Domain.Recording.Storage.mothers.StorageIdMother import StorageIdMother
from tests.Domain.Recording.Storage.mothers.StoragePathMother import StoragePathMother

class StorageMother:
    @staticmethod
    def create(id: str | None = None, path: str | None = None) -> Storage:
        return Storage(
            id=StorageIdMother.create(id).value,
            path=StoragePathMother.create(path).value
        )