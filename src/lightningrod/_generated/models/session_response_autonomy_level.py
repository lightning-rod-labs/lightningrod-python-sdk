from enum import Enum


class SessionResponseAutonomyLevel(str, Enum):
    AUTONOMOUS = "autonomous"
    GUIDED = "guided"
    SEMI_AUTO = "semi_auto"

    def __str__(self) -> str:
        return str(self.value)
