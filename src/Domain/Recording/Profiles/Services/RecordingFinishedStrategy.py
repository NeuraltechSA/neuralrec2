from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface

class ProfileRecordingFinishedStrategy:
    def __init__(self, repository: ProfileRepositoryInterface):
        self.repository = repository
    
    async def execute(self, profile:Profile) -> None:
        profile.set_recording_stopped()
        await self.repository.save(profile)
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProfileRecordingFinishedStrategy):
            return False
        return self.repository == other.repository