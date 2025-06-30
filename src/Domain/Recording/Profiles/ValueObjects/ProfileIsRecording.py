from dataclasses import dataclass

@dataclass(frozen=True)
class ProfileIsRecording:
    value: bool 