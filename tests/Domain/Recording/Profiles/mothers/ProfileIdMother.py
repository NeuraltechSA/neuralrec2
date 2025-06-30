import uuid
from src.Domain.Recording.Profiles.ValueObjects.ProfileId import ProfileId


class ProfileIdMother:
    @staticmethod
    def create(id: str | None = None) -> ProfileId:
        if id is None:
            id = str(uuid.uuid4())
        return ProfileId(id)
