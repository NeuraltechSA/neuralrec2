import asyncio
import sys
from uuid import UUID
from src.Domain.Recording.Profiles.Services.ConcurrentRecordingService import ConcurrentRecordingService
from src.Infraestructure.Recording.Profiles.ProfileSleeper import ProfileSleeper
from src.Infraestructure.Recording.Storage.SqliteStorageRepository import SqliteStorageRepository
from src.Domain.Recording.Storage.Services.LocalStorageFinder import LocalStorageFinder
from src.Domain.Recording.Storage.Services.RemoteStorageFinder import RemoteStorageFinder
from src.Domain.Recording.Profiles.Services.RecordingService import RecordingService
from src.Application.Recording.Profiles.UseCases.RunRecordingLoopUseCase import RunRecordingLoopUseCase
from src.Infraestructure.Recording.Profiles.FfmpegProfileRecorder import FfmpegProfileRecorder
from src.Infraestructure.Recording.Profiles.BeanieProfileRepository import BeanieProfileRepository
from src.Infraestructure.SharedKernel.TimeProvider import TimeProvider
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.Infraestructure.Recording.Profiles.ProfileDocument import ProfileDocument

async def main():
    client = AsyncIOMotorClient("mongodb://root:toor@127.0.0.1:27017/testDB")
    await init_beanie(database=client.testDB, document_models=[ProfileDocument])
    

    storage_repository = SqliteStorageRepository()
    profile_repository = BeanieProfileRepository()
    profile_recorder = FfmpegProfileRecorder()
    local_storage_finder = LocalStorageFinder(storage_repository)
    remote_storage_finder = RemoteStorageFinder(storage_repository)
    recording_service = RecordingService(profile_repository, profile_recorder, local_storage_finder, remote_storage_finder, TimeProvider())

    run_loop_use_case = RunRecordingLoopUseCase(
        ConcurrentRecordingService(recording_service, profile_repository, TimeProvider()), 
        ProfileSleeper())
    await run_loop_use_case.execute(1)
    

if __name__ == "__main__":
    asyncio.run(main())