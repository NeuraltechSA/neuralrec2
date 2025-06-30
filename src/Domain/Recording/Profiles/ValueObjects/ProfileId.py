from src.Domain.SharedKernel.ValueObjects.GuidValueObject import GuidValueObject

class ProfileId(GuidValueObject):
    def __init__(self, value: str):
        super().__init__(value)
