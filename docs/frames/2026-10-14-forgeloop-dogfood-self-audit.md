---
type: frame
date: 2026-10-14
status: current
task: ForgeLoop dogfood self audit
discovery: docs/discoveries/2026-10-14-forgeloop-dogfood-self-audit.md
tags: [dogfood, release, validation, workflow]
---

# Frame: ForgeLoop dogfood self audit

## Goal

Use ForgeLoop's own workflow to validate ForgeLoop as a source-alpha and release-candidate tool. The run should leave a clear evidence trail and should not overstate stable-production readiness.

## In Scope

- Exercise Discover, Frame, Build, Check, and Capture using ForgeLoop commands and notes.
- Run pointer-first memory and token reporting.
- Run local health, release, compatibility, governance, secrets, lint, and test commands.
- Record a check note and capture note if the run succeeds or reveals a useful lesson.
- Open a PR instead of pushing directly to protected `main`.

## Out Of Scope

- Closing the stable-production blockers.
- Live Claude Code authentication acceptance.
- Installing or executing OpenCLI.
- Merging Dependabot maintenance PRs.
- Claiming full production readiness.

## Approach

Run a narrow dogfood loop. Only add evidence notes unless a real defect appears. Treat stable-gate failure as expected if it matches the documented blockers.

## Files Likely To Change

- `docs/discoveries/2026-10-14-forgeloop-dogfood-self-audit.md`
- `docs/frames/2026-10-14-forgeloop-dogfood-self-audit.md`
- `docs/builds/2026-10-18-forgeloop-dogfood-self-audit.md`
- `docs/checks/2026-10-18-forgeloop-dogfood-self-audit.md`
- `docs/captures/2026-10-18-forgeloop-dogfood-self-audit.md`
- `docs/palace/indexes/memory-index.json`
- `docs/palace/indexes/memory-index.md`

## Build Steps

1. Create and fill Discovery and Frame notes.
2. Run the representative CLI, release, and validation commands.
3. Create a Check note with exact evidence and any limitations.
4. Create a Capture note with the reusable lesson.
5. Refresh the memory index.
6. Commit the evidence notes on a branch and let GitHub CI validate them.

## Validation

- `python -m unittest discover -s tests`
- `python -m ruff check forgeloop tests`
- `python -m forgeloop validate .`
- `python -m forgeloop doctor .`
- `python -m forgeloop compat .`
- `python -m forgeloop release gate .`
- `python -m forgeloop release gate . --target stable`
- `python -m forgeloop setup . --tool all-supported --dry-run`
- `python -m forgeloop opencli plan .`
- `python -m forgeloop hook-simulate PreCompact .`
- `python -m forgeloop secrets check .`
- `python -m forgeloop governance audit .`
- `python -m forgeloop governance verify .`
- `python -m forgeloop index . --check`

## Risks

- Stable gate failure must not be treated as a defect when it fails for the known stable blockers.
- Token savings must be reported as measured output for this run, not a general marketing claim.
- Documentation-only changes still need CI because branch protection requires it.

## Rollback

Revert the dogfood evidence commit or close the PR. No runtime behaviour should change unless the validation uncovers and fixes a defect.

## Capture Target

Capture that ForgeLoop can run a realistic self-validation loop and that its release gate correctly separates source-alpha readiness from stable-production blockers.
