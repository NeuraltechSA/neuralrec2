from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRecorderInterface import ProfileRecorderInterface
from src.Domain.Recording.Storage.Services.LocalStorageFinder import LocalStorageFinder
from src.Domain.Recording.Storage.Services.RemoteStorageFinder import RemoteStorageFinder
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
import datetime


class RecordingService:
    def __init__(
        self, 
        profile_repository: ProfileRepositoryInterface, 
        profile_recorder: ProfileRecorderInterface,
        local_storage_finder: LocalStorageFinder,
        remote_storage_finder: RemoteStorageFinder
    ):
        self.profile_repository = profile_repository
        self.profile_recorder = profile_recorder
        self.local_storage_finder = local_storage_finder
        self.remote_storage_finder = remote_storage_finder
        
    def start_recording(self, now: datetime.datetime) -> None:
        profiles = self.profile_repository.find_active(now)
        local_storage = self.local_storage_finder.find_local_storage()
        remote_storage = self.remote_storage_finder.find_remote_storage()
        for profile in profiles:
            profile.ensure_is_in_range(now)
            self.profile_recorder.record_async(
                profile, 
                ProfileVideoStoragePath(local_storage.path.value),
                ProfileVideoStoragePath(remote_storage.path.value)
            )
            profile.set_recording_started()
            self.profile_repository.save(profile) 
            # TODO: domain events