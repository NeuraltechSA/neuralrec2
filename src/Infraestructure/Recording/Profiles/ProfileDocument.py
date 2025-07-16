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
    recording_seconds: int
    weekdays: List[int]
    is_recording: bool = False
    video_prefix: str
    
    
    @staticmethod
    def map_from(profile: Profile):
        return ProfileDocument(
            id=UUID(profile.id.value),
            uri=profile.uri.value,
            day_range=profile.day_range.value,
            time_range=profile.time_range.value,
            recording_seconds=profile.recording_seconds.value,
            weekdays=[day.value for day in profile.weekdays.value],
            is_recording=profile.is_recording.value,
            video_prefix=profile.video_prefix.value
        )
    
    def map_to(self) -> 'Profile':
        dump = self.model_dump()
        return Profile(
            id=str(dump["id"]),
            uri=dump["uri"],
            day_range=dump["day_range"],
            time_range=dump["time_range"],
            recording_seconds=dump["recording_seconds"],
            weekdays=dump["weekdays"],
            is_recording=dump["is_recording"],
            video_prefix=dump["video_prefix"]
        )
    
    
    class Settings:
        name = "profiles"