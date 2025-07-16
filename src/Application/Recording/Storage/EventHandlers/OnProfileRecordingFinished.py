from src.Domain.Recording.Profiles.Events.ProfileRecordingFinishedEvent import ProfileRecordingFinishedEvent
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
from src.Application.Recording.Storage.UseCases.MoveFileToRemoteStorageUseCase import MoveFileToRemoteStorageUseCase

class OnProfileRecordingFinished:
    def __init__(self, 
                 move_file_to_remote_storage_use_case: MoveFileToRemoteStorageUseCase,
                 logger: LoggerInterface
                 ):
        self.move_file_to_remote_storage_use_case = move_file_to_remote_storage_use_case
        self.logger = logger
            
    async def __call__(self, event: ProfileRecordingFinishedEvent):
        self.logger.debug(f"Recording finished event received from profile {event.profile_id}")
        await self.move_file_to_remote_storage_use_case.execute(event.recording_path)