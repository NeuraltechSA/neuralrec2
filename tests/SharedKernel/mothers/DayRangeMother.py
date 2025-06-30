from src.SharedKernel.ValueObjects.DayRange import DayRange


class DayRangeMother:
    @staticmethod
    def create(start: int, end: int) -> DayRange:
        return DayRange(start, end)