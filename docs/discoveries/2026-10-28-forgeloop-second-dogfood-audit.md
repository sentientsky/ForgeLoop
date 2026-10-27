---
type: discovery
date: 2026-10-28
status: current
task: ForgeLoop second dogfood audit
related_wing:
related_room:
tags: [dogfood, workflow, validation, security, release]
---

# Discovery: ForgeLoop Second Dogfood Audit

## User Goal

Use ForgeLoop itself to audit its workflow and product behaviour, find reproducible problems, correct them, and verify the complete loop without making unsupported claims of perfection.

## Repo State

The working tree is clean on `forge/structured-stable-evidence` at commit `66adaae`. PR #44 contains the recent setup symlink fix, patched CI trust-store lock, and fail-closed stable-evidence handling. Its latest CI, CodeQL, and fuzz checks passed. The PR remains open for independent review; the Scorecard vulnerability alert remains against `main` until a reviewed change lands and the scanner reruns.

ForgeLoop reports 33 indexed memory records. Its prior dogfood run and the 2026-10-28 security audit are relevant memory.

## Relevant Files And Folders

- `CLAUDE.md`
- `README.md`
- `.claude/skills/discover/SKILL.md`
- `.claude/skills/frame/SKILL.md`
- `.claude/skills/check/SKILL.md`
- `.claude/skills/capture/SKILL.md`
- `forgeloop/cli.py`
- `forgeloop/core.py`
- `forgeloop/release_gate.py`
- `tests/test_forgeloop.py`
- `docs/checks/` and `docs/captures/`

## Related Memory

- Previous dogfood capture: `docs/captures/2026-10-18-forgeloop-dogfood-self-audit.md`.
- Latest security capture: `docs/captures/2026-10-28-security-audit-fixes.md`.
- Stable release evidence: `docs/captures/2026-10-18-structured-stable-release-evidence.md`.
- Pointer-first output from `forgeloop pack` selected 8 of 33 records and reported byte-based measurements; these are run-specific, not a universal token claim.

## Constraints

- Do not call the system 100% or defect-free.
- Do not mark stable release gates passed without live Claude, independent reviewer, or provider evidence.
- Do not merge or bypass branch protection.
- Keep any product changes tied to reproduced behavior or explicit gaps in the intended workflow.
- Avoid printing secret values during checks.

## Assumptions

- A useful dogfood run should exercise both normal and fail-closed paths, not only happy-path CLI output.
- Only change code when a defect is reproduced or a workflow requirement is demonstrably missing.
- OpenCLI remains plan-only and must not be installed or invoked during this audit.

## Missing Context

- This local run cannot validate Claude Code behaviour without an authenticated clean session.
- It cannot supply independent maintainer review or provider-backed erasure evidence.

## Risks

- Generated notes can make the memory index stale unless it is rebuilt and checked.
- Local CLI success could be mistaken for stable production evidence unless external blockers remain explicit.
- Any generated test data must stay in temporary directories and outside the repository.

## Safest Next Step

Frame a bounded self-audit that exercises CLI contracts, safety refusals, repository health, and release gates; fix only reproducible gaps, then rerun tests and GitHub checks.
