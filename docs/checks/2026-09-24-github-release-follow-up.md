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
- Audited commit at the start: `00c8768`
- CI, CodeQL, and Scorecard all passed on `00c8768`; earlier failed runs were corrected and remain visible in workflow history.
- The current open Scorecard findings included branch protection, un-hash-pinned CI installs, and no detected fuzzer. These are repository posture findings, not CodeQL source alerts.

## Scorecard Failure

The scheduled Scorecard job was rejected by the Scorecard publishing service because `security-events: write` and `id-token: write` were granted at workflow scope. Scorecard requires its publish permissions to be scoped to the analysis job.

The workflow now keeps global `contents: read` and grants the three needed permissions only to the analysis job. ForgeLoop validation has a regression check for this scope boundary.

The next run showed that the action was pinned to the annotated tag object rather than the commit behind it. GitHub's API and the upstream Git ref confirm `4eaacf0543bb3f2c246792bd56e8cdeffafb205a` as the peeled commit for `v2.4.3`; the workflow now pins that commit. Scorecard then identified the same tag-object issue for `github/codeql-action/upload-sarif`. The `v4.36.2` tag resolves to `8aad20d150bbac5944a9f9d289da16a4b0d87c1e`, which is now used consistently in the CodeQL and Scorecard workflows.

## CI Lint Update

CI installed Ruff 0.16.8 from the open-ended development dependency. The local machine previously had Ruff 0.15.18, which did not report the newer rules. The current source now passes Ruff 0.16.8, including stricter imports, timezone-aware dates, and narrower exception handling for optional tokenisation.

Local validation passed after these fixes: 47 unit tests, 73 percent branch coverage, Ruff 0.16.8, repository validation, doctor, compatibility, governance audit and log verification, secrets checks, package build, Twine checks, and installed-wheel smoke test.

## Evidence Still Needed

The follow-up implementation now hash-locks CI and release tooling, runs bounded Atheris fuzzing, enables Dependabot alerts/security updates and private vulnerability reporting, and protects `main` with required PR checks. Scorecard's project-age, review-history, OpenSSF badge, and language-detection signals cannot be honestly cleared by changing source code or creating artificial history. Python fuzzing is real and tested here, but Scorecard's detector does not currently recognise this Python integration.

## Source

- OpenSSF Scorecard Action workflow restrictions: https://github.com/ossf/scorecard-action#workflow-restrictions
- Official example scopes publishing permissions to the analysis job: https://github.com/ossf/scorecard-action/blob/main/.github/workflows/scorecards.yml
