---
type: capture
date: 2026-05-18
status: current
valid_from: 2026-05-18
tags: [opencli, registry, drift, integration]
---

# OpenCLI Registry Drift

## Observation

On 2026-05-18, npm reported `@jackwener/opencli` latest as `1.7.22` with package engine metadata `node >=20.0.0`.

The official OpenCLI installation docs still stated Node.js `>=21.0.0`.

## Decision

ForgeLoop keeps the stricter docs baseline for install readiness and adds live npm metadata as an explicit optional status check.

Use:

```bash
python -m forgeloop opencli status . --fetch-npm
```

## Why

Registry metadata and docs can drift.

ForgeLoop should not silently relax install checks based on live network data, but it should show the drift so maintainers can make a conscious release decision.

