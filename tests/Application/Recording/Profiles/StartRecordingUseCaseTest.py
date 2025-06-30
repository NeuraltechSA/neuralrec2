import datetime
import pytest
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.Contracts.ProfileRecorderInterface import ProfileRecorderInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from tests.Domain.Recording.Profiles.mothers.ProfileMother import ProfileMother
from src.Application.Recording.Profiles.UseCases.StartRecordingUseCase import StartRecordingUseCase
from unittest.mock import MagicMock, call

class TestStartRecordingUseCase:
    __profile_recorder: MagicMock
    __profile_repository: MagicMock
    

    @pytest.fixture(autouse=True)
    def setup(self):
        self.__profile_recorder = MagicMock(spec=ProfileRecorderInterface)
        self.__profile_repository = MagicMock(spec=ProfileRepositoryInterface)
        self.__use_case = StartRecordingUseCase(self.__profile_repository, self.__profile_recorder)
    
    def __given_profile_repository_find_active(self, profiles: list[Profile]):
        self.__profile_repository.find_active.return_value = profiles
    
    def test_should_start_recording_single_profile(self):
        #Given
        profile = ProfileMother.create()
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        self.__given_profile_repository_find_active([profile])
        
        #When
        self.__use_case.execute(date)
        
        #Then
        self.__profile_repository.find_active.assert_called_once_with(date)
        self.__profile_repository.set_recording.assert_called_once_with(profile.id.value, True)
        self.__profile_recorder.record_async.assert_called_once_with(profile)
    
    def test_should_start_recording_multiple_profiles(self):
        #Given
        profile1 = ProfileMother.create()
        profile2 = ProfileMother.create()
        profiles = [profile1, profile2]
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        self.__given_profile_repository_find_active(profiles)
        
        #When
        self.__use_case.execute(date)
        
        #Then
        self.__profile_repository.find_active.assert_called_once_with(date)
        self.__profile_repository.set_recording.assert_has_calls([call(p._id.value, True) for p in profiles])
        self.__profile_recorder.record_async.assert_has_calls([call(p) for p in profiles])
        
    def test_should_not_start_recording_if_no_profiles_are_active(self):
        #Given
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        self.__given_profile_repository_find_active([])
        
        #When
        self.__use_case.execute(date)
        
        #Then
        self.__profile_repository.find_active.assert_called_once_with(date)
        self.__profile_recorder.record_async.assert_not_called()
        self.__profile_repository.set_recording.assert_not_called()