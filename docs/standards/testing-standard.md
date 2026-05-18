---
type: standard
date: 2026-04-17
status: current
tags: [testing, validation, ci]
---

# Testing Standard

ForgeLoop should test the system that helps other systems test themselves.

## Required Checks

Run these before release:

```bash
python -m unittest discover -s tests
python -m forgeloop doctor .
python -m forgeloop validate .
python -m forgeloop index . --check
python -m forgeloop hook-simulate PreCompact .
```

## What Tests Should Cover

- frontmatter parsing
- required files and folders
- skill metadata
- reviewer agent metadata
- risky hook patterns
- possible secret patterns
- memory index generation
- version consistency
- malformed JSON
- safe note creation
- dry-run hook simulation
- doctor checks
- optional integration readiness

## CI

The GitHub Actions workflow should run on:

- pull requests
- pushes
- Python 3.10
- Python 3.11
- Python 3.12

## Test Philosophy

Start with small deterministic tests.

Add heavier integration tests only when the behaviour exists and is stable.
