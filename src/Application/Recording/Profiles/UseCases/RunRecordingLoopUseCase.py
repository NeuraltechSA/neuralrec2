from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
from src.Domain.Recording.Profiles.Services.ConcurrentRecordingService import ConcurrentRecordingService
from src.Domain.Recording.Profiles.Contracts.ProfileSleeperInterface import ProfileSleeperInterface
from src.Domain.Recording.Profiles.Exceptions.ProfileInvalidLoopWaitSecondsException import ProfileInvalidLoopWaitSecondsException
from src.Domain.Recording.Profiles.Exceptions.ProfileInvalidLoopIterationCountException import ProfileInvalidLoopIterationCountException
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface

class RunRecordingLoopUseCase:
    """
    Caso de uso para ejecutar un bucle de grabación con intervalos de espera.
    
    Arquitectura:
    - El thread principal se bloquea durante el sleep
    - Las grabaciones se ejecutan en threads secundarios via ConcurrentRecordingService
    - El loop principal controla el timing entre grabaciones
    """
    
    def __init__(self, 
                 recording_service: ConcurrentRecordingService,
                 profile_sleeper: ProfileSleeperInterface,
                 profile_repository: ProfileRepositoryInterface,
                 logger: LoggerInterface
    ):
        self.recording_service = recording_service
        self.profile_sleeper = profile_sleeper
        self.profile_repository = profile_repository
        self.logger = logger
        
    async def execute(self, wait_seconds: int, max_iterations: int | None = None) -> None:
        """
        Executes the recording loop.
        
        Args:
            wait_seconds: Seconds to wait between recordings (blocks main thread)
            max_iterations: Maximum number of iterations (None for infinite)
        """
        self.ensure_valid_wait_seconds(wait_seconds)
        self.ensure_valid_max_iterations(max_iterations)
        self.reset_recordings()
        
        self.logger.info(f"Running recording loop with wait_seconds: {wait_seconds} and max_iterations: {max_iterations}")
        iteration = 0
        while True:
            try:
                iteration += 1
                await self.recording_service.start_recording()
            except Exception as e:
                self.logger.error(f"Error in recording loop iteration {iteration}: {e}")
            self.profile_sleeper.sleep(wait_seconds)
            if iteration == max_iterations:
                self.logger.info(f"Max iterations reached: {max_iterations}")
                break

    def reset_recordings(self) -> None:
        self.profile_repository.set_all_as_not_recording()

    def ensure_valid_wait_seconds(self, wait_seconds: int) -> None:
        if wait_seconds <= 0:
            raise ProfileInvalidLoopWaitSecondsException(wait_seconds)
    
    def ensure_valid_max_iterations(self, max_iterations: int | None) -> None:
        if max_iterations is not None and max_iterations <= 0:
            raise ProfileInvalidLoopIterationCountException(max_iterations)