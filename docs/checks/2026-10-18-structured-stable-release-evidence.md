---
type: check
date: 2026-10-18
status: current
task: Structured stable release evidence
build:
tags: [release, governance, security, evidence]
---

# Check: Structured stable release evidence

## Summary

The stable release gate no longer infers three critical promotion conditions from Markdown phrases. It now reads a size-bounded, versioned JSON manifest whose default entries are deliberately blocked. A passing entry must link to a safe repository evidence path, have a non-future ISO date, and include role-specific fields for Claude acceptance, independent review, or provider erasure verification.

## Validation

- `python -m unittest discover -s tests`
  - Passed: 70 tests.
- `python -m ruff check forgeloop tests`
  - Passed.
- `python -m coverage run -m unittest discover -s tests && python -m coverage report`
  - Passed: 74% total coverage, above the configured 70% floor.
- `python -m forgeloop validate .` and `python -m forgeloop release gate .`
  - Passed. Source-alpha remains ready and the three stable conditions remain deliberately blocked.
- `python -m build --no-isolation`, `python -m twine check`, and `python tests/package_smoke.py`
  - Passed for both source and wheel distributions, including an isolated wheel installation.

## Reviewer Findings

### Architecture

- P1: None found.
- P2: None found.
- P3: The stable manifest is an integrity and completeness guard, not proof of the linked external facts. Protected review remains necessary.

### Security

- P1: None found.
- P2: None found.
- P3: Evidence paths are restricted to existing files under `docs/`; the manifest never accepts provider URLs, credentials, or external file paths.

### Testing

- P1: None found.
- P2: None found.
- P3: New tests cover a valid structured-evidence fixture and a missing required erasure field.

### Documentation

- P1: None found.
- P2: None found.
- P3: The release checklist and roadmap explain the new boundary and the remaining human/provider work.

## Consolidated Findings

### P1

- None.

### P2

- None.

### P3

- None.

## Capture Candidates

- Stable-release policy should use explicit, machine-validated evidence records rather than rely on the presence or absence of prose phrases.
