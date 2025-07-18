import datetime
from src.Domain.Recording.Profiles.Exceptions.ProfileAlreadyRecordingException import ProfileAlreadyRecordingException  
from src.Domain.Recording.Profiles.Exceptions.ProfileOutOfRangeException import ProfileOutOfRangeException
from src.Domain.Recording.Profiles.ValueObjects.ProfileIsRecording import ProfileIsRecording
from src.Domain.Recording.Profiles.ValueObjects.ProfileWeekdays import ProfileWeekdays
from src.Domain.Recording.Profiles.ValueObjects.ProfileId import ProfileId
from src.Domain.Recording.Profiles.ValueObjects.ProfileCameraUri import ProfileCameraUri
from src.Domain.Recording.Profiles.ValueObjects.ProfileRecordingSeconds import ProfileRecordingSeconds
from src.Domain.SharedKernel.AggregateRoot import AggregateRoot
from src.Domain.Recording.Profiles.ValueObjects.ProfileDayRange import ProfileDayRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileTimeRange import ProfileTimeRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoPrefix import ProfileVideoPrefix


class Profile(AggregateRoot):
    _id: ProfileId
    _video_prefix: ProfileVideoPrefix
    _uri: ProfileCameraUri
    _day_range: ProfileDayRange
    _time_range: ProfileTimeRange
    _recording_seconds: ProfileRecordingSeconds
    _weekdays: ProfileWeekdays
    _is_recording: ProfileIsRecording
    
    def __init__(
        self,
        id: str,
        uri: str,
        day_range: tuple[tuple[int, int], tuple[int, int]],
        time_range: tuple[tuple[int, int], tuple[int, int]],
        recording_seconds: int,
        weekdays: list[int],
        is_recording: bool,
        video_prefix: str
    ):
        self._id = ProfileId(id)
        self._uri = ProfileCameraUri(uri)
        self._day_range = ProfileDayRange(day_range[0], day_range[1])
        self._time_range = ProfileTimeRange(time_range[0], time_range[1])
        self._recording_seconds = ProfileRecordingSeconds(recording_seconds)
        self._weekdays = ProfileWeekdays(weekdays)
        self._is_recording = ProfileIsRecording(is_recording)
        self._video_prefix = ProfileVideoPrefix(video_prefix)
    @property
    def id(self) -> ProfileId:
        return self._id
    
    @property
    def uri(self) -> ProfileCameraUri:
        return self._uri
    
    @property
    def day_range(self) -> ProfileDayRange:
        return self._day_range
    
    @property
    def time_range(self) -> ProfileTimeRange:
        return self._time_range
    
    @property
    def recording_seconds(self) -> ProfileRecordingSeconds:
        return self._recording_seconds
    
    @property
    def weekdays(self) -> ProfileWeekdays:
        return self._weekdays
    
    @property
    def is_recording(self) -> ProfileIsRecording:
        return self._is_recording
    
    @property
    def video_prefix(self) -> ProfileVideoPrefix:
        return self._video_prefix
    
    def is_in_range(self, now: datetime.datetime) -> bool:
        if not self._day_range.is_in_range(now.day, now.month):
            return False
        if not self._time_range.is_in_range(now.hour, now.minute):
            return False
        if not self._weekdays.is_weekday_allowed(now.weekday()):
            return False
        return True
    
    def ensure_is_ready_to_record(self, now: datetime.datetime) -> None:
        if not self.is_in_range(now):
            raise ProfileOutOfRangeException(self._id.value)
        if self._is_recording.value:
            raise ProfileAlreadyRecordingException(self._id.value)
    
    def set_recording_started(self) -> None:
        self._is_recording = ProfileIsRecording(True)
        #TODO: trigger event
    
    def set_recording_stopped(self) -> None:
        self._is_recording = ProfileIsRecording(False)
        #TODO: trigger event
    
    
    # TODO: create method