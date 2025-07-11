from src.Domain.Recording.Storage.ValueObjects.StoragePath import StoragePath

class Storage:
    _path:StoragePath
    def __init__(self, path:str):
        self._path = StoragePath(path)

    @property
    def path(self) -> StoragePath:
        return self._path
    
    # TODO: create method