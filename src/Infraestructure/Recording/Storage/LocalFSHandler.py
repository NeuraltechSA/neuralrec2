from src.Domain.Recording.Storage.Contracts.LocalStorageHandlerInterface import LocalStorageHandlerInterface
from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath
import os
import glob
        
class LocalFSHandler(LocalStorageHandlerInterface):
    
    def remove(self, src: StorageFilePath) -> None:
        os.remove(src.value)

    def exists(self, src: StorageFilePath) -> bool:
        return os.path.exists(src.value)

    def get_all_files(self, path:str) -> list[StorageFilePath]:
        files = glob.glob(os.path.join(path, '**', '*'), recursive=True)
        files = [f for f in files if os.path.isfile(f)]
        return [StorageFilePath(f) for f in files]