from datetime import datetime
import random
from src.Domain.Recording.Profiles.ValueObjects.ProfileDay import ProfileDay


class ProfileDayMother:
    @staticmethod
    def create(day: int | None = None, 
               month: int | None = None
    ) -> ProfileDay:
        if month is None:
            month = random.randint(1, 12)
        if day is None:
            # Validate the date before creating datetime to avoid outº of range errors
            days_in_month = {
                1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
            }
            max_days = days_in_month.get(month, 28)
            day = random.randint(1, max_days)
        
        return ProfileDay(day, month)
    
    
    