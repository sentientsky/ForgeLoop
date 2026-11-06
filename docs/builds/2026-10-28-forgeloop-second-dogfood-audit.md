---
type: build
date: 2026-10-28
status: current
task: ForgeLoop second dogfood audit
frame: docs/frames/2026-10-28-forgeloop-second-dogfood-audit.md
tags: [dogfood, workflow, validation, security]
---

# Build: ForgeLoop Second Dogfood Audit

## Frame Used

`docs/frames/2026-10-28-forgeloop-second-dogfood-audit.md`.

## Change Log

- Used `forgeloop pack` and `tokens` to retrieve the prior dogfood and current security/release lessons without loading all memory files.
- Ran the intro, status, setup menu and JSON dry run, compatibility report, doctor, PreCompact simulation, OpenCLI plan, secrets check, governance checks, source-alpha gate, and stable gate.
- Ran profile adoption in disposable directories. Confirmed clean preview performs no writes; clean apply creates only the two allowlisted Codex files; a user-owned conflicting `AGENTS.md` is preserved and causes the documented non-zero partial-conflict result.
- Kept OpenCLI plan-only. It was not installed or executed.
- No product-code defect was reproduced, so no runtime code was changed during this dogfood pass.

## Validation Run

- Command: `python -m forgeloop doctor .`
  - Result: overall `ok`; no repository, compatibility, secrets, memory, governance, or CI configuration errors.
- Command: ForgeLoop setup dry run and profile-only adoption probes.
  - Result: no writes during preview; user-owned content preserved; expected files created during apply; conflict returned exit code 1.
- Command: source-alpha and stable release gates.
  - Result: source alpha passed. Stable gate blocked only on Claude clean-session acceptance, independent maintainer review, and provider-backed erasure evidence.
- Command: `python -m forgeloop pack` and `python -m forgeloop tokens`.
  - Result: 8 of 33 records selected; 87.9% byte reduction vs selected source and 96.2% vs corpus for this query, estimated tokens only.

## Decisions Made During Build

- Decision: Treat the first adoption-probe non-zero exit as a harness mistake, then rerun with both clean and conflicting destinations.
- Reason: Existing project policy explicitly treats partial conflicts as non-zero while preserving the conflicting file and applying only non-conflicting files.
- Decision: Do not change runtime code when the implementation matches documented and tested behavior.
- Reason: Avoid introducing unnecessary change into a security-reviewed branch.

## Plan Changes

The anticipated defect-fix step was not needed. The adoption conflict result was expected; the audit expanded the fixture to verify both preservation and partial application.

## Ready For Check

- [x] Implementation complete
- [x] Validation run or limitation stated
- [x] Risks carried forward
