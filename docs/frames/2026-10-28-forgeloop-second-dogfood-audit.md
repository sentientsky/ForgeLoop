---
type: frame
date: 2026-10-28
status: current
task: ForgeLoop second dogfood audit
discovery: docs/discoveries/2026-10-28-forgeloop-second-dogfood-audit.md
tags: [dogfood, workflow, validation, security, release]
---

# Frame: ForgeLoop Second Dogfood Audit

## Goal

Demonstrate that ForgeLoop's own task loop, CLI, memory handling, and readiness gates behave as documented, and fix any concrete defect found.

## In Scope

- Use ForgeLoop to create and maintain Discover, Frame, Build, Check, and Capture evidence.
- Exercise help, status, pointer-first pack/token report, setup dry run, compatibility, doctor, source-alpha and stable release gates.
- Exercise safe failure cases for setup, note creation, and CLI input where practical.
- Run tests, lint, coverage, dependency audit, package checks, and hosted PR checks.
- Preserve verified human/provider release blockers.

## Out Of Scope

- Claiming ForgeLoop is flawless or stable-production ready.
- Installing OpenCLI or making live browser/network actions through it.
- Authenticating Claude Code, performing independent review, or attesting provider deletion.
- Merging PR #44 or closing other maintainers' PRs.

## Approach

Use existing commands and tests first. Create disposable fixtures in temporary directories. Compare CLI behavior to documented safety and release rules. Make only narrowly scoped code fixes for reproducible failures, then rerun affected checks and GitHub CI.

## Files Likely To Change

- `docs/discoveries/2026-10-28-forgeloop-second-dogfood-audit.md`
- `docs/frames/2026-10-28-forgeloop-second-dogfood-audit.md`
- `docs/builds/2026-10-28-forgeloop-second-dogfood-audit.md`
- `docs/checks/2026-10-28-forgeloop-second-dogfood-audit.md`
- `docs/captures/2026-10-28-forgeloop-second-dogfood-audit.md`
- `docs/palace/indexes/memory-index.json`
- `docs/palace/indexes/memory-index.md`
- Product code and tests only if a defect is reproduced.

## Build Steps

1. Exercise the documented workflow and inspect actual CLI output and error handling.
2. Probe setup, adoption, note creation, and release gates with temporary hostile or malformed inputs.
3. Patch only confirmed issues and add a focused regression test for each.
4. Run the complete local validation matrix, then inspect hosted checks on the resulting commit.
5. Complete Check and Capture notes and refresh the memory index.

## Validation

- Unit tests, Ruff, branch coverage, Bandit, and pip-audit.
- `validate`, `doctor`, `compat`, setup dry run, OpenCLI plan, hook simulation, secrets and governance checks, index check, context pack, and token report.
- Source-alpha must pass; stable release should block only on documented external gates.
- Build source and wheel distributions, Twine checks, installed-wheel smoke test, GitHub CI, CodeQL, and fuzz checks.

## Risks

- Some safety probes can create or delete data if run against the real repository; all destructive probes must use disposable temporary roots.
- The repository's `doctor` command can read the external secrets file metadata. Do not display secret contents.
- The current branch carries recent security fixes; keep any new changes isolated and rerun hosted checks.

## Rollback

Revert only commits created for this dogfood pass. Keep the prior security remediation commits intact. Temporary fixtures are deleted by their context managers.

## Capture Target

Record which user-facing ForgeLoop behaviors were exercised, any discovered defect and regression test, reproducible check results, and limits that still require real humans or providers.
