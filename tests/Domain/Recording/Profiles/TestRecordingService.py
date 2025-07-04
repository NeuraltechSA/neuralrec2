import datetime
import pytest
from src.Domain.Recording.Profiles.Exceptions.ProfileAlreadyRecordingException import ProfileAlreadyRecordingException
from src.Domain.Recording.Storage.Services.LocalStorageFinder import LocalStorageFinder
from src.Domain.Recording.Storage.Services.RemoteStorageFinder import RemoteStorageFinder
from tests.Domain.Recording.Storage.mothers.StorageMother import StorageMother
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.Contracts.ProfileRecorderInterface import ProfileRecorderInterface
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from tests.Domain.Recording.Profiles.mothers.ProfileMother import ProfileMother
from unittest.mock import MagicMock, call
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from tests.Domain.Recording.Storage.mothers.StoragePathMother import StoragePathMother
from tests.Domain.Recording.Profiles.mothers.ProfileDayRangeMother import ProfileDayRangeMother
from src.Domain.Recording.Profiles.Exceptions.ProfileOutOfRangeException import ProfileOutOfRangeException
from src.Domain.Recording.Profiles.Services.RecordingService import RecordingService

class TestRecordingService:
    __profile_recorder: MagicMock
    __profile_repository: MagicMock
    __local_storage_finder: MagicMock
    __remote_storage_finder: MagicMock

    @pytest.fixture(autouse=True)
    def setup(self):
        self.__profile_recorder = MagicMock(spec=ProfileRecorderInterface)
        self.__profile_repository = MagicMock(spec=ProfileRepositoryInterface)
        self.__local_storage_finder = MagicMock(spec=LocalStorageFinder)
        self.__remote_storage_finder = MagicMock(spec=RemoteStorageFinder)
        self.__service = RecordingService(
            self.__profile_repository, 
            self.__profile_recorder,
            self.__local_storage_finder,
            self.__remote_storage_finder
        )
    
    def __given_profile_repository_finds_active(self, profiles: list[Profile]):
        self.__profile_repository.find_active.return_value = profiles
        
    def __given_local_storage_finder_finds(self, path: str | None = None):
        self.__local_storage_finder.find_local_storage.return_value = StorageMother.create(path=path)
    
    def __given_remote_storage_finder_finds(self, path: str | None = None):
        self.__remote_storage_finder.find_remote_storage.return_value = StorageMother.create(path=path)
    
    def __then_profile_is_recording(self, profile: Profile):
        assert profile.is_recording.value == True
        
    def __then_profile_is_recorded(self, profile: Profile, local_storage_path: str, remote_storage_path: str):
        self.__profile_recorder.record_async.assert_called_once_with(
            profile,
            ProfileVideoStoragePath(local_storage_path),
            ProfileVideoStoragePath(remote_storage_path)
        )
        
    def __then_multiple_profiles_are_recorded(self, profiles: list[Profile], local_storage_path: str, remote_storage_path: str):
        self.__profile_recorder.record_async.assert_has_calls(
            [
                call(profile, ProfileVideoStoragePath(local_storage_path), ProfileVideoStoragePath(remote_storage_path))
                for profile in profiles
            ]
        )
    
    def __then_profile_is_not_recorded(self):
        self.__profile_recorder.record_async.assert_not_called()
    
    def __then_profile_is_saved(self, profile: Profile):
        self.__profile_repository.save.assert_called_once_with(profile)
        
    def __then_multiple_profiles_are_saved(self, profiles: list[Profile]):
        self.__profile_repository.save.assert_has_calls(
            [
                call(profile)
                for profile in profiles
            ]
        )
    
    def __then_profile_is_not_saved(self):
        self.__profile_repository.save.assert_not_called()
        
    def __then_profiles_from_date_are_searched(self, date: datetime.datetime):
        self.__profile_repository.find_active.assert_called_once_with(date)
      
    def test_should_start_recording_single_profile(self, mocker):
        #Given
        profile = ProfileMother.create(
            day_range=((1,1),(1,12)),
            time_range=((0,0),(23,59)),
            recording_minutes=10,
            weekdays=[0,1,2,3,4,5,6]
        )
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        local_storage_path = StoragePathMother.create().value
        remote_storage_path = StoragePathMother.create().value
        self.__given_profile_repository_finds_active([profile])
        self.__given_local_storage_finder_finds(local_storage_path)
        self.__given_remote_storage_finder_finds(remote_storage_path)
        
        #When
        self.__service.start_recording(date)
        
        #Then
        self.__then_profiles_from_date_are_searched(date)
        self.__then_profile_is_recorded(profile, local_storage_path, remote_storage_path)
        self.__then_profile_is_recording(profile)
        self.__then_profile_is_saved(profile)
    
    def test_should_start_recording_multiple_profiles(self):
        #Given
        profile1 = ProfileMother.create(
            day_range=((1,1),(1,12)),
            time_range=((0,0),(23,59)),
            recording_minutes=10,
            weekdays=[0,1,2,3,4,5,6]
        )
        profile2 = ProfileMother.create(
            day_range=((1,1),(1,12)),
            time_range=((0,0),(23,59)),
            recording_minutes=10,
            weekdays=[0,1,2,3,4,5,6]
        )
        profiles = [profile1, profile2]
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        local_storage_path = StoragePathMother.create().value
        remote_storage_path = StoragePathMother.create().value
        self.__given_local_storage_finder_finds(local_storage_path)
        self.__given_remote_storage_finder_finds(remote_storage_path)
        self.__given_profile_repository_finds_active(profiles)
        
        #When
        self.__service.start_recording(date)
        
        #Then
        self.__then_profiles_from_date_are_searched(date)
        self.__then_multiple_profiles_are_recorded(profiles, local_storage_path, remote_storage_path)
        self.__then_profile_is_recording(profile1)
        self.__then_profile_is_recording(profile2)
        self.__then_multiple_profiles_are_saved(profiles)
        
    def test_should_not_start_recording_if_no_profiles_are_active(self):
        #Given
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        self.__given_profile_repository_finds_active([])
        
        #When
        self.__service.start_recording(date)
        
        #Then
        self.__then_profile_is_not_recorded()
        self.__then_profile_is_not_saved()
        
    def test_should_throw_exception_if_profile_is_not_in_range(self):
        #Given
        profile = ProfileMother.create(
            day_range=((1,2),(1,12)),
            time_range=((0,0),(23,59)),
            recording_minutes=10,
            weekdays=[0,1,2,3,4,5,6]
        )
        out_of_range_date = datetime.datetime(2025, 1, 2, 0, 0, 0)
        local_storage_path = StoragePathMother.create().value
        remote_storage_path = StoragePathMother.create().value
        self.__given_profile_repository_finds_active([profile])
        self.__given_local_storage_finder_finds(local_storage_path)
        self.__given_remote_storage_finder_finds(remote_storage_path)
        
        #When
        with pytest.raises(ProfileOutOfRangeException): 
            self.__service.start_recording(out_of_range_date)
        
        #Then
        self.__then_profile_is_not_recorded()
        self.__then_profile_is_not_saved()
        
    def test_should_throw_exception_if_profile_is_already_recording(self):
        #Given
        profile = ProfileMother.create(
            day_range=((1,1),(1,12)),
            time_range=((0,0),(23,59)),
            recording_minutes=10,
            weekdays=[0,1,2,3,4,5,6],
            is_recording=True
        )
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        local_storage_path = StoragePathMother.create().value
        remote_storage_path = StoragePathMother.create().value
        self.__given_profile_repository_finds_active([profile])
        self.__given_local_storage_finder_finds(local_storage_path)
        self.__given_remote_storage_finder_finds(remote_storage_path)
        
        #When
        with pytest.raises(ProfileAlreadyRecordingException):
            self.__service.start_recording(date)
        
        #Then
        self.__then_profile_is_not_recorded()
        self.__then_profile_is_not_saved()