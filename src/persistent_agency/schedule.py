from __future__ import annotations

from datetime import datetime, time

from .state import OperatingMode


class CircadianSchedule:
    """Prototype schedule from the paper.

    The schedule changes operating priorities. It does not generate thoughts.
    """

    def mode_at(self, timestamp: datetime) -> OperatingMode:
        t = timestamp.time()
        if time(7, 0) <= t < time(8, 0):
            return OperatingMode.ORIENTATION
        if time(8, 0) <= t < time(12, 0):
            return OperatingMode.HUMAN_WORK
        if time(12, 0) <= t < time(13, 0):
            return OperatingMode.OPEN_COGNITION
        if time(13, 0) <= t < time(17, 0):
            return OperatingMode.HUMAN_WORK
        if time(17, 0) <= t < time(21, 0):
            return OperatingMode.AUTONOMOUS_COGNITION
        return OperatingMode.CONSOLIDATION
