from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface
from src.Domain.Recording.Profiles.Services.RecordingService import RecordingService
from src.Domain.Recording.Profiles.Contracts.ProfileSleeperInterface import ProfileSleeperInterface
from src.Domain.Recording.Profiles.Exceptions.ProfileInvalidLoopWaitSecondsException import ProfileInvalidLoopWaitSecondsException
from src.Domain.Recording.Profiles.Exceptions.ProfileInvalidLoopIterationCountException import ProfileInvalidLoopIterationCountException

class RunLoopUseCase:
    def __init__(self, 
                 time_provider: TimeProviderInterface, 
                 recording_service: RecordingService,
                 profile_sleeper: ProfileSleeperInterface
    ):
        self.recording_service = recording_service
        self.time_provider = time_provider
        self.profile_sleeper = profile_sleeper
        
    def execute(self, wait_seconds: int, max_iterations: int | None = None) -> None:
        while True:
            self.recording_service.start_recording(self.time_provider.now())
            self.profile_sleeper.sleep(wait_seconds)
            if max_iterations is not None:
                max_iterations -= 1
                if max_iterations == 0:
                    break

    def ensure_valid_wait_seconds(self, wait_seconds: int) -> None:
        if wait_seconds <= 0:
            raise ProfileInvalidLoopWaitSecondsException(wait_seconds)
    
    def ensure_valid_max_iterations(self, max_iterations: int | None) -> None:
        if max_iterations is not None and max_iterations <= 0:
            raise ProfileInvalidLoopIterationCountException(max_iterations)