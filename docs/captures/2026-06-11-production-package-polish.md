---
type: capture
date: 2026-06-11
status: current
valid_from: 2026-06-11
tags: [release, packaging, docs, github, production]
---

# Production Package Polish

## Decision

ForgeLoop's production package baseline includes community health files, issue and pull request templates, release publishing docs, command reference, troubleshooting, support docs, and release workflows.

## Why

A package can pass tests and still feel unfinished to users.

Production polish needs:

- clear install and command docs
- troubleshooting paths
- changelog and support policy
- contribution and security gates
- issue and pull request templates
- package build and publishing guidance
- optional supply-chain checks

## Reusable Lesson

Treat release assets as part of the product, not repository decoration.

ForgeLoop now checks production release assets through `python -m forgeloop doctor .`.

