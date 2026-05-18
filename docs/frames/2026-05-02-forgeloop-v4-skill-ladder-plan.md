# ForgeLoop V4 Skill Ladder Plan

Date: 2026-05-02

## Goal

Make ForgeLoop feel effortless while becoming much stronger at thinking, review, memory, and token control.

The core loop remains:

1. Discover
2. Frame
3. Build
4. Check
5. Capture

V4 adds a skill ladder around that loop. The ladder gives the agent extra discipline only when the task needs it.

## Product Principle

ForgeLoop should not become a giant prompt that loads everything every time. It should be a small operating system:

- Load the smallest useful instruction first.
- Read the repo before guessing.
- Use precise shared language.
- Build feedback loops before fixing.
- Review with the right specialists.
- Capture only durable lessons.
- Refresh old lessons when reality changes.

## V4 Shape

### Core Skills

Keep these as the default path:

- `discover`: inspect repo, task, constraints, and memory.
- `frame`: plan scope, files, risk, validation, and capture target.
- `build`: implement in small reversible steps.
- `check`: test and review the result.
- `capture`: save the reusable lesson.
- `pack-context`: load compact memory packets before full notes.

### Advanced Skills

Add these as optional support skills:

- `align`: question fuzzy goals, sharpen terms, and update project language.
- `probe`: diagnose bugs by building a repeatable signal before guessing.
- `tdd`: build one tested behaviour slice at a time.
- `deepen`: find places where complexity should move behind a clearer interface.
- `simplify`: review recent changes for reuse, clarity, dead code, and efficiency.
- `refresh-memory`: review old captures and solutions for stale or duplicate guidance.

### Shared Documents

Add these lightweight anchors:

- `docs/language/PROJECT_LANGUAGE.md`
- `docs/decisions/`
- `templates/project-language-template.md`
- `templates/decision-template.md`
- `templates/review-finding-template.md`

These should stay short. They are there to save tokens and prevent repeated confusion.

## Implementation Units

### U1. Project language

Goal: give agents and humans the same terms for the project.

Files to add:

- `docs/language/README.md`
- `docs/language/PROJECT_LANGUAGE.md`
- `templates/project-language-template.md`
- `.claude/skills/align/SKILL.md`

Rules:

- Human-readable only.
- No hidden AI-only language.
- One sentence per term.
- Include aliases to avoid when useful.
- Record ambiguities and resolutions.

Validation:

- Run `python -m forgeloop validate .`
- Run `python -m forgeloop tokens "project language" . --tool all-supported`

### U2. Tiny decisions

Goal: record only decisions that a future maintainer would otherwise misunderstand.

Files to add:

- `docs/decisions/README.md`
- `templates/decision-template.md`
- `.claude/skills/align/references/decision-rules.md`

Rules:

- Record only hard-to-reverse, surprising, real trade-off decisions.
- Keep most decisions to one short paragraph.
- Use sequential names such as `0001-keep-local-secrets-outside-repo.md`.

Validation:

- Confirm decision templates do not encourage paperwork.
- Confirm no secret-bearing examples are present.

### U3. Probe skill

Goal: improve bug fixing by making the first deliverable a reliable signal.

Files to add:

- `.claude/skills/probe/SKILL.md`
- `templates/probe-template.md`
- `docs/standards/debugging-feedback-loop-standard.md`

Rules:

- Reproduce first.
- Build or find a deterministic signal.
- Generate three to five ranked hypotheses.
- Test one hypothesis at a time.
- Remove debug instrumentation before completion.
- Capture prevention after the fix.

Validation:

- Add a sample probe note in `examples/`.
- Run normal ForgeLoop tests.

### U4. TDD tracer bullet skill

Goal: add test-first behaviour without turning every task into a ceremony.

Files to add:

- `.claude/skills/tdd/SKILL.md`
- `.claude/skills/tdd/references/test-quality.md`
- `templates/tdd-cycle-template.md`

Rules:

- One behaviour slice at a time.
- Test through public interfaces where possible.
- Avoid testing private implementation details.
- Refactor only after green checks.

Validation:

- Add examples for tiny, medium, and bug-fix tasks.

### U5. Architecture deepening skill

Goal: improve code quality by finding shallow modules and weak interfaces.

Files to add:

- `.claude/skills/deepen/SKILL.md`
- `.claude/skills/deepen/references/architecture-language.md`
- `.claude/skills/deepen/references/interface-options.md`
- `.claude/agents/maintainability-reviewer.md`

Rules:

- Use clear ForgeLoop architecture terms.
- Present candidates before proposing changes.
- Use a deletion test.
- Treat the interface as the test surface.
- Avoid adding abstraction unless it reduces real complexity.

Validation:

- Add one example architecture review note.
- Confirm the skill does not tell agents to refactor without user context.

### U6. Dynamic review routing

Goal: make Check stronger without running every reviewer every time.

Files to add:

- `docs/standards/review-routing-standard.md`
- `templates/review-finding-template.md`
- New reviewers as needed:
  - `correctness-reviewer`
  - `maintainability-reviewer`
  - `performance-reviewer`
  - `api-contract-reviewer`
  - `reliability-reviewer`
  - `data-reviewer`
  - `adversarial-reviewer`

Rules:

- Always use correctness, testing, maintainability, and project standards for non-trivial code changes.
- Add security reviewer for trust boundaries, secrets, auth, user input, external services, and file writes.
- Add performance reviewer for hot paths, caching, query patterns, and repeated work.
- Add data reviewer for migrations, persistence, schema, and destructive changes.
- Add adversarial reviewer for large, security-sensitive, or high-impact changes.

Validation:

- Add tests for reviewer routing once implemented in CLI.
- Keep review output structured and deduplicated.

### U7. Doctor command

Goal: make setup, portability, and safety visible in one command.

Files to modify:

- `forgeloop/cli.py`
- `forgeloop/setup.py`
- Add `forgeloop/doctor.py`
- Add tests in `tests/`

Checks:

- Git repo present.
- Required files present.
- Tool profile selected.
- Local setup file is gitignored.
- External secrets path is outside the repo.
- Repo `.env` files are absent.
- Python version is supported.
- Token counting optional dependency status is clear.
- Symlink writes are refused.
- Memory index is current.
- No generated cache folders are committed.

Validation:

- `python -m unittest discover -s tests`
- `python -m forgeloop doctor .`
- `python -m forgeloop validate .`

### U8. Memory refresh

Goal: keep captures and solutions useful as the repo evolves.

Files to add:

- `.claude/skills/refresh-memory/SKILL.md`
- `templates/memory-refresh-template.md`
- `docs/standards/memory-refresh-standard.md`

Rules:

- Classify old notes as keep, update, consolidate, supersede, stale, or delete candidate.
- Never delete automatically in MVP.
- Prefer marking stale or superseded to rewriting history.
- Update indexes after refresh.

Validation:

- Add a dry-run mode before any write mode.
- Run `python -m forgeloop index . --check`.

## Security Requirements

- Keep secrets outside the repo by default.
- Refuse symlinked writes for config and generated local state.
- Do not run destructive cleanup without an ownership manifest.
- No automatic deletion outside the repository.
- No provider API calls for token counting unless the user explicitly opts in later.
- Session history must be opt-in and local-only.
- Review all file write paths for path traversal.

## Token Requirements

- Every skill should be concise.
- Detailed rules should live in references loaded only when needed.
- `pack-context` remains the default memory access path.
- Public token-saving claims require exact command output, exact profile, date, and whether the count was exact or estimated.
- Do not claim 80 or 90 percent savings as a product claim until measured across a public benchmark set.

## Compatibility Requirements

- Claude Code remains the richest native target.
- Codex remains the strongest portable target through `AGENTS.md` and CLI workflows.
- Cursor, Copilot, Gemini, Windsurf, Cline/Roo, JetBrains AI, Kiro, OpenCode, and Aider should keep thin native entry files that point back to shared ForgeLoop docs.
- Future installer work should use managed manifests before writing to user-level tool folders.

## Suggested Order

1. Add project language, tiny decisions, and Align.
2. Add Probe and TDD.
3. Add Deepen and Simplify.
4. Add review routing and more reviewers.
5. Add Doctor.
6. Add memory refresh.
7. Add optional session history.
8. Add measured token benchmark examples.

## Success Criteria

- A new user can install ForgeLoop, pick their coding tool, and understand the next action in under five minutes.
- A non-trivial task produces a compact trail: language updates, decisions if needed, plan, checks, and capture.
- Check uses only relevant reviewers.
- Token reporting proves packet savings without hype.
- Security checks fail closed when local state or secrets are unsafe.

