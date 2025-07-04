import uuid
from src.Domain.Recording.Storage.ValueObjects.StorageId import StorageId

class StorageIdMother:
    @staticmethod
    def create(id: str | None = None) -> StorageId:
        if id is None:
            id = str(uuid.uuid4())
        return StorageId(id)