from dataclasses import dataclass
from typing_extensions import override
from src.Domain.SharedKernel.DomainEvent import DomainEvent
from typing import final

@dataclass(frozen=True)
@final
class RecordingFinishedEvent(DomainEvent):
    profile_id: str
    video_path: str
    
    @property
    @override
    def event_name(self) -> str:
        return "recording_finished"