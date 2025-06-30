from datetime import datetime
from src.Domain.Recording.Profiles.ValueObjects.ProfileDayRange import ProfileDayRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileTimeRange import ProfileTimeRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileWeekdays import ProfileWeekdays
from tests.Domain.Recording.Profiles.mothers.ProfileMother import ProfileMother
import pytest

class TestProfile:
    
    @pytest.mark.parametrize("now, start_time, end_time", 
    [
        # Now is 00:00:00. Recording is allowed from 00:00 to 23:59
        ( datetime(2025, 1, 1, 0, 0, 0), (0, 0), (23, 59)),
        # Now is 23:59:59. Recording is allowed from 00:00 to 23:59
        (datetime(2025, 1, 1, 23, 59, 59),(0, 0), (23, 59)),
        # Now is 00:00:00. Recording is allowed from 00:00 to 23:59
        (datetime(2025, 1, 1, 0, 0, 0), (0, 0), (23, 59)),
        # Now is 23:59:59. Recording is allowed from 00:00 to 23:59
        (datetime(2025, 1, 1, 23, 59, 59), (0, 0), (23, 59))
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
        
    @pytest.mark.parametrize("now, start_day, end_day", 
    [
        # Now is january 1st. Recording is allowed from january 1st to december 31st
        (datetime(2025, 1, 1, 0, 0, 0), (1, 1), (31, 12)),
        # Now is december 31st. Recording is allowed from january 1st to december 31st
        (datetime(2025, 12, 31, 0, 0, 0), (1, 1), (31, 12)),
        # Now is june 1st. Recording is allowed from january 1st to december 31st
        (datetime(2025, 6, 1, 0, 0, 0), (1, 1), (31, 12)),
        # Now is january 1st. Recording is allowed from january 1st to january 1st
        (datetime(2025, 1, 1, 0, 0, 0), (1, 1), (1, 1)),
    ])
    def test_day_should_be_in_range(
        self, now, start_day, end_day):
        # Given
        profile = ProfileMother.create(
            day_range=ProfileDayRange(start_day, end_day),
            time_range=ProfileTimeRange((0, 0), (23, 59)),
            weekdays=ProfileWeekdays([0, 1, 2, 3, 4, 5, 6])
        )
        
        # When
        result = profile.is_in_range(now)
        
        # Then
        assert result is True
        
    @pytest.mark.parametrize("now, weekdays", 
    [
        # Now is monday. Recording is allowed on monday
        (datetime(2025, 6, 2, 0, 0, 0), [0, 1, 2, 3, 4]),
        # Now is friday. Recording is allowed on friday
        (datetime(2025, 6, 6, 0, 0, 0), [0, 1, 2, 3, 4]),
        # Now is wednesday. Recording is allowed on wednesday
        (datetime(2025, 6, 4, 0, 0, 0), [0, 1, 2, 3, 4])
    ])
    def test_weekday_should_be_in_range(
        self, now, weekdays):
        # Given
        profile = ProfileMother.create(
            day_range=ProfileDayRange((1, 1), (31, 12)),
            time_range=ProfileTimeRange((0, 0), (23, 59)),
            weekdays=ProfileWeekdays(weekdays)
        )
        
        # When
        result = profile.is_in_range(now)
        
        # Then
        assert result is True
        
    @pytest.mark.parametrize("now, start_day, end_day", 
    [
        # Now is january 1st. Recording is allowed from january 2nd to january 31st
        (datetime(2025, 1, 1, 0, 0, 0), (2, 1), (31, 1)),
        # Now is february 1st. Recording is allowed from january 2nd to january 31st
        (datetime(2025, 2, 1, 0, 0, 0), (2, 1), (31, 1)),
    ])
    def test_day_should_not_be_in_range(
        self, now, start_day, end_day):
        # Given
        profile = ProfileMother.create(
            day_range=ProfileDayRange(start_day, end_day),
            time_range=ProfileTimeRange((0, 0), (23, 59)),
            weekdays=ProfileWeekdays([0, 1, 2, 3, 4, 5, 6])
        )
        
        # When
        result = profile.is_in_range(now)
        
        # Then
        assert result is False
        
    @pytest.mark.parametrize("now, start_time, end_time", 
    [
        # Now is 00:09:59. Recording is allowed from 10:00 to 20:00
        (datetime(2025, 1, 1, 0, 9, 59), (10, 0), (20, 00)),
        # Now is 20:01:00. Recording is allowed from 10:00 to 20:00
        (datetime(2025, 1, 1, 20, 1, 0), (10, 0), (20, 00))
    ])
    def test_time_should_not_be_in_range(
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
        assert result is False
        