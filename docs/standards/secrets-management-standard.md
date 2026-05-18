---
type: standard
date: 2026-04-17
status: current
tags: [security, secrets, configuration]
---

# Secrets Management Standard

ForgeLoop must be safe to publish as open source at any moment.

That means real secrets do not live in the repository.

## Rules

- Commit `.env.example` with blank values only.
- Never commit `.env`, `.env.local`, `.envrc`, `secrets.env`, or any `*.env` file.
- Store local development secrets outside the repository.
- Do not print secret values in CLI output.
- Do not store secrets in captures, solutions, logs, indexes, or memory notes.
- Use GitHub repository secrets or a real secret manager for CI/CD.
- Rotate any secret that was committed, pasted into an issue, or printed in logs.

## Local Development

Create the external secrets file:

```bash
python -m forgeloop secrets init .
```

Show where the file lives:

```bash
python -m forgeloop secrets path .
```

Check the setup:

```bash
python -m forgeloop secrets check .
python -m forgeloop validate .
```

The external file is stored under a platform-specific ForgeLoop config directory, outside the project folder.

## Why Not A Real `.env` In The Repo?

A real `.env` file is easy to commit by accident.

ForgeLoop keeps only the shape of the environment in the repo and keeps values outside the repo.

## CI/CD

CI/CD secrets should use the hosting provider's secret store.

For GitHub, use repository or organisation secrets and enable push protection where available.

## Emergency Response

If a secret leaks:

1. Revoke or rotate it immediately.
2. Remove it from the current code.
3. Treat git history as compromised.
4. Check logs, captures, indexes, and issues for copies.
5. Document the incident without repeating the secret value.

