from src.Domain.SharedKernel.ValueObjects.RequiredStringValueObject import RequiredStringValueObject
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ProfileCameraUri(RequiredStringValueObject):
    
    def __post_init__(self):
        self.__ensure_is_valid_rtsp_uri(self.value)
    
    def __ensure_is_valid_rtsp_uri(self, uri: str):
        if not re.match(r'^rtsp://[^\s]+$', uri):
            raise ValueError("Invalid RTSP URI format")