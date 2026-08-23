---
type: capture
date: 2026-08-23
status: current
valid_from: 2026-08-23
tags: [governance, memory, privacy, retention, provenance, security]
---

# Governed Memory Foundation

## What Changed

ForgeLoop now validates governed-memory metadata and keeps a metadata-only local audit log outside the repository. The audit log stores hashes of opaque references and verifies its own SHA-256 chain.

## Durable Rule

Personal data does not belong in Git-tracked Markdown. A repository note may contain an opaque pointer to an external provider, but that provider must own access control, retention, export, and erasure evidence for the data it holds.

## Why This Matters

Deleting a working-tree file does not erase Git history, clones, forks, backups, embeddings, graph stores, caches, exports, or provider replicas. A ForgeLoop audit event can document an action, but never proves that those separate stores have completed deletion.

## Reusable Pattern

1. Keep the pointer note `internal`.
2. Describe the externally governed content with `governed_content_classification`.
3. Require provenance, purpose, lawful basis, jurisdiction, retention, and opaque storage reference.
4. Run `forgeloop governance audit` before commit.
5. Record only hashed opaque references in the external audit log.
6. Claim erasure only after every affected provider supplies evidence.

## Follow-Up

Design provider adapters only when each target can expose a scoped deletion and retention-evidence contract that can be tested end to end.
