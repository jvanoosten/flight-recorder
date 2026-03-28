# Feature: Flight Recorder

## Problem
Components that use finite state machines to trigger actions based on 
current state and incoming events need a flight recorder that records the 
incoming events, actions taken, and new state.  The flight recorder 
is a diagnostic tool used to help debug issues in state machine rules.  

## Goal
Create a python object for recording the current state, incoming event, 
actions taken, and new state.

## Non-goals
- Persistent storage to disk
- Database integration
- Thread-safe or process-safe behavior unless later required
- Filtering or searching records
- Serialization or export formats
- Timestamps unless explicitly added later

## Public API

### Constructor
The `FlightRecorder` constructor should accept a fixed buffer size. 

Example:

```python
recorder = FlightRecorder(capacity=100)
```

### Methods 
record(...)

The object must expose a method with this signature:

```python
record(current_state: str, event: str, actions_taken: list, new_state: str) -> None
```
Behavior:

create a new record containing the four input values
append the record to the circular buffer
if the buffer is full, overwrite the oldest record

get_records()

The object must expose:

```python
get_records() -> list
```

Behavior:

return all currently stored records
records must be returned in chronological order from oldest to newest
returned records must reflect the current logical contents of the circular buffer

Record Structure

Each stored record must contain these fields:

current_state: str
event: str
actions_taken: list
new_state: str

Preferred representation:

either a dataclass
or a small immutable record structure

Example logical record:

```python
{
    "current_state": "Idle",
    "event": "start",
    "actions": {"turn_key", "start_engine",
    "new_state": "Running"
}
```

Buffer Behavior
Capacity

The recorder has a fixed maximum capacity set at construction time.

Append behavior

If the buffer is not full:

append the new record

If the buffer is full:

overwrite the oldest record
maintain correct chronological ordering in get_records()
Ordering

get_records() must always return records in logical time order:

oldest surviving record first
newest record last

Error Handling

The initial implementation should assume all four record(...) inputs are strings.

Open choice for constructor:

either reject non-positive capacity values with ValueError
or document a minimum capacity requirement and enforce it

Recommended behavior:

raise ValueError if capacity <= 0

## Design Notes

Implementation may use:

a list plus write index
collections.deque(maxlen=...)
another bounded in-memory structure

The implementation should prioritize:

simplicity
bounded memory
clear behavior
easy testability

If deque(maxlen=...) satisfies all requirements cleanly, it is acceptable.

Example Usage

```pyhton
recorder = FlightRecorder(capacity=3)

recorder.record("Idle", "start", {"turn_key", "start_engine"}, "Running")
recorder.record("Running", "pause", {"engage_clutch"}, "Paused")
recorder.record("Paused", "resume",  {"release_clutch"}, "Running")

records = recorder.get_records()
```

Expected logical contents:

Idle, start, {turn_key, start_engine}, Running
Running, pause, {engage_clutch}, Paused
Paused, resume, {release_clutch}, Running

After adding one more record:

```python
recorder.record("Running", "stop", {"stop_engine"}, "Stopped")
```

Expected logical contents:

Running, pause, {engage_clutch}, Paused
Paused, resume, {release_clutch}, Running
Running, stop, {stop_engine}, Stopped

The oldest record should have been overwritten.

## Acceptance Criteria

The feature is complete when all of the following are true:

A FlightRecorder class exists.
It accepts a fixed capacity at construction time.
record(state, event, {actions}, new_state) stores a record.
get_records() returns all currently stored records.
When capacity is exceeded, the oldest record is overwritten.
get_records() returns records in chronological order.
Invalid capacity values are rejected.
Unit tests cover both normal and wraparound behavior.

## Testing plan
Unit tests
create recorder with valid capacity
reject zero or negative capacity
record one event and retrieve it
record multiple events below capacity
record exactly at capacity
record beyond capacity and verify oldest is overwritten
verify ordering after wraparound
verify returned record contents match inputs exactly

Suggested edge-case tests
capacity of 1
repeated identical events
empty recorder returns empty list

## Acceptance criteria
Clear pass/fail list.

## Risks
Buffer entries may get over written before system has 
time to get the records to diagnose the problem. 

## Open questions
Should I had a Flask app to create a test the flight controller.

---

