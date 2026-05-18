# ForgeLoop V4.1 Deployment And Audit Hardening Plan

Date: 2026-05-04

## Goal

Turn ForgeLoop from a strong repo-local operating system into a production-ready open source package that can prove:

- it installs safely
- its skills trigger correctly
- its memory system saves tokens
- its checks catch real risks
- its workflows behave consistently across Claude Code and Codex first

## Scope

In scope:

- skill evaluation standard
- deployment acceptance tests
- doctor command
- worktree lifecycle standard
- verification-before-completion standard
- stricter contribution gates
- review routing standard

Out of scope for this phase:

- publishing to GitHub
- marketplace submission
- automatic writes into global tool folders
- broad session history ingestion
- public token-saving claims

## Implementation Units

### U1. Skill Evaluation Standard

Create:

- `docs/standards/skill-evaluation-standard.md`
- `templates/skill-eval-template.md`
- `examples/skill-evals/`

The standard should define:

- natural prompt trigger tests
- explicit skill request tests
- pressure scenarios
- before and after evidence
- transcript capture
- pass and fail criteria
- token report attached to each eval

This is inspired by Superpowers' "skills as tested behaviour" idea, but should be original to ForgeLoop.

### U2. Deployment Acceptance Matrix

Create:

- `docs/standards/deployment-acceptance-standard.md`
- `templates/deployment-acceptance-template.md`
- `docs/compatibility/deployment-matrix.md`

Each target tool needs:

- entry files present
- install path documented
- clean-session acceptance prompt
- expected first workflow response
- limitations
- last verified date

Claude Code and Codex should be mandatory first. Other tools can start as documented but unverified.

### U3. Doctor Command

Add:

- `forgeloop/doctor.py`
- `tests/test_doctor.py`
- `doctor` subcommand in `forgeloop/cli.py`

Checks:

- validation passes
- memory index exists and is current
- selected tool profile is present
- external secrets file is outside repo
- no real `.env` files are present
- compatibility report passes
- token exactness status is clear
- optional tokenizer dependency status is shown
- generated cache folders are ignored
- CI workflow exists and includes tests, validation, secrets, compatibility, tokens, and index checks

Output should be human-readable and JSON-capable.

### U4. Verification Before Completion

Create:

- `.claude/skills/verify-completion/SKILL.md`
- `docs/standards/verification-before-completion-standard.md`

Rules:

- no completion claim without fresh evidence
- state exact command run
- state result and limitation
- no "should pass" phrasing
- if validation cannot be run, say so plainly

### U5. Worktree Lifecycle Standard

Create:

- `.claude/skills/worktree-lifecycle/SKILL.md`
- `docs/standards/worktree-lifecycle-standard.md`
- `templates/worktree-handoff-template.md`

Rules:

- never start large implementation on default branch without explicit confirmation
- prefer `.worktrees/` only if ignored
- run baseline checks before work
- record finishing options: merge, PR, keep, discard
- require typed confirmation before discard

CLI support should start as dry-run only.

### U6. Review Routing Standard

Create:

- `docs/standards/review-routing-standard.md`
- `templates/review-finding-template.md`

Add future reviewers:

- correctness
- maintainability
- performance
- reliability
- API contract
- data
- adversarial

Keep security reviewer as mandatory whenever any trust boundary changes.

### U7. Contribution Gate Hardening

Update:

- `CONTRIBUTING.md`
- `SECURITY.md`
- `docs/GITHUB_PAGE.md`

Add:

- one problem per PR
- no speculative fixes without evidence
- skill changes require evaluation notes
- AI-generated PRs require human review
- new tool support requires clean-session acceptance transcript
- public claims require measured evidence

## Security Requirements

- No global tool writes until managed manifests exist.
- No cleanup of user files without ownership proof.
- No symlink-following writes.
- No shell command generated from untrusted input.
- No token provider API calls without explicit opt-in.
- No session-history scanning without opt-in.

## Success Criteria

- `python -m forgeloop doctor .` reports a clear health summary.
- Claude Code and Codex have documented clean-session acceptance tests.
- New skills have eval templates.
- Check stage has a stricter verification gate.
- Contributor docs block low-quality AI PRs before public launch.

## Strategic Verdict

V4 made ForgeLoop smarter.

V4.1 should make ForgeLoop harder to fool.

