from random import random
from src.Domain.Recording.Profiles.ValueObjects.ProfileWeekday import ProfileWeekday


class ProfileWeekdayIndexMother:
    @staticmethod
    def create(index: int = -1) -> ProfileWeekday:
        if index == -1:
            index = random.randint(0, 6)
        return ProfileWeekday(index)
    
    @staticmethod
    def create_invalid() -> ProfileWeekday:
        return ProfileWeekday(random.randint(7, 100))