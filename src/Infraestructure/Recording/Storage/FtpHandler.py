from src.Domain.Recording.Storage.Contracts.RemoteStorageHandlerInterface import RemoteStorageHandlerInterface
from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath
import ftplib

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
        with ftplib.FTP() as ftp_connection:
            ftp_connection.connect(self.host, self.port)
            ftp_connection.login(self.username, self.password)
            with open(src.value, "rb") as file:
                ftp_connection.storbinary(f"STOR {dst.value}", file)

    async def exists(self, src: StorageFilePath) -> bool:
        # TODO: secure connection
        with ftplib.FTP() as ftp_connection:
            ftp_connection.connect(self.host, self.port)
            ftp_connection.login(self.username, self.password)
            try:
                ftp_connection.size(src.value)
                return True
            except ftplib.error_perm:
                return False
