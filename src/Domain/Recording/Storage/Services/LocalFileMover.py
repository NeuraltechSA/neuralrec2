from src.Domain.Recording.Storage.Contracts.LocalStorageHandlerInterface import LocalStorageHandlerInterface
from src.Domain.Recording.Storage.Contracts.RemoteStorageHandlerInterface import RemoteStorageHandlerInterface
from src.Domain.Recording.Storage.Contracts.StorageRepositoryInterface import StorageRepositoryInterface
from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath
import os
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface

class LocalFileMover:
    def __init__(self, 
                 remote_storage_handler: RemoteStorageHandlerInterface, 
                 local_storage_handler: LocalStorageHandlerInterface,
                 storage_repository: StorageRepositoryInterface,
                 logger: LoggerInterface
        ):
        self.remote_storage_handler = remote_storage_handler
        self.local_storage_handler = local_storage_handler
        self.storage_repository = storage_repository
        self.logger = logger
        
    async def move(self, src: str):
        """
        Moves a file from the local storage to the remote storage.
        If the file already exists in the remote storage, it will be overwritten.
        If the file does not exist in the local storage, it will raise an error.
        
        Args:
            src: The path to the file to move.
            
        Raises:
            FileExistsError: If the file already exists in the remote storage.
            FileNotFoundError: If the file does not exist in the local storage.
        """
        src_path = StorageFilePath(src)
        dst_path = self._get_dst_path(src_path)
        self._ensure_local_file_exists(src_path)
        await self._ensure_remote_file_not_exists(dst_path)
        self.logger.debug(f"Uploading file {src_path.value} to {dst_path.value}")
        await self.remote_storage_handler.upload(src_path, dst_path)
        self.logger.debug(f"Removing file {src_path.value} from local storage")
        self.local_storage_handler.remove(src_path)
        self.logger.debug(f"File {src_path.value} moved successfully")
        # TODO: rollback (?)

    def _get_dst_path(self, src: StorageFilePath) -> StorageFilePath:
        local_storage = self.storage_repository.get_local_storage()
        remote_storage = self.storage_repository.get_remote_storage()
        relative_path = src.get_relative_path(local_storage.path.value)
        self.logger.debug(f"Joining path {remote_storage.path.value} with {relative_path}")
        dst_path = os.path.join(os.path.sep,remote_storage.path.value,relative_path.lstrip(os.path.sep))
        self.logger.debug(f"Joined path: {dst_path}")
        return StorageFilePath(dst_path)

    async def _ensure_remote_file_not_exists(self, dst: StorageFilePath):
        self.logger.debug(f"Ensuring remote file {dst.value} does not exist")
        if await self.remote_storage_handler.exists(dst):
            raise FileExistsError(f"File {dst.value} already exists")

    def _ensure_local_file_exists(self, src: StorageFilePath):
        self.logger.debug(f"Ensuring local file {src.value} exists")
        if not self.local_storage_handler.exists(src):
            raise FileNotFoundError(f"File {src.value} not found")