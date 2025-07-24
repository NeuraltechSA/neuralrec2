from src.Domain.Recording.Profiles.Contracts.ProfileRecorder import ProfileRecorder
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Domain.Recording.Profiles.Services.RecordingFinishedStrategy import ProfileRecordingFinishedStrategy
from src.Domain.Recording.Profiles.Entities.Profile import Profile


class GSProfileRecorder(ProfileRecorder):
    def __init__(self, profile_name: str):
        self.profile_name = profile_name

    def _record_async(self, profile: Profile, storage_path: ProfileVideoStoragePath, recording_finished_strategy: ProfileRecordingFinishedStrategy) -> None:
        pass