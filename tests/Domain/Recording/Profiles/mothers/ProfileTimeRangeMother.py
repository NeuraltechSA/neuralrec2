from src.Domain.Recording.Profiles.ValueObjects.ProfileTimeRange import ProfileTimeRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileTime import ProfileTime
import random

class ProfileTimeRangeMother:
    @staticmethod
    def create() -> ProfileTimeRange:
        start_time = (random.randint(0, 23), random.randint(0, 59))
        end_time = (random.randint(0, 23), random.randint(0, 59))
        
        # Ensure end_time is after start_time
        while (start_time[0] > end_time[0] or (start_time[0] == end_time[0] and start_time[1] >= end_time[1])):
            end_time = (random.randint(0, 23), random.randint(0, 59))

        return ProfileTimeRange(start_time, end_time)