---
name: tdd
description: Use for risky behaviour changes where one tested tracer bullet should be built before broader implementation.
---

# TDD

Use this skill when behaviour matters more than file shape.

## Inputs

- Framed task.
- Public interface or user workflow.
- Existing tests.
- Risk level.

## Steps

1. Choose one behaviour slice.
2. Write or identify the smallest failing check.
3. Implement only enough code to pass that check.
4. Refactor only after the check is green.
5. Repeat for the next behaviour slice.
6. Record what was intentionally not tested.

## Output

Use `templates/tdd-cycle-template.md` for non-trivial cycles.

## Rules

- Test through public interfaces when possible.
- Avoid testing private implementation details.
- Keep each cycle small.
- Do not add broad mocks that hide integration risk.
- State when TDD is not a good fit for the task.

## Done When

- The core behaviour has executable proof.
- The tests are readable.
- Remaining gaps are visible.

