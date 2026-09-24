# Roadmap And Current Status

## Current Status

ForgeLoop is a public GitHub source alpha. The repository is configured as a starter template, and the `v0.1.0` source release is published. Its `adopt` command safely adds allowlisted tool entry files to an existing project, but does not merge conflicts or install/manage the full CLI/runtime there. Existing-project adoption is deliberately a narrow optional integration; the source template remains the complete distribution. Profile-file presence does not prove that an external AI tool loaded the profile.

The current source includes the five-stage workflow, Claude Code skills, portable tool instruction profiles, memory palace structure, Forge Context Packets, measured token reporting, external secrets handling, optional OpenCLI integration, release checks, CodeQL, fuzzing, GitHub governance, and governed-memory metadata checks.

Automated evidence:

- Hosted CI tests Python 3.10 through 3.14 on Ubuntu, Windows, and macOS; lint, validation, and isolated CLI wheel smoke tests run on Ubuntu.
- CodeQL and a bounded seeded fuzz workflow run on GitHub Actions.
- The local compatibility check confirms only that required profile files exist.
- Clean-session CLI acceptance passed for Codex on 2026-09-24; Claude Code's run was blocked by API authentication failure. Evidence and exact limits are in `docs/compatibility/deployment-evals/2026-05-18-clean-session-acceptance.md`.
- The Python wheel is an internal smoke-test artifact only; no PyPI distribution is published.

## Before Stable Promotion

- Re-authenticate Claude Code interactively and repeat the clean-session CLI acceptance. Add desktop/UI acceptance only if a specific desktop integration is claimed.
- Add a second trusted maintainer. Until then, independent human review is unavailable; do not count AI review or self-approval as a substitute.
- Change branch protection to require at least one independent approval and code-owner review after a second maintainer is active. Current protection enforces nine CI contexts, but requires zero approvals and does not require code-owner review.
- Work through the four open Scorecard maturity alerts honestly: complete a human-reviewed OpenSSF Best Practices assessment before adding a badge; allow the repository to age and remain active for `Maintained`; earn `Code-Review` through real independent reviews; enable review requirements only when a second reviewer exists. Do not manufacture history or dismiss maturity signals as code vulnerabilities.
- Obtain provider-specific deletion evidence before enabling any external memory integration or making erasure/compliance claims. ForgeLoop currently ships no external-store deletion adapter.
- Grow tests for CLI branches and optional OpenCLI integration beyond the current coverage floor.
- Keep the current adopter profile-only unless full-runtime adoption is explicitly made a core promise. A future managed installer needs ownership manifests, update/rollback rules, and modified-file-preserving uninstall tests on all supported platforms.
- Revisit Python distribution only after resolving the PyPI name and import-namespace collision and packaging the full product.

The 2026-09-24 closure audit is in `docs/checks/2026-09-24-production-closure-audit.md`. ForgeLoop is **not a production/stable go**; keep public status at source alpha until the human-review and Claude acceptance gates are closed.

## Contributions

Good first contributions are small, testable, and tied to a real workflow. Read `CONTRIBUTING.md`, `GOVERNANCE.md`, and `docs/compatibility/deployment-matrix.md` before proposing support claims.
