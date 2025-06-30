from datetime import datetime
from src.Domain.Recording.Profiles.ValueObjects.ProfileDayRange import ProfileDayRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileTimeRange import ProfileTimeRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileWeekdays import ProfileWeekdays
from tests.Domain.Recording.Profiles.mothers.ProfileMother import ProfileMother
import pytest

class TestProfile:
    
    '''
    @pytest.mark.parametrize("now, start_day, end_day, start_time, end_time, weekdays, expected_result", 
    [
        # Now is january 1st. Recording is allowed from january 1st to december 31st
        (
            datetime(2025, 1, 1, 12, 0, 0), 
            (1, 1), (1, 12), 
            (0, 0), (23, 59), 
            [0, 1, 2, 3, 4, 5, 6],
            True
        ),
        # Now is december 31st. Recording is allowed from january 1st to december 31st
        (
            datetime(2025, 12, 31, 12, 0, 0), 
            (1, 1), (31, 12), 
            (0, 0), (23, 59), 
            [0, 1, 2, 3, 4, 5, 6],
            True
        ),
        # Now is june 1st. Recording is allowed from january 1st to december 31st
        (
            datetime(2025, 6, 1, 12, 0, 0), 
            (1, 1), (31, 12), 
            (0, 0), (23, 59), 
            [0, 1, 2, 3, 4, 5, 6],
            True
        ),
        # Now is january 1st. Recording is allowed from january 1st to january 1st
        (
            datetime(2025, 1, 1, 12, 0, 0), 
            (1, 1), (1, 1), 
            (0, 0), (23, 59), 
            [0, 1, 2, 3, 4, 5, 6],
            True
        ),
        # Now is january 1st. Recording is allowed from january 2nd to january 3rd
        (
            datetime(2025, 1, 1, 12, 0, 0), 
            (2, 1), (3, 1), 
            (0, 0), (23, 59), 
            [0, 1, 2, 3, 4, 5, 6],
            False
        ),
        # Now is 00:00:00. Recording is allowed from 00:00 to 23:59
        (
            datetime(2025, 1, 1, 0, 0, 0), 
            (1, 1), (31, 12), 
            (0, 0), (23, 59), 
            [0, 1, 2, 3, 4, 5, 6],
            True
        ),
        # Now is 23:59:59. Recording is allowed from 00:00 to 23:59
        (
            datetime(2025, 1, 1, 23, 59, 59), 
            (1, 1), (31, 12), 
            (0, 0), (23, 59), 
            [0, 1, 2, 3, 4, 5, 6],
            True
        )
    ])
    def test_in_range_should_return_expected_result(
        self, now, start_day, end_day, start_time, end_time, weekdays, expected_result):
        # Given
        profile = ProfileMother.create(
            day_range=ProfileDayRange(start_day, end_day),
            time_range=ProfileTimeRange(start_time, end_time),
            weekdays=ProfileWeekdays(weekdays)
        )
        
        # When
        result = profile.is_in_range(now)
        
        # Then
        assert result is expected_result
    '''
    
    @pytest.mark.parametrize("now, start_time, end_time, expected_result", 
    [
        # Now is 00:00:00. Recording is allowed from 00:00 to 23:59
        ( datetime(2025, 1, 1, 0, 0, 0), (0, 0), (23, 59)),
        # Now is 23:59:59. Recording is allowed from 00:00 to 23:59
        (datetime(2025, 1, 1, 23, 59, 59),(0, 0), (23, 59)),
        # Now is 00:00:00. Recording is allowed from 00:00 to 23:59
        (datetime(2025, 1, 1, 0, 0, 0), (0, 0), (23, 59)),
        # Now is 23:59:59. Recording is allowed from 00:00 to 23:59
        (datetime(2025, 1, 1, 23, 59, 59), (0, 0), (23, 59)),
    ])
    def test_time_should_be_in_range(
        self, now, start_time, end_time):
        # Given
        profile = ProfileMother.create(
            day_range=ProfileDayRange((1, 1), (31, 12)),
            time_range=ProfileTimeRange(start_time, end_time),
            weekdays=ProfileWeekdays([0, 1, 2, 3, 4, 5, 6])
        )
        
        # When
        result = profile.is_in_range(now)
        
        # Then
        assert result is True