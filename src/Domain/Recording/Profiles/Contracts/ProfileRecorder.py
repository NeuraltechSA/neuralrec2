import abc
from typing import Callable, final
from src.Domain.Recording.Profiles.Entities.Profile import Profile
from src.Domain.Recording.Profiles.ValueObjects.ProfileVideoStoragePath import ProfileVideoStoragePath
from src.Domain.SharedKernel.EventBusInterface import EventBusInterface
from src.Domain.Recording.Profiles.Events.RecordingFinishedEvent import RecordingFinishedEvent
from src.Domain.Recording.Profiles.ValueObjects.ProfilesToRecord import ProfilesToRecord

class ProfileRecorder(abc.ABC):
    
    def __init__(self, event_bus: EventBusInterface):
        self.__event_bus = event_bus

    @final
    def record_many_async(
        self, 
        profiles: ProfilesToRecord, 
        storage_path: ProfileVideoStoragePath
    ) -> None:
        for profile in profiles:
            self._record_async(
                profile, 
                storage_path, 
                lambda profile, video_path: self.__on_recording_finished_raise_event(profile, video_path))
    
    
    @final
    def __on_recording_finished_raise_event(self, profile: Profile, video_path:str) -> None:
        self.__event_bus.publish(RecordingFinishedEvent(profile.id.value, video_path))

    @abc.abstractmethod
    def _record_async(self, 
                      profile: Profile, 
                      storage_path: ProfileVideoStoragePath,
                      on_recording_finished: Callable[[Profile, str], None]):
        pass
    
    