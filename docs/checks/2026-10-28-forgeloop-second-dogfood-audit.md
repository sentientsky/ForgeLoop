---
type: check
date: 2026-10-28
status: current
task: ForgeLoop second dogfood audit
build: docs/builds/2026-10-28-forgeloop-second-dogfood-audit.md
tags: [dogfood, workflow, validation, security, release]
---

# Check: ForgeLoop Second Dogfood Audit

## Summary

ForgeLoop completed a user-style self-audit of its command surface, memory packet, setup/adoption safety, health checks, and release gates. No new product-code defect was reproduced. The one unexpected command result was traced to an incorrect test expectation: non-zero exit for a partial adoption conflict is documented and intentional.

## Validation

- `python -m forgeloop --help`, `intro --plain`, `status .`, `setup --list`, `setup . --tool all-supported --dry-run --json`, `compat .`, `doctor .`, and `hook-simulate PreCompact . --json`
  - Passed. Dry-run did not write configuration; compatibility described file presence only; hook simulation reported `executes_commands: false`.
- Temporary adoption test, clean destination
  - Preview exited 0 without writing. Apply exited 0 and created `AGENTS.md` and `docs/HOW_TO_USE.md`.
- Temporary adoption test, conflicting destination
  - Preview and apply exited 1. The existing user-owned `AGENTS.md` content remained byte-for-byte unchanged; the non-conflicting guide was created during apply.
- Initial full test run immediately after note creation
  - Four tests correctly failed because the new Capture made the memory index stale. `doctor` surfaced the stale index and the source-alpha gate failed closed. Rebuilt the index; this was expected enforcement, not a product defect.
- `python -m unittest discover -s tests` after index refresh
  - Passed: 76 tests.
- `python -m ruff check forgeloop tests`, `python -m forgeloop validate .`, `python -m forgeloop doctor .`, and `python -m forgeloop index . --check`
  - Passed.
- `python -m coverage run --branch -m unittest discover -s tests` and coverage report
  - Passed: 75% branch coverage against a 70% minimum.
- `uvx --from pip-audit pip-audit --requirement .github/requirements-ci.txt`
  - No known vulnerabilities found.
- `uvx --from bandit bandit -q -r forgeloop`
  - Three low-severity heuristic findings and no medium/high findings. The token-estimate field name is not a credential. The OpenCLI subprocess uses an argument list, `shell=False`, and a timeout.
- `python -m build --no-isolation`, `python -m twine check dist/*`, and `python tests/package_smoke.py dist .`
  - Source and wheel builds passed, Twine checks passed, and isolated wheel smoke test passed.
- Hosted GitHub CI, CodeQL, and fuzz checks passed on the code-identical preceding commit `66adaae`. This dogfood pass changes documentation and the memory index only; hosted checks for its final commit are still required.
- `python -m forgeloop opencli plan .`
  - Passed in plan-only mode. OpenCLI was not installed or invoked.
- `pack` and `tokens` for `self audit secure setup release gate workflow`
  - Selected 8 of 33 indexed records. Report measured 87.9% byte reduction against selected source and 96.2% against indexed corpus for this query. Token values are estimates, not exact provider counts or universal savings claims.
- `python -m forgeloop secrets check .`, `governance audit .`, and `governance verify .`
  - Passed without displaying secret values; no governed records or audit events were present.
- `python -m forgeloop release gate .`
  - Source alpha passed; public status and claims checks passed.
- `python -m forgeloop release gate . --target stable`
  - Returned the expected non-zero result with exactly three known evidence blockers: live Claude acceptance, independent maintainer review, and provider-backed external erasure evidence.
- Full unit tests, Ruff, coverage, dependency audit, package build/smoke, and hosted CI are recorded after the final run below.

## Reviewer Findings

### Architecture

- P1: None found.
- P2: Full runtime installation/update/uninstall remains outside the product promise; the repository template is the complete distribution.
- P3: None found.

### Security

- P1: None found during this pass. The previous setup symlink and CI certificate dependency fixes remain present on this branch.
- P2: Bandit emits three low-severity heuristics; manual review found no medium/high-risk behavior. OpenCLI and third-party tool behavior remain external; the plan command does not establish their runtime safety.
- P3: None found.

### Testing

- P1: None found.
- P2: Local simulation cannot substitute for authenticated Claude acceptance or independent human review.
- P3: None found.

### Documentation

- P1: None found.
- P2: None found; the observed non-zero partial-conflict result is documented in installation guidance.
- P3: None found.

## Consolidated Findings

### P1

- None.

### P2

- Stable production promotion remains blocked by external/human evidence requirements, as intended.
- The Scorecard dependency vulnerability alert remains attached to `main` until a reviewed remediation is merged and Scorecard rescans.

### P3

- None.

## Capture Candidates

- A non-zero adoption result can mean partial conflict, not total rollback: inspect per-file actions, preserve conflicting user files, and verify which absent files were safely added.
