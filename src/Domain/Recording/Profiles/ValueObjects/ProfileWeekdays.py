from dataclasses import dataclass
from src.Domain.Recording.Profiles.ValueObjects.ProfileWeekday import ProfileWeekday

@dataclass(frozen=True)
class ProfileWeekdays:
    value:list[ProfileWeekday]
    
    def __init__(self, value: list[int]):
        object.__setattr__(self, "value", [ProfileWeekday(index) for index in value])
    
    def __post_init__(self):
        self.ensure_is_not_empty(self.value)
        self.ensure_no_duplicates(self.value)
        
    def ensure_no_duplicates(self, value: list[ProfileWeekday]):
        if len(value) != len(set(value)):
            raise ValueError("Weekdays cannot have duplicates")
            #TODO: raise custom exception
        
    def ensure_is_not_empty(self, value: list[ProfileWeekday]):
        if len(value) == 0:
            raise ValueError("Weekdays cannot be empty")
            #TODO: raise custom exception
            
    def is_weekday_allowed(self, weekday: int) -> bool:
        return any(weekday == w.value for w in self.value)