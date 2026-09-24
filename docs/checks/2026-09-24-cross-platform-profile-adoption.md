---
type: check
date: 2026-09-24
status: current
task: Cross-platform profile adoption
tags: [installer, security, portability, ci]
---

# Check: Cross-platform profile adoption

## Summary

Added `forgeloop adopt` as a preview-first, profile-only installer for existing projects. It uses a fixed tool-profile allowlist, does not overwrite differing files, uses exclusive file creation, rejects traversal and symlink/junction/reparse-point components, and rolls back files created by the current run when a later write fails. Codex's generic README requirement was made optional so adoption does not inject ForgeLoop's README into a host project.

Hosted tests now cover Python 3.10-3.14 on Ubuntu, Windows, and macOS. The first matrix run exposed a non-canonical macOS temporary path in a test fixture; the fixture was corrected to test the intended leaf-file behaviour, and all subsequent platform runs passed. The stable `cross-platform` aggregator is required by branch protection so matrix expansion cannot strand the status gate. This verifies ForgeLoop's code on those runner images, not live loading or behaviour inside the named AI coding tools.

## Validation

- `python -m ruff check forgeloop tests`: passed.
- `python -m unittest discover -s tests`: 61 tests passed.
- `python -m coverage run -m unittest discover -s tests` and `python -m coverage report --fail-under=70`: passed at 73% branch coverage.
- `python -m forgeloop validate .`, `compat .`, `doctor .`, `index . --check`, `secrets check .`, `governance audit .`, and `governance verify .`: passed.
- `git diff --check`: passed.
- GitHub PR #26 at implementation commit `ede7e01`: Python 3.10-3.14 passed on Ubuntu, Windows, and macOS; package quality, CodeQL, fuzz, and the stable `cross-platform` aggregator passed.
- GitHub `main` required checks now include `cross-platform`; all eight existing required checks and strict branch-up-to-date enforcement were preserved.

## Reviewer Findings

### Architecture

- P1: None found.
- P2: None found.
- P3: None found.

### Security

- P1: None found in the reviewed change.
- P2: None found in the reviewed change.
- P3: The portable path checks do not provide native directory-handle protection against another local process deliberately replacing a directory during installation. Run without elevated privileges in a trusted workspace; differing static files and observed reparse points are rejected.

### Testing

- P1: None found in the reviewed change.
- P2: None found after hosted Windows and macOS matrices passed.
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

- The profile adopter is additive only; it does not provide managed full-runtime installation, automatic merge, update, backup, or uninstall.
- The installer does not use native directory-handle APIs to defeat a hostile local process racing parent-directory changes; run it unprivileged in a trusted workspace.
- Live clean-session behaviour inside Claude Code and Codex still needs dated acceptance evidence.

## Capture Candidates

- Prefer an additive installer that previews exact paths, preserves every differing file, and reports a partial conflict as non-zero instead of silently merging AI instructions.
- File presence proves packaging only. Tool compatibility still needs dated clean-session evidence in each actual client.
