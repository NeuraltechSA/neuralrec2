from src.Domain.Recording.Storage.Contracts.LocalStorageHandlerInterface import LocalStorageHandlerInterface
from src.Domain.Recording.Storage.Contracts.RemoteStorageHandlerInterface import RemoteStorageHandlerInterface
from src.Domain.Recording.Storage.Services.LocalFileMover import LocalFileMover
from src.Infraestructure.Recording.Storage.StorageRepository import StorageRepository
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface

class MoveLocalStoredFilesToRemoteUseCase:
    def __init__(self, 
                 storage_repository: StorageRepository,
                 local_storage_handler: LocalStorageHandlerInterface,
                 local_file_mover: LocalFileMover,
                 logger: LoggerInterface):
        self.storage_repository = storage_repository
        self.local_storage_handler = local_storage_handler
        self.local_file_mover = local_file_mover
        self.logger = logger
        
    async def execute(self):
        path = self.storage_repository.get_local_storage().path.value
        files = self.local_storage_handler.get_all_files(path)
        self.logger.info(f"Found {len(files)} files in {path} to move")
        for file in files:
            await self.local_file_mover.move(file.value)