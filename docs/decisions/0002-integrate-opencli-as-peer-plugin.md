---
type: decision
date: 2026-05-18
status: accepted
tags: [opencli, integration, security]
---

# 0002 Integrate OpenCLI As A Peer Plugin

ForgeLoop integrates OpenCLI as an optional peer plugin instead of copying OpenCLI source or making it a core dependency.

## Context

OpenCLI can expose browser, website, Electron, and local tool surfaces to AI agents. Browser-backed commands are privileged because they can reuse logged-in sessions.

## Decision

ForgeLoop provides a local plugin source, install plan, doctor checks, and security rules. The actual OpenCLI package remains external and installs only with explicit user action.

## Consequence

ForgeLoop gains an automation bridge without inheriting OpenCLI's runtime surface as core product risk.

