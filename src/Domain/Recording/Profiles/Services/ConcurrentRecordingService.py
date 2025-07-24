from typing import final
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
from src.Domain.Recording.Profiles.Services.ReadyProfileFinder import ReadyProfileFinder
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRecorder import ProfileRecorder
from src.Domain.Recording.Storage.Contracts.StorageRepositoryInterface import StorageRepositoryInterface
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.ValueObjects.ProfilesToRecord import ProfilesToRecord

@final
class ConcurrentRecordingService:
    def __init__(self, 
                 profile_repository: ProfileRepositoryInterface,
                 time_provider: TimeProviderInterface,
                 profile_recorder: ProfileRecorder,
                 storage_repository: StorageRepositoryInterface,
                 logger: LoggerInterface
    ):
        self.profile_repository = profile_repository
        self.time_provider = time_provider
        self.profile_recorder = profile_recorder
        self.ready_profile_finder = ReadyProfileFinder(profile_repository, time_provider)
        self.logger = logger
        self.storage_repository = storage_repository
    
    async def start_recording(self) -> None:
        try:
            profiles = await self.ready_profile_finder.find_ready_to_record()
            local_storage = self.storage_repository.get_local_storage()
            if len(profiles) == 0: 
                return
            self.logger.info(f"Found {len(profiles)} profiles to record")
            self.profile_recorder.record_many_async(
                ProfilesToRecord(profiles), 
                ProfileVideoStoragePath(local_storage.path.value),
            )
            self.logger.debug("Recording started")
            await self._set_profiles_recording_started(profiles)
            # TODO: domain events, transaction
        except Exception as e:
            self.logger.error(f"Error recording: {e}")
            raise e
    
    async def _set_profiles_recording_started(self, profiles: list[Profile]) -> None:
        for profile in profiles:
            profile.set_recording_started()
            await self.profile_repository.save(profile)
    