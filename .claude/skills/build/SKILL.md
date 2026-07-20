---
name: build
description: Implement an approved ForgeLoop frame in small, reversible steps while recording progress and validation.
---

# Build

Use this skill when a frame is ready and implementation should begin.

The goal is to make the change safely, without losing the thread of what was done and why.

## Inputs

- Approved frame.
- Relevant discovery note.
- User request.
- Current repository state.

## Steps

1. Re-read the frame.
2. Confirm the smallest first change.
3. Make one focused change at a time.
4. Run relevant checks after meaningful changes.
5. Record progress when the task is more than a tiny edit.
6. Stop and update the frame if reality differs from the plan.
7. Keep final changes easy to review.

## Output

For non-trivial work, create or update a build note in `docs/builds/`.

Use `templates/build-template.md`.

## Build Note Naming

Use this pattern:

```text
docs/builds/YYYY-MM-DD-short-task-name.md
```

## Rules

- Do not make unrelated refactors.
- Do not mix experiments with final changes.
- Prefer small commits or small change sets.
- Keep user-facing behaviour clear.
- Run validation where practical.
- State any validation that could not be run.

## Done When

- The framed change is implemented.
- Important validation has run or the limitation is recorded.
- The change is ready for Check.

