---
type: capture
date: 2026-04-26
status: current
valid_from: 2026-04-26
tags: [memory, token-economy, forgepack, v3]
---

# Capture: ForgeLoop V3 Token Economy

## Decision

ForgeLoop V3 uses compact context packets before loading memory.

The principle is:

```text
compact by default, exact by reference
```

## Why

Large memory folders waste tokens and can make Claude less reliable.

Opaque AI-only languages reduce auditability.

ForgeLoop keeps the exact memory in markdown and sends Claude a compact FCP/1 pointer packet first.

## Implementation

Use:

```bash
python -m forgeloop pack "task query" . --limit 5
```

The packet includes paths, tags, headings, status, and scores. It does not include full note bodies.

It also reports rendered packet bytes, selected source bytes, all memory bytes, and measured savings percentages.

## Follow-Up

Add tokenizer-backed measurement before replacing the current bytes divided by 4 token estimate.
