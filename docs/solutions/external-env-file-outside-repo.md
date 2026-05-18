---
type: solution
date: 2026-04-17
status: current
tags: []
---

# Solution: External Env File Outside Repo

## Problem

Local `.env` files are useful, but they are easy to commit by accident. For an open source project, this creates a direct credential leak risk.

## Solution

Commit `.env.example` with blank values only.

Create the real local secrets file outside the repository:

```bash
python -m forgeloop secrets init .
python -m forgeloop secrets path .
```

Check the setup before sharing:

```bash
python -m forgeloop secrets check .
python -m forgeloop validate .
```

## Why It Works

The repo keeps the expected key names, but the values live in a user-specific ForgeLoop config directory. Validation fails if real `.env`-style files appear inside the project.

## Use When

- a contributor needs local API keys
- a repo may become public
- the project needs an example env file without committing values

## Do Not Use When

- production secrets need rotation, audit, and fine-grained access
- a managed secret store is available and required
- secrets need to be shared between team members

## Validation

- `python -m forgeloop secrets check .`
- `python -m forgeloop validate .`

## Related Notes

- Capture: `docs/captures/2026-04-17-external-secrets-outside-repository.md`
- Standard: `docs/standards/secrets-management-standard.md`
