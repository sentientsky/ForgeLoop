---
type: compatibility
status: current
tags: [compatibility, claude-code, codex, cursor, gemini, windsurf]
---

# AI Coding Tool Compatibility

ForgeLoop should work across AI coding tools without turning the repository into a pile of duplicated prompts.

The compatibility rule is:

```text
one workflow, tool-native entry points
```

## Supported Entry Points

| Tool | Entry point | Status | Notes |
| --- | --- | --- | --- |
| Claude Code | `CLAUDE.md`, `.claude/skills/`, `.claude/agents/` | Primary | Best supported path. Skills, reviewers, and hook simulation are designed for Claude Code first. |
| Codex | `AGENTS.md` | Primary | Gives Codex the loop, validation commands, safety rules, and FCP memory workflow. |
| Cursor | `.cursor/rules/forgeloop.mdc`, `AGENTS.md` | Supported | Cursor gets an always-on project rule plus the shared agent instructions. |
| GitHub Copilot | `.github/copilot-instructions.md`, `AGENTS.md` | Supported | Copilot gets repository custom instructions plus the shared agent file. |
| Gemini CLI / Gemini Code Assist | `GEMINI.md`, `AGENTS.md` | Supported | Gemini gets a native memory entry file plus the shared agent file. |
| Windsurf | `.windsurf/rules/forgeloop.md`, `AGENTS.md` | Supported | Windsurf gets a concise workspace rule and can also read `AGENTS.md`. |
| Cline | `.clinerules/forgeloop.md`, `.clineignore`, `AGENTS.md` | Supported | Cline gets project rules and a context ignore file. |
| Roo Code | `.roo/rules/forgeloop.md`, `AGENTS.md` | Supported | Roo gets workspace rules that map to the ForgeLoop loop. |
| JetBrains AI | `.aiassistant/rules/forgeloop.md`, `AGENTS.md` | Beta | JetBrains AI gets project rules, but IDE attachment behaviour should still be checked by the user. |
| Kiro | `.kiro/steering/product.md`, `.kiro/steering/tech.md`, `.kiro/steering/structure.md`, `AGENTS.md` | Beta | Kiro gets steering files aligned with the ForgeLoop product, tech, and structure. |
| OpenCode | `.opencode/agents/forge-review.md`, `AGENTS.md` | Supported | OpenCode gets a read-only review subagent and the shared instruction file. |
| Aider | `.aider.conf.yml`, `AGENTS.md` | Portable | Aider is configured to read `AGENTS.md`. |
| Generic coding agents | `AGENTS.md`, `README.md`, `docs/HOW_TO_USE.md` | Portable | Agents that do not understand Claude skills can still follow the core workflow. |

## Setup Menu

Run:

```bash
python -m forgeloop setup .
```

Preview without writing:

```bash
python -m forgeloop setup . --tool claude-code --dry-run
```

The setup menu writes `.forgeloop.local.json`, which is ignored by Git.

## Compatibility Check

Run:

```bash
python -m forgeloop compat .
```

Machine-readable form:

```bash
python -m forgeloop compat . --json
```

This checks whether the expected tool entry files are present.

## Claude Code

Claude Code remains the richest integration.

Use:

- `CLAUDE.md` for compact project rules
- `.claude/skills/` for on-demand workflows
- `.claude/agents/` for reviewer roles
- `.claude/hooks/` for future opt-in automation

Keep `CLAUDE.md` short. Move specialised guidance into skills and memory files.

## Codex

Codex should read `AGENTS.md` before work starts.

ForgeLoop uses `AGENTS.md` to provide:

- workflow rules
- token economy rules
- validation commands
- safety requirements
- definition of done

Codex should use `python -m forgeloop pack "<query>" . --limit 5` before reading broad memory.

## Cursor

Cursor project rules live in `.cursor/rules/`.

ForgeLoop provides `.cursor/rules/forgeloop.mdc` as an always-applied rule so Cursor Agent sees the core loop and validation commands.

Cursor can also use `AGENTS.md` as a simpler shared instruction source.

## GitHub Copilot

GitHub Copilot uses `.github/copilot-instructions.md` for repository-wide custom instructions.

ForgeLoop keeps this file short and points it back to `AGENTS.md`.

## Gemini

Gemini uses `GEMINI.md` as its native project memory entry point.

ForgeLoop keeps this file short and points it back to `AGENTS.md`, `pack`, and `tokens`.

## Windsurf

Windsurf workspace rules live in `.windsurf/rules/`.

ForgeLoop provides a concise workspace rule. It avoids duplicating the whole workflow and points back to `AGENTS.md`.

## Cline And Roo Code

Cline uses `.clinerules/` and Roo Code uses `.roo/rules/`.

ForgeLoop gives both tools small project rules plus a `.clineignore` file to avoid loading caches, build output, and generated files.

## JetBrains AI

JetBrains AI can use project rules from `.aiassistant/rules/`.

This profile is marked beta because users should confirm their IDE has attached the rule to the active chat or review.

## Kiro

Kiro steering files live in `.kiro/steering/`.

ForgeLoop provides `product.md`, `tech.md`, and `structure.md` so Kiro has the product purpose, validation commands, and folder map without reading the whole repository.

## OpenCode

OpenCode can use `AGENTS.md` plus project agents in `.opencode/agents/`.

ForgeLoop provides `forge-review.md` as a read-only review subagent.

## Aider

Aider uses `.aider.conf.yml` to read `AGENTS.md`.

ForgeLoop disables auto-commits in that config so the user stays in control.

## Coming Soon

The setup menu lists these as planned until native profiles are tested:

- ChatGPT coding workspace
- Amazon Q Developer
- Zed
- Replit
- Qwen Code / Factory Droid / Pi

## Compatibility Risks

- Tools treat instruction files as guidance, not hard enforcement.
- Some tools truncate long instruction files.
- Tool-specific rule loaders can change over time.
- Hooks and automatic context injection are not portable across tools.
- Cursor and Codex do not use Claude Code skills directly.
- Exact token counting is model-specific. ForgeLoop labels estimates clearly unless a local exact tokenizer is available.
- Rule files can become token ballast if they duplicate long docs.

## Design Decision

ForgeLoop keeps the core workflow in portable markdown and keeps tool-specific files small.

Future integrations should adapt to the same commands instead of creating separate memory systems.

## Token Measurement

Run:

```bash
python -m forgeloop tokens "memory validation" . --tool all-supported --limit 5
```

Each tool report includes an `exact` field.

Only make public savings claims from reports where the measurement command, tool profile, and exact flag are included.

## Sources Checked

- Claude Code memory and instruction loading: https://code.claude.com/docs/en/memory
- Claude Code cost guidance for moving detailed instructions into skills: https://code.claude.com/docs/en/costs
- OpenAI Codex `AGENTS.md` guidance: https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex agent loop and instruction chain: https://openai.com/index/unrolling-the-codex-agent-loop/
- Cursor rules documentation: https://docs.cursor.com/en/context
- Gemini CLI memory commands: https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md
- Windsurf memories and rules: https://docs.windsurf.com/plugins/cascade/memories
- Cline rules and memory bank: https://docs.cline.bot/customization/cline-rules
- JetBrains AI project rules: https://www.jetbrains.com/help/ai-assistant/configure-project-rules.html
- Kiro steering: https://kiro.help/docs/kiro/steering
- OpenCode agents and permissions: https://opencode.ai/docs/agents/
- AGENTS.md cross-tool convention: https://agents.md/
