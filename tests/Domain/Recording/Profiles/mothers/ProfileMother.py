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
from src.Domain.Recording.Profiles.ValueObjects.ProfileDay import ProfileDay
from src.Domain.Recording.Profiles.ValueObjects.ProfileTime import ProfileTime
from src.Domain.Recording.Profiles.ValueObjects.ProfileRecordingMinutes import ProfileRecordingMinutes
from src.Domain.Recording.Profiles.ValueObjects.ProfileWeekdays import ProfileWeekdays

class ProfileMother:
    @staticmethod
    def create(
        id: ProfileId | None = None,
        uri: ProfileCameraUri | None = None,
        day_range: ProfileDayRange | None = None,
        time_range: ProfileTimeRange | None = None,
        recording_minutes: ProfileRecordingMinutes | None = None,
        weekdays: ProfileWeekdays | None = None,
        is_recording: bool | None = None
    ) -> Profile:

        return Profile(
            id=id.value if id is not None else ProfileIdMother.create().value,
            uri=uri.value if uri is not None else ProfileCameraUriMother.create().value,
            day_range=day_range.get_value() if day_range is not None else ProfileDayRangeMother.create().get_value(),
            time_range=time_range.get_value() if time_range is not None else ProfileTimeRangeMother.create().get_value(),
            recording_minutes=recording_minutes.value if recording_minutes is not None else ProfileRecordingMinutesMother.create().value,
            weekdays= [weekday.value for weekday in (weekdays.value if weekdays is not None else ProfileWeekdaysMother.create().value)],
            is_recording=is_recording if is_recording is not None else False
        )