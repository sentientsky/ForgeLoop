---
name: deepen
description: Use when a module, workflow, or interface feels shallow, duplicated, leaky, or hard to extend safely.
---

# Deepen

Use this skill when architecture needs clearer boundaries.

## Inputs

- Changed or problematic files.
- Existing architecture notes.
- Tests and user workflows.
- Known pain points.

## Steps

1. Name the friction in plain language.
2. Identify the current interface.
3. Ask what should remain stable if the implementation changes.
4. Offer two or three small interface options.
5. Choose the option that removes real complexity.
6. Avoid abstraction unless it reduces duplication, risk, or cognitive load.

## Output

Create an architecture note or check finding when the task is substantial.

## Rules

- Present candidates before refactoring.
- Prefer deletion of complexity over new layers.
- Treat the interface as the test surface.
- Do not refactor unrelated areas.

## Done When

- The boundary is clearer.
- The change is smaller than the problem it solves.
- Tests or checks prove the public behaviour still works.

