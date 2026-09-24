---
type: check
date: 2026-09-24
status: current
valid_from: 2026-09-24
tags: [release, security, governance, compatibility, github]
---

# Production Closure Audit

This is a point-in-time evidence record, not a guarantee, certification, or production approval.

## Decision

**No-go for stable or production promotion.** Keep ForgeLoop labelled as a public source alpha. The source-template workflow is clearly scoped, but Claude Code acceptance and independent human review remain open. Do not claim external-store erasure support.

## Closed In This Pass

- Ran Codex CLI `0.155.0-alpha.9.2` in a fresh, ephemeral, read-only session. It read the requested project instructions and returned the five-stage workflow, the pointer-first `pack` command, and the OpenCLI safety rule. No files were written and no commands were run. This is CLI evidence only; it does not validate Codex desktop or every model.
- Tightened governance erasure logging. New `erase` events require an opaque evidence reference, and the audit log stores only its hash. The verifier still accepts existing `FGA/1` records and supports appending `FGA/2` records. Malformed action types now produce an invalid-log result rather than crashing verification.
- Confirmed the existing-project installer is intentionally profile-only. The canonical full distribution is the GitHub template. A managed full-runtime installer is not being added to this release because its update and uninstall semantics would create a broader file-ownership and conflict surface than the current product promises.
- Rechecked the live main branch protection and security-alert state on GitHub.
- Local Windows verification passed: 65 unit tests; 74% branch coverage against a 70% threshold; Ruff; repository validation; doctor; compatibility profile check; setup dry-run; OpenCLI plan; memory-index check; secrets check; governance audit and log verification; source/wheel build; Twine metadata check; isolated wheel smoke test. The build used a temporary output directory because existing `dist/` artifacts were present.

## Still Open

- Claude Code `2.1.92` initialised a fresh no-write print session, then returned repeated API `401 authentication_failed` responses. The run was stopped after six retries. Local auth status reported logged in, but this is not a passing acceptance. Re-authenticate interactively, then repeat the test.
- `sentientsky/ForgeLoop` currently has one admin collaborator. Branch protection strictly requires nine CI checks and enforces administrators, linear history, and conversation resolution, but requires zero approving reviews and no code-owner review. Do not count AI review as an independent maintainer. Add a trusted second human before raising the approval requirement, otherwise the protected branch would be unmergeable.
- GitHub reports four open Scorecard maturity alerts: `CII-Best-Practices` score 0 (no badge effort detected), `Maintained` score 0 (repository is younger than 90 days), `Code-Review` score 0 (0/16 approved changesets), and `Branch-Protection` score 3 (no required approver or code-owner review). These are maturity findings, not source-code vulnerability alerts. A real badge assessment, passage of time with activity, independent review history, and a second maintainer are required; do not manufacture these signals.
- Dependabot security alerts and secret-scanning alerts were both zero at the time checked. Provider secret scanning and push protection are enabled. GitHub's generic non-provider pattern scanning is not available for this user-owned repository under the documented eligibility rules, which currently limit it to organisation-owned repositories on GitHub Team with Secret Protection.
- ForgeLoop has no external-store connector or provider deletion adapter. `--evidence-ref` is an operator-supplied pointer, not evidence verification. No provider-specific deletion claim is supported until real provider evidence and end-to-end tests exist.

## Release Scope

Existing-project `adopt` remains optional and additive: preview by default, create only missing profile files, preserve conflicts. Full runtime install/update/uninstall is explicitly not promised. If that becomes a core use case, design and test a managed asset manifest, user-edit conflict policy, rollback, and modified-file-preserving uninstall on Windows, macOS, and Linux before advertising it.

The current GitHub release remains `v0.1.0` source alpha. This audit does not create or promote a release.

## Repeat Actions

1. Re-authenticate Claude Code with the account owner present and repeat the clean-session check in `docs/compatibility/deployment-evals/2026-05-18-clean-session-acceptance.md`.
2. Invite a trusted second maintainer with the least privileges needed for review, add the person to `.github/CODEOWNERS`, then require one independent approval and code-owner review in branch protection.
3. Complete the OpenSSF Best Practices assessment only after a maintainer verifies each answer and its evidence.
4. Add a provider adapter only with a specific provider, documented deletion scope, retention/backup behavior, and repeatable integration tests.

## External References

- [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)
- [OpenSSF Best Practices criteria](https://www.bestpractices.dev/en/criteria?details=true&rationale=true)
- [GitHub generic secret-pattern eligibility](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/detect-secret-leaks/enabling-secret-scanning-for-generic-patterns)
