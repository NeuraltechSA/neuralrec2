from dataclasses import dataclass
from src.Domain.SharedKernel.ValueObjects.TimeValueObject import TimeValueObject

@dataclass(frozen=True)
class TimeRangeValueObject:
    start_time: TimeValueObject
    end_time: TimeValueObject
    
    def __init__(self, start_time: tuple[int, int], end_time: tuple[int, int]):
        object.__setattr__(self, "start_time", TimeValueObject(start_time[0], start_time[1]))
        object.__setattr__(self, "end_time", TimeValueObject(end_time[0], end_time[1]))
    
    def __post_init__(self):
        self.__ensure_is_valid_time_range(self.start_time, self.end_time)
        
    def __ensure_is_valid_time_range(self, start_time: TimeValueObject, end_time: TimeValueObject):
        if not start_time.is_before(end_time):
            raise ValueError("Start time must be before end time")
            #TODO: raise custom exception
            
    def get_value(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return self.start_time.get_value(), self.end_time.get_value()
    
    def is_in_range(self, hour: int, minute: int) -> bool:
        return self.start_time.is_equal(TimeValueObject(hour, minute)) or \
                self.end_time.is_equal(TimeValueObject(hour, minute)) or \
                (self.start_time.is_before(TimeValueObject(hour, minute)) and \
                self.end_time.is_after(TimeValueObject(hour, minute)))