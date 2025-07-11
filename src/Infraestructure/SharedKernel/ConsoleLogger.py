from src.Domain.SharedKernel.LoggerInterface import LoggerInterface


class ConsoleLogger(LoggerInterface):
    def info(self, message: str) -> None:
        print(f"INFO: {message}")
    
    def error(self, message: str) -> None:
        print(f"ERROR: {message}")
    
    def warn(self, message: str) -> None:
        print(f"WARNING: {message}")
    
    def debug(self, message: str) -> None:
        print(f"DEBUG: {message}")
    