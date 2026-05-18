---
type: capture
date: 2026-05-11
status: current
valid_from: 2026-05-11
tags: [opencli, integration, security, plugin]
---

# OpenCLI Integration Capture

## Decision

ForgeLoop integrates OpenCLI as an optional peer plugin.

OpenCLI is installed or updated with `@latest` only when the user explicitly runs the ForgeLoop OpenCLI install command with `--execute`.

## Why

This gives ForgeLoop deterministic browser, Electron, website, and local CLI automation without copying OpenCLI code or making it a required dependency.

## Safety Rule

Browser-backed OpenCLI commands are privileged because they reuse the user's logged-in browser session.

ForgeLoop must not run those commands silently, and it must not save sensitive browser output into memory.

## Reusable Pattern

For fast-moving external tools:

- integrate as a peer dependency
- keep install explicit
- check versions and local readiness
- avoid vendoring source
- document the trust boundary
- add doctor checks

