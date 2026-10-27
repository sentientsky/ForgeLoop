---
type: capture
date: 2026-10-28
status: current
task: ForgeLoop second dogfood audit
supersedes:
superseded_by:
valid_from: 2026-10-28
valid_to:
tags: [dogfood, adoption, validation, workflow]
---

# Capture: ForgeLoop Second Dogfood Audit

## What Happened

ForgeLoop was used as a user would use it to inspect its own repository. The CLI, menu, dry-run setup, compatibility report, health checks, hook simulation, memory packet, OpenCLI plan, secrets/governance checks, and release gates behaved as documented. Disposable adoption tests confirmed preview-only behavior, safe additive writes, conflict preservation, and a non-zero result when any profile entry conflicts.

No new runtime-code change was needed. The initial manual probe incorrectly expected a zero exit for a conflict; checking the documented contract and rerunning the clean and conflict cases resolved the discrepancy.

## Exact Source Text

The adoption result for the conflict fixture was:

```text
different file already exists; preserved
```

## Decision Or Lesson

Interpret command exit codes together with structured per-file output. For `adopt`, a non-zero exit can indicate that some files were safely created while a conflicting user-owned file was preserved. It does not mean the operation overwrote the conflict or that every planned write was rolled back.

## Why It Matters

This avoids falsely reporting correct safety behavior as a bug, while ensuring callers still notice that the full requested profile was not installed.

## Where It Belongs

- CLAUDE.md: No change required.
- Skill: `check` and `capture`.
- Agent: API-contract and adversarial reviewers.
- Hook: Not applicable.
- Standard: Existing installer policy already requires preview, per-file conflict reporting, and non-zero status for partial conflict.
- Solution: No separate solution note required; this is an operational interpretation of existing behavior.
- Palace drawer: This capture and its linked check.

## Links

- Discovery: [second dogfood discovery](../discoveries/2026-10-28-forgeloop-second-dogfood-audit.md).
- Frame: [second dogfood frame](../frames/2026-10-28-forgeloop-second-dogfood-audit.md).
- Build: [second dogfood build](../builds/2026-10-28-forgeloop-second-dogfood-audit.md).
- Check: [second dogfood check](../checks/2026-10-28-forgeloop-second-dogfood-audit.md).
- Palace memory: memory index refreshed after this capture.

## Will This Prevent Future Rework?

Partly. The behavior is already covered by docs and tests; this capture records a concrete user-style run and clarifies how to interpret the partial-conflict exit status.
