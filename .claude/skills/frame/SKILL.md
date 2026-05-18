---
name: frame
description: Convert a discovery into a clear implementation plan with scope, files, validation, risks, rollback, and capture targets.
---

# Frame

Use this skill after Discover and before Build.

The goal is to turn an idea into a plan that is small enough to execute and clear enough to review.

## Inputs

- User request.
- Latest discovery note.
- Relevant standards and memory.
- Known constraints.

## Steps

1. Summarise the goal.
2. Define what is in scope.
3. Define what is out of scope.
4. List affected files or likely file areas.
5. Record assumptions.
6. Choose the smallest practical implementation path.
7. Define validation steps.
8. Identify risks and rollback.
9. Decide what should be captured if the work succeeds.

## Output

Create a frame in `docs/frames/` for non-trivial tasks.

Use `templates/frame-template.md`.

## Frame Naming

Use this pattern:

```text
docs/frames/YYYY-MM-DD-short-task-name.md
```

## Rules

- Keep the plan short enough to use.
- Avoid vague steps such as "update files" or "fix logic".
- Do not plan broad rewrites unless the task truly requires them.
- Prefer reversible changes.
- Call out risky assumptions.

## Done When

- A builder can follow the plan without guessing.
- Validation is clear.
- The user or maintainer can see the trade-offs.
- Capture targets are named.

