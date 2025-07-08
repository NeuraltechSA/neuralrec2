import datetime
from src.Domain.Recording.Profiles.Entities.Profile import Profile
import abc

class ProfileRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    async def find_ready_to_record(self, now: datetime.datetime) -> list[Profile]:
        pass
    
    @abc.abstractmethod
    async def find_one_by_id(self, id: str) -> Profile | None:
        pass
    
    @abc.abstractmethod
    async def save(self, profile: Profile) -> None:
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
    
    
    
    