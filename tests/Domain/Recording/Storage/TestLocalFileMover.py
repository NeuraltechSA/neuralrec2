from unittest.mock import MagicMock, call
from src.Domain.Recording.Storage.Entities.Storage import Storage
from src.Domain.Recording.Storage.Services.LocalFileMover import LocalFileMover
from src.Domain.Recording.Storage.Contracts.RemoteStorageHandlerInterface import RemoteStorageHandlerInterface
from src.Domain.Recording.Storage.Contracts.LocalStorageHandlerInterface import LocalStorageHandlerInterface
from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath
from src.Domain.Recording.Storage.Contracts.StorageRepositoryInterface import StorageRepositoryInterface
import pytest
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
from src.Infraestructure.SharedKernel.ConsoleLogger import ConsoleLogger

class TestLocalFileMover:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.__manager = MagicMock()
        self.__remote_storage_handler = MagicMock(spec=RemoteStorageHandlerInterface)
        self.__local_storage_handler = MagicMock(spec=LocalStorageHandlerInterface)
        self.__storage_repository = MagicMock(spec=StorageRepositoryInterface)
        self.__logger = ConsoleLogger()
        self.__local_file_mover = LocalFileMover(
            self.__remote_storage_handler, 
            self.__local_storage_handler,
            self.__storage_repository,
            self.__logger
        )
        self.__manager.attach_mock(self.__remote_storage_handler, 'remote_storage_handler')
        self.__manager.attach_mock(self.__local_storage_handler, 'local_storage_handler')
    
    def __given_remote_file_not_exists(self):
        self.__remote_storage_handler.exists.return_value = False
    
    def __given_remote_file_exists(self):
        self.__remote_storage_handler.exists.return_value = True
    
    def __given_local_file_exists(self):
        self.__local_storage_handler.exists.return_value = True
    
    def __given_local_file_not_exists(self):
        self.__local_storage_handler.exists.return_value = False
    
    def __given_local_storage_is(self, path: str):
        self.__storage_repository.get_local_storage.return_value = Storage(path)
    
    def __given_remote_storage_is(self, path: str):
        self.__storage_repository.get_remote_storage.return_value = Storage(path)
    
    def __then_local_file_existance_is_checked(self, src: str):
        return call.local_storage_handler.exists(StorageFilePath(src))
    
    def __then_remote_file_existance_is_checked(self, dst: str):
        return call.remote_storage_handler.exists(StorageFilePath(dst))
    
    def __then_local_file_is_removed(self, src: str):
        return call.local_storage_handler.remove(StorageFilePath(src))
    
    def __then_remote_file_is_uploaded(self, src: str, dst: str):
        return call.remote_storage_handler.upload(StorageFilePath(src), StorageFilePath(dst))
    
    def __then_remote_storage_handler_is_not_called(self):
        self.__remote_storage_handler.upload.assert_not_called()
        
    def __then_local_storage_handler_is_not_called(self):
        self.__local_storage_handler.remove.assert_not_called()
        
    
    @pytest.mark.asyncio
    async def test_should_move_file_successfully(self):
        # Given
        src = "/src/local/2025/06/01/file.txt"
        dst = "/src/remote/2025/06/01/file.txt"
        self.__given_local_storage_is("src/local")
        self.__given_remote_storage_is("src/remote")
        self.__given_local_file_exists()
        self.__given_remote_file_not_exists()
        
        # When
        await self.__local_file_mover.move(src)
        
        # Then
        self.__manager.assert_has_calls([
            self.__then_local_file_existance_is_checked(src),
            self.__then_remote_file_existance_is_checked(dst),
            self.__then_remote_file_is_uploaded(src, dst),
            self.__then_local_file_is_removed(src)
        ])
        
    @pytest.mark.asyncio
    async def test_should_throw_exception_when_local_file_does_not_exist(self):
        # Given
        src = "src/test/file.txt"
        self.__given_local_file_not_exists()
        self.__given_local_storage_is("src/local")
        
        # When
        with pytest.raises(FileNotFoundError):
            await self.__local_file_mover.move(src)
            
        # Then
        self.__then_remote_storage_handler_is_not_called()
        self.__then_local_storage_handler_is_not_called()
    
    @pytest.mark.asyncio
    async def test_should_throw_exception_when_remote_file_exists(self):
        # Given
        src = "src/test/file.txt"
        self.__given_remote_file_exists()
        self.__given_local_storage_is("src/local")
        
        # When
        with pytest.raises(FileExistsError):
            await self.__local_file_mover.move(src)
            
        # Then
        self.__then_remote_storage_handler_is_not_called()
        self.__then_local_storage_handler_is_not_called()
        