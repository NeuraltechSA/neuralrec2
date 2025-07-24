from dataclasses import dataclass
from src.Domain.Recording.Profiles.Entities.Profile import Profile

@dataclass(frozen=True)
class ProfilesToRecord:
    value: list[Profile]
    max_profiles: int = 6

    def __post_init__(self):
        self.ensure_is_not_empty()
        self.ensure_no_duplicates()
        self.ensure_max_profiles()
    
    
    def ensure_is_not_empty(self):
        if len(self.value) == 0:
            # TODO: raise custom exception
            raise ValueError("Profiles to record cannot be empty")

    def ensure_no_duplicates(self):
        if len(self.value) != len(set(self.value)):
            # TODO: raise custom exception
            raise ValueError("Profiles to record cannot have duplicates")
    
    def ensure_max_profiles(self):
        if len(self.value) > self.max_profiles:
            # TODO: raise custom exception
            raise ValueError("Profiles to record cannot have more than 6 profiles")
    
    def __iter__(self):
        return iter(self.value)
    
    def __len__(self):
        return len(self.value)