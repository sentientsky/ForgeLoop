# Maintainer Guide

This guide is for people preparing ForgeLoop for public use.

## Routine Checks

```bash
python -m pip install -e ".[dev]"
python -m ruff check forgeloop tests
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m build
python -m twine check dist/*
python tests/package_smoke.py dist .
```

## Review Priorities

1. Security and secrets.
2. Correctness of commands and docs.
3. Compatibility with Claude Code and Codex.
4. Token measurement honesty.
5. Beginner clarity.

## Issue Triage

- Bugs need reproduction steps and doctor output.
- Feature requests need a clear user workflow.
- Tool integrations need a compatibility file and acceptance prompt.
- Security issues should move to private handling.

## Maintenance Rhythm

- Review security and dependency alerts weekly.
- Triage new issues and pull requests at least weekly.
- Review compatibility notes and AI tool instructions monthly.
- Refresh clean-session compatibility evidence before each minor release.
- Remove stale memory only through a superseding capture or decision record.

Approval authority, sole-maintainer safeguards, and high-risk review rules live in `../GOVERNANCE.md`.

For first-time repository publication and settings, follow `GITHUB_SETUP.md`.

## Release Notes

Keep `CHANGELOG.md` concise.

Mention:

- new commands
- changed workflow rules
- compatibility changes
- security hardening
- known limitations

## Package Metadata

The final project URLs are prepared locally for the first push:

```toml
[project.urls]
Homepage = "https://github.com/sentientsky/ForgeLoop"
Documentation = "https://github.com/sentientsky/ForgeLoop/tree/main/docs"
Issues = "https://github.com/sentientsky/ForgeLoop/issues"
Source = "https://github.com/sentientsky/ForgeLoop"
```
