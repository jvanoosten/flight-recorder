# CHANGELOG

## [Unreleased]

### Added

- `FlightRecorder` class in `src/flight_recorder.py` implementing a fixed-capacity circular
  buffer for recording state machine transitions.
  - `FlightRecorder(capacity: int)` — raises `ValueError` for non-positive capacity.
  - `record(current_state, event, actions_taken, new_state)` — appends a `FlightRecord`;
    overwrites the oldest entry when capacity is exceeded.
  - `get_records() -> list[FlightRecord]` — returns all stored records oldest-first.
- `FlightRecord` frozen dataclass with fields `current_state`, `event`, `actions_taken`
  (stored as `tuple[str, ...]`), and `new_state`.
- 15 unit tests in `tests/test_flight_recorder.py` covering normal operation, circular
  wraparound, edge cases (capacity=1, empty recorder, zero/negative capacity rejection).
