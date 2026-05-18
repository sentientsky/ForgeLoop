---
type: benchmark
date: 2026-05-18
status: current
tags: [tokens, benchmark, fcp]
---

# Token Packet Baseline

## Command

```bash
python -m forgeloop tokens "release readiness OpenCLI security compatibility" . --tool codex --limit 5
```

## Result

- Tool profile: Codex
- Exact: false
- Method: UTF-8 bytes divided by 4
- Packet tokens: 280
- Selected source tokens: 1168
- Corpus source tokens: 6559
- Savings against selected source: 76.0 percent

## Caveat

This is a local estimate, not a public product claim.

Public claims need repeated fixtures, exact tokenizer evidence when available, and dated command output.

