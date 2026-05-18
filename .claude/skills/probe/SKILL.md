---
name: probe
description: Use for bugs, regressions, flaky behaviour, or confusing failures where a repeatable signal is needed before fixing.
---

# Probe

Use this skill before Build when the problem is a failure, bug, or unexplained behaviour.

## Inputs

- User report.
- Error output.
- Relevant files.
- Existing tests or reproduction steps.

## Steps

1. Reproduce the problem or explain why it cannot be reproduced locally.
2. Create the smallest reliable signal: test, command, log, or manual check.
3. List three to five ranked hypotheses.
4. Test one hypothesis at a time.
5. Keep the first fix small.
6. Remove temporary debug output before completion.
7. Capture the prevention pattern if the bug teaches something reusable.

## Output

Create a probe note from `templates/probe-template.md` when the investigation is non-trivial.

## Rules

- Do not guess before creating a signal.
- Do not fix multiple hypotheses at once.
- Do not leave debug instrumentation behind.
- Treat flaky tests as bugs in the signal first.

## Done When

- The signal is repeatable.
- The cause is known or the uncertainty is explicit.
- The fix can be checked against the same signal.

