import abc
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath

class ProfileVideoUploaderInterface(abc.ABC):
    @abc.abstractmethod
    def upload(self, storage_path: ProfileVideoStoragePath) -> None:
        pass
    @abc.abstractmethod
    def delete(self, storage_path: ProfileVideoStoragePath) -> None:
        pass