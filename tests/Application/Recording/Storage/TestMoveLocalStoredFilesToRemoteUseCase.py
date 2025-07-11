from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath
from src.Application.Recording.Storage.UseCases.MoveLocalStoredFilesToRemoteUseCase import MoveLocalStoredFilesToRemoteUseCase
from unittest.mock import MagicMock, call, Mock
from src.Domain.Recording.Storage.Contracts.LocalStorageHandlerInterface import LocalStorageHandlerInterface
from src.Domain.Recording.Storage.Services.LocalFileMover import LocalFileMover
from src.Infraestructure.Recording.Storage.StorageRepository import StorageRepository
from src.Domain.Recording.Storage.Entities.Storage import Storage
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
import pytest

class TestMoveLocalStoredFilesToRemoteUseCase:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.__local_storage_handler = MagicMock(spec=LocalStorageHandlerInterface)
        self.__local_file_mover = Mock(spec=LocalFileMover)
        self.__storage_repository = MagicMock(spec=StorageRepository)
        self.__logger = MagicMock(spec=LoggerInterface)
        self.__move_local_stored_files_to_remote_use_case = MoveLocalStoredFilesToRemoteUseCase(
            self.__storage_repository,
            self.__local_storage_handler,
            self.__local_file_mover,
            self.__logger)
        
    def __given_local_storage_handler_returns_files(self, paths: list[StorageFilePath]):
        self.__local_storage_handler.get_all_files.return_value = paths
    
    def __given_local_storage_path_is(self, path: str):
        self.__storage_repository.get_local_storage.return_value = Storage(path)
    
    def __then_local_file_mover_is_called_to_move_files(self, paths: list[StorageFilePath]):
        self.__local_file_mover.move.assert_has_calls([
            call(path.value)
            for path in paths
        ])
        
    def __then_local_file_mover_is_not_called(self):
        self.__local_file_mover.assert_not_called()
        
    def __then_get_all_files_is_called_with_path(self, path: str):
        self.__local_storage_handler.get_all_files.assert_called_once_with(path)
        
    @pytest.mark.asyncio
    async def test_should_move_files_successfully(self):
        # Given
        path = "src/local"
        self.__given_local_storage_path_is(path)
        self.__given_local_storage_handler_returns_files([StorageFilePath("file1.txt"), StorageFilePath("file2.txt")])
        
        # When
        await self.__move_local_stored_files_to_remote_use_case.execute()
        
        # Then
        self.__then_get_all_files_is_called_with_path(path)
        self.__then_local_file_mover_is_called_to_move_files([StorageFilePath("file1.txt"), StorageFilePath("file2.txt")])
        
    @pytest.mark.asyncio
    async def test_should_do_nothing_when_no_files_are_found(self):
        # Given
        self.__given_local_storage_handler_returns_files([])
        
        # When
        await self.__move_local_stored_files_to_remote_use_case.execute()
        
        # Then
        self.__then_local_file_mover_is_not_called()