from typing import BinaryIO, Callable, Optional
from src.Domain.Recording.Storage.Contracts.RemoteStorageHandlerInterface import RemoteStorageHandlerInterface
from src.Domain.Recording.Storage.ValueObjects.StorageFilePath import StorageFilePath
import ftplib
try:
    import ssl
except ImportError:
    _SSLSocket = None
else:
    _SSLSocket = ssl.SSLSocket
    
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
        
        
    def _storbinary(self, ftp_connection: ftplib.FTP, cmd: str, fp: BinaryIO, blocksize: int = 8192, callback: Callable[[bytes], None] | None = None, rest: Optional[int] = None):
        # TODO: temp fix for ssl connection. MUST BE REMOVED
        ftp_connection.voidcmd('TYPE I')
        with ftp_connection.transfercmd(cmd, rest) as conn:
            while 1:
                buf = fp.read(blocksize)
                if not buf: break
                conn.sendall(buf)
                if callback: callback(buf)
            # shutdown ssl layer
            if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                # HACK: Instead of attempting unwrap the connection, pass here
                pass


    async def upload(self, src: StorageFilePath, dst: StorageFilePath):
        # TODO: secure connection
        with ftplib.FTP() as ftp_connection:
            ftp_connection.connect(self.host, self.port)
            ftp_connection.login(self.username, self.password)
            with open(src.value, "rb") as file:
                self._storbinary(ftp_connection, f"STOR {dst.value}", file)
                # TODO: check if is needed to overwrite the file, in case of an error

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
