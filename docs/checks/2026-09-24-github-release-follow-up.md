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
- Published commits: `0fb3fbc` (governance-first memory controls), `26e1349` (Scorecard permission scope)
- GitHub code scanning reported zero alerts across all states during this review; scheduled CodeQL runs passed.

## Scorecard Failure

The scheduled Scorecard job was rejected by the Scorecard publishing service because `security-events: write` and `id-token: write` were granted at workflow scope. Scorecard requires its publish permissions to be scoped to the analysis job.

The workflow now keeps global `contents: read` and grants the three needed permissions only to the analysis job. ForgeLoop validation has a regression check for this scope boundary.

The next run showed that the action was pinned to the annotated tag object rather than the commit behind it. GitHub's API and the upstream Git ref confirm `4eaacf0543bb3f2c246792bd56e8cdeffafb205a` as the peeled commit for `v2.4.3`; the workflow now pins that commit. Scorecard then identified the same tag-object issue for `github/codeql-action/upload-sarif`. The `v4.36.2` tag resolves to `8aad20d150bbac5944a9f9d289da16a4b0d87c1e`, which is now used consistently in the CodeQL and Scorecard workflows.

## CI Lint Update

CI installed Ruff 0.16.8 from the open-ended development dependency. The local machine previously had Ruff 0.15.18, which did not report the newer rules. The current source now passes Ruff 0.16.8, including stricter imports, timezone-aware dates, and narrower exception handling for optional tokenisation.

Local validation passed after these fixes: 47 unit tests, 73 percent branch coverage, Ruff 0.16.8, repository validation, doctor, compatibility, governance audit and log verification, secrets checks, package build, Twine checks, and installed-wheel smoke test.

## Evidence Still Needed

The corrected workflow needs one green push run to close this review. Scorecard's low scores for branch protection, project age, reviewed changes, and fuzzing describe repository maturity and settings, not a source-code vulnerability. Do not attempt to inflate these scores with artificial PR history.

## Source

- OpenSSF Scorecard Action workflow restrictions: https://github.com/ossf/scorecard-action#workflow-restrictions
- Official example scopes publishing permissions to the analysis job: https://github.com/ossf/scorecard-action/blob/main/.github/workflows/scorecards.yml
