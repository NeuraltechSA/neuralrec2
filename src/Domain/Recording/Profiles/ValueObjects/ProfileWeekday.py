from src.Domain.SharedKernel.ValueObjects.IntValueObject import IntValueObject

class ProfileWeekday(IntValueObject):
    def __init__(self, value: int):
        self.__ensure_is_valid_weekday_index(value)
        super().__init__(value)
        
    def __ensure_is_valid_weekday_index(self, value: int):
        if value < 0 or value > 6:
            raise ValueError("Invalid weekday index")
            #TODO: raise custom exception
        