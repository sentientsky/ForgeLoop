---
type: standard
date: 2026-05-11
status: current
tags: [deployment, release, compatibility, acceptance]
---

# Deployment Acceptance Standard

ForgeLoop supports many AI coding tools, but support must mean more than "a file exists".

Each supported target should have a clean-session acceptance result.

## Acceptance Levels

- Full: native entry file, tested setup path, validation commands, and known limitations.
- Supported: portable entry file plus at least one tested workflow.
- Beta: entry file exists, but clean-session behaviour needs more real-world testing.
- Portable: generic instructions work, but the tool has no deep native integration yet.

## Required Evidence

For each target, record:

- tool name
- support level
- entry files
- setup command
- last verified date
- validation command
- known limitations
- next improvement

Use `templates/deployment-acceptance-template.md`.

## Release Rule

Before a public release, run:

```bash
python -m forgeloop doctor .
python -m forgeloop validate .
python -m forgeloop compat .
python -m unittest discover -s tests
```

Claims about compatibility should match the acceptance level.

