---
type: frame
date: 2026-05-11
status: current
tags: [opencli, integration, security]
---

# Frame: OpenCLI Integration

## Goal

Add OpenCLI as an optional integrated peer plugin for ForgeLoop.

## Scope

- ForgeLoop CLI status, plan, and install commands for OpenCLI.
- Local OpenCLI plugin source.
- Security-first documentation.
- Doctor checks for integration readiness.
- Claude skill for OpenCLI use.

## Non-Goals

- Copy OpenCLI source.
- Require OpenCLI for normal ForgeLoop use.
- Automatically run browser-backed automation.
- Store browser credentials or site data.

## Risks

- Global npm install can fail or change the user's machine.
- Browser bridge reuses logged-in sessions.
- OpenCLI versions can drift.
- Plugin command API may evolve.

## Controls

- Install requires explicit `--execute`.
- Doctor checks plugin source and Node readiness.
- Browser doctor requires explicit `--run-doctor`.
- Docs state that OpenCLI is integrated, not copied.

## Validation

```bash
python -m forgeloop opencli status .
python -m forgeloop opencli plan .
python -m forgeloop doctor .
python -m forgeloop validate .
python -m unittest discover -s tests
```

## Capture Target

Capture the peer-plugin pattern as a reusable solution.

