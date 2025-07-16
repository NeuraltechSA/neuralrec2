import random
from src.Domain.Recording.Profiles.ValueObjects.ProfileRecordingSeconds import ProfileRecordingSeconds


class ProfileRecordingSecondsMother:
    @staticmethod
    def create(seconds: int | None = None) -> ProfileRecordingSeconds:
        if seconds is None:
            seconds = random.randint(1, 7200)
        return ProfileRecordingSeconds(seconds)

    @staticmethod
    def create_invalid() -> ProfileRecordingSeconds:
        return ProfileRecordingSeconds(random.randint(7201, 10000)) 