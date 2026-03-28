# AGENT_LOOP.md

## Purpose
This file defines the autonomous coding loop for the agent working in this repository.

The agent must follow this process in order, for every task.

---

## Core Operating Principles

1. Do not guess when the repository already contains an answer.
2. Prefer small, safe, verifiable changes over large speculative changes.
3. Never bypass validation.
4. Never use `git commit --no-verify`.
5. Do not mark work complete unless all required validations pass.
6. If documentation, specs, and code disagree, identify the conflict and resolve it carefully.
7. If a task is ambiguous, prefer the safest interpretation and leave a clear note in the recap.
8. Always leave the repository in a clean, reviewable state.

---

## Files to Read First

Before starting work, read these files in this order:

1. `AGENTS.md`
2. `TODO.md`
3. `Docs/architecture.md`
4. `Docs/domain-rules.md`
5. `Docs/testing-strategy.md`
6. relevant files in `Specs/`

Ignore any spec file prefixed with `draft-`.

---

## Task Selection Rules

When choosing the next task:

1. First fix any failing tests or broken builds.
2. Then address high-priority bugs listed in `TODO.md`.
3. Then implement approved specs from `Specs/`.
4. Do not start speculative work not described in docs, TODOs, or specs.
5. Only work on one task at a time unless explicitly instructed otherwise.

---

## Standard Work Loop

### Step 1: Check repo state
Run:

```bash
git status
```
