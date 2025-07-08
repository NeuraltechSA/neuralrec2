import asyncio
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
    
    async def start_recording(self) -> None:
        now = self.time_provider.now()
        profiles = await self.profile_repository.find_ready_to_record(now)
        print(profiles)
        for profile in profiles:
            asyncio.ensure_future(self.recording_service.record_profile(profile))
            await self.recording_service.set_recording_started(profile)
            # TODO: domain events