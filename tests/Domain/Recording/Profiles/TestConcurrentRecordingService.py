import datetime
import pytest
from src.Domain.Recording.Storage.Contracts.StorageRepositoryInterface import StorageRepositoryInterface
from src.Domain.SharedKernel.TimeProviderInterface import TimeProviderInterface
from src.Domain.Recording.Profiles.Exceptions.ProfileAlreadyRecordingException import ProfileAlreadyRecordingException
from tests.Domain.Recording.Storage.mothers.StorageMother import StorageMother
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.Contracts.ProfileRecorder import ProfileRecorder
from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface
from tests.Domain.Recording.Profiles.mothers.ProfileMother import ProfileMother
from unittest.mock import MagicMock, call
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from tests.Domain.Recording.Storage.mothers.StoragePathMother import StoragePathMother
from src.Domain.Recording.Profiles.Exceptions.ProfileOutOfRangeException import ProfileOutOfRangeException
from src.Domain.Recording.Profiles.Services.ConcurrentRecordingService import ConcurrentRecordingService
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
from src.Domain.SharedKernel.EventBusInterface import EventBusInterface
from src.Domain.Recording.Profiles.ValueObjects.ProfilesToRecord import ProfilesToRecord

class TestConcurrentRecordingService:
    __profile_recorder: MagicMock | None = None
    __profile_repository: MagicMock | None = None
    __storage_repository: MagicMock | None = None
    __time_provider: MagicMock | None = None
    __logger: MagicMock | None = None
    __event_bus: MagicMock | None = None
    __service: ConcurrentRecordingService | None = None

    @pytest.fixture(autouse=True)
    def setup(self):
        self.__profile_recorder = MagicMock(spec=ProfileRecorder)
        self.__profile_repository = MagicMock(spec=ProfileRepositoryInterface)
        self.__storage_repository = MagicMock(spec=StorageRepositoryInterface)
        self.__time_provider = MagicMock(spec=TimeProviderInterface)
        self.__logger = MagicMock(spec=LoggerInterface)
        self.__event_bus = MagicMock(spec=EventBusInterface)
        self.__service = ConcurrentRecordingService(
            self.__profile_repository, # pyright: ignore[reportAny]
            self.__time_provider, # pyright: ignore[reportAny]
            self.__profile_recorder, # pyright: ignore[reportAny]
            self.__storage_repository, # pyright: ignore[reportAny]
            self.__logger # pyright: ignore[reportAny]
        )
        
    def __given_now_is(self, now: datetime.datetime):
        assert self.__time_provider is not None
        self.__time_provider.now_utc.return_value = now # pyright: ignore[reportAny]
    
    def __given_profile_repository_finds_ready_to_record(self, profiles: list[Profile]):
        assert self.__profile_repository is not None
        self.__profile_repository.find_ready_to_record.return_value = profiles # pyright: ignore[reportAny]
        
    def __given_storage_repository_finds_local_storage(self, path: str | None = None):
        assert self.__storage_repository is not None
        self.__storage_repository.get_local_storage.return_value = StorageMother.create(path=path) # pyright: ignore[reportAny]
    
    def __then_profile_is_recording(self, profile: Profile):
        assert profile.is_recording.value == True
        
    def __then_profiles_are_recorded(self, profiles: list[Profile], local_storage_path: str):
        assert self.__profile_recorder is not None
        self.__profile_recorder.record_many_async.assert_called_once_with(  # pyright: ignore[reportAny]
            ProfilesToRecord(profiles),
            ProfileVideoStoragePath(local_storage_path)
        )
    
    def __then_profile_is_not_recorded(self):
        assert self.__profile_recorder is not None
        self.__profile_recorder.record_many_async.assert_not_called() # pyright: ignore[reportAny]
    
    def __then_profile_is_saved(self, profile: Profile):
        assert self.__profile_repository is not None
        self.__profile_repository.save.assert_called_once_with(profile) # pyright: ignore[reportAny]
        
    def __then_multiple_profiles_are_saved(self, profiles: list[Profile]):
        assert self.__profile_repository is not None
        self.__profile_repository.save.assert_has_calls( # pyright: ignore[reportAny]
            [
                call(profile)
                for profile in profiles
            ]
        )
    
    def __then_profile_is_not_saved(self):
        assert self.__profile_repository is not None
        self.__profile_repository.save.assert_not_called() # pyright: ignore[reportAny]
        
    def __then_profiles_from_date_are_searched(self, date: datetime.datetime):
        assert self.__profile_repository is not None
        self.__profile_repository.find_ready_to_record.assert_called_once_with(date) # pyright: ignore[reportAny]
      
    @pytest.mark.asyncio
    async def test_should_start_recording_single_profile(self):
        #Given
        profile = ProfileMother.create(
            day_range=((1,1),(1,12)),
            time_range=((0,0),(23,59)),
            recording_seconds=600,
            weekdays=[0,1,2,3,4,5,6]
        )
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        local_storage_path = StoragePathMother.create().value
        self.__given_profile_repository_finds_ready_to_record([profile])
        self.__given_storage_repository_finds_local_storage(local_storage_path)
        self.__given_now_is(date)
        
        #When
        assert self.__service is not None
        await self.__service.start_recording()
        
        #Then
        self.__then_profiles_from_date_are_searched(date)
        self.__then_profiles_are_recorded([profile], local_storage_path)
        self.__then_profile_is_recording(profile)
        self.__then_profile_is_saved(profile)
    
    @pytest.mark.asyncio
    async def test_should_start_recording_multiple_profiles(self):
        #Given
        profile1 = ProfileMother.create(
            day_range=((1,1),(1,12)),
            time_range=((0,0),(23,59)),
            recording_seconds=600,
            weekdays=[0,1,2,3,4,5,6]
        )
        profile2 = ProfileMother.create(
            day_range=((1,1),(1,12)),
            time_range=((0,0),(23,59)),
            recording_seconds=600,
            weekdays=[0,1,2,3,4,5,6]
        )
        profiles = [profile1, profile2]
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        local_storage_path = StoragePathMother.create().value
        self.__given_storage_repository_finds_local_storage(local_storage_path)
        self.__given_profile_repository_finds_ready_to_record(profiles)
        self.__given_now_is(date)
        #When
        assert self.__service is not None
        await self.__service.start_recording()
        
        #Then
        self.__then_profiles_from_date_are_searched(date)
        self.__then_profiles_are_recorded(profiles, local_storage_path)
        self.__then_profile_is_recording(profile1)
        self.__then_profile_is_recording(profile2)
        self.__then_multiple_profiles_are_saved(profiles)
        
    @pytest.mark.asyncio
    async def test_should_not_start_recording_if_no_profiles_are_active(self):
        #Given
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        local_storage_path = StoragePathMother.create().value
        self.__given_storage_repository_finds_local_storage(local_storage_path)
        self.__given_profile_repository_finds_ready_to_record([])
        self.__given_now_is(date)
        #When
        assert self.__service is not None
        await self.__service.start_recording()
        
        #Then
        self.__then_profile_is_not_recorded()
        self.__then_profile_is_not_saved()
        
    @pytest.mark.asyncio
    async def test_should_throw_exception_if_profile_is_not_in_range(self):
        #Given
        profile = ProfileMother.create(
            day_range=((1,2),(1,12)),
            time_range=((0,0),(23,59)),
            recording_seconds=600,
            weekdays=[0,1,2,3,4,5,6]
        )
        out_of_range_date = datetime.datetime(2025, 1, 2, 0, 0, 0)
        local_storage_path = StoragePathMother.create().value
        self.__given_now_is(out_of_range_date)
        self.__given_profile_repository_finds_ready_to_record([profile])
        self.__given_storage_repository_finds_local_storage(local_storage_path)
        self.__given_now_is(out_of_range_date)
        #When
        with pytest.raises(ProfileOutOfRangeException): 
            assert self.__service is not None
            await self.__service.start_recording()
        
        #Then
        self.__then_profile_is_not_recorded()
        self.__then_profile_is_not_saved()
        
    @pytest.mark.asyncio
    async def test_should_throw_exception_if_profile_is_already_recording(self):
        #Given
        profile = ProfileMother.create(
            day_range=((1,1),(1,12)),
            time_range=((0,0),(23,59)),
            recording_seconds=600,
            weekdays=[0,1,2,3,4,5,6],
            is_recording=True
        )
        date = datetime.datetime(2025, 1, 1, 0, 0, 0)
        local_storage_path = StoragePathMother.create().value
        self.__given_profile_repository_finds_ready_to_record([profile])
        self.__given_storage_repository_finds_local_storage(local_storage_path)
        self.__given_now_is(date)
        
        #When
        with pytest.raises(ProfileAlreadyRecordingException):
            assert self.__service is not None
            await self.__service.start_recording()
        
        #Then
        self.__then_profile_is_not_recorded()
        self.__then_profile_is_not_saved()