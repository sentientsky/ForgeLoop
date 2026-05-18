---
name: simplify
description: Use after a change or before release to reduce avoidable complexity, duplication, stale wording, and token ballast.
---

# Simplify

Use this skill after Build or during release polish.

## Inputs

- Changed files.
- Current docs.
- Test and validation output.
- Token report when context size matters.

## Steps

1. Find duplicated wording, duplicated logic, stale examples, and oversized always-loaded text.
2. Remove or consolidate what is not carrying product value.
3. Keep beginner-facing docs direct.
4. Move detail into optional references when it is not needed every time.
5. Re-run validation after simplification.

## Output

Create a check finding or capture note when simplification teaches a reusable pattern.

## Rules

- Do not simplify away useful safety detail.
- Do not change behaviour without tests.
- Prefer one clear source of truth.
- Keep examples realistic.

## Done When

- The system is easier to read.
- The behaviour is unchanged unless intentionally updated.
- Validation still passes.

