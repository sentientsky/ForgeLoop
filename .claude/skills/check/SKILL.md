---
name: check
description: Review completed work using ForgeLoop's specialist viewpoints, tests, validation, and P1/P2/P3 triage.
---

# Check

Use this skill after Build and before Capture.

The goal is to catch issues before the work is considered complete and to identify learnings worth saving.

## Inputs

- User request.
- Discovery, frame, and build notes.
- Changed files.
- Test and validation output.

## Specialist Reviewers

Use these reviewers when relevant:

- `architecture-reviewer`
- `security-reviewer`
- `test-reviewer`
- `docs-reviewer`
- `correctness-reviewer`
- `maintainability-reviewer`
- `performance-reviewer`
- `reliability-reviewer`
- `api-contract-reviewer`
- `data-reviewer`
- `adversarial-reviewer`

## Steps

1. Summarise what changed.
2. Run relevant tests, linters, type checks, or manual checks.
3. Select reviewers using `docs/standards/review-routing-standard.md`.
4. Merge findings into one clear list.
5. Prioritise findings:
   - P1: must fix before completion.
   - P2: should fix soon.
   - P3: useful improvement, not blocking.
6. Fix P1 items before calling the work done.
7. Record unresolved P2 and P3 items.
8. Run verify-completion before final handoff.
9. Identify anything that should be captured.

## Output

Create a check note in `docs/checks/`.

Use `templates/check-template.md`.

## Check Note Naming

Use this pattern:

```text
docs/checks/YYYY-MM-DD-short-task-name.md
```

## Rules

- Findings must be concrete.
- Avoid vague warnings.
- If no issues are found, say so.
- Prefer file-specific notes where possible.
- Do not treat style preferences as P1 unless they break the product.
- Use extra reviewers for commands, installers, plugins, browser access, secrets, or release claims.

## Done When

- Relevant reviewers have been used or consciously skipped.
- P1 findings are resolved.
- Remaining risks are visible.
- Capture has a clear starting point.
