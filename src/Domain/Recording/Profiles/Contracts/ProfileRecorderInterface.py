import abc
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath

class ProfileRecorderInterface(abc.ABC):
    @abc.abstractmethod
    def record_async(
        self, 
        profile: Profile, 
        local_storage_path: ProfileVideoStoragePath,
        remote_storage_path: ProfileVideoStoragePath,
    ) -> None:
        pass
    
    
    #TODO: pending implementation
    #@abc.abstractmethod
    #def stop(self, profile: Profile) -> None:
    #    pass
    
    
    
    
    
    
    