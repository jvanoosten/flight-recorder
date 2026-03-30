"""FastAPI backend for FlightRecorder."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from src.flight_recorder import FlightRecorder

app = FastAPI(title="Flight Recorder API")

recorder = FlightRecorder(capacity=100)


class RecordRequest(BaseModel):
    current_state: str
    event: str
    actions: list[str] = []
    new_state: str


class RecordResponse(BaseModel):
    current_state: str
    event: str
    actions: list[str]
    new_state: str


@app.post("/record", status_code=201)
def post_record(body: RecordRequest) -> dict:
    recorder.record(
        current_state=body.current_state,
        event=body.event,
        actions_taken=body.actions,
        new_state=body.new_state,
    )
    return {"status": "ok"}


@app.get("/records", response_model=list[RecordResponse])
def get_records() -> list[RecordResponse]:
    return [
        RecordResponse(
            current_state=r.current_state,
            event=r.event,
            actions=list(r.actions_taken),
            new_state=r.new_state,
        )
        for r in recorder.get_records()
    ]


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())
