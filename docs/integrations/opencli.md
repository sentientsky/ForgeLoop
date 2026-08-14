---
type: integration
date: 2026-05-11
status: current
tags: [opencli, integration, plugin, browser, automation]
---

# OpenCLI Integration

ForgeLoop integrates OpenCLI as an external peer plugin.

OpenCLI is integrated, not copied. ForgeLoop does not vendor OpenCLI source, adapters, skills, browser extension code, or command registry files.

## Why It Exists

OpenCLI gives AI agents a deterministic command surface for websites, browser sessions, Electron apps, and local tools.

ForgeLoop adds the discipline around it:

- discovery before action
- explicit install plan
- no hidden browser automation
- security review for privileged tasks
- memory capture only after sensitive data is filtered
- measurable context packets before token-saving claims

## Install Flow

Check local readiness:

```bash
python -m forgeloop opencli status .
```

Check current npm package metadata when you want to compare against the live registry:

```bash
python -m forgeloop opencli status . --fetch-npm
```

Preview the plan:

```bash
python -m forgeloop opencli plan .
```

Install or update OpenCLI and install the ForgeLoop plugin source:

```bash
python -m forgeloop opencli install . --execute
```

Include OpenCLI's AI skills only when you want them installed into the local AI-agent skill system:

```bash
python -m forgeloop opencli install . --execute --with-skills
```

Run OpenCLI's own doctor only when you are ready for the local daemon and browser bridge checks:

```bash
python -m forgeloop opencli install . --execute --run-doctor
```

## What The Installer Does

ForgeLoop uses the latest OpenCLI package spec:

```bash
npm install -g @jackwener/opencli@latest
```

Then it installs this repository's plugin source:

```bash
opencli plugin install integrations/opencli
```

The actual command uses an absolute path and fixed arguments. It does not use shell interpolation. It refuses plugin folders or manifests that use symlinks, then verifies the installed binary and command registry with `opencli --version` and `opencli list -f json` before optional doctor or skill steps.

ForgeLoop keeps a conservative Node.js baseline from the OpenCLI installation docs. The npm package metadata can change faster than the docs, so `--fetch-npm` records registry drift instead of silently changing the local policy.

## Plugin Commands

The local plugin exposes read-only ForgeLoop commands through OpenCLI:

- `opencli forgeloop status`
- `opencli forgeloop doctor`
- `opencli forgeloop pack --query "memory validation"`

These commands call `python -m forgeloop` with fixed subprocess arguments.

## Security Rules

- Do not run browser-backed OpenCLI commands without explicit user intent.
- Treat logged-in browser sessions as privileged.
- Do not capture cookies, tokens, private messages, payment data, or private account data into ForgeLoop memory.
- Ask before posting, deleting, buying, messaging, or changing account state.
- Keep OpenCLI configuration and browser credentials outside the ForgeLoop repository.
- Run `python -m forgeloop doctor .` before release.

## Useful ForgeLoop Commands

```bash
python -m forgeloop opencli status .
python -m forgeloop opencli plan .
python -m forgeloop opencli install . --execute
python -m forgeloop doctor .
python -m forgeloop compat .
```

## References

- OpenCLI website: https://opencli.info/
- Getting started: https://opencli.info/docs/guide/getting-started.html
- Installation: https://opencli.info/docs/guide/installation.html
- Plugins: https://opencli.info/docs/guide/plugins.html
- Browser Bridge: https://opencli.info/docs/guide/browser-bridge.html
- GitHub repository: https://github.com/jackwener/opencli
