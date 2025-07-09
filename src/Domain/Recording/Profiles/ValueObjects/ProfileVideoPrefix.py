from src.Domain.Recording.Profiles.Exceptions.ProfileVideoPrefixInvalidLenghtException import ProfileVideoPrefixInvalidLenghtException
from src.Domain.SharedKernel.ValueObjects.RequiredStringValueObject import RequiredStringValueObject

class ProfileVideoPrefix(RequiredStringValueObject):
    
    def ensure_valid_length(self) -> None:
        if len(self.value) < 3 or len(self.value) > 50:
            raise ProfileVideoPrefixInvalidLenghtException(len(self.value), 3, 50)
    