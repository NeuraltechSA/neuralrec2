import datetime
from src.Domain.Recording.Profiles.Contracts.ProfileRecorderInterface import ProfileRecorderInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface


class StartRecordingUseCase:
    def __init__(
        self, 
        profile_repository: ProfileRepositoryInterface, 
        profile_recorder: ProfileRecorderInterface
    ):
        self.profile_repository = profile_repository
        self.profile_recorder = profile_recorder
        
    def execute(self, now: datetime.datetime) -> None:
        profiles = self.profile_repository.find_active(now)
        for profile in profiles:            
            profile.start_recording(now)
            self.profile_recorder.record_async(profile)
        
        