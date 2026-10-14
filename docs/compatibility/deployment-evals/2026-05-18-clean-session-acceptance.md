---
type: deployment-acceptance
date: 2026-09-24
status: current
tags: [deployment, compatibility, release]
---

# Clean-Session Acceptance Pack

This file records one real Codex CLI acceptance and one blocked Claude Code CLI attempt. It is not evidence that other tools or interactive desktop sessions have been tested.

It does not pretend to be a live transcript from every external product UI. It records the repeatable check a maintainer should run when refreshing public compatibility claims.

## Universal Prompt

```text
Read this repository's AI instructions, explain the ForgeLoop workflow in five bullets, then say which validation command you would run first.
```

Expected answer:

- Mentions Discover, Frame, Build, Check, Capture.
- Points to the tool's native entry file or `AGENTS.md`.
- Recommends `python -m forgeloop pack "<task query>" . --limit 5` before broad memory reads, then the relevant validation command.
- Does not load broad memory folders before using `pack`.
- Does not propose writing files before discovery.

## Tool Matrix

| Tool | Entry file | Expected first validation | Status |
| --- | --- | --- | --- |
| Claude Code | `CLAUDE.md` | `python -m forgeloop pack "<task query>" . --limit 5` | Blocked: Claude Code 2.1.92 returned repeated API `401 authentication_failed` responses despite local auth status reporting logged in; rerun after interactive re-authentication |
| Codex | `AGENTS.md` | `python -m forgeloop pack "<task query>" . --limit 5` | Passed in Codex CLI 0.155.0-alpha.9.2, ephemeral session, read-only sandbox; CLI only |
| Cursor | `.cursor/rules/forgeloop.mdc` | `python -m forgeloop validate .` | Prompt defined; current live acceptance not recorded |
| GitHub Copilot | `.github/copilot-instructions.md` | `python -m forgeloop validate .` | Prompt defined; current live acceptance not recorded |
| Gemini | `GEMINI.md` | `python -m forgeloop tokens "memory validation" . --tool gemini` | Prompt defined; current live acceptance not recorded |
| Windsurf | `.windsurf/rules/forgeloop.md` | `python -m forgeloop pack "memory validation" .` | Prompt defined; current live acceptance not recorded |
| Cline | `.clinerules/forgeloop.md` | `python -m forgeloop doctor .` | Prompt defined; current live acceptance not recorded |
| Roo Code | `.roo/rules/forgeloop.md` | `python -m forgeloop doctor .` | Prompt defined; current live acceptance not recorded |
| JetBrains AI | `.aiassistant/rules/forgeloop.md` | `python -m forgeloop validate .` | Beta, needs IDE attachment check |
| Kiro | `.kiro/steering/` | `python -m forgeloop validate .` | Beta, needs steering attachment check |
| OpenCode | `.opencode/agents/forge-review.md` and `AGENTS.md` | `python -m forgeloop compat .` | Prompt defined; current live acceptance not recorded |
| Aider | `.aider.conf.yml` and `AGENTS.md` | `python -m forgeloop validate .` | Portable check |
| Generic agents | `AGENTS.md` | `python -m forgeloop doctor .` | Portable check |

## Recording A Live Check

Copy `templates/deployment-acceptance-template.md`, fill the actual prompt, response, validation command, and limitation, then update `docs/compatibility/deployment-matrix.md`.

## 2026-09-24 Run

- Codex CLI was run with `--sandbox read-only --ephemeral --ignore-user-config`. It read `AGENTS.md`, `CLAUDE.md`, `docs/GETTING_STARTED.md`, and the verification standard, then correctly identified Discover, Frame, Build, Check, Capture; recommended the pointer-first `pack` command; and observed the OpenCLI safety rule. It reported that no files or commands were changed. This validates the CLI instruction path, not Codex desktop or every supported model.
- Claude Code was run in print mode with no-session persistence and no write-capable tools. It emitted session initialisation, then repeated API `401 authentication_failed` responses. The run was stopped after six retries. The local auth-status command said logged in, so the discrepancy needs interactive account re-authentication and a rerun; Claude acceptance is not passed.
- Neither result is a certification or a guarantee for future CLI versions. Repeat after tool upgrades and before release promotion.

## Rerun Claude Code

The recorded Claude check is blocked by API authentication failures. Do not count it as a pass until a fresh session completes successfully. Re-authenticate interactively from a terminal first:

```text
claude auth status
claude auth login
```

If the session still returns `401 authentication_failed`, sign out and authenticate again:

```text
claude auth logout
claude auth login
```

Then, from the repository root, run this read-only check in a fresh session:

```text
claude -p --tools Read --permission-mode plan --setting-sources project --no-session-persistence --output-format text "Read CLAUDE.md, docs/GETTING_STARTED.md, and docs/standards/verification-before-completion-standard.md. In no more than 8 concise bullets, state the prescribed workflow, the first safe command for a new task, and one important safety or review rule. Do not modify files or run commands. If a file is unavailable, say so."
```

Count the check as passed only if the command exits successfully, identifies Discover, Frame, Build, Check, and Capture, recommends the pointer-first `python -m forgeloop pack "<task query>" . --limit 5` command, gives a relevant safety or review rule, and leaves the working tree unchanged. Any authentication error, missing instruction, attempted write, or non-zero exit is a failure; record the actual result rather than treating it as accepted. Verify the working tree with `git status --short` after the run.
