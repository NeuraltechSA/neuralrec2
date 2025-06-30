from src.Domain.Recording.Profiles.ValueObjects.ProfileWeekdays import ProfileWeekdays
import random
        
class ProfileWeekdaysMother:
    @staticmethod
    def create() -> ProfileWeekdays:
        weekdays = random.sample(range(7), random.randint(0, 6))
        return ProfileWeekdays(weekdays)