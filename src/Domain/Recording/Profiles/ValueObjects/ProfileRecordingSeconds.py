from src.Domain.SharedKernel.ValueObjects.IntValueObject import IntValueObject
from dataclasses import dataclass

@dataclass(frozen=True)
class ProfileRecordingSeconds(IntValueObject):
    def __post_init__(self):
        self.__ensure_is_valid_seconds(self.value)
        
    def __ensure_is_valid_seconds(self, value: int):
        # el sistema no permite grabar mas de 2 horas (7200 segundos)
        if value < 1 or value > 7200:
            raise ValueError("Invalid seconds")
            #TODO: raise custom exception 