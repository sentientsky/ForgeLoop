---
type: check
date: 2026-09-24
status: current
tags: [github, codeql, scorecard, release, security]
---

# GitHub Release Follow-Up

## Remote State

- Public repository: `sentientsky/ForgeLoop`
- Default branch: `main`
- Published commit: `0fb3fbc` (governance-first memory controls)
- GitHub code scanning reported zero alerts across all states during this review; scheduled CodeQL runs passed.

## Scorecard Failure

The scheduled Scorecard job was rejected by the Scorecard publishing service because `security-events: write` and `id-token: write` were granted at workflow scope. Scorecard requires its publish permissions to be scoped to the analysis job.

The workflow now keeps global `contents: read` and grants the three needed permissions only to the analysis job. ForgeLoop validation has a regression check for this scope boundary.

Local validation passed: 47 unit tests, 73 percent branch coverage, Ruff, repository validation, doctor, compatibility, governance audit and log verification, secrets checks, package build, Twine checks, and installed-wheel smoke test.

## Evidence Still Needed

After this fix is pushed, confirm the Scorecard run succeeds. Its low scores for branch protection, project age, reviewed changes, and fuzzing describe repository maturity and settings, not a source-code vulnerability. Do not attempt to inflate these scores with artificial PR history.

## Source

- OpenSSF Scorecard Action workflow restrictions: https://github.com/ossf/scorecard-action#workflow-restrictions
- Official example scopes publishing permissions to the analysis job: https://github.com/ossf/scorecard-action/blob/main/.github/workflows/scorecards.yml
