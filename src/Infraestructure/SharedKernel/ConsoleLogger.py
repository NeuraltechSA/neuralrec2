import sys
from typing_extensions import override
from src.Domain.SharedKernel.LoggerInterface import LoggerInterface


class ConsoleLogger(LoggerInterface):
    @override
    def info(self, message: str) -> None:
        _ = sys.stdout.write(f"INFO: {message}")
        _ = sys.stdout.flush()
    
    @override
    def error(self, message: str) -> None:
        _ = sys.stderr.write(f"ERROR: {message}")
        _ = sys.stderr.flush()
    
    @override
    def warn(self, message: str) -> None:
        _ = sys.stderr.write(f"WARNING: {message}")
        _ = sys.stderr.flush()
    
    @override
    def debug(self, message: str) -> None:
        _ = sys.stdout.write(f"DEBUG: {message}")
        _ = sys.stdout.flush()
    