---
type: decision
date: 2026-05-18
status: accepted
tags: [memory, security, release]
---

# 0001 Keep ForgeLoop Local First

ForgeLoop keeps memory, validation, token measurement, and release checks local-first for the public MVP.

## Context

Hosted services, provider APIs, active hooks, MCP servers, vector search, and browser bridges can all be useful later. They also add secrets, network calls, install complexity, and trust boundaries.

## Decision

The public release keeps the core product dependency-light and local-first. Optional integrations such as OpenCLI stay explicit and opt-in.

## Consequence

ForgeLoop is easier to audit and safer to publish, but advanced automation remains roadmap work until it has stronger tests and opt-in setup.

