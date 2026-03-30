"""Tests for the Flight Recorder FastAPI endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.api import app, recorder


@pytest.fixture(autouse=True)
def clear_recorder():
    """Reset the shared recorder buffer before each test."""
    recorder._buffer.clear()
    yield
    recorder._buffer.clear()


client = TestClient(app)


def test_post_record_returns_201():
    res = client.post(
        "/record",
        json={
            "current_state": "Idle",
            "event": "start",
            "actions": ["turn_key", "start_engine"],
            "new_state": "Running",
        },
    )
    assert res.status_code == 201
    assert res.json() == {"status": "ok"}


def test_get_records_returns_stored_record():
    client.post(
        "/record",
        json={
            "current_state": "Idle",
            "event": "start",
            "actions": ["turn_key"],
            "new_state": "Running",
        },
    )
    res = client.get("/records")
    assert res.status_code == 200
    records = res.json()
    assert len(records) == 1
    assert records[0]["current_state"] == "Idle"
    assert records[0]["event"] == "start"
    assert records[0]["actions"] == ["turn_key"]
    assert records[0]["new_state"] == "Running"


def test_get_records_empty():
    res = client.get("/records")
    assert res.status_code == 200
    assert res.json() == []


def test_get_records_chronological_order():
    transitions = [
        ("Idle", "start", [], "Running"),
        ("Running", "pause", [], "Paused"),
        ("Paused", "resume", [], "Running"),
    ]
    for cs, ev, ac, ns in transitions:
        client.post(
            "/record",
            json={"current_state": cs, "event": ev, "actions": ac, "new_state": ns},
        )
    records = client.get("/records").json()
    assert [r["current_state"] for r in records] == ["Idle", "Running", "Paused"]
    assert [r["new_state"] for r in records] == ["Running", "Paused", "Running"]


def test_post_record_missing_required_field_returns_422():
    res = client.post(
        "/record",
        json={"current_state": "Idle", "event": "start"},  # missing new_state
    )
    assert res.status_code == 422


def test_post_record_actions_defaults_to_empty():
    res = client.post(
        "/record",
        json={"current_state": "A", "event": "go", "new_state": "B"},
    )
    assert res.status_code == 201
    records = client.get("/records").json()
    assert records[0]["actions"] == []


def test_buffer_overwrite_preserves_capacity():
    """Verify circular buffer behavior: oldest record is dropped when full."""
    capacity = recorder._buffer.maxlen
    assert capacity is not None

    for i in range(capacity + 2):
        client.post(
            "/record",
            json={
                "current_state": f"S{i}",
                "event": "tick",
                "actions": [],
                "new_state": f"S{i + 1}",
            },
        )

    records = client.get("/records").json()
    assert len(records) == capacity
    # Oldest records overwritten; first record should be index 2
    assert records[0]["current_state"] == "S2"
    assert records[-1]["current_state"] == f"S{capacity + 1}"


def test_index_returns_html():
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
