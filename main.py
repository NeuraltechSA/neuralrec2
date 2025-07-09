import asyncio
from src.Domain.Recording.Profiles.Services.ConcurrentRecordingService import ConcurrentRecordingService
from src.Infraestructure.Recording.Profiles.ProfileSleeper import ProfileSleeper
from src.Infraestructure.Recording.Storage.SqliteStorageRepository import SqliteStorageRepository
from src.Domain.Recording.Profiles.Services.ConcurrentRecordingService import ConcurrentRecordingService
from src.Application.Recording.Profiles.UseCases.RunRecordingLoopUseCase import RunRecordingLoopUseCase
from src.Infraestructure.Recording.Profiles.FfmpegProfileRecorder import FfmpegProfileRecorder
from src.Infraestructure.Recording.Profiles.BeanieProfileRepository import BeanieProfileRepository
from src.Infraestructure.SharedKernel.TimeProvider import TimeProvider
from beanie import init_beanie
from src.Infraestructure.Recording.Profiles.ProfileDocument import ProfileDocument
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from src.Infraestructure.SharedKernel.LoguruLogger import LoguruLogger

async def main():
    load_dotenv()
    client = AsyncIOMotorClient(str(os.getenv("MONGO_URI")))
    await init_beanie(database=client.get_database(os.getenv("MONGO_DB_NAME")), document_models=[ProfileDocument])
    logger = LoguruLogger()

    storage_repository = SqliteStorageRepository()
    profile_repository = BeanieProfileRepository()
    profile_recorder = FfmpegProfileRecorder(logger, TimeProvider())
    run_loop_use_case = RunRecordingLoopUseCase(
        ConcurrentRecordingService(
            profile_repository, 
            TimeProvider(),
            profile_recorder,
            storage_repository,
            logger
        ), 
        ProfileSleeper(),
        profile_repository,
        logger
    )
    
    await run_loop_use_case.execute(1)

if __name__ == "__main__":
    asyncio.run(main())