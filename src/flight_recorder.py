"""Flight recorder for finite state machine diagnostics."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class FlightRecord:
    """Immutable record of a single state machine transition."""

    current_state: str
    event: str
    actions_taken: tuple[str, ...]
    new_state: str


class FlightRecorder:
    """Circular buffer recording state machine transitions for diagnostics.

    Records are stored in chronological order. When the buffer is full,
    the oldest record is overwritten by the newest.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError(f"capacity must be a positive integer, got {capacity}")
        self._buffer: deque[FlightRecord] = deque(maxlen=capacity)

    def record(
        self,
        current_state: str,
        event: str,
        actions_taken: list[str],
        new_state: str,
    ) -> None:
        """Append a transition record to the circular buffer.

        If the buffer is full, the oldest record is overwritten.
        """
        self._buffer.append(
            FlightRecord(
                current_state=current_state,
                event=event,
                actions_taken=tuple(actions_taken),
                new_state=new_state,
            )
        )

    def get_records(self) -> list[FlightRecord]:
        """Return all stored records in chronological order (oldest first)."""
        return list(self._buffer)
