## Purpose

This file defines how autonomous coding agents should operate in this repository.

Agents must follow the workflow defined in:

1. `AGENT_LOOP.md` — operational workflow
2. `REVIEW_PERSONAS.md` — structured review process
3. repository documentation in `Docs/`

This file serves as the entry point and routing guide.

---

# Agent Operating Principles

Agents working in this repository must follow these rules:

1. Prioritize correctness and safety over speed.
2. Prefer small, reviewable changes over large speculative changes.
3. Never bypass repository validation rules.
4. Never commit code that fails tests or lint checks.
5. Avoid making changes outside the scope of the selected task.
6. Always leave a clear recap for human reviewers.
7. Never overwrite or discard human-authored work without explicit justification.

Agents must **never use:**
git commit --no-verify

All commits must pass repository validation.

---

# Required Reading Order

Before performing any task, read files in this order:

1. `AGENT_LOOP.md`
2. `TODO.md`
3. `Docs/architecture.md`
4. `Docs/domain-rules.md`
5. `Docs/testing-strategy.md`
6. `Specs/`

Ignore any spec files prefixed with:
draft-

---

# Repository Structure
AGENTS.md
AGENT_LOOP.md
REVIEW_PERSONAS.md

Docs/
Specs/
src/
tests/

TODO.md
CHANGELOG.md

---

# Task Sources

Agents may only perform tasks described in:

- `TODO.md`
- approved specifications in `Specs/`
- explicitly identified bug fixes

Agents must **not invent new tasks**.

---

# Priority Order for Work

Tasks must be selected in this priority order:

1. Fix failing tests
2. Fix broken builds
3. Address high-priority bugs in `TODO.md`
4. Implement approved specs
5. Improve test coverage where weak

Never start new features while baseline validation fails.

---

# Validation Requirements

All code changes must pass validation before committing.

Minimum required checks:
pre-commit run --all-files
pytest

Depending on the repository configuration, additional checks may include:
ruff check .
ruff format --check .
mypy .
npm run lint
npm run test
npm run build

The authoritative validation commands are defined in the repository scripts.

If validation fails:
1. identify the cause
2. fix the issue
3. rerun validation

Repeat until successful.

---

# Testing Expectations

Agents must follow the testing rules defined in:
Docs/testing-strategy.md

General guidelines:

- bug fixes require regression tests
- new features require tests
- tests should encode acceptance criteria
- tests must remain readable and deterministic

Agents must not remove tests without justification.

---

# Documentation Requirements

Documentation must be updated when behavior, architecture, or workflows change.

Possible locations:
Docs/
README.md
CHANGELOG.md

Documentation changes should be included in the same commit as the implementation.

---

# Commit Standards

Commits must be:

- small
- focused
- reviewable
- logically grouped

Commit message format:
<type>: <short summary>

Why:

explanation of the problem or goal

What changed:

summary of the implementation

Validation:

tests or checks run

Example types:
fix
feat
refactor
docs
test

---

# Review Requirement

Before committing, evaluate the change using the personas defined in:
REVIEW_PERSONAS.md

Minimum review questions:

- Does the change follow repository architecture?
- Are domain rules preserved?
- Is the code understandable and maintainable?
- Are tests sufficient?
- Will this change surprise a user or developer?

If concerns are identified, revise the implementation before committing.

---

# Tracking Work
Agents must update tracking files as appropriate.

Possible updates include:
TODO.md
CHANGELOG.md

ompleted tasks should be marked clearly.

---

# Human Review Support

Agents must leave a clear recap after completing each task.

Recap format:
Task completed:
Files changed:
Tests added or updated:
Validation run:
Risks or open questions:
Suggested next step:

The recap should help a human reviewer understand the change quickly.

---

# Stop Conditions

Agents must stop and report clearly if:

- instructions conflict
- required information is missing
- validation failures are unrelated and unsafe to fix
- a product decision is required
- secrets or credentials are required

In these cases, the agent must report:

- what was attempted
- what blocked progress
- what human input is required

---

# Forbidden Actions

Agents must not:

- bypass validation
- disable tests to make builds pass
- remove large portions of code without justification
- invent requirements not present in docs or specs
- commit secrets or credentials
- overwrite human changes silently

---

# Definition of Done

A task is considered complete only when:

- the implementation matches the spec or bug report
- relevant tests are added or updated
- validation checks pass
- documentation is updated if needed
- tracking files are updated
- the commit is clear and reviewable
- a recap has been provided

## Read Watchdog Feedback

Before selecting a new task, check `REVIEW_FEEDBACK.md`.

If there is feedback on the most recent commit:
- read it fully
- address high-severity issues first
- do not continue to the next major task until critical issues are resolved or explicitly documente
