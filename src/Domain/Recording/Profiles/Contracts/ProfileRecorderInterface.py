import abc
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath

class ProfileRecorderInterface(abc.ABC):
    @abc.abstractmethod
    def record(
        self, 
        profile: Profile, 
        storage_path: ProfileVideoStoragePath
    ) -> None:
        pass
    
    
    #TODO: pending implementation
    #@abc.abstractmethod
    #def stop(self, profile: Profile) -> None:
    #    pass
    
    
    
    
    
    
    