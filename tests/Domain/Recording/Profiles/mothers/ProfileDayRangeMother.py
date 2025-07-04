import random
from src.Domain.Recording.Profiles.ValueObjects.ProfileDayRange import ProfileDayRange

class ProfileDayRangeMother:
    @staticmethod
    def create(
        day_range: tuple[tuple[int, int],tuple[int, int]] | None = None
    ) -> ProfileDayRange:
        if day_range is None:
            day_range = (
                (random.randint(1, 31), random.randint(1, 12)),
                (random.randint(1, 31), random.randint(1, 12))
            )

        return ProfileDayRange(
            day_range[0], 
            day_range[1]
        )