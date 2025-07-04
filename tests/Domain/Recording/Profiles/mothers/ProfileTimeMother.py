import random
from src.Domain.Recording.Profiles.ValueObjects.ProfileTime import ProfileTime


class ProfileTimeMother:
    @staticmethod
    def create(hour: int = -1, minute: int = -1, second: int = -1) -> ProfileTime:
        if hour == -1:
            hour = random.randint(0, 23)
        if minute == -1:
            minute = random.randint(0, 59)
            
        return ProfileTime(hour, minute)
    
