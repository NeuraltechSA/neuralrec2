import time
from src.Domain.Recording.Profiles.Contracts.ProfileSleeperInterface import ProfileSleeperInterface

class ProfileSleeper(ProfileSleeperInterface):
    def sleep(self, seconds: int) -> None:
        time.sleep(seconds)