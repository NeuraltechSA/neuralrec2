from dataclasses import dataclass
from src.Domain.SharedKernel.ValueObjects.DayValueObject import DayValueObject

@dataclass(frozen=True)
class DayRangeValueObject:
    start_day: DayValueObject
    end_day: DayValueObject
    
    def __init__(self, start_day: tuple[int, int], end_day: tuple[int, int]):
        object.__setattr__(self, "start_day", DayValueObject(start_day[0], start_day[1]))
        object.__setattr__(self, "end_day", DayValueObject(end_day[0], end_day[1]))
    
    def __post_init__(self):
        self.__ensure_is_valid_day_range(self.start_day, self.end_day)
        
    def __ensure_is_valid_day_range(self, start_day: DayValueObject, end_day: DayValueObject):
        if not start_day.is_before(end_day):
            raise ValueError("Start day must be before end day")
            #TODO: raise custom exception
            
    def get_value(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return self.start_day.get_value(), self.end_day.get_value()
    
    def is_in_range(self, day: int, month: int) -> bool:
        return self.start_day.is_equal(DayValueObject(day, month)) or \
                self.end_day.is_equal(DayValueObject(day, month)) or \
                (self.start_day.is_before(DayValueObject(day, month)) and \
                self.end_day.is_after(DayValueObject(day, month)))