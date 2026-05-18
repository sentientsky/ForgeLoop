# ForgeLoop

ForgeLoop is an open source operating system for AI-assisted engineering.

It helps Claude Code users move fast without losing clarity, discipline, memory, review quality, or long-term learning.

## What It Does

ForgeLoop turns AI coding into a repeatable loop:

1. Discover the repo and the task.
2. Frame the work before editing.
3. Build in small, reversible steps.
4. Check with specialist review viewpoints.
5. Capture the lesson so the next task is easier.

## Why It Helps

AI coding often fails because the assistant forgets decisions, loads too much context, skips review, or repeats mistakes.

ForgeLoop gives the assistant:

- clear project rules
- reusable Claude Code skills
- specialist reviewer agents
- templates for every stage
- local-first project memory
- secure secrets handling
- validation commands
- release health checks
- compact context packets for token-efficient recall
- optional OpenCLI integrated peer plugin
- portable entry points for Claude Code, Codex, Cursor, Copilot, Gemini, Windsurf, Cline, Roo Code, JetBrains AI, Kiro, OpenCode, Aider, and generic agents
- release guides, FAQ, benchmark notes, and deployment acceptance prompts

## Token-Efficient Memory

ForgeLoop V3 introduces Forge Context Packets.

Run:

```bash
python -m forgeloop pack "memory token optimisation" . --limit 5
python -m forgeloop tokens "memory token optimisation" . --limit 5
```

Claude receives a tiny pointer packet instead of a pile of memory files.

The full knowledge stays in markdown. The packet points to the exact files to open when detail is needed.

The packet reports measured byte savings, and the token command reports tool-specific estimates or exact counts when a matching local tokenizer is available.

This keeps ForgeLoop auditable, portable, and open source friendly.

## Quick Start

```bash
python -m forgeloop setup .
python -m forgeloop doctor .
python -m forgeloop validate .
python -m forgeloop compat .
python -m forgeloop tokens "memory validation" . --limit 5
python -m unittest discover -s tests
python -m forgeloop intro
```

Read:

- `docs/WHAT_IT_IS.md`
- `docs/GETTING_STARTED.md`
- `docs/HOW_TO_USE.md`
- `docs/RELEASE_GUIDE.md`

Then use the five-stage workflow inside Claude Code:

```text
/discover Describe the task
/frame Turn the discovery into a plan
/build Implement the plan
/check Review the result
/capture Store the lesson
```

## Repository Includes

- `README.md`
- `CLAUDE.md`
- `AGENTS.md`
- `GEMINI.md`
- `.claude/skills/`
- `.claude/agents/`
- `.claude/hooks/`
- `.cursor/rules/`
- `.github/copilot-instructions.md`
- `.windsurf/rules/`
- `.clinerules/`
- `.roo/rules/`
- `.aiassistant/rules/`
- `.kiro/steering/`
- `.opencode/agents/`
- `.aider.conf.yml`
- `docs/`
- `docs/language/`
- `docs/decisions/`
- `docs/benchmarks/`
- `memory/`
- `templates/`
- `examples/`
- `forgeloop/` Python CLI
- `integrations/opencli/` optional OpenCLI peer plugin
- `tests/`

## Security First

ForgeLoop keeps secrets outside the repo.

```bash
python -m forgeloop secrets init .
python -m forgeloop secrets check .
```

Hooks are not active by default. They should be simulated, reviewed, and tested before use.

OpenCLI is optional and integrated, not copied. The install path is explicit:

```bash
python -m forgeloop opencli plan .
python -m forgeloop opencli install . --execute
```

Browser-backed OpenCLI commands reuse logged-in browser sessions, so ForgeLoop treats them as privileged actions.

## Open Source Positioning

ForgeLoop is original, markdown-first, dependency-light, and MIT licensed.

It borrows broad ideas from the wider memory-tool ecosystem, such as progressive disclosure and markdown source-of-truth, but uses original wording, structure, and implementation.

## Roadmap

- optional local full-text search
- safe opt-in context hooks
- larger public benchmark set
- optional cross-tool memory connectors
- OpenCLI command hardening and clean-session evals
- native profiles for Amazon Q, Zed, Replit, Qwen Code, Factory Droid, and Pi
