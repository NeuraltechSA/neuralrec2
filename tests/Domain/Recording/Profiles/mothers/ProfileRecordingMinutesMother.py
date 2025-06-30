import random
from src.Domain.Recording.Profiles.ValueObjects.ProfileRecordingMinutes import ProfileRecordingMinutes


class ProfileRecordingMinutesMother:
    @staticmethod
    def create(minutes: int | None = None) -> ProfileRecordingMinutes:
        if minutes is None:
            minutes = random.randint(1, 120)
        return ProfileRecordingMinutes(minutes)

    @staticmethod
    def create_invalid() -> ProfileRecordingMinutes:
        return ProfileRecordingMinutes(random.randint(121, 1000))