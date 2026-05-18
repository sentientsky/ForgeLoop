---
type: solution
date: 2026-05-11
status: current
tags: [opencli, plugin, integration, security]
---

# OpenCLI Integrated Peer Plugin

## Problem

ForgeLoop can benefit from OpenCLI's browser and CLI automation, but copying OpenCLI would create licence, version drift, maintenance, and security problems.

## Solution

Use a peer-plugin pattern.

ForgeLoop keeps:

- a local plugin source
- a safe install plan
- doctor checks
- security rules
- capture and review standards

OpenCLI remains external and is installed with the official package path:

```bash
npm install -g @jackwener/opencli@latest
```

## Why This Works

The boundary is clear.

OpenCLI owns browser and adapter runtime behaviour. ForgeLoop owns workflow discipline, safety checks, memory, review, and release evidence.

## Use When

- integrating a fast-moving external developer tool
- avoiding vendored source
- adding a privileged automation surface
- keeping an open source project original

## Validation

Run:

```bash
python -m forgeloop opencli status .
python -m forgeloop opencli plan .
python -m forgeloop doctor .
```

