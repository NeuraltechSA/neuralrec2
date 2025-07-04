from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface

import datetime
from src.Domain.Recording.Profiles.Entities.Profile import Profile

class SqliteProfileRepository(ProfileRepositoryInterface):
    profiles: list[Profile] = [
        Profile(
                id="c32d8b45-92fe-44f6-8b61-42c2107dfe87",
                uri="http://webcam01.ecn.purdue.edu/mjpg/video.mjpg",
                day_range=((1, 1), (31, 12)),
                time_range=((0, 0), (23, 59)),
                recording_minutes=60,
                weekdays=[0, 1, 2, 3, 4, 5, 6],
                is_recording=False
        ),
        Profile(
                id="c32d8b45-92fe-44f6-8b61-42c2107dfe88",
                uri="http://webcam.rhein-taunus-krematorium.de/mjpg/video.mjpg",
                day_range=((1, 1), (31, 12)),
                time_range=((0, 0), (23, 59)),
                recording_minutes=60,
                weekdays=[0, 1, 2, 3, 4, 5, 6],
                is_recording=False
            )
    ]
    
    def __init__(self, db_path: str):
        self.__db_path = db_path

    def find_active(self, date: datetime.datetime) -> list[Profile]:
        # TODO: check if the profile is in the range of the date
        return [p for p in self.profiles if not p.is_recording.value]

    def find_one_by_id(self, id: str) -> Profile | None:
        return next((p for p in self.profiles if p.id == id), None)
    
    def save(self, profile: Profile) -> None:
        self.profiles.append(profile)