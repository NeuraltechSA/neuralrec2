from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface

class ReadyProfileFinder:
    def __init__(
        self, 
        profile_repository: ProfileRepositoryInterface, 
        time_provider: TimeProviderInterface
    ):
        self.profile_repository = profile_repository
        self.time_provider = time_provider
    
    async def find_ready_to_record(self) -> list[Profile]:
        """
        Finds profiles and ensures they are ready to record.
        A profile is ready to record if:
        - It is not already recording
        - It is within the time range
        - It is within the day range
        - It is within the weekdays
        - It is within the recording minutes
        """
        now = self.time_provider.now_utc()
        profiles = await self.profile_repository.find_ready_to_record(now)
        self._ensure_profiles_are_ready_to_record(profiles)
        return profiles
    
    def _ensure_profiles_are_ready_to_record(self, profiles: list[Profile]) -> None:
        now = self.time_provider.now_utc()
        for profile in profiles:
            profile.ensure_is_ready_to_record(now)