# Roadmap And Current Status

## Current Status

ForgeLoop is a public GitHub source alpha. The repository is configured as a starter template, and the `v0.1.0` source release is published. Its `adopt` command safely adds allowlisted tool entry files to an existing project, but does not merge conflicts or install/manage the full CLI/runtime there. Existing-project adoption is deliberately a narrow optional integration; the source template remains the complete distribution. Profile-file presence does not prove that an external AI tool loaded the profile.

The current source includes the five-stage workflow, Claude Code skills, portable tool instruction profiles, memory palace structure, Forge Context Packets, measured token reporting, external secrets handling, optional OpenCLI integration, release checks, CodeQL, fuzzing, GitHub governance, and governed-memory metadata checks.

Automated evidence:

- Hosted CI tests Python 3.10 through 3.14 on Ubuntu, Windows, and macOS; lint, validation, and isolated CLI wheel smoke tests run on Ubuntu.
- CodeQL and a bounded seeded fuzz workflow run on GitHub Actions.
- `forgeloop compat` confirms profile files only. It does not launch external coding tools or prove they loaded instructions. The clean-session protocol is a manually executed, evidence-recorded behaviour check.
- Clean-session CLI acceptance passed for Codex on 2026-09-24; Claude Code's run was blocked by API authentication failure. Evidence and exact limits are in `docs/compatibility/deployment-evals/2026-05-18-clean-session-acceptance.md`.
- The Python wheel is an internal smoke-test artifact only; no PyPI distribution is published.

## Before Stable Promotion

- Keep `docs/release/stable-evidence.json` blocked until each linked evidence record is current, reviewed, complete, and has a valid expiry. The manifest prevents documentation wording changes from silently changing the stable-release decision; it is not proof on its own.
- Re-authenticate Claude Code interactively and repeat the clean-session CLI acceptance. Add desktop/UI acceptance only if a specific desktop integration is claimed.
- Add a second trusted maintainer. Until then, independent human review is unavailable; do not count AI review or self-approval as a substitute.
- Change branch protection to require at least one independent approval and code-owner review after a second maintainer is active. Current protection enforces nine CI contexts, but requires zero approvals and does not require code-owner review.
- Work through the four open Scorecard maturity alerts honestly: complete a human-reviewed OpenSSF Best Practices assessment before adding a badge; allow the repository to age and remain active for `Maintained`; earn `Code-Review` through real independent reviews; enable review requirements only when a second reviewer exists. Do not manufacture history or dismiss maturity signals as code vulnerabilities.
- Obtain provider-specific deletion evidence before enabling any external memory integration or making erasure/compliance claims. ForgeLoop currently ships no external-store deletion adapter.
- Focused CLI and OpenCLI failure-path coverage was expanded on 2026-11-07. Local branch coverage is 75% for `cli.py` and 87% for `opencli.py` (80% total); continue testing these surfaces as features change. The Claude clean-session acceptance remains an external authenticated-session task.
- CI dependency lock, Python 3.10 `tomli` pin, and paired CodeQL action update were merged in PR #61; no Dependabot PRs were open at the 2026-11-12 audit. Recheck the live queue before each maintenance run.
- Keep the current adopter profile-only unless full-runtime adoption is explicitly made a core promise. A future managed installer needs ownership manifests, update/rollback rules, and modified-file-preserving uninstall tests on all supported platforms.
- Revisit Python distribution only after resolving the PyPI name and import-namespace collision and packaging the full product.

The 2026-09-24 closure audit is in `docs/checks/2026-09-24-production-closure-audit.md`. ForgeLoop is **not a production/stable go**; keep public status at source alpha until the human-review and Claude acceptance gates are closed.

## To-Do List Of Additions

Repo-side implementation completed on 2026-11-12 where possible; external-tool acceptance and provider evidence remain explicit gates:

- Implemented local capture candidates with explicit propose, show, and approve steps; no transcript ingestion or automatic persistence. Review content for secrets and personal data before approval.
- Added a tiny deterministic retrieval regression set in unit tests; current ranker is unchanged. Expand the hand-reviewed set before any ranking modification.
- Added an optional read-only Beads bridge using `bd ready --json --brief`, with bounded results, timeout, and no installation, setup, claiming, or syncing. It relies on an existing local Beads installation; monitor upstream CLI changes and do not broaden it into a second task graph.
- A clean-session acceptance protocol and durable evidence template are documented, but actual behaviour still requires running each external tool. Codex CLI evidence exists; Claude remains blocked on authenticated access, and other tools have not passed live acceptance.

## Contributions

Good first contributions are small, testable, and tied to a real workflow. Read `CONTRIBUTING.md`, `GOVERNANCE.md`, and `docs/compatibility/deployment-matrix.md` before proposing support claims.
