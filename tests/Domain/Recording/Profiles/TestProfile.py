from datetime import datetime
from src.Domain.Recording.Profiles.Exceptions.ProfileAlreadyRecordingException import ProfileAlreadyRecordingException
from src.Domain.Recording.Profiles.Exceptions.ProfileOutOfRangeException import ProfileOutOfRangeException
from tests.Domain.Recording.Profiles.mothers.ProfileMother import ProfileMother
import pytest

class TestProfile:
    @pytest.mark.parametrize("now, start_time, end_time", 
    [
        # Now is 00:00:00. Recording is allowed from 00:00 to 23:59
        (datetime(2025, 1, 1, 0, 0, 0), (0, 0), (23, 59)),
        # Now is 23:59:59. Recording is allowed from 00:00 to 23:59
        (datetime(2025, 1, 1, 23, 59, 59),(0, 0), (23, 59)),
        # Now is 22:00:00. Recording is allowed. from 08:00 to 23:00
        (datetime(2025, 1, 1, 22, 0, 0), (8, 0), (23,0)),
        # Now is 22:00:00. Recording is allowed from 21:00 to 06:00
        (datetime(2025, 1, 1, 22, 0, 0), (21, 0), (6, 0)),
        # Now is 05:00:00. Recording is allowed from 21:00 to 06:00
        (datetime(2025, 1, 1, 5, 0, 0), (21, 0), (6, 0))
    
    ])
    def test_time_should_be_in_range(
        self, now, start_time, end_time):
        # Given
        profile = ProfileMother.create(
            day_range=((1, 1), (31, 12)),
            time_range=(start_time, end_time),
            weekdays=[0, 1, 2, 3, 4, 5, 6]
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
        # Now is december 11th. Recording is allowed from december 10th to january 31st
        (datetime(2025, 12, 11, 0, 0, 0), (10, 12), (31, 1)),
        # Now is january 10th. Recording is allowed from december 10th to january 31st
        (datetime(2025, 1, 10, 0, 0, 0), (10, 12), (31, 1))
    ])
    def test_day_should_be_in_range(
        self, now, start_day, end_day):
        # Given
        profile = ProfileMother.create(
            day_range=(start_day, end_day),
            time_range=((0, 0), (23, 59)),
            weekdays=[0, 1, 2, 3, 4, 5, 6]
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
    ], ids=[
        'Monday on Monday-Tuesday-Wednesday-Thursday-Friday',
        'Friday on Monday-Tuesday-Wednesday-Thursday-Friday',
        'Wednesday on Monday-Tuesday-Wednesday-Thursday-Friday'
    ])
    def test_weekday_should_be_in_range(
        self, now, weekdays):
        # Given
        profile = ProfileMother.create(
            day_range=((1, 1), (31, 12)),
            time_range=((0, 0), (23, 59)),
            weekdays=weekdays
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
        # Now is december 9th. Recording is allowed from december 10th to january 31st
        (datetime(2025, 12, 9, 0, 0, 0), (10, 12), (31, 1)),
        # Now is february 1st. Recording is allowed from december 10th to january 31st
        (datetime(2025, 2, 1, 0, 0, 0), (10, 12), (31, 1))
    ], ids=[
        '01/01 in 02/01-31/01',
        '01/02 in 02/01-31/01',
        '09/12 in 10/12-31/01',
        '01/02 in 10/12-31/01'
    ])
    def test_day_should_not_be_in_range(
        self, now, start_day, end_day):
        # Given
        profile = ProfileMother.create(
            day_range=(start_day, end_day),
            time_range=((0, 0), (23, 59)),
            weekdays=[0, 1, 2, 3, 4, 5, 6]
        )
        
        # When
        result = profile.is_in_range(now)
        
        # Then
        assert result is False
        
    @pytest.mark.parametrize("now, start_time, end_time", 
    [
        (datetime(2025, 1, 1, 0, 9, 59), (10, 0), (20, 00)),
        (datetime(2025, 1, 1, 20, 1, 0), (10, 0), (20, 00)),
        (datetime(2025, 1, 1, 6, 1, 0), (21, 0), (6, 0)),
        (datetime(2025, 1, 1, 20, 59, 0), (21, 0), (6, 0)),
    ], ids=[
        '00:09:59 in 10:00-20:00', 
        '20:01:00 in 10:00-20:00', 
        '06:01:00 in 21:00-06:00', 
        '20:59:00 in 21:00-06:00'])
    def test_time_should_not_be_in_range(
        self, now, start_time, end_time):
        # Given
        profile = ProfileMother.create(
            day_range=((1, 1), (31, 12)),
            time_range=(start_time, end_time),
            weekdays=[0, 1, 2, 3, 4, 5, 6]
        )
        
        # When
        result = profile.is_in_range(now)
        
        # Then
        assert result is False
    
    @pytest.mark.parametrize("now, weekdays", 
    [
        (datetime(2025, 6, 2, 0, 0, 0), [1, 2, 3, 4]),
        (datetime(2025, 6, 6, 0, 0, 0), [0, 1, 2, 3]),
        (datetime(2025, 6, 4, 0, 0, 0), [0, 1, 3, 4])
    ], ids=[
        'Monday not in Tuesday-Wednesday-Thursday-Friday',
        'Friday not in Monday-Tuesday-Wednesday-Thursday',
        'Wednesday not in Monday-Tuesday-Thursday-Friday'
    ])
    def test_weekday_should_not_be_in_range(
        self, now, weekdays):
        # Given
        profile = ProfileMother.create(
            day_range=((1, 1), (31, 12)),
            time_range=((0, 0), (23, 59)),
            weekdays=weekdays
        )
        
        # When
        result = profile.is_in_range(now)
        
        # Then
        assert result is False
    
        
    def test_ensure_is_ready_to_record_should_raise_exception_if_not_in_range(
        self):
        # Given
        profile = ProfileMother.create(
            day_range=((2, 1), (31, 12)),
            time_range=((0, 0), (23, 59)),
            weekdays=[0, 1, 2, 3, 4, 5, 6]
        )
        
        # When/Then
        with pytest.raises(ProfileOutOfRangeException):
            profile.ensure_is_ready_to_record(datetime(2025, 1, 1, 0, 0, 0))
    
    def test_ensure_is_ready_to_record_should_not_raise_exception_if_in_range(
        self):
        # Given
        profile = ProfileMother.create(
            day_range=((1, 1), (31, 12)),
            time_range=((0, 0), (23, 59)),
            weekdays=[0, 1, 2, 3, 4, 5, 6]
        )
        
        # When/Then
        profile.ensure_is_ready_to_record(datetime(2025, 1, 1, 0, 0, 0))
    
    def test_ensure_is_ready_to_record_should_raise_exception_if_already_recording(
        self):
        # Given
        profile = ProfileMother.create(
            day_range=((1, 1), (31, 12)),
            time_range=((0, 0), (23, 59)),
            weekdays=[0, 1, 2, 3, 4, 5, 6],
            is_recording=True
        )
        
        # When/Then
        with pytest.raises(ProfileAlreadyRecordingException):
            profile.ensure_is_ready_to_record(datetime(2025, 1, 1, 0, 0, 0))
    
    def test_ensure_is_ready_to_record_should_not_raise_exception_if_not_recording(
        self):
        # Given
        profile = ProfileMother.create(
            day_range=((1, 1), (31, 12)),
            time_range=((0, 0), (23, 59)),
            weekdays=[0, 1, 2, 3, 4, 5, 6],
            is_recording=False
        )
        
        # When/Then
        profile.ensure_is_ready_to_record(datetime(2025, 1, 1, 0, 0, 0))
        
    def test_set_recording_started_should_set_is_recording_to_true(
        self):
        # Given
        profile = ProfileMother.create(
            day_range=((1, 1), (31, 12)),
            time_range=((0, 0), (23, 59)),
            weekdays=[0, 1, 2, 3, 4, 5, 6],
            is_recording=False
        )
        
        # When
        profile.set_recording_started()
        
        # Then
        assert profile.is_recording.value is True