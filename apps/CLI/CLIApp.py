import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv
from src.Infraestructure.SharedKernel.LoguruLogger import LoguruLogger
from src.Infraestructure.Recording.Storage.StorageRepository import StorageRepository
from src.Infraestructure.Recording.Profiles.BeanieProfileRepository import BeanieProfileRepository
from src.Infraestructure.Recording.Profiles.ProfileDocument import ProfileDocument
from src.Application.Recording.Profiles.UseCases.RunRecordingLoopUseCase import RunRecordingLoopUseCase
from src.Domain.Recording.Profiles.Services.ConcurrentRecordingService import ConcurrentRecordingService
from src.Infraestructure.Recording.Profiles.ProfileSleeper import ProfileSleeper
from src.Infraestructure.Recording.Profiles.FfmpegProfileRecorder import FfmpegProfileRecorder
from src.Infraestructure.SharedKernel.TimeProvider import TimeProvider
from src.Application.Recording.Storage.UseCases.MoveLocalStoredFilesToRemoteUseCase import MoveLocalStoredFilesToRemoteUseCase
from src.Infraestructure.Recording.Storage.LocalFSHandler import LocalFSHandler
from src.Domain.Recording.Storage.Services.LocalFileMover import LocalFileMover
from src.Infraestructure.Recording.Storage.FtpHandler import FtpHandler

class CLIApp:
    def __init__(self):
        self.init_env()
        self.init_logger()
        self.init_db()
        self.init_use_cases()
    
    def init_env(self):
        load_dotenv()
    
    def init_db(self):
        client = AsyncIOMotorClient(str(os.getenv("MONGO_URI")))
        asyncio.run(init_beanie(database=client.get_database(os.getenv("MONGO_DB_NAME")), document_models=[ProfileDocument]))
    
    def init_logger(self):
        self.logger = LoguruLogger()
    
    def init_recording_loop_use_case(self):
        profile_repository = BeanieProfileRepository()
        storage_repository = StorageRepository()
        time_provider = TimeProvider()
        logger = LoguruLogger()
        
        self.run_recording_loop_use_case = RunRecordingLoopUseCase(
            ConcurrentRecordingService(
                profile_repository,
                time_provider,
                FfmpegProfileRecorder(logger, time_provider),
                storage_repository,
                logger
            ),
            ProfileSleeper(),
            profile_repository,
            logger
        )
        
    def init_move_local_stored_files_to_remote_use_case(self):
        storage_repository = StorageRepository()
        local_storage_handler = LocalFSHandler()
        logger = LoguruLogger()
        
        self.move_local_stored_files_to_remote_use_case = MoveLocalStoredFilesToRemoteUseCase(
            storage_repository,
            local_storage_handler,
            LocalFileMover(
                FtpHandler(
                    str(os.getenv("FTP_HOST")),
                    int(os.getenv("FTP_PORT", "")),
                    str(os.getenv("FTP_USERNAME")),
                    str(os.getenv("FTP_PASSWORD"))
                ),
                local_storage_handler,
                storage_repository,
                logger
            ),
            logger
        )
    
    def init_use_cases(self):
        self.init_recording_loop_use_case()
        self.init_move_local_stored_files_to_remote_use_case()
        
    async def run_recording_loop(self):
        try:
            await self.run_recording_loop_use_case.execute(1)
        except Exception as e:
            self.logger.error(f"Error running recording loop: {e}")
            raise e
    
    async def run_move_local_stored_files_to_remote(self):
        try:
            await self.move_local_stored_files_to_remote_use_case.execute()
        except Exception as e:
            self.logger.error(f"Error moving local stored files to remote: {e}")
            raise e