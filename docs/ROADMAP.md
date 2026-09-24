# Roadmap And Current Status

## Current Status

ForgeLoop is a public GitHub source alpha. The repository is intended to be used as a starter template for a new project. Its local CLI selects a tool profile and checks repository files; it does not merge ForgeLoop into an existing project or prove that an external AI tool loaded the profile.

The current source includes the five-stage workflow, Claude Code skills, portable tool instruction profiles, memory palace structure, Forge Context Packets, measured token reporting, external secrets handling, optional OpenCLI integration, release checks, CodeQL, fuzzing, GitHub governance, and governed-memory metadata checks.

Automated evidence:

- CI tests Python 3.10 through 3.14, lint, validation, and the CLI wheel in isolation.
- CodeQL and a bounded seeded fuzz workflow run on GitHub Actions.
- The local compatibility check confirms only that required profile files exist.
- Clean-session behaviour inside each external tool still needs current, recorded acceptance evidence.
- The Python wheel is an internal smoke-test artifact only; no PyPI distribution is published.

## Production Work Still Needed

- Build a conflict-aware installer for adopting ForgeLoop in existing repositories, including preview, backup, update, and rollback behaviour.
- Record clean-session acceptance results for Claude Code and Codex first, then each other tool before making stronger compatibility claims.
- Expand Windows and macOS CI coverage; current hosted CI runs on Ubuntu, although maintainers may test locally on other systems.
- Grow tests for CLI branches and optional OpenCLI integration beyond the current coverage floor.
- Add a second maintainer and require one independent review for protected-branch changes when available.
- Revisit Python distribution only after resolving the PyPI name and import-namespace collision and packaging the full product.
- Reassess governed-memory claims with external-store deletion evidence before making legal or certification claims.

## Contributions

Good first contributions are small, testable, and tied to a real workflow. Read `CONTRIBUTING.md`, `GOVERNANCE.md`, and `docs/compatibility/deployment-matrix.md` before proposing support claims.
