from src.Domain.SharedKernel.ValueObjects.IntValueObject import IntValueObject
from dataclasses import dataclass

@dataclass(frozen=True)
class ProfileRecordingMinutes(IntValueObject):
    def __post_init__(self):
        self.__ensure_is_valid_minutes(self.value)
        
    def __ensure_is_valid_minutes(self, value: int):
        # el sistema no permite grabar mas de 2 horas
        if value < 1 or value > 120:
            raise ValueError("Invalid minutes")
            #TODO: raise custom exception
            
            
            
            
            