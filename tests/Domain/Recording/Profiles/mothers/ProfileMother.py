import datetime
from src.Domain.Recording.Profiles.ValueObjects.ProfileDayRange import ProfileDayRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileTimeRange import ProfileTimeRange
from src.Domain.Recording.Profiles.ValueObjects.ProfileWeekdays import ProfileWeekdays
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.ValueObjects.ProfileCameraUri import ProfileCameraUri
from src.Domain.Recording.Profiles.ValueObjects.ProfileId import ProfileId
from tests.Domain.Recording.Profiles.mothers.ProfileCameraUriMother import ProfileCameraUriMother
from tests.Domain.Recording.Profiles.mothers.ProfileDayRangeMother import ProfileDayRangeMother
from tests.Domain.Recording.Profiles.mothers.ProfileTimeRangeMother import ProfileTimeRangeMother
from tests.Domain.Recording.Profiles.mothers.ProfileWeekdaysMother import ProfileWeekdaysMother
from tests.Domain.Recording.Profiles.mothers.ProfileIdMother import ProfileIdMother
from tests.Domain.Recording.Profiles.mothers.ProfileRecordingMinutesMother import ProfileRecordingMinutesMother
from tests.Domain.Recording.Profiles.mothers.ProfileVideoPrefixMother import ProfileVideoPrefixMother
from src.Domain.Recording.Profiles.ValueObjects.ProfileDay import ProfileDay
from src.Domain.Recording.Profiles.ValueObjects.ProfileTime import ProfileTime
from src.Domain.Recording.Profiles.ValueObjects.ProfileRecordingMinutes import ProfileRecordingMinutes
from src.Domain.Recording.Profiles.ValueObjects.ProfileWeekdays import ProfileWeekdays

class ProfileMother:
    @staticmethod
    def create(
        id: str | None = None,
        uri: str | None = None,
        day_range: tuple[tuple[int, int],tuple[int, int]] | None = None,
        time_range: tuple[tuple[int, int],tuple[int, int]] | None = None,
        recording_minutes: int | None = None,
        weekdays: list[int] | None = None,
        is_recording: bool | None = None,
        video_prefix: str | None = None
    ) -> Profile:

        return Profile(
            id=ProfileIdMother.create(id).value,
            uri=ProfileCameraUriMother.create(uri).value,
            day_range=ProfileDayRangeMother.create(day_range).value,
            time_range=ProfileTimeRangeMother.create(time_range).value,
            recording_minutes=ProfileRecordingMinutesMother.create(recording_minutes).value,
            weekdays=[weekday.value for weekday in ProfileWeekdaysMother.create(weekdays).value],
            is_recording=is_recording if is_recording is not None else False,
            video_prefix=ProfileVideoPrefixMother.create(video_prefix).value
        )
        