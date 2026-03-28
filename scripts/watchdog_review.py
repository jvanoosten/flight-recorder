from __future__ import annotations

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / ".watchdog_last_commit"
FEEDBACK_FILE = ROOT / "REVIEW_FEEDBACK.md"

POLL_SECONDS = 20


def run(cmd: list[str]) -> str:
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_head_commit() -> str:
    return run(["git", "rev-parse", "HEAD"])


def get_commit_subject(commit: str) -> str:
    return run(["git", "log", "-1", "--pretty=%s", commit])


def get_commit_diff(commit: str) -> str:
    return run(["git", "show", "--stat", "--patch", "--format=fuller", commit])


def load_last_reviewed_commit() -> str | None:
    if STATE_FILE.exists():
        return STATE_FILE.read_text().strip() or None
    return None


def save_last_reviewed_commit(commit: str) -> None:
    STATE_FILE.write_text(commit + "\n")


def append_feedback(text: str) -> None:
    if not FEEDBACK_FILE.exists():
        FEEDBACK_FILE.write_text("# REVIEW_FEEDBACK.md\n\n")
    with FEEDBACK_FILE.open("a", encoding="utf-8") as f:
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")


def build_review_prompt(commit: str, subject: str, diff: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
You are the watchdog reviewer for this repository.

Review commit {commit}.
Commit subject: {subject}
Timestamp: {timestamp}

Read repository guidance from:
- AGENTS.md
- REVIEW_PERSONAS.md
- TODO.md

You are reviewing the commit shown below.

Your output must be markdown that appends directly into REVIEW_FEEDBACK.md.

Required format:

## Commit: {commit[:7]}
Date: {timestamp}
Reviewer: watchdog-agent

### Summary
...

### Findings
- Severity: high|medium|low
  Area: ...
  Issue: ...
  Recommendation: ...

### Persona Notes
- Architect: ...
- Domain Expert: ...
- Code Expert: ...
- Designer: ...
- Performance Expert: ...
- Human Advocate: ...

### Required Follow-up
- ...

If there are no significant issues, say so clearly.

Here is the commit diff:

{diff}
""".strip()


def review_commit_with_external_agent(prompt: str) -> str:
    """
    Replace this function with your chosen reviewer CLI.
    Examples:
      - codex exec ...
      - claude ...
      - another local wrapper
    """
    # Placeholder implementation:
    return (
        "## Commit: pending\n"
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        "Reviewer: watchdog-agent\n\n"
        "### Summary\n"
        "Placeholder review. Replace review_commit_with_external_agent() with a real agent call.\n\n"
        "### Findings\n"
        "- Severity: medium\n"
        "  Area: setup\n"
        "  Issue: Watchdog review function is not connected to an agent yet.\n"
        "  Recommendation: Wire this script to Codex CLI or Claude Code.\n\n"
        "### Persona Notes\n"
        "- Architect: not evaluated\n"
        "- Domain Expert: not evaluated\n"
        "- Code Expert: not evaluated\n"
        "- Designer: not evaluated\n"
        "- Performance Expert: not evaluated\n"
        "- Human Advocate: placeholder only\n\n"
        "### Required Follow-up\n"
        "- Connect the watchdog to a reviewing agent CLI.\n"
    )


def process_once() -> None:
    head = get_head_commit()
    last = load_last_reviewed_commit()

    if head == last:
        return

    subject = get_commit_subject(head)
    diff = get_commit_diff(head)
    prompt = build_review_prompt(head, subject, diff)
    review = review_commit_with_external_agent(prompt)

    append_feedback("\n" + review + "\n")
    save_last_reviewed_commit(head)
    print(f"Reviewed commit {head[:7]}: {subject}")


def main() -> int:
    print("Starting watchdog reviewer...")
    while True:
        try:
            process_once()
        except subprocess.CalledProcessError as e:
            print("Git command failed:", e, file=sys.stderr)
        except Exception as e:
            print("Unexpected error:", e, file=sys.stderr)

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main())
