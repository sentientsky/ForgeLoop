---
type: frame
date: 2026-04-26
status: current
tags: [v3, memory, token-economy, forgepack]
---

# ForgeLoop V3 Token Memory Plan

## Goal

Make ForgeLoop much more token-efficient without losing the full source of truth.

The core strategy is lossless by reference:

- exact content stays in markdown
- Claude receives compact pointers first
- full files load only when needed

## Non-Goals

- Do not create an opaque AI-only language.
- Do not add a database as the core source of truth.
- Do not activate automatic hooks by default.
- Do not claim exact token savings until measured.
- Do not copy MemPalace, memsearch, claude-mem, or other projects.

## V3 Architecture

### L0: Always-Loaded Instructions

`CLAUDE.md` remains the small operating manual.

It should contain rules, not long knowledge.

### L1: Forge Context Packet

`python -m forgeloop pack "<query>" .` returns FCP/1.

FCP includes ranked paths, headings, tags, status, and byte estimates.

### L2: Source Markdown

Claude opens only the files listed in the packet that are useful for the task.

### L3: Durable Knowledge

Captures and solutions are promoted when a lesson repeats.

### L4: Optional Retrieval Engines

Future versions may add local SQLite FTS, BM25, embeddings, or graph retrieval.

Those tools must remain derived indexes. Markdown stays canonical.

## Build Scope For This Phase

Completed in this V3 pass:

- `forgeloop pack` CLI command
- FCP/1 text renderer
- measured FCP byte reporting
- pointer-only context tests
- `pack-context` Claude skill
- ForgePack language reference
- memory tools field review
- beginner how-to document
- GitHub page copy
- V3 capture and reusable solution note

## Security Requirements

- Reject secret-like packet queries.
- Keep packets ASCII and readable.
- Never include full memory body text in FCP output.
- Keep real `.env` files outside the repository.
- Keep hooks opt-in until they have deterministic tests and limits.

## Validation

Run:

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop compat .
python -m forgeloop pack "memory token optimisation" . --limit 5
python -m forgeloop index .
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m compileall forgeloop tests
```

## Next Phases

1. Add a measured context report that compares packet size against source file size.
2. Add optional local SQLite FTS for larger memory sets.
3. Add safe hook examples for `UserPromptSubmit` and `PreCompact`.
4. Add chunk anchors inside long capture notes.
5. Add stale-memory checks for superseded decisions.
6. Add a benchmark fixture before making public savings claims.
