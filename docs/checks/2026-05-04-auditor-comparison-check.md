# Auditor Comparison Check

Date: 2026-05-04

## Scope

This check compares ForgeLoop against:

- Matt Pocock skills
- Every Compound Engineering plugin
- Obra Superpowers

The check focuses on production readiness, security posture, deployment maturity, token discipline, workflow quality, and long-term maintainability.

## Checks Run

```bash
python -m forgeloop status . --json
python -m forgeloop validate .
python -m forgeloop secrets check .
python -m forgeloop compat .
python -m forgeloop tokens "auditor security deployment superpowers comparison" . --tool codex
python -m unittest discover -s tests
```

## Results

- ForgeLoop validation passed.
- Unit tests passed: 24 tests.
- Compatibility report passed for all supported targets.
- External secrets file exists outside the repo.
- Token packet report for the audit query showed estimated 82.4 percent savings against selected source text.
- The repository is still a fresh git repo with uncommitted files.

## Findings

### P1: Deployment Is Not Yet Stronger Than Superpowers Or Every

ForgeLoop has broad compatibility files, but it does not yet have marketplace packaging, plugin manifests for all targets, install acceptance tests, versioned release flow, or real cross-tool plugin install verification.

This means ForgeLoop is not yet deployable at the same maturity level as the reviewed repositories.

Recommended action:

- Add deployment acceptance tests.
- Add managed install manifests before writing to user-level tool folders.
- Add versioned release checklist and plugin packaging plan.

### P1: Skill Behaviour Is Not Yet Tested

ForgeLoop validates file structure, but it does not prove that skills trigger correctly or change agent behaviour under pressure.

Recommended action:

- Add `docs/standards/skill-evaluation-standard.md`.
- Add natural prompt and explicit skill request tests.
- Add pressure scenarios for discipline skills.

### P1: Doctor Command Is Missing

Resolved on 2026-05-18. ForgeLoop now includes `python -m forgeloop doctor .`.

ForgeLoop has separate validation, compatibility, secrets, tokens, and index commands. A user-friendly production repo needs one `doctor` command that explains setup health in one place.

Recommended action:

- Implement `python -m forgeloop doctor .`.
- Include security, portability, tool profile, token, memory index, and CI readiness checks.

### P2: Worktree Lifecycle Is Not Yet Defined

ForgeLoop encourages safe changes, but it does not yet define isolated branch creation, ignored worktree folders, baseline tests, finishing options, or cleanup.

Recommended action:

- Add a `worktree` standard first.
- Keep CLI support dry-run until safety checks are complete.

### P2: Review Routing Needs A Real Router

ForgeLoop's four current reviewers are useful, but the system does not yet select reviewers dynamically based on changed files, security boundaries, data risks, performance surfaces, or API contracts.

Recommended action:

- Implement a review routing standard.
- Add structured finding schema.
- Add conditional reviewers gradually.

### P2: Contributor Gates Need To Be Stricter Before Public GitHub

The current contribution file is friendly. It should become stricter before public launch.

Recommended action:

- Require one problem per PR.
- Require evidence for behaviour-shaping skill changes.
- Require human review of AI-generated PRs.
- Require duplicate issue and PR search.

## What ForgeLoop Is Already Better At

- Beginner-safe mental model.
- Memory-first design.
- Token packet measurement.
- Explicit "no public savings claim without proof" posture.
- External secrets path outside the repo.
- Broad repo-local AI tool compatibility.

## What ForgeLoop Must Catch Up On

- Real plugin packaging.
- Skill evals.
- Worktree lifecycle.
- Dynamic review routing.
- Doctor command.
- Release process.

## Auditor Verdict

ForgeLoop has the better product thesis for memory and token discipline. It does not yet have the better production deployment system.

The next phase should be hardening, not feature expansion.
