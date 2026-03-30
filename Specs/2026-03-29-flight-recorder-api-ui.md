# Feature: Flight Recorder API and Web UI

## Status
Draft

## Summary
Add a FastAPI backend and a simple HTML frontend to interact with the FlightRecorder.

The system will:
- expose REST endpoints to record events and retrieve history
- provide a browser-based UI to submit events and view recorded transitions

---

## Problem
The FlightRecorder currently exists only as an in-memory Python object.

There is no:
- external interface
- API access
- user interface

This limits usability for:
- debugging
- demonstration
- interactive testing

---

## Goals

1. Expose FlightRecorder functionality via a FastAPI backend
2. Allow recording events via HTTP
3. Allow retrieving recorded transitions via HTTP
4. Provide a minimal HTML frontend to:
   - submit new records
   - display recorded transitions
5. Keep the implementation simple and easy to test

---

## Non-Goals

- Authentication
- Persistence to database
- Multi-user support
- Advanced UI frameworks (React, Vue, etc.)
- Styling beyond minimal usability

---

## Architecture Overview

Components:

- FastAPI backend
- In-memory FlightRecorder instance
- HTML frontend served by FastAPI

Flow:

Browser → FastAPI → FlightRecorder → Response → Browser

---

## Backend API

### POST /record

Request body:

```json
{
  "current_state": "Idle",
  "event": "start",
  "actions": {"turn_key", "start_engine"}
  "new_state": "Running"
}
```
Behavior:

calls FlightRecorder.record(...)
returns success response

### GET /records

Response:

[
  {
    "state": "Idle",
    "event": "start",
    "actions": {"turn_key", "start_engine"}
    "new_state": "Running"
  }
]

Behavior:

returns all records in chronological order

---

## Frontend UI

### Requirements

The UI must:

Provide a form with fields:
state
event
transition
new_state
Provide a submit button to call POST /record
Display a list of recorded transitions
Refresh data after submission

## Implementation Guidelines

### Backend:

use FastAPI
define Pydantic model for request validation
create a single shared FlightRecorder instance

### Frontend:

use plain HTML + minimal JavaScript (fetch API)
no frameworks required

Example Usage

User opens browser:

http://localhost:8000

User enters:

state: Idle
event: start

Clicks submit → record stored → UI updates list

---

## Acceptance Criteria
FastAPI app runs locally
POST /record stores a record
GET /records returns correct data
UI can submit new records
UI displays updated records
Circular buffer behavior is preserved
No crashes on invalid input (validation handled)

---

## Test Plan
Backend tests
POST valid record
GET returns records
validation rejects bad input
buffer overwrite behavior still correct
Manual UI tests
submit form
verify record appears
verify ordering
verify behavior after buffer overflow

---

## File Structure (Expected)

src/
  flight_recorder.py
  api.py

templates/
  index.html

tests/
  test_api.py


---

## Open Questions
Should the recorder reset on server restart?
Should we add timestamps?
Should UI auto-refresh or poll?

---

# 🧠 Key design principle (importan  