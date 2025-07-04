import datetime
from src.Domain.Recording.Profiles.Entities.Profile import Profile
import abc

class ProfileRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def find_active(self, date: datetime.datetime) -> list[Profile]:
        pass
    
    @abc.abstractmethod
    def find_one_by_id(self, id: str) -> Profile | None:
        pass
    
    @abc.abstractmethod
    def save(self, profile: Profile) -> None:
        pass
    
    '''
    def find_all(self) -> List[Profile]:
        pass
        
    @abc.abstractmethod
    def save(self, profile: Profile) -> None:
        pass
    
    @abc.abstractmethod
    def find_by_id(self, id: str) -> Profile:
        pass
    '''
    
    
    
    