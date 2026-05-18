---
type: standard
date: 2026-04-17
status: current
tags: [mcp, security, design]
---

# MCP Safety Design

ForgeLoop should not ship a live MCP server until the boundary is boring, tested, and safe.

## Phase 1: No Live MCP

Current state:

- no MCP server
- no write tools
- no automatic memory writes
- no protocol process

This is intentional. The CLI and validation layer must stay reliable first.

## Phase 2: Read-Only MCP

The first MCP server should expose only read-only tools:

- status
- list memory records
- read memory index
- search local markdown index by exact text

No write tools in the first MCP release.

## Phase 3: Controlled Writes

Write tools may be added only after:

- argument validation exists
- malformed-input tests exist
- null-argument tests exist
- max-size tests exist
- stdout/stderr protocol tests exist
- audit-log redaction exists
- write operations are explicit and reversible

## Required Server Rules

- stdout must contain protocol messages only.
- human logs must go to stderr.
- every input must be type checked.
- every string must have length limits.
- every path must resolve inside the repository root.
- symlinks must be rejected for memory writes.
- secrets must be scanned before writes.
- errors must be structured and must not leak sensitive content.

## Tool Naming

Use ForgeLoop language.

Recommended future names:

- `forgeloop_status`
- `forgeloop_list_memory`
- `forgeloop_read_index`
- `forgeloop_search_index`
- `forgeloop_create_note`

Avoid copying another project's MCP tool names or product terminology.

