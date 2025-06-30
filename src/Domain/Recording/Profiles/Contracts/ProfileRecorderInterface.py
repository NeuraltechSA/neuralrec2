import abc
from src.Domain.Recording.Profiles.Entities.Profile import Profile

class ProfileRecorderInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def record_async(self, profile: Profile) -> None:
        pass
    
    #TODO: pending implementation
    #@abc.abstractmethod
    #def stop(self, profile: Profile) -> None:
    #    pass
    
    
    
    
    
    
    