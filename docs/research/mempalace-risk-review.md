---
type: research
date: 2026-04-17
status: current
tags: [memory, safety, originality, research]
---

# MemPalace Risk Review

This note records what ForgeLoop should learn from reviewing the attached `mempalace-develop.zip` package and public MemPalace material.

The goal is not to clone MemPalace. The goal is to understand useful memory patterns and avoid known design, security, portability, and positioning risks.

## What To Learn

Useful ideas:

- local-first memory
- preserving exact source text when wording matters
- a structured mental model for memory
- time-aware facts
- background capture at safe workflow moments
- MCP-style access as a future integration layer
- tests for hooks, package versions, input handling, and indexing

## What To Avoid

Avoid these risks from the beginning:

- unbounded file ingestion
- following symlinks while mining memory
- shell hooks that use unsafe interpolation or `eval`
- MCP tools accepting null or malformed arguments
- hardcoded protocol versions
- stdout pollution in protocol servers
- storing secrets in memory or logs
- benchmark claims that are not clearly reproducible
- very large benchmark artefacts in the main repo
- version drift between package, plugin, and docs
- platform assumptions that break on Windows, macOS, Linux, or Apple Silicon

## ForgeLoop Response

ForgeLoop starts with a dependency-light validation CLI instead of a vector database.

This is deliberate:

- fewer installation problems
- easier beginner setup
- easier open source review
- fewer platform surprises
- clearer boundary between workflow and retrieval engine

ForgeLoop can add MCP, vector search, or hosted services later. The MVP should first prove that the workflow, memory structure, validation, and capture habits are useful.

## Naming And Originality

ForgeLoop should keep its own product language.

Use:

- ForgeLoop
- Discover, Frame, Build, Check, Capture
- local memory index
- memory records
- capture notes
- solution notes
- entity notes
- timeline notes

Avoid adopting distinctive MemPalace product terms such as branded compression dialects, closet/hall/tunnel layers, or their installation language.

## Sources Reviewed

- Attached package: `mempalace-develop.zip`
- Official release notes: https://github.com/MemPalace/mempalace/releases
- Official site: https://mempalaceofficial.com/
- Hook documentation: https://mempalaceofficial.com/guide/hooks.html
- Memory stack documentation: https://mempalaceofficial.com/concepts/memory-stack.html
- Public critique, treated as unverified but useful for risk thinking: https://gist.github.com/roman-rr/0569fc487cc620f54a70c90ab50d32e3

