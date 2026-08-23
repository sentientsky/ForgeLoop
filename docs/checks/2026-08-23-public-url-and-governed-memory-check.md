---
type: check
date: 2026-08-23
status: current
tags: [release, security, governance, urls, codeql]
---

# Public URL And Governed Memory Check

## Scope

- public metadata URL placeholders
- sensitive-path output reported by CodeQL
- governed-memory metadata and audit-log safety
- source, package, and installed-wheel checks

## Findings

### Resolved

- `secrets init` no longer prints the external secrets path in routine text or JSON output.
- `secrets check` no longer exposes the external full path in routine text or JSON output.
- Repository validation rejects common GitHub account placeholders before publication.
- Governed-memory metadata is checked for provenance, lawful basis, jurisdiction, retention, and opaque identifiers.
- The audit log stores metadata hashes only and is verified as a hash chain.

### Boundaries

- ForgeLoop does not store personal data in Git-tracked Markdown.
- ForgeLoop does not certify legal compliance or third-party erasure completion.
- The previously configured `sentientsky/ForgeLoop` remote was unavailable during this check, so remote CodeQL alerts could not be queried. A replacement public repository must run CodeQL after the verified push.

## Validation Evidence

- Ruff passed.
- 45 unit tests passed.
- Branch coverage was 72 percent, above the enforced 70 percent floor.
- `forgeloop validate`, `doctor`, `compat`, `index --check`, `governance audit`, `governance verify`, and `secrets check` passed.
- Package build, Twine metadata validation, and installed-wheel smoke test passed.

## Outcome

No P1 issue remains in the local release tree. The next required evidence is a fresh GitHub Actions run on the replacement public repository.
