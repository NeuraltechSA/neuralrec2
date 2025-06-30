import uuid
from src.Domain.Recording.Profiles.ValueObjects.ProfileCameraUri import ProfileCameraUri


class ProfileCameraUriMother:
    @staticmethod
    def create(uri: str | None = None) -> ProfileCameraUri:
        if uri is None:
            uri = f"rtsp://admin:123456@localhost:8080/camera/{uuid.uuid4()}"
        return ProfileCameraUri(uri)
    