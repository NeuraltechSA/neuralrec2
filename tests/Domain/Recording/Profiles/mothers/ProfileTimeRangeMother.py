from src.Domain.Recording.Profiles.ValueObjects.ProfileTimeRange import ProfileTimeRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileTime import ProfileTime
import random

class ProfileTimeRangeMother:
    @staticmethod
    def create(time_range: tuple[tuple[int, int],tuple[int, int]] | None = None) -> ProfileTimeRange:
        if time_range is None:
            time_range = (
                (random.randint(0, 23), random.randint(0, 59)),
                (random.randint(0, 23), random.randint(0, 59))
            )

        return ProfileTimeRange(time_range[0], time_range[1])