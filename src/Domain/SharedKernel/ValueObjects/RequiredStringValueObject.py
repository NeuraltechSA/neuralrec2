from src.Domain.SharedKernel.ValueObjects.StringValueObject import StringValueObject

class RequiredStringValueObject(StringValueObject):
    def __post_init__(self):
        self.__ensure_is_not_empty(self.value)
        
    def __ensure_is_not_empty(self, value: str):
        if not value or not value.strip():
            raise ValueError("Value cannot be empty")

