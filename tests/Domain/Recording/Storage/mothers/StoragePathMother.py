import random
import string
from src.Domain.Recording.Storage.ValueObjects.StoragePath import StoragePath

class StoragePathMother:
    @staticmethod
    def create(path: str | None = None) -> StoragePath:
        if path is None:
            path = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return StoragePath(path)