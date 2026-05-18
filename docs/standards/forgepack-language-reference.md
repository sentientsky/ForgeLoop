---
type: standard
status: current
tags: [memory, context, token-economy, forgepack]
---

# ForgePack Language Reference

ForgePack is the compact memory language used by ForgeLoop V3.

Its text format is called FCP, short for Forge Context Packet.

The purpose is simple: give Claude enough information to choose the right memory file without loading the whole memory system.

## Principle

ForgePack is not a secret language and not an opaque compression trick.

It is:

- compact for the model
- readable by humans
- safe to paste into issues and reviews
- lossless by reference, because the packet points to exact markdown files

The full content remains in normal markdown. The packet carries only metadata and pointers.

## FCP/1 Format

An FCP/1 packet looks like this:

```text
FCP/1
Q=memory token optimisation
MODE=PTR
LOSSLESS=BY_REFERENCE
RECORDS=2/10
MEASURE=UTF8_BYTES;TOKEN_EST=BYTES/4
FCP_BYTES=420
SELECTED_SRC_BYTES=4200
ALL_MEMORY_BYTES=12000
SAVE_SELECTED=90.0%
SAVE_ALL=96.5%
RULE=READ_LISTED_SOURCE_ONLY_WHEN_NEEDED
LEGEND=R|S=score|T=type|ST=status|G=tags|P=path|H=heading
R0|S=21|T=capture|ST=current|G=memory,token|P=docs/captures/example.md|H=Token Economy
END
```

## Fields

- `FCP/1`: format and version.
- `Q`: the task query used to build the packet.
- `MODE=PTR`: the packet is pointer-only.
- `LOSSLESS=BY_REFERENCE`: exact content is preserved in the source file.
- `RECORDS`: returned records over total memory records.
- `MEASURE`: measurement basis.
- `FCP_BYTES`: rendered packet size in UTF-8 bytes.
- `SELECTED_SRC_BYTES`: bytes in selected source files.
- `ALL_MEMORY_BYTES`: bytes in every indexed memory file.
- `SAVE_SELECTED`: measured savings against selected source files.
- `SAVE_ALL`: measured savings against all indexed memory files.
- `RULE`: how Claude should use the packet.
- `LEGEND`: field names for record lines.
- `R0`, `R1`, `R2`: ranked memory records.
- `S`: relevance score from local keyword metadata.
- `T`: record type, such as `capture` or `solution`.
- `ST`: status, such as `current` or `superseded`.
- `G`: tags.
- `P`: exact source path.
- `H`: heading or title.

## How Claude Should Use It

1. Read the FCP packet.
2. Pick only the records that look relevant.
3. Open the exact file path in `P` when detail is needed.
4. Ignore low-confidence records if they do not fit the task.
5. If no record matches, run normal discovery search.
6. Capture the missing memory after the task if the gap is useful.

## Safety Rules

- Never include secrets in a packet query.
- Never treat packet metadata as exact truth.
- Never replace the source markdown with only the packet.
- Never make claims about 80 or 90 percent token savings unless the exact before and after sizes are measured.
- Treat token estimates as approximate until a tokenizer-backed benchmark exists.
- Use `python -m forgeloop tokens "<task query>" . --tool <tool>` for tool-specific reports.
- Treat a token count as exact only when the report says `exact: true`.
- Prefer boring, inspectable text over clever unreadable encodings.

## Why This Beats Context Dumps

Context dumps make Claude read everything first and decide later.

ForgePack asks Claude to decide from a small index first, then read exact files only when needed.

This gives ForgeLoop a path towards large token savings while keeping the memory trustworthy and open source friendly.
