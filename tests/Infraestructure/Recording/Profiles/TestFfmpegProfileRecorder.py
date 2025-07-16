import os
import pytest
from src.Infraestructure.Recording.Profiles.FfmpegProfileRecorder import FfmpegProfileRecorder
from src.Infraestructure.SharedKernel.ConsoleLogger import ConsoleLogger
from src.Infraestructure.SharedKernel.TimeProvider import TimeProvider
from tests.Domain.Recording.Profiles.mothers.ProfileMother import ProfileMother
from src.Domain.Recording.Profiles.Services.RecordingFinishedStrategy import ProfileRecordingFinishedStrategy
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Infraestructure.Recording.Profiles.BeanieProfileRepository import BeanieProfileRepository
from src.Infraestructure.Recording.Profiles.ProfileDocument import ProfileDocument
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import asyncio
from testcontainers.mongodb import MongoDbContainer
from unittest.mock import MagicMock
from datetime import datetime
import time

class TestFfmpegProfileRecorder:
    
    def teardown(self):
        self.mongo.stop()
        self.client.close()
    
    @pytest.fixture(autouse=True)
    def setup(self,request):
        request.addfinalizer(self.teardown)
        self.__time_provider = MagicMock()
        
    async def init_db(self):
        self.mongo = MongoDbContainer("mongo:7.0.21")
        self.mongo.start()
        self.client = AsyncIOMotorClient(self.mongo.get_connection_url())
        await init_beanie(database=self.client.get_database(self.mongo.dbname), document_models=[ProfileDocument])

    async def __then_profile_is_not_recording(self, id: str):
        stored_profile = await self.__repository.find_one_by_id(id)
        if stored_profile is None:
            raise Exception("Profile not found")
        assert stored_profile.is_recording.value == False
    
    async def __then_profile_is_recording(self, id: str):
        stored_profile = await self.__repository.find_one_by_id(id)
        if stored_profile is None:
            raise Exception("Profile not found")
        assert stored_profile.is_recording.value == True
    
    def __then_video_file_should_be_created(self, recording_path: str):
        assert os.path.exists(recording_path)
        
    def __given_time_is(self, datetime: datetime):
        self.__time_provider.now_local.return_value = datetime
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_should_record_profile(self):
        await self.init_db()
        self.__recorder = FfmpegProfileRecorder(
            ConsoleLogger(),
            self.__time_provider
        )
        self.__repository = BeanieProfileRepository()
        
        # Given
        self.__given_time_is(datetime(2025, 1, 1, 12, 0, 0))
        recording_path = "/app/videos"
        recording_prefix = "test"
        recording_profile = ProfileMother.create(
            uri="rtsp://localhost:8554/mystream", #"rtsp://admin:neuraltech2024@localhost:8845",
            recording_seconds=5,
            is_recording=False,
            video_prefix=recording_prefix,
            day_range=((1,1),(31,12)),
            time_range=((0,0),(23,59)),
            weekdays=[0,1,2,3,4,5,6]
        )
        await self.__repository.save(recording_profile)
        
        # When
        await self.__recorder.record_many_async(
            [recording_profile],
            ProfileVideoStoragePath(recording_path),
            ProfileRecordingFinishedStrategy(
                repository=self.__repository
            )
        )

        # Then
        await self.__then_profile_is_recording(recording_profile.id.value)
        self.__recorder.wait_recordings_to_finish()
        await self.__then_profile_is_not_recording(recording_profile.id.value)
        self.__then_video_file_should_be_created(f"{recording_path}/{recording_prefix}_2025-01-01_12-00-00.mkv")