# ForgeLoop

ForgeLoop is an open source operating system for AI-assisted engineering.

It helps vibe coders move quickly without losing clarity, review quality, project memory, or long-term learning. Instead of asking Claude Code to simply "build the thing", ForgeLoop gives each task a repeatable loop:

1. Discover
2. Frame
3. Build
4. Check
5. Capture

The goal is simple: every useful task should make the next task easier.

## Why ForgeLoop Exists

AI coding is fast, but speed can create a new kind of mess:

- unclear requirements
- forgotten decisions
- repeated mistakes
- weak review
- lost context between sessions
- code that works once but teaches nothing

ForgeLoop turns AI coding into a disciplined workflow. It gives Claude Code a product-like system of rules, skills, reviewers, templates, and memory folders so one person can work with the structure of a small engineering team.

## Who It Is For

ForgeLoop is built for:

- vibe coders who want more reliable AI output
- solo builders using Claude Code
- open source maintainers who want repeatable contribution workflows
- non-programmers who want a safer way to guide AI coding
- teams experimenting with agent-assisted development

You do not need to be an expert programmer to use the system. You do need to describe what you want, review the result, and let the workflow keep a clear trail.

## The Five Stages

### 1. Discover

Inspect the project before planning. Understand the task, current repo state, constraints, missing context, related memory, and likely risks.

Output goes in `docs/discoveries/`.

### 2. Frame

Turn the discovered context into a clear plan. Define scope, files, assumptions, validation, risks, and rollback.

Output goes in `docs/frames/`.

### 3. Build

Implement in small, reversible steps. Keep changes focused, run checks as you go, and record important progress.

Output notes go in `docs/builds/`.

### 4. Check

Review the result through multiple lenses: architecture, security, testing, and documentation. Findings are prioritised as P1, P2, or P3.

Output goes in `docs/checks/`.

### 5. Capture

Store the lesson, decision, reusable pattern, or fix so ForgeLoop compounds over time.

Output goes in `docs/captures/`, `docs/solutions/`, and the palace memory folders.

## Memory Palace Layer

ForgeLoop includes a local-first memory structure inspired by the idea of a memory palace, but implemented with original naming, rules, and files.

The memory model has five parts:

- Wings: broad domains such as product, engineering, design, or operations.
- Rooms: focused workstreams, sessions, topics, or projects inside a wing.
- Drawers: exact artefacts such as plans, decisions, fixes, reviews, and lessons.
- Entities: named things that can change over time, such as tools, modules, policies, or preferences.
- Timelines: records of what was true, when it became true, and when it changed.

This keeps memory useful without turning it into a flat pile of notes.

## Repository Map

```text
ForgeLoop/
+-- README.md
+-- CLAUDE.md
+-- AGENTS.md
+-- GEMINI.md
+-- LICENSE
+-- CONTRIBUTING.md
+-- .gitignore
+-- .claude/
|   +-- skills/
|   +-- agents/
|   +-- hooks/
|   +-- commands/
+-- .cursor/
+   +-- rules/
+-- .windsurf/
+   +-- rules/
+-- .clinerules/
+-- .roo/
+   +-- rules/
+-- .kiro/
+   +-- steering/
+-- .opencode/
+   +-- agents/
+-- integrations/
+   +-- opencli/
+-- docs/
|   +-- discoveries/
|   +-- frames/
|   +-- builds/
|   +-- checks/
|   +-- captures/
|   +-- solutions/
|   +-- standards/
|   +-- language/
|   +-- decisions/
|   +-- benchmarks/
|   +-- palace/
+-- memory/
+-- templates/
+-- examples/
```

## Quick Start

New here? Start with `docs/WHAT_IT_IS.md`, then `docs/GETTING_STARTED.md`, then `docs/HOW_TO_USE.md`.

1. Open this folder in Claude Code.
2. Run the setup menu:

```bash
python -m forgeloop setup .
```

3. Ask your AI coding tool to read its entry file:

- Claude Code: `CLAUDE.md`
- Codex: `AGENTS.md`
- Cursor: `.cursor/rules/forgeloop.mdc`
- GitHub Copilot: `.github/copilot-instructions.md`
- Gemini: `GEMINI.md`
- Windsurf: `.windsurf/rules/forgeloop.md`
- Cline: `.clinerules/forgeloop.md`
- Roo Code: `.roo/rules/forgeloop.md`
- JetBrains AI: `.aiassistant/rules/forgeloop.md`
- Kiro: `.kiro/steering/`
- OpenCode: `AGENTS.md` and `.opencode/agents/forge-review.md`
- Aider: `.aider.conf.yml` and `AGENTS.md`

4. Start with the Discover stage:

```text
/discover Add a simple export button to this app
```

5. Use the output to frame the task:

```text
/frame Use the latest discovery and create a build plan
```

6. Build only after the frame is clear:

```text
/build Implement the approved frame in small steps
```

7. Run the review stage:

```text
/check Review the changes using the ForgeLoop reviewers
```

8. Capture the learning:

```text
/capture Store the decision, reusable fix, and any changed facts
```

Claude Code skills become slash commands when they are placed under `.claude/skills/<skill-name>/SKILL.md`.

Before reading older memory, ask ForgeLoop for a compact pointer packet:

```bash
python -m forgeloop pack "memory token optimisation" . --limit 5
```

This prints a Forge Context Packet, or FCP. It is a small index of likely useful notes. Open only the listed files that are actually needed.

## What Is Included In The MVP

This first version includes:

- a complete project README
- a project-level `CLAUDE.md`
- five Claude Code skills
- four specialist reviewer agents
- reusable templates for every stage
- a local memory palace structure
- contribution and licence files
- example workflows for beginners
- hook and command guidance without unsafe defaults
- a small ForgeLoop CLI for validation, memory indexing, and status checks
- a compact context packet command for token-efficient memory lookup
- unit tests and a GitHub Actions workflow

It intentionally does not include a full MCP server, hosted dashboard, or automatic background capture yet. Those belong in later phases after the manual workflow proves useful.

## Production Checks

ForgeLoop includes a dependency-light Python CLI.

Run these from the repository root:

```bash
python -m forgeloop validate .
python -m forgeloop setup . --list
python -m forgeloop setup . --tool claude-code --dry-run
python -m forgeloop compat .
python -m forgeloop doctor .
python -m forgeloop tokens "memory validation" . --limit 5
python -m forgeloop intro
python -m forgeloop index .
python -m forgeloop pack "memory validation" . --limit 5
python -m forgeloop status .
python -m forgeloop opencli status .
python -m forgeloop opencli plan .
python -m forgeloop new frame "Add export button" .
python -m forgeloop hook-simulate PreCompact .
python -m forgeloop secrets init .
python -m forgeloop secrets check .
python -m unittest discover -s tests
```

Use `validate` before sharing changes. It checks required files, Claude skill metadata, reviewer agent metadata, JSON validity, possible secrets, risky hook patterns, large files, version consistency, and memory note structure.

Use `intro` to show the orange ASCII ForgeLoop banner. Use `python -m forgeloop intro --plain` when writing to logs or terminals that should not use colour.

Use `index` after adding capture notes, solution notes, entity notes, timeline notes, or palace drawer notes. It creates deterministic local memory indexes in `docs/palace/indexes/`.

Use `pack` before loading broad memory. It returns pointer-only FCP/1 output, so the AI can choose exact files instead of reading whole folders.

The packet now reports measured UTF-8 byte savings against selected source files and all indexed memory files. Treat token estimates as approximate until a tokenizer-backed benchmark is added.

Use `tokens` for tool-specific packet reports. Codex can use an exact local count when the optional `tiktoken` extra is installed. Other tool profiles clearly label counts as estimates unless a matching exact tokenizer is available.

Install the optional tokenizer support only when needed:

```bash
pip install -e ".[tokenizers]"
```

Use `compat` to check whether the expected Claude Code, Codex, Cursor, Copilot, Gemini, Windsurf, Cline, Roo, JetBrains AI, Kiro, OpenCode, Aider, and generic agent entry files exist.

Use `doctor` as the fuller release health check. It combines structure validation, compatibility, secrets state, memory-index freshness, CI readiness, optional tokenizer availability, and OpenCLI integration status.

Use `setup` to choose a local AI coding tool profile. It writes `.forgeloop.local.json`, which is ignored by Git. Use `--dry-run` to preview without writing.

Use `opencli plan` to preview the optional OpenCLI integration. OpenCLI is integrated as an external peer plugin, not copied into ForgeLoop. Install only when you explicitly choose:

```bash
python -m forgeloop opencli install . --execute
```

Use `new` to create stage notes safely from templates. It only supports known note kinds, generates safe file names, refuses path traversal, and does not overwrite unless `--force` is explicit.

## Advanced Skill Ladder

The beginner path remains the five-stage loop.

ForgeLoop also includes optional deeper skills:

- Align for fuzzy goals and shared terms.
- Probe for bug diagnosis.
- TDD for risky behaviour slices.
- Deepen for architecture boundaries.
- Simplify for release polish and token ballast.
- Refresh Memory for stale or conflicting notes.

These skills load only when useful.

Use `hook-simulate` to dry-run future capture hook behaviour without executing commands or reading transcript files.

Use `secrets init` to create a local secrets file outside the repository. The repo keeps only `.env.example` with blank values. Real `.env`-style files inside the repo fail validation.

In CI, use:

```bash
python -m forgeloop index . --check
```

That fails if the committed index is out of date.

## Design Decisions From MemPalace Review

ForgeLoop borrows the broad idea of structured, local-first memory, but it does not copy MemPalace code, prompts, branding, or unusual product terms.

Important choices:

- start with markdown memory and deterministic indexes before vector search
- keep hooks disabled by default until they are proven safe
- use Python standard library code for the first validation layer
- avoid unbounded file ingestion
- skip symlink-based memory shortcuts
- avoid benchmark claims until results are reproducible
- keep package, docs, and CI version checks aligned

## Secrets

ForgeLoop keeps secrets out of the repository.

Committed:

- `.env.example` with blank values
- docs explaining required keys

Not committed:

- `.env`
- `.env.local`
- `.envrc`
- `secrets.env`
- any `*.env` file with real values

Create your local external secrets file:

```bash
python -m forgeloop secrets init .
python -m forgeloop secrets path .
```

Check before publishing:

```bash
python -m forgeloop secrets check .
python -m forgeloop validate .
```

This follows the open-source safety test from Twelve-Factor config: the codebase should be publishable without exposing credentials.

## Working Principle

ForgeLoop should stay simple at the surface and deep underneath.

Users should experience a clear five-step workflow. The memory palace, reviewers, templates, and future automation should support that workflow, not compete with it.

## V3 Token Economy

ForgeLoop V3 uses the rule: compact by default, exact by reference.

The full lesson remains in normal markdown. Claude first receives a short FCP packet with file paths, tags, types, and headings. When more detail is needed, Claude opens the exact source file. This is how ForgeLoop aims for major token reduction without hiding information in an opaque AI-only language.

Read:

- `docs/HOW_TO_USE.md`
- `docs/WHAT_IT_IS.md`
- `docs/GETTING_STARTED.md`
- `docs/RELEASE_GUIDE.md`
- `docs/GITHUB_PAGE.md`
- `docs/standards/forgepack-language-reference.md`
- `docs/integrations/opencli.md`
- `docs/benchmarks/README.md`
- `docs/frames/2026-04-26-forgeloop-v3-token-memory-plan.md`

## Tool Compatibility

ForgeLoop is strongest in Claude Code, but now includes portable entry points for other AI coding tools:

- Claude Code: `CLAUDE.md`, `.claude/skills/`, `.claude/agents/`
- Codex: `AGENTS.md`
- Cursor: `.cursor/rules/forgeloop.mdc` and `AGENTS.md`
- GitHub Copilot: `.github/copilot-instructions.md` and `AGENTS.md`
- Gemini CLI: `GEMINI.md` and `AGENTS.md`
- Windsurf: `.windsurf/rules/forgeloop.md` and `AGENTS.md`
- Cline: `.clinerules/forgeloop.md`, `.clineignore`, and `AGENTS.md`
- Roo Code: `.roo/rules/forgeloop.md` and `AGENTS.md`
- JetBrains AI: `.aiassistant/rules/forgeloop.md` and `AGENTS.md`
- Kiro: `.kiro/steering/` and `AGENTS.md`
- OpenCode: `.opencode/agents/forge-review.md` and `AGENTS.md`
- Aider: `.aider.conf.yml` and `AGENTS.md`
- OpenCLI: `integrations/opencli/` as an optional peer plugin
- Generic agents: `AGENTS.md`, `README.md`, `docs/HOW_TO_USE.md`

Check readiness:

```bash
python -m forgeloop compat .
```

Choose a local profile:

```bash
python -m forgeloop setup .
```

## Claude Code References

ForgeLoop follows the current Claude Code structure for project skills, project subagents, hooks, and persistent project instructions:

- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code hooks: https://code.claude.com/docs/en/hooks
- Claude Code memory: https://code.claude.com/docs/en/memory
- OWASP secrets management: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- GitHub push protection: https://docs.github.com/en/code-security/how-tos/secure-your-secrets/work-with-leak-prevention
- Twelve-Factor config: https://www.12factor.net/config

## Licence

ForgeLoop is released under the MIT Licence. See `LICENSE`.
