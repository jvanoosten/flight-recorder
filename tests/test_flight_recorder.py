"""Tests for FlightRecorder circular buffer."""

import pytest

from src.flight_recorder import FlightRecord, FlightRecorder

# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_create_with_valid_capacity() -> None:
    recorder = FlightRecorder(capacity=10)
    assert recorder.get_records() == []


def test_create_with_capacity_of_one() -> None:
    recorder = FlightRecorder(capacity=1)
    assert recorder.get_records() == []


def test_reject_zero_capacity() -> None:
    with pytest.raises(ValueError):
        FlightRecorder(capacity=0)


def test_reject_negative_capacity() -> None:
    with pytest.raises(ValueError):
        FlightRecorder(capacity=-5)


# ---------------------------------------------------------------------------
# Basic recording
# ---------------------------------------------------------------------------


def test_empty_recorder_returns_empty_list() -> None:
    recorder = FlightRecorder(capacity=5)
    assert recorder.get_records() == []


def test_record_one_event_and_retrieve() -> None:
    recorder = FlightRecorder(capacity=5)
    recorder.record("Idle", "start", ["turn_key", "start_engine"], "Running")
    records = recorder.get_records()
    assert len(records) == 1
    assert records[0].current_state == "Idle"
    assert records[0].event == "start"
    assert records[0].actions_taken == ("turn_key", "start_engine")
    assert records[0].new_state == "Running"


def test_record_contents_match_inputs_exactly() -> None:
    recorder = FlightRecorder(capacity=5)
    recorder.record("StateA", "evt", ["act1", "act2"], "StateB")
    rec = recorder.get_records()[0]
    assert rec == FlightRecord("StateA", "evt", ("act1", "act2"), "StateB")


def test_record_multiple_events_below_capacity() -> None:
    recorder = FlightRecorder(capacity=5)
    recorder.record("Idle", "start", ["turn_key"], "Running")
    recorder.record("Running", "pause", ["engage_clutch"], "Paused")
    records = recorder.get_records()
    assert len(records) == 2
    assert records[0].current_state == "Idle"
    assert records[1].current_state == "Running"


def test_record_exactly_at_capacity() -> None:
    recorder = FlightRecorder(capacity=3)
    recorder.record("S0", "e0", [], "S1")
    recorder.record("S1", "e1", [], "S2")
    recorder.record("S2", "e2", [], "S3")
    records = recorder.get_records()
    assert len(records) == 3
    assert records[0].current_state == "S0"
    assert records[2].current_state == "S2"


# ---------------------------------------------------------------------------
# Circular buffer / wraparound
# ---------------------------------------------------------------------------


def test_record_beyond_capacity_overwrites_oldest() -> None:
    recorder = FlightRecorder(capacity=3)
    recorder.record("Idle", "start", ["turn_key", "start_engine"], "Running")
    recorder.record("Running", "pause", ["engage_clutch"], "Paused")
    recorder.record("Paused", "resume", ["release_clutch"], "Running")
    recorder.record("Running", "stop", ["stop_engine"], "Stopped")

    records = recorder.get_records()
    assert len(records) == 3
    assert records[0].current_state == "Running"
    assert records[0].event == "pause"
    assert records[1].current_state == "Paused"
    assert records[2].current_state == "Running"
    assert records[2].event == "stop"


def test_ordering_after_wraparound_is_chronological() -> None:
    recorder = FlightRecorder(capacity=3)
    for i in range(6):
        recorder.record(f"S{i}", f"e{i}", [], f"S{i + 1}")

    records = recorder.get_records()
    assert len(records) == 3
    assert records[0].current_state == "S3"
    assert records[1].current_state == "S4"
    assert records[2].current_state == "S5"


def test_capacity_one_always_keeps_latest_record() -> None:
    recorder = FlightRecorder(capacity=1)
    recorder.record("A", "e1", [], "B")
    recorder.record("B", "e2", [], "C")
    recorder.record("C", "e3", [], "D")
    records = recorder.get_records()
    assert len(records) == 1
    assert records[0].current_state == "C"
    assert records[0].new_state == "D"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_repeated_identical_events() -> None:
    recorder = FlightRecorder(capacity=3)
    recorder.record("Idle", "ping", [], "Idle")
    recorder.record("Idle", "ping", [], "Idle")
    recorder.record("Idle", "ping", [], "Idle")
    records = recorder.get_records()
    assert len(records) == 3
    assert all(r.event == "ping" for r in records)


def test_empty_actions_list() -> None:
    recorder = FlightRecorder(capacity=5)
    recorder.record("A", "noop", [], "A")
    rec = recorder.get_records()[0]
    assert rec.actions_taken == ()


def test_get_records_returns_new_list_each_call() -> None:
    recorder = FlightRecorder(capacity=5)
    recorder.record("A", "e", [], "B")
    first = recorder.get_records()
    second = recorder.get_records()
    assert first == second
    assert first is not second
