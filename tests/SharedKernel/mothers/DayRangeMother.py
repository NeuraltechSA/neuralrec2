from src.Domain.SharedKernel.ValueObjects.DayRangeValueObject import DayRangeValueObject

class DayRangeMother:
    @staticmethod
    def create(start: int, end: int) -> DayRange:
        return DayRange(start, end)