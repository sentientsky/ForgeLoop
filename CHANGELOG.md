# Changelog

All notable ForgeLoop changes should be recorded here.

ForgeLoop follows practical semantic versioning:

- patch versions for fixes and documentation corrections
- minor versions for new compatible commands, skills, templates, or integrations
- major versions for breaking workflow, CLI, or package changes

## 0.1.0 - 2026-09-24

- clarified GitHub-template alpha distribution and removed PyPI publishing to prevent a package-name/import collision
- changed compatibility reporting to state that it checks profile-file presence, not live external-tool behaviour
- added full-source GitHub release archives with secret-path screening and build provenance
- added downloadable SHA-256 checksums and fail-closed verification for release retries
- replaced outdated first-push and PyPI setup instructions with current repository operations
- added Python 3.13 and 3.14 CI coverage
- raised developer-tool minimums to match tested hash-locked CI versions and aligned CodeQL, Scorecard, and provenance actions with reviewed upstream updates
- added Ruff linting and a measured branch-coverage floor
- added an isolated installed-wheel smoke test to CI and releases
- pinned every external GitHub Action to a full commit SHA
- added CodeQL scanning, release tag verification, and build provenance
- added pip dependency updates to Dependabot
- added public governance and one-time GitHub setup guidance
- added public roadmap and current-status guidance
- added workflow validation for unsafe triggers, broad permissions, and moving action tags
- fixed the ignore rules so the Claude Build skill is included in fresh clones
- hardened external-secret writes against dangling symlinks and made OpenCLI install verification match its published plan
- raised the release validation tool floor to Twine 7 for current Core Metadata compatibility
- prepared the public repository identity, metadata URLs, security contact, and code-owner routing for `sentientsky/ForgeLoop`
- removed routine external-secrets paths from CLI and JSON status output to prevent sensitive-path disclosures
- scoped Scorecard publishing permissions to its analysis job so OpenSSF accepts the attested workflow
- pinned Scorecard to the verified upstream commit behind its annotated v2.4.3 tag
- replaced annotated CodeQL action tag-object pins with the verified v4.36.2 commit
- scoped CodeQL security-event publishing permission to its analysis job
- replaced floating GitHub workflow tool installs with cross-platform hash-locked requirements
- added a bounded seeded Atheris workflow for frontmatter parser fuzzing
- enabled GitHub Dependabot alerts, security updates, and private vulnerability reporting
- configured Dependabot to monitor the hash-locked GitHub tooling requirements
- protected `main` with required pull requests, CI, CodeQL, fuzz checks, linear history, and no force-push or deletion
- pinned GitHub Actions jobs to Ubuntu 24.04 to avoid floating runner-image transitions
- updated Python code to satisfy current Ruff diagnostics and narrowed optional-tokenizer error handling
- added governed-memory metadata checks for provenance, lawful basis, jurisdiction, retention, and opaque external-store pointers
- added an external metadata-only, tamper-evident governance audit log with hash-chain verification
- documented strict boundaries: no personal data in Git-tracked memory, no certification claim, and no unsupported claim of third-party erasure completion

## 0.1.0 - Public Release Foundation

Initial public-release foundation.

Included:

- five-stage ForgeLoop workflow
- Claude Code project skills and reviewer agents
- portable AI coding tool entry files
- local memory palace and generated memory index
- Forge Context Packets and token reports
- validation, doctor, compatibility, secrets, setup, and OpenCLI commands
- external secrets workflow
- optional OpenCLI peer integration
- release guides, FAQ, benchmarks, deployment acceptance prompts, and contribution gates
- production package polish: support docs, command reference, troubleshooting, publishing guide, issue templates, PR template, Dependabot, release workflow, and Scorecard workflow

Known limitations:

- exact token counting requires optional tokenizer support
- OpenCLI is optional and must be installed explicitly
- live clean-session compatibility transcripts should be refreshed as target tools evolve
