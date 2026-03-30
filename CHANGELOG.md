# CHANGELOG

## [Unreleased]

### Added

- FastAPI backend in `src/api.py` exposing `POST /record` and `GET /records` endpoints
  backed by a shared in-memory `FlightRecorder(capacity=100)` instance.
- HTML frontend in `templates/index.html` served at `/`; allows submitting transitions
  and viewing the recorded list via plain JavaScript fetch.
- 8 API tests in `tests/test_api.py` covering: record creation, retrieval, ordering,
  validation rejection, default empty actions, circular-buffer overflow, and HTML response.
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
