import os
from typing import Any, final
import pytest
from pyventus.events import EventLinker
from src.Domain.Recording.Profiles.Events.RecordingFinishedEvent import RecordingFinishedEvent
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
from testcontainers.mongodb import MongoDbContainer
from unittest.mock import MagicMock
from datetime import datetime
from src.Infraestructure.SharedKernel.PyventusBus import PyventusBus

@final
class TestFfmpegProfileRecorder:
    __time_provider: MagicMock | None = None
    __event_bus: PyventusBus | None = None
    __repository: BeanieProfileRepository | None = None
    __mongo: MongoDbContainer | None = None
    __client: AsyncIOMotorClient[dict[str, Any]] | None = None
    
    def teardown(self):
        assert self.__mongo is not None
        assert self.__client is not None
        self.__mongo.stop()
        self.__client.close()
    
    @pytest.fixture(autouse=True)
    def setup(self,request):
        request.addfinalizer(self.teardown)
        self.__time_provider = MagicMock()
        self.__event_bus = PyventusBus()
        self.__repository = BeanieProfileRepository()
    async def init_db(self):
        self.__mongo = MongoDbContainer("mongo:7.0.21")
        self.__mongo.start()
        self.__client = AsyncIOMotorClient(self.__mongo.get_connection_url())
        await init_beanie(database=self.__client.get_database(self.__mongo.dbname), document_models=[ProfileDocument])

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
    async def should_record_profile(self):
        
        assert self.__repository is not None
        
        await self.init_db()
        recorder = FfmpegProfileRecorder(
            ConsoleLogger(),
            self.__time_provider,
            self.__event_bus
        )
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
        
        @EventLinker.on("recording_finished")
        def on_recording_finished(event: RecordingFinishedEvent):
            print(f"Recording finished: {event.video_path}")
        
        # When
        time_before = datetime.now()
        print(time_before)
        await recorder.record_many_async(
            [recording_profile],
            ProfileVideoStoragePath(recording_path)
        )
        recorder.wait_recordings_to_finish()
        time_after = datetime.now()
        print(time_after)

        # Then
        await self.__then_profile_is_recording(recording_profile.id.value)
        #recorder.wait_recordings_to_finish()
        await self.__then_profile_is_not_recording(recording_profile.id.value)
        self.__then_video_file_should_be_created(f"{recording_path}/{recording_prefix}_2025-01-01_12-00-00.mkv")