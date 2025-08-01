from typing_extensions import override
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
from loguru import logger

class LoguruLogger(LoggerInterface):
    def __init__(self):
        # TODO: load from config
        _ = logger.add("logs/app.log", level="DEBUG", rotation="100 MB", retention="30 days", enqueue=True)
        _ = logger.add("logs/error.log", level="ERROR", rotation="100 MB", retention="30 days", enqueue=True)
        
    @override
    def info(self, message: str) -> None:
        logger.info(message)

    @override
    def error(self, message: str) -> None:
        logger.error(message)
    
    @override
    def debug(self, message: str) -> None:
        logger.debug(message)
    
    @override
    def warn(self, message: str) -> None:
        logger.warning(message)
