---
type: check
date: 2026-10-18
status: current
task: ForgeLoop dogfood self audit
build: docs/builds/2026-10-18-forgeloop-dogfood-self-audit.md
tags: [dogfood, validation, packaging, release]
---

# Check: ForgeLoop dogfood self audit

## Summary

ForgeLoop was used as the system under test for a complete Discover, Frame, Build, Check, and Capture cycle. No runtime code changed. Core tests, static checks, repository validation, packaging, safe adoption, and source-alpha release readiness all passed. The stable release gate correctly remained blocked by evidence that cannot be manufactured locally.

## Validation

- `python -m unittest discover -s tests`, `python -m ruff check forgeloop tests`, and `python -m forgeloop validate .`
  - Passed: 68 tests passed, Ruff passed, and repository validation passed.
- `python -m forgeloop doctor .`, `compat .`, `setup . --tool all-supported --dry-run`, `opencli plan .`, and `hook-simulate PreCompact .`
  - Passed or produced safe dry-run/plan output. OpenCLI was correctly reported as optional and not installed.
- `python -m forgeloop secrets check .`, `governance audit .`, and `governance verify .`
  - Passed: no secret values were displayed; the empty audit log was valid.
- `python -m build --no-isolation`, `python -m twine check`, and `python tests/package_smoke.py`
  - Passed for source and wheel distributions, including isolated wheel installation.
- Disposable Git repository adoption with `adopt --tool codex`, preview then `--apply`
  - Passed: only the expected `AGENTS.md` and `docs/HOW_TO_USE.md` files were created.
- `python -m forgeloop pack` and `token-report`
  - Passed. This run estimated 82.8% selection savings, not a universal or exact token-saving claim.
- `python -m forgeloop release gate . --target stable`
  - Correctly returned non-zero because clean-session acceptance, independent review, and external-store erasure evidence are still outstanding.

## Reviewer Findings

### Architecture

- P1: None found.
- P2: No new finding. Stable promotion remains blocked by tracked external and human evidence requirements.
- P3: None found.

### Security

- P1: None found.
- P2: No new finding. No secret values were printed during the local secrets check; external provider erasure evidence remains an intentional stable-release block.
- P3: None found.

### Testing

- P1: None found.
- P2: No new finding. A live Claude Code clean-session acceptance is not reproducible by this local run and remains tracked as a release gate.
- P3: None found.

### Documentation

- P1: None found.
- P2: None found.
- P3: None found.

## Consolidated Findings

### P1

- None.

### P2

- No new defects. The stable-release blocks are retained because they need independent or external evidence.

### P3

- None.

## Capture Candidates

- A complete local dogfood run can demonstrate source-alpha readiness, but release claims that depend on humans, hosted tools, or external storage must remain separately evidenced.
