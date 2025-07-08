from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRecorderInterface import ProfileRecorderInterface
from src.Domain.Recording.Storage.Services.LocalStorageFinder import LocalStorageFinder
from src.Domain.Recording.Storage.Services.RemoteStorageFinder import RemoteStorageFinder
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath



class RecordingService:
    def __init__(
        self, 
        profile_repository: ProfileRepositoryInterface, 
        profile_recorder: ProfileRecorderInterface,
        local_storage_finder: LocalStorageFinder,
        remote_storage_finder: RemoteStorageFinder,
        time_provider: TimeProviderInterface
    ):
        self.profile_repository = profile_repository
        self.profile_recorder = profile_recorder
        self.local_storage_finder = local_storage_finder
        self.remote_storage_finder = remote_storage_finder
        self.time_provider = time_provider
        
    async def record_profile(self, profile: Profile) -> None:
        now = self.time_provider.now()
        profile.ensure_is_ready_to_record(now)
        local_storage = self.local_storage_finder.find_local_storage()
        # TODO: handle exception, transaction, (UoW) etc.
        self.profile_recorder.record(
            profile, 
            ProfileVideoStoragePath(local_storage.path.value)
        )
        await self.set_recording_stopped(profile)
        # TODO: move to remote storage
    
    async def set_recording_started(self, profile: Profile) -> None:
        profile.set_recording_started()
        await self.profile_repository.save(profile)
        
    async def set_recording_stopped(self, profile: Profile) -> None:
        profile.set_recording_stopped()
        await self.profile_repository.save(profile)
    
    