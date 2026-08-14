---
type: capture
date: 2026-08-14
status: current
valid_from: 2026-08-14
tags: [github, release, governance, ownership, security]
---

# Capture: Public Repository Identity

## Decision

ForgeLoop's first public repository is prepared for `sentientsky/ForgeLoop`.

## Applied Values

- Python package homepage, documentation, issues, and source URLs point to the final repository path.
- Private vulnerability reporting points to the repository's GitHub security-advisory form.
- Default code-owner review requests route to `@sentientsky`.
- Public package metadata continues to use `ForgeLoop contributors` rather than a personal email address.

## Why It Matters

The repository can be pushed without placeholder URLs or weak review routing. Personal email addresses are unnecessary for GitHub ownership and are not added to public package metadata by default.

## Remaining Owner Actions

Create the empty public GitHub repository, push `main`, enable security and branch rules, and configure PyPI Trusted Publishing as described in `docs/GITHUB_SETUP.md`.
