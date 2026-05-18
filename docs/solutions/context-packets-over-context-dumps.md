---
type: solution
status: current
tags: [memory, context, token-economy, forgepack]
---

# Context Packets Over Context Dumps

## Problem

AI agents often waste tokens by reading whole memory folders before they know which notes matter.

This creates cost, noise, and worse recall.

## Solution

Use a compact packet first.

The packet should contain:

- query
- result count
- source path
- heading
- type
- tags
- status
- relevance score

Then the agent opens only the exact source files that are needed.

The packet should also report measured byte savings so public claims are evidence-backed.

## ForgeLoop Command

```bash
python -m forgeloop pack "task query" . --limit 5
```

## Why It Works

The packet is cheap to read, but the source remains exact.

This gives most of the benefit of compression without losing evidence or creating a private format that only the model can inspect.

The current token estimate is approximate and should not be presented as an exact tokenizer count.

## Reuse Rule

Any future search engine, vector index, or graph system should return FCP-compatible packets before it returns full content.
