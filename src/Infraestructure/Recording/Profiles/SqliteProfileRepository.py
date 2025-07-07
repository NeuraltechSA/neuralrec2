from src.Domain.Recording.Profiles.Contracts.ProfileRepositoryInterface import ProfileRepositoryInterface

import datetime
from src.Domain.Recording.Profiles.Entities.Profile import Profile

class SqliteProfileRepository(ProfileRepositoryInterface):
    profiles: list[Profile] = [
        Profile(
                id="c32d8b45-92fe-44f6-8b61-42c2107dfe87",
                uri="rtsp://admin:neuraltech2025@localhost:8844",
                day_range=((1, 1), (31, 12)),
                time_range=((0, 0), (23, 59)),
                recording_minutes=60,
                weekdays=[0, 1, 2, 3, 4, 5, 6],
                is_recording=False
        ),
        Profile(
                id="c32d8b45-92fe-44f6-8b61-42c2107dfe88",
                uri="rtsp://admin:neuraltech2025@localhost:8845",
                day_range=((1, 1), (31, 12)),
                time_range=((0, 0), (23, 59)),
                recording_minutes=60,
                weekdays=[0, 1, 2, 3, 4, 5, 6],
                is_recording=False
            )
    ]
    
    def __init__(self, db_path: str):
        self.__db_path = db_path

    def find_ready_to_record(self, date: datetime.datetime) -> list[Profile]:
        # TODO: check if the profile is in the range of the date
        return [p for p in self.profiles if not p.is_recording.value]

    def find_one_by_id(self, id: str) -> Profile | None:
        return next((p for p in self.profiles if p.id == id), None)
    
    def save(self, profile: Profile) -> None:
        if profile.id not in [p.id for p in self.profiles]:
            self.profiles.append(profile)
        else:
            self.profiles[self.profiles.index(profile)] = profile