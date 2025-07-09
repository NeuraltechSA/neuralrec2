import abc
from typing import final
from src.Domain.Recording.Profiles.Services.RecordingFinishedStrategy import ProfileRecordingFinishedStrategy
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath

class ProfileRecorder(abc.ABC):
    @final
    async def record_many_async(
        self, 
        profiles: list[Profile], 
        storage_path: ProfileVideoStoragePath,
        recording_finished_strategy: ProfileRecordingFinishedStrategy
    ) -> None:
        for profile in profiles:
            self._record_async(profile, storage_path, recording_finished_strategy)
    
    @abc.abstractmethod
    def _record_async(self, 
                      profile: Profile, 
                      storage_path: ProfileVideoStoragePath, 
                      recording_finished_strategy: ProfileRecordingFinishedStrategy) -> None:
        pass
    
    