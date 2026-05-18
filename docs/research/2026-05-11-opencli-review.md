---
type: research
date: 2026-05-11
status: current
tags: [opencli, research, integration]
---

# OpenCLI Review

## Sources Reviewed

- https://opencli.info/
- https://opencli.info/docs/guide/getting-started.html
- https://opencli.info/docs/guide/installation.html
- https://opencli.info/docs/guide/plugins.html
- https://opencli.info/docs/guide/browser-bridge.html
- https://github.com/jackwener/opencli
- https://claudemarketplaces.com/skills/jackwener/opencli/opencli-usage

## Findings

OpenCLI is a Node-based tool that turns websites, browser sessions, Electron apps, and local tools into deterministic command-line surfaces.

The current standard install path is:

```bash
npm install -g @jackwener/opencli
```

OpenCLI documents Node.js >= 21 for the npm path.

Update on 2026-05-18: the npm registry reported `@jackwener/opencli` latest as `1.7.22` and package engine metadata as `node >=20.0.0`, while the OpenCLI installation docs still said Node.js `>=21.0.0`. ForgeLoop therefore keeps the stricter docs baseline by default and exposes `python -m forgeloop opencli status . --fetch-npm` to make this drift visible.

The update path uses:

```bash
npm install -g @jackwener/opencli@latest
```

Browser-backed commands use a Chrome or Chromium browser bridge and a local daemon. This is useful, but it is privileged because it reuses logged-in browser sessions.

OpenCLI plugins can be installed from GitHub, git URLs, or local folders. A plugin may include `opencli-plugin.json`.

OpenCLI skills can be installed with:

```bash
npx skills add jackwener/opencli
```

## Integration Decision

ForgeLoop should integrate OpenCLI, not copy it.

The correct shape is:

- keep OpenCLI as an external peer dependency
- install `@jackwener/opencli@latest` only when explicitly requested
- provide a local ForgeLoop OpenCLI plugin source
- keep browser-backed actions behind explicit user intent
- route all public safety and completion checks through ForgeLoop's own doctor, check, and capture system

## Adopted Ideas

- deterministic CLI surfaces for repeatable actions
- plugin source with metadata
- explicit doctor command
- browser bridge treated as a privileged capability
- command output that is friendly to AI tools

## Rejected Ideas

- copying OpenCLI skills into ForgeLoop
- vendoring OpenCLI adapters
- auto-running browser bridge setup during normal ForgeLoop setup
- making OpenCLI a required dependency for ForgeLoop core
