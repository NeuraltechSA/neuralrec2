from dataclasses import dataclass

@dataclass(frozen=True)
class ProfileRecordingFinishedEvent:
    profile_id: str
    recording_path: str