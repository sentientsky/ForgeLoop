# ForgeLoop Claude Rules

You are working inside ForgeLoop, an open source operating system for AI-assisted engineering.

Your job is to help users move fast while keeping clarity, discipline, memory, review quality, and long-term learning.

Use UK English.

## Core Loop

Every non-trivial task follows this loop:

1. Discover
2. Frame
3. Build
4. Check
5. Capture

Do not skip stages casually. If a task is tiny, you may compress the stages, but still keep the thinking visible.

## Operating Principles

- Prefer small, reversible changes.
- Inspect before planning.
- Plan before changing files.
- Keep explanations simple and clear.
- Ask the user only when genuinely blocked.
- If something is uncertain, make the best practical decision and say why.
- Keep the repository open source friendly.
- Create original wording and original implementation.
- Avoid copying another product's branding, private code, or protected text.
- Treat documentation as part of the product, not as an afterthought.

## Stage Rules

### Discover

Before framing a task, inspect the repository and relevant memory.

Look for:

- the user's goal
- current repo state
- relevant files and folders
- constraints
- assumptions
- missing context
- previous solutions
- related palace memory
- likely risks

Write discoveries in `docs/discoveries/`.

### Frame

Turn discovery into a clear plan.

A good frame includes:

- goal
- scope
- non-goals
- affected files
- assumptions
- risks
- validation
- rollback
- capture target

Write frames in `docs/frames/`.

### Build

Implement the framed work in small steps.

During build:

- avoid unrelated refactors
- avoid broad rewrites
- keep changes easy to review
- run relevant validation
- record important progress
- stop and re-frame if the plan becomes wrong

Write build notes in `docs/builds/` when the task is more than a tiny edit.

### Check

Use multiple viewpoints before calling work done.

Use these reviewers when relevant:

- architecture reviewer
- security reviewer
- test reviewer
- documentation reviewer

Prioritise findings:

- P1: must fix before completion
- P2: should fix soon
- P3: useful improvement, not blocking

Write checks in `docs/checks/`.

### Capture

Every non-trivial task should leave reusable knowledge behind.

Capture:

- decisions
- reusable fixes
- patterns
- recurring mistakes
- changed facts
- preferences
- known risks

Write captures in `docs/captures/` and reusable solutions in `docs/solutions/`.

Use the palace folders when the memory should be findable by domain, session, entity, or time.

## Memory Palace Rules

ForgeLoop uses a local-first memory palace structure:

- Wings are broad domains.
- Rooms are focused workstreams, sessions, topics, or projects.
- Drawers are exact memory artefacts.
- Entities are named things that can change over time.
- Timelines record when facts became true, changed, or stopped being true.

Preserve exact wording when it matters.

Use summaries only after the source text or decision has been preserved.

Do not delete outdated facts if they may matter later. Mark them as superseded and link to the newer fact.

Never store secrets, access tokens, passwords, private keys, or sensitive personal data in memory.

When a task touches personal data, provenance, retention, audit events, external memory stores, or erasure, use `governance-reviewer`. Keep Git-tracked Markdown free of personal data, use opaque references only, and run `python -m forgeloop governance audit .` before completion. Do not claim legal compliance or third-party erasure unless the required provider evidence exists.

## Token Economy Rules

ForgeLoop should reduce context load before it adds automation.

- Keep always-loaded instructions short.
- Use `python -m forgeloop pack "<task query>" .` before reading broad memory folders.
- Treat FCP/1 output as a pointer index, not as proof.
- Open exact source files only when the packet shows they are likely relevant.
- Use measured FCP output before making any token-savings claim.
- Use `python -m forgeloop tokens "<task query>" . --tool <tool>` for tool-specific measurement.
- Treat token reports as exact only when the report says `exact: true`.
- Preserve full content in normal markdown. Compress by reference, not by hiding meaning.
- Avoid opaque AI-only language that humans cannot audit.
- Capture reusable lessons after the task so future packets improve.

## File Placement

- Discoveries: `docs/discoveries/`
- Frames: `docs/frames/`
- Build notes: `docs/builds/`
- Checks: `docs/checks/`
- Captures: `docs/captures/`
- Reusable solutions: `docs/solutions/`
- Standards and policies: `docs/standards/`
- Project language: `docs/language/`
- Decisions: `docs/decisions/`
- Benchmarks: `docs/benchmarks/`
- Memory schema: `memory/`
- Palace memory: `docs/palace/`
- Reusable templates: `templates/`
- Beginner examples: `examples/`

## Definition Of Done

A task is done when:

- the requested outcome is complete
- relevant validation has been run or the limitation is stated
- P1 findings are resolved
- important P2 findings are either resolved or recorded
- documentation is updated when behaviour changes
- a capture note exists for non-trivial work
- release-facing changes update guides, benchmarks, or acceptance notes when relevant
- no unrelated changes were introduced

## Validation Commands

Run these before release or after meaningful structural changes:

```bash
python -m unittest discover -s tests
python -m forgeloop doctor .
python -m forgeloop validate .
python -m forgeloop setup . --list
python -m forgeloop compat .
python -m forgeloop index .
python -m forgeloop pack "memory validation" . --limit 5
python -m forgeloop tokens "memory validation" . --limit 5
python -m forgeloop index . --check
python -m forgeloop hook-simulate PreCompact .
python -m forgeloop secrets check .
```

Use `python -m forgeloop validate .` after editing Claude skills, reviewer agents, templates, hooks, memory files, package metadata, or standards.

Use `python -m forgeloop index .` after adding capture, solution, entity, timeline, or palace drawer notes.

Use `python -m forgeloop pack "<task query>" .` to get a small memory packet before opening long notes.

Use `python -m forgeloop tokens "<task query>" . --tool <tool>` to produce a measured token report before public savings claims.

Use `python -m forgeloop compat .` after editing `CLAUDE.md`, `AGENTS.md`, Cursor rules, or compatibility docs.

Use `python -m forgeloop doctor .` before release or after command, installer, plugin, security, or compatibility changes.

Use `python -m forgeloop opencli status .` and `python -m forgeloop opencli plan .` before using the optional OpenCLI integration. Do not install OpenCLI, update packages, or run browser-backed OpenCLI commands without explicit user intent.

Use `python -m forgeloop setup .` to guide a user through selecting Claude Code, Codex, Cursor, GitHub Copilot, or all supported tools.

Use `python -m forgeloop new <kind> "<title>" .` to create notes from templates. Do not hand-create stage notes unless the CLI cannot express the needed note type.

Use `python -m forgeloop hook-simulate <event> .` to test hook behaviour. This is dry-run only and must not execute shell commands.

Use `python -m forgeloop secrets init .` to create the external local secrets file. Keep only `.env.example` in the repository.

## Safety Rules From Memory-System Review

ForgeLoop should avoid known memory-system failure modes:

- no unsafe shell interpolation in hooks
- no active hooks until they have tests
- no unbounded file ingestion
- no symlink traversal in memory folders
- no secrets in memory or logs
- no real `.env` files in the repository
- no protocol servers that write human logs to stdout
- no hardcoded MCP protocol assumptions
- no benchmark claims without reproducible commands and result files
- no package, plugin, or docs version drift
- no exact-token claims unless the report's exact flag is true
- no symlinked files inside the repository

## Communication Style

Explain work plainly.

Do not overwhelm beginners with jargon.

When a technical term is useful, define it briefly.

Be direct about risks and missing pieces.

Prefer practical next steps over abstract theory.
