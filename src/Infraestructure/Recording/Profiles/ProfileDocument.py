from uuid import UUID, uuid4
from beanie import Document, PydanticObjectId
from typing import List

from pydantic import Field
from src.Domain.Recording.Profiles.Entities.Profile import Profile

class ProfileDocument(Document):
    id: UUID =  Field(default_factory=uuid4)
    uri: str
    day_range: tuple[tuple[int, int], tuple[int, int]]
    time_range: tuple[tuple[int, int], tuple[int, int]]
    recording_minutes: int
    weekdays: List[int]
    is_recording: bool = False
    
    
    @staticmethod
    def map_from(profile: Profile):
        return ProfileDocument(
            id=UUID(profile.id.value),
            uri=profile.uri.value,
            day_range=profile.day_range.value,
            time_range=profile.time_range.value,
            recording_minutes=profile.recording_minutes.value,
            weekdays=[day.value for day in profile.weekdays.value],
            is_recording=profile.is_recording.value
        )
    
    def map_to(self) -> 'Profile':
        return Profile(
            id=str(self.id),
            uri=self.uri,
            day_range=self.day_range,
            time_range=self.time_range,
            recording_minutes=self.recording_minutes,
            weekdays=self.weekdays,
            is_recording=self.is_recording
        )
    
    
    class Settings:
        name = "profiles"