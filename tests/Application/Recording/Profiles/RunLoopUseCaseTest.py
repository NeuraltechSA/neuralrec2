from unittest.mock import MagicMock
import pytest
from src.Application.Recording.Profiles.UseCases.RunLoopUseCase import RunLoopUseCase
from src.Domain.Recording.Profiles.Contracts.ProfileRecorderInterface import ProfileRecorderInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from tests.Domain.Recording.Profiles.mothers.ProfileMother import ProfileMother


class RunLoopUseCaseTest:
    __profile_repository: MagicMock
    __profile_recorder: MagicMock
    __run_loop_use_case: RunLoopUseCase
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.__profile_repository = MagicMock(spec=ProfileRepositoryInterface)
        self.__profile_recorder = MagicMock(spec=ProfileRecorderInterface)
        self.__run_loop_use_case = RunLoopUseCase(
            self.__profile_repository, 
            self.__profile_recorder
        )
        
    def test_should_start_recording_profiles(self):
        #Given
        self.__profile_repository.find_active.return_value = [ProfileMother.create()]
        
        #When
        #run_loop_use_case.execute()
        
        #Then