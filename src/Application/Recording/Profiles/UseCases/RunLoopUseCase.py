import time
from src.Application.Recording.Profiles.UseCases.StartRecordingUseCase import StartRecordingUseCase
from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface

class RunLoopUseCase:
    def __init__(self, time_provider: TimeProviderInterface, start_recording_use_case: StartRecordingUseCase):
        self.start_recording_use_case = start_recording_use_case
        self.time_provider = time_provider
    
    def execute(self, wait_seconds: int) -> None:
        while True:
            self.start_recording_use_case.execute(self.time_provider.now())
            time.sleep(wait_seconds)