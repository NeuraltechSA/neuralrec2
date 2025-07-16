import random
from src.Domain.Recording.Profiles.ValueObjects.ProfileDayRange import ProfileDayRange
from tests.Domain.Recording.Profiles.mothers.ProfileDayMother import ProfileDayMother

class ProfileDayRangeMother:
    @staticmethod
    def create(
        day_range: tuple[tuple[int, int],tuple[int, int]] | None = None
    ) -> ProfileDayRange:
        if day_range is None:
            day_range = (
                (
                    ProfileDayMother.create().value, 
                    ProfileDayMother.create().value
                )
            )

        return ProfileDayRange(
            day_range[0], 
            day_range[1]
        )