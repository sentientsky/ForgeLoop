---
type: check
date: 2026-09-24
status: draft
task: Cross-platform profile adoption
tags: [installer, security, portability, ci]
---

# Check: Cross-platform profile adoption

## Summary

Added `forgeloop adopt` as a preview-first, profile-only installer for existing projects. It uses a fixed tool-profile allowlist, does not overwrite differing files, uses exclusive file creation, rejects traversal and symlink/junction/reparse-point components, and rolls back files created by the current run when a later write fails. Codex's generic README requirement was made optional so adoption does not inject ForgeLoop's README into a host project.

Hosted tests now cover Python 3.10-3.14 on Ubuntu, Windows, and macOS. The stable `cross-platform` aggregator is intended as the branch-protection context so matrix expansion cannot strand the required status check. This verifies ForgeLoop's code on those runner images, not live loading or behaviour inside the named AI coding tools.

## Validation

- `python -m ruff check forgeloop tests`: passed.
- `python -m unittest discover -s tests`: 61 tests passed.
- `python -m coverage run -m unittest discover -s tests` and `python -m coverage report --fail-under=70`: passed at 73% branch coverage.
- `python -m forgeloop validate .`, `compat .`, `doctor .`, `index . --check`, `secrets check .`, `governance audit .`, and `governance verify .`: passed.
- `git diff --check`: passed.
- GitHub Windows/macOS/Linux CI matrix and branch-protection context: pending pull request checks and repository-settings update.

## Reviewer Findings

### Architecture

- P1:
- P2:
- P3:

### Security

- P1: None found in the reviewed change.
- P2: None found in the reviewed change.
- P3: The portable path checks do not provide native directory-handle protection against another local process deliberately replacing a directory during installation. Run without elevated privileges in a trusted workspace; differing static files and observed reparse points are rejected.

### Testing

- P1: None found in the reviewed change.
- P2: Hosted Windows and macOS results are pending.
- P3: Live Claude Code and Codex clean-session acceptance is not exercised by this CLI test suite.

### Documentation

- P1: None found in the reviewed change.
- P2: None found in the reviewed change.
- P3: The adopter adds entry profiles only, not the CLI/runtime, automatic merge, backup, update, or uninstall support. This limit is stated in the user guides.

## Consolidated Findings

### P1

- None.

### P2

- None.

### P3

- None.

## Capture Candidates

- Prefer an additive installer that previews exact paths, preserves every differing file, and reports a partial conflict as non-zero instead of silently merging AI instructions.
- File presence proves packaging only. Tool compatibility still needs dated clean-session evidence in each actual client.
