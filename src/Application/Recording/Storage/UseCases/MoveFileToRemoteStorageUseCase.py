from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath
from src.Domain.Recording.Storage.Services.LocalFileMover import LocalFileMover

class MoveFileToRemoteStorageUseCase:
    def __init__(self,
                 local_file_mover: LocalFileMover):
        self.local_file_mover = local_file_mover

    async def execute(self, src: str):
        await self.local_file_mover.move(src)
        