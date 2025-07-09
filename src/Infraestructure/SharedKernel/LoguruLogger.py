from src.Domain.SharedKernel.LoggerInterface import LoggerInterface
from loguru import logger

class LoguruLogger(LoggerInterface):
    def __init__(self):
        # TODO: load from config
        logger.add("logs/app.log", level="DEBUG", rotation="100 MB", retention="30 days", enqueue=True)
        logger.add("logs/error.log", level="ERROR", rotation="100 MB", retention="30 days", enqueue=True)
        
    def info(self, message: str) -> None:
        logger.info(message)

    def error(self, message: str) -> None:
        logger.error(message)
    
    def debug(self, message: str) -> None:
        logger.debug(message)
    
    def warn(self, message: str) -> None:
        logger.warning(message)
