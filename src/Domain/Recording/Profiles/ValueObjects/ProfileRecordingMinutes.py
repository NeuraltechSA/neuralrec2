from src.Domain.SharedKernel.ValueObjects.IntValueObject import IntValueObject


class ProfileRecordingMinutes(IntValueObject):
    def __init__(self, value: int):
        self.__ensure_is_valid_minutes(value)
        super().__init__(value)
        
    def __ensure_is_valid_minutes(self, value: int):
        # el sistema no permite grabar mas de 2 horas
        if value < 1 or value > 120:
            raise ValueError("Invalid minutes")
            #TODO: raise custom exception
            
            
            
            
            