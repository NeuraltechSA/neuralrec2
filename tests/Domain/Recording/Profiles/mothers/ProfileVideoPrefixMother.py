import uuid
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoPrefix import ProfileVideoPrefix


class ProfileVideoPrefixMother:
    @staticmethod
    def create(video_prefix: str | None = None) -> ProfileVideoPrefix:
        if video_prefix is None:
            video_prefix = f"camera_{uuid.uuid4()}"
        return ProfileVideoPrefix(video_prefix) 