---

# Example `REVIEW_PERSONAS.md`

```md
# REVIEW_PERSONAS.md

## Purpose
This file defines the review personas the agent must use before and after implementation.

These personas are not fictional roleplay. They are structured review lenses meant to catch different classes of mistakes.

For each meaningful change, the agent should evaluate the work through these personas and revise the implementation if needed.

---

# 1. Designer

## Focus
User experience, clarity, usability, consistency, and friction.

## Questions to Ask
- Does this change make the user flow clearer or more confusing?
- Does it introduce unnecessary steps?
- Are labels, messages, names, and outputs understandable?
- Is behavior consistent with the rest of the product?
- Are edge-case states handled gracefully?

## Red Flags
- confusing names
- inconsistent UI or output wording
- error messages that are too technical
- hidden behavior changes
- overly complex user flows

## Action Guidance
Request changes if the feature works technically but feels confusing, inconsistent, or awkward to use.

---

# 2. Architect

## Focus
System design, boundaries, maintainability, and fit with repository architecture.

## Questions to Ask
- Does this change fit existing architectural patterns?
- Is logic placed in the correct layer/module?
- Does it preserve clear separation of concerns?
- Is the solution small and extensible?
- Does it introduce coupling that will hurt future work?

## Red Flags
- business logic in UI or transport layers
- duplication of core logic
- leaky abstractions
- shortcuts that bypass established architecture
- large cross-cutting edits without strong need

## Action Guidance
Request changes if the solution works now but degrades overall system structure.

---

# 3. Domain Expert

## Focus
Business rules, domain invariants, correctness, and policy adherence.

## Questions to Ask
- Does the implementation obey documented business/domain rules?
- Are validation rules enforced correctly?
- Are edge cases handled according to spec?
- Are permissions, statuses, thresholds, or workflows correct?
- Is any important domain rule missing from tests?

## Red Flags
- incorrect business logic
- assumptions not supported by specs
- missing validation
- incorrect handling of edge cases
- state transitions that violate domain rules

## Action Guidance
Request changes if technical correctness exists but domain correctness is weak or incomplete.

---

# 4. Code Expert

## Focus
Readability, simplicity, correctness, idiomatic code, and test quality.

## Questions to Ask
- Is the code easy for another developer to understand?
- Is it simpler than the alternatives?
- Are names clear and consistent?
- Are tests meaningful rather than superficial?
- Is error handling appropriate?

## Red Flags
- clever but hard-to-read code
- weak variable/function naming
- duplicated code
- overly long functions
- brittle tests
- commented-out dead code
- broad exception swallowing

## Action Guidance
Request changes if the code passes tests but is hard to maintain or understand.

---

# 5. Performance Expert

## Focus
Efficiency, scalability, unnecessary work, latency, memory, and resource usage.

## Questions to Ask
- Does this add repeated expensive work?
- Are there obvious inefficiencies in loops, queries, or network calls?
- Could this regress performance at larger scale?
- Is caching, batching, or pagination needed?
- Does the change increase startup time, runtime, or memory meaningfully?

## Red Flags
- repeated database or API calls
- N+1 patterns
- unnecessary recomputation
- loading large datasets unnecessarily
- expensive work in hot paths

## Action Guidance
Request changes when performance risks are material, especially in critical paths.

Note: do not over-optimize low-impact code. Prefer clear code unless performance matters.

---

# 6. Human Advocate

## Focus
Reviewability, trust, safety, operational clarity, and developer ergonomics.

## Questions to Ask
- Will a human reviewer understand this change quickly?
- Is the commit focused and easy to review?
- Are the risks and tradeoffs visible?
- Were docs and TODOs updated appropriately?
- Would this change surprise a teammate?

## Red Flags
- giant unfocused commits
- hidden behavioral changes
- no explanation of tradeoffs
- missing docs for changed behavior
- unsafe assumptions
- poor handoff notes

## Action Guidance
Request changes if the implementation is technically sound but hard for a human team to safely review, approve, or operate.

---

## Review Procedure

For each task, review in this order:

1. Architect
2. Domain Expert
3. Code Expert
4. Designer
5. Performance Expert
6. Human Advocate

---

## Minimum Review Output Format

Before implementation, briefly note:

```text
Pre-implementation review
- Architect:
- Domain Expert:
- Code Expert:
- Designer:
- Performance:
- Human Advocate:

After implementation, briefly note:

Post-implementation review
- Architect:
- Domain Expert:
- Code Expert:
- Designer:
- Performance:
- Human Advocate:

Keep these notes concise but specific.



