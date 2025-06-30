from src.Domain.SharedKernel.ValueObjects.RequiredStringValueObject import RequiredStringValueObject
import re

class ProfileCameraUri(RequiredStringValueObject):
    
    def __post_init__(self):
        self.__ensure_is_valid_uri(self.value)
    
    def __ensure_is_valid_uri(self, uri: str):
        # Check for basic URI structure with scheme and authority
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://[^\s]+$', uri):
            raise ValueError("Invalid URI format")