from src.Infraestructure.Recording.Storage.StorageRepository import StorageRepository
from src.Infraestructure.SharedKernel.LoguruLogger import LoguruLogger
from src.Application.Recording.Storage.UseCases.MoveLocalStoredFilesToRemoteUseCase import MoveLocalStoredFilesToRemoteUseCase
from src.Domain.Recording.Storage.Services.LocalFileMover import LocalFileMover
from src.Infraestructure.Recording.Storage.FtpHandler import FtpHandler
from src.Infraestructure.Recording.Storage.LocalFSHandler import LocalFSHandler
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    logger = LoguruLogger()
    storage_repository = StorageRepository()
    ftp_handler = FtpHandler(
        os.getenv("FTP_HOST",""), 
        int(os.getenv("FTP_PORT","")), 
        os.getenv("FTP_USERNAME",""), 
        os.getenv("FTP_PASSWORD","")
    )
    local_fs_handler = LocalFSHandler()
    file_mover = LocalFileMover(ftp_handler, local_fs_handler, storage_repository, logger)
    move_local_to_remote_use_case = MoveLocalStoredFilesToRemoteUseCase(
        storage_repository,
        local_fs_handler, 
        file_mover,
        logger
    )
    await move_local_to_remote_use_case.execute()

if __name__ == "__main__":
    asyncio.run(main())