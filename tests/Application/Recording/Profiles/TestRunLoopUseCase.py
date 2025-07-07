from unittest.mock import MagicMock, call
import pytest
from src.Application.Recording.Profiles.UseCases.RunRecordingLoopUseCase import RunRecordingLoopUseCase
from src.Domain.Recording.Profiles.Contracts.ProfileSleeperInterface import ProfileSleeperInterface
from src.Domain.Recording.Profiles.Services.ConcurrentRecordingService import ConcurrentRecordingService
from src.Domain.Recording.Profiles.Exceptions.ProfileInvalidLoopWaitSecondsException import ProfileInvalidLoopWaitSecondsException
from src.Domain.Recording.Profiles.Exceptions.ProfileInvalidLoopIterationCountException import ProfileInvalidLoopIterationCountException
import random

class TestRunLoopUseCase:
    __recording_service: MagicMock
    __profile_sleeper: MagicMock
    __run_loop_use_case: RunRecordingLoopUseCase
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.__recording_service = MagicMock(spec=ConcurrentRecordingService)
        self.__profile_sleeper = MagicMock(spec=ProfileSleeperInterface)
        self.__run_loop_use_case = RunRecordingLoopUseCase(
            self.__recording_service,
            self.__profile_sleeper
        )
        
    def __then_recording_service_is_called_n_times(self, n: int):
        self.__recording_service.start_recording.assert_has_calls([call() for _ in range(n)])
    
    def __then_profile_sleeper_is_called_n_times(self, n: int, wait_seconds: int):
        self.__profile_sleeper.sleep.assert_has_calls([call(wait_seconds) for _ in range(n)])
    
    def test_should_record_profiles_in_loop(self):
        #Given
        wait_seconds = random.randint(1, 20)
        max_iterations = random.randint(1, 20)
        
        #When
        self.__run_loop_use_case.execute(wait_seconds, max_iterations)
        
        #Then
        self.__then_recording_service_is_called_n_times(max_iterations)
        self.__then_profile_sleeper_is_called_n_times(max_iterations, wait_seconds)
    
    def test_should_throw_exception_when_wait_seconds_is_zero(self):
        #Given
        wait_seconds = 0
        
        #When & Then
        with pytest.raises(ProfileInvalidLoopWaitSecondsException):
            self.__run_loop_use_case.ensure_valid_wait_seconds(wait_seconds)
    
    def test_should_throw_exception_when_wait_seconds_is_negative(self):
        #Given
        wait_seconds = -5
        
        #When & Then
        with pytest.raises(ProfileInvalidLoopWaitSecondsException):
            self.__run_loop_use_case.ensure_valid_wait_seconds(wait_seconds)
    
    def test_should_throw_exception_when_max_iterations_is_zero(self):
        #Given
        max_iterations = 0
        
        #When & Then
        with pytest.raises(ProfileInvalidLoopIterationCountException):
            self.__run_loop_use_case.ensure_valid_max_iterations(max_iterations)
    
    def test_should_throw_exception_when_max_iterations_is_negative(self):
        #Given
        max_iterations = -3
        
        #When & Then
        with pytest.raises(ProfileInvalidLoopIterationCountException):
            self.__run_loop_use_case.ensure_valid_max_iterations(max_iterations)
    
    def test_should_accept_none_max_iterations(self):
        #Given
        max_iterations = None
        
        #When & Then
        self.__run_loop_use_case.ensure_valid_max_iterations(max_iterations)  # Should not raise exception
    
    def test_should_accept_positive_max_iterations(self):
        #Given
        max_iterations = 10
        
        #When & Then
        self.__run_loop_use_case.ensure_valid_max_iterations(max_iterations)  # Should not raise exception