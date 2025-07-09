from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
from src.Domain.Recording.Profiles.Services.RecordingFinishedStrategy import ProfileRecordingFinishedStrategy
from src.Domain.Recording.Profiles.Services.ReadyProfileFinder import ReadyProfileFinder
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRecorder import ProfileRecorder
from src.Domain.Recording.Storage.Contracts.StorageRepositoryInterface import StorageRepositoryInterface
from src.Domain.Recording.Storage.Services.LocalStorageFinder import LocalStorageFinder
from src.Domain.Recording.Storage.Services.RemoteStorageFinder import RemoteStorageFinder
from src.Domain.Recording.Profiles.Entities.Profile import Profile
    

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
        self.local_storage_finder = LocalStorageFinder(storage_repository)
        self.remote_storage_finder = RemoteStorageFinder(storage_repository)
        self.logger = logger
    
    async def start_recording(self) -> None:
        try:
            profiles = await self.ready_profile_finder.find_ready_to_record()
            local_storage = self.local_storage_finder.find_local_storage()
            if len(profiles) == 0: 
                return
            self.logger.info(f"Found {len(profiles)} profiles to record")
            await self.profile_recorder.record_many_async(
                profiles, 
                ProfileVideoStoragePath(local_storage.path.value),
                ProfileRecordingFinishedStrategy(self.profile_repository)
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
    
    async def _set_profile_recording_stopped(self, profile: Profile) -> None:
        profile.set_recording_stopped()
        await self.profile_repository.save(profile)
    