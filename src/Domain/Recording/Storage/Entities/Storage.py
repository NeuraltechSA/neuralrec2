from src.Domain.Recording.Storage.ValueObjects.StorageId import StorageId
from src.Domain.Recording.Storage.ValueObjects.StoragePath import StoragePath

class Storage:
    _id:StorageId
    _path:StoragePath
    def __init__(self, id:str, path:str):
        self._id = StorageId(id)
        self._path = StoragePath(path)

    @property
    def id(self) -> StorageId:
        return self._id

    @property
    def path(self) -> StoragePath:
        return self._path