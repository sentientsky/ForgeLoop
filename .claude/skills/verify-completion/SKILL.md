---
name: verify-completion
description: Use before final handoff to prove the task is actually complete, validated, documented, and safe to close.
---

# Verify Completion

Use this skill after Check and before final response.

The goal is to stop polished but unfinished work from slipping through.

## Inputs

- User request.
- Frame or plan.
- Changed files.
- Test and validation output.
- Check findings.
- Capture note, when the task was non-trivial.

## Steps

1. Restate the requested outcome in one sentence.
2. Compare the outcome against what was actually changed.
3. Confirm every P1 finding is fixed or explicitly blocked.
4. Confirm relevant validation has run.
5. Confirm documentation changed when user-facing behaviour changed.
6. Confirm non-trivial work has a capture or solution note.
7. Check for unsafe leftovers such as secrets, generated caches, broad permissions, or unreviewed hooks.
8. State any remaining limitation plainly.

## Output

Create a short completion evidence block:

```text
Completion evidence
- Outcome:
- Validation:
- P1 status:
- Docs:
- Capture:
- Residual risk:
```

## Rules

- Do not invent validation.
- Do not hide skipped checks.
- Do not call work complete when a P1 issue remains.
- Prefer concrete file and command evidence.
- Keep the handoff short enough for a beginner to understand.

## Done When

- The requested outcome is demonstrably complete.
- The validation evidence is visible.
- Any remaining risk is named.
- The next action is clear.

