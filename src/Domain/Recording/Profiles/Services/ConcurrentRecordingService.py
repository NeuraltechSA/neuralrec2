from multiprocessing import Process
from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from src.Domain.Recording.Profiles.Services.RecordingService import RecordingService

class ConcurrentRecordingService:
    def __init__(self, 
                 recording_service: RecordingService,
                 profile_repository: ProfileRepositoryInterface,
                 time_provider: TimeProviderInterface
    ):
        self.recording_service = recording_service
        self.profile_repository = profile_repository
        self.time_provider = time_provider
    
    def start_recording(self) -> None:
        now = self.time_provider.now()
        profiles = self.profile_repository.find_ready_to_record(now)
        
        for profile in profiles:
            # Create and start a separate process for each profile
            process = Process(target=self.recording_service.record_profile, args=(profile,),)
            process.start()
                
            # TODO: domain events