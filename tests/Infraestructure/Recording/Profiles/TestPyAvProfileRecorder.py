import subprocess
from threading import Thread
from unittest.mock import MagicMock, patch
from src.Infraestructure.SharedKernel.ConsoleLogger import ConsoleLogger
from src.Infraestructure.Recording.Profiles.PyAvProfileRecorder import PyAvProfileRecorder
from src.Infraestructure.SharedKernel.TimeProvider import TimeProvider
from src.Infraestructure.SharedKernel.PyventusBus import PyventusBus
from testcontainers.mongodb import MongoDbContainer
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any
from beanie import init_beanie
import pytest
from src.Infraestructure.Recording.Profiles.ProfileDocument import ProfileDocument
from datetime import datetime, timezone
from tests.Domain.Recording.Profiles.mothers.ProfileMother import ProfileMother
from src.Infraestructure.Recording.Profiles.BeanieProfileRepository import BeanieProfileRepository
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Domain.Recording.Profiles.ValueObjects.ProfilesToRecord import ProfilesToRecord
import os
import cv2
import random

class TestPyAvProfileRecorder:
    __logger: ConsoleLogger | None = None
    __time_provider: TimeProvider | None = None
    __event_bus: PyventusBus | None = None
    __repository: BeanieProfileRepository | None = None
    __mongo: MongoDbContainer | None = None
    __client: AsyncIOMotorClient[dict[str, Any]] | None = None # pyright: ignore[reportExplicitAny]
    __recorder: PyAvProfileRecorder | None = None
    
    
    @pytest.fixture(autouse=True)
    async def setup(self):
        self.__time_provider = TimeProvider()
        self.__event_bus = PyventusBus()
        self.__repository = BeanieProfileRepository()
        self.__recorder = PyAvProfileRecorder(ConsoleLogger(), self.__time_provider, self.__event_bus)
        
        await self.init_db()
    
    async def init_db(self):
        self.__mongo = MongoDbContainer("mongo:7.0.21")
        _ = self.__mongo.start()
        self.__client = AsyncIOMotorClient(self.__mongo.get_connection_url())
        await init_beanie(database=self.__client.get_database(self.__mongo.dbname), document_models=[ProfileDocument])
    
    
    async def __given_profile_exists(self, profile: Profile):
        assert self.__repository is not None
        await self.__repository.save(profile)
    
    def __given_video_file_not_exists(self, path: str):
        if os.path.exists(path):
            os.remove(path)
        
    def __given_rtsp_streaming_is_running(
        self, 
        duration: int,
        rtsp_uri: str
    ):
        #ffmpeg -re -stream_loop -1 -i 00d62ef3-cac2-40cd-926e-da24a07b898e.mp4 -c copy -f rtsp rtsp://localhost:8554/mystream
        Thread(target=lambda:  subprocess.run([
            "ffmpeg", "-re", "-stream_loop", "-1", 
            "-i", "/app/tests/Infraestructure/Recording/Profiles/Resources/rtsp.mp4",
            "-c", "copy", "-f", "rtsp","-t",str(duration), rtsp_uri])).start()
        # ffmpeg -re -stream_loop -1 -i /app/tests/Infraestructure/Recording/Profiles/Resources/rtsp.mp4 -c copy -f rtsp rtsp://localhost:8554/mystream
        
    async def __then_profile_is_not_recording(self, id: str):
        assert self.__repository is not None
        stored_profile = await self.__repository.find_one_by_id(id)
        if stored_profile is None:
            raise Exception("Profile not found")
        assert stored_profile.is_recording.value == False
    
    async def __then_profile_is_recording(self, id: str):
        assert self.__repository is not None
        stored_profile = await self.__repository.find_one_by_id(id)
        if stored_profile is None:
            raise Exception("Profile not found")
        assert stored_profile.is_recording.value == True
    
    async def __then_video_is_created(self, path:str, duration:int):
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0
        read_duration = self.__get_video_duration_seconds(path)
        assert duration == read_duration
    
    def __get_video_duration_seconds(self, path: str) -> int:
        cap = cv2.VideoCapture(path)
        return round(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
    
    async def __given_video_file_exists(self, path: str):
        if not os.path.exists(path):
            raise Exception("Video file not found")
    
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_should_record_profile(self):
        #self.__given_time_is(datetime(2025, 1, 1, 12, 0, 0))
        # Given
        current_time = datetime(2025, 1, 1, 12, 0, 0)
        with patch.object(self.__time_provider, 'now_local', return_value=current_time):
            recording_path = "/app/videos"
            recording_prefix = "test"
            recording_seconds = random.randint(1, 5)
            rtsp_uri = "rtsp://localhost:8554/mystream"
            expected_video_path = f"{recording_path}/{recording_prefix}_2025-01-01_12-00-00.mkv"
            recording_profile = ProfileMother.create(
                uri=rtsp_uri, #"rtsp://admin:neuraltech2024@localhost:8845",
                recording_seconds=recording_seconds,
                is_recording=False,
                video_prefix=recording_prefix,
                day_range=((1,1),(31,12)),
                time_range=((0,0),(23,59)),
                weekdays=[0,1,2,3,4,5,6]
            )
            self.__given_video_file_not_exists(expected_video_path)
            #self.__given_rtsp_streaming_is_running(
            #    recording_seconds * 2, 
            #    rtsp_uri
            #)
            await self.__given_profile_exists(recording_profile)
            
            # When
            assert self.__recorder is not None
            self.__recorder.record_many_async(
                ProfilesToRecord([recording_profile]), 
                ProfileVideoStoragePath(recording_path)
            )
            self.__recorder.wait_recordings_to_finish()
            
            # Then
            await self.__then_video_is_created(expected_video_path, recording_seconds)
            

    # TODO: agregar test de sobreescritura de video y de fallo de grabacion