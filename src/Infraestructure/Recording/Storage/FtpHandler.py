from src.Domain.Recording.Storage.Contracts.RemoteStorageHandlerInterface import RemoteStorageHandlerInterface
from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath
from aioftp import Client

class FtpHandler(RemoteStorageHandlerInterface):
    def __init__(self, 
                 host: str, 
                 port: int, 
                 username: str, 
                 password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password


    async def upload(self, src: StorageFilePath, dst: StorageFilePath):
        # TODO: secure connection
        async with Client.context(self.host, self.port, self.username, self.password) as client:
            await client.upload(src.value, dst.value, write_into=True)

    async def exists(self, src: StorageFilePath) -> bool:
        # TODO: secure connection
        async with Client.context(self.host, self.port, self.username, self.password) as client:
            return await client.exists(src.value)
