import random
from src.Domain.Recording.Profiles.ValueObjects.ProfileDayRange import ProfileDayRange

class ProfileDayRangeMother:
    @staticmethod
    def create() -> ProfileDayRange:
        start_day = (random.randint(1, 31), random.randint(1, 12))
        end_day = (random.randint(1, 31), random.randint(1, 12))
        
        # Ensure end_day is after start_day
        while (start_day[1] > end_day[1] or (start_day[1] == end_day[1] and start_day[0] >= end_day[0])):
            end_day = (random.randint(1, 31), random.randint(1, 12))

        return ProfileDayRange(
            start_day, 
            end_day
        )