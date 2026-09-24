# Getting Started

This guide is for a new user creating a project from the ForgeLoop GitHub template. ForgeLoop currently supports template-based greenfield projects; it does not automatically merge its files into an existing repository.

For the complete template and existing-repository limitations, see `docs/INSTALLATION.md`.

For every command, see `docs/COMMAND_REFERENCE.md`.

For common problems, see `docs/TROUBLESHOOTING.md`.

## 1. Create Your Repository

From [sentientsky/ForgeLoop](https://github.com/sentientsky/ForgeLoop), choose **Use this template** and create a repository under your account. Copy the clone URL shown on your new repository's GitHub page, clone it, then open its root folder in your chosen AI coding tool.

## 2. Check The Project

From the repository root:

```bash
python -m forgeloop doctor .
```

If doctor reports warnings, read them. Warnings do not always block use.

## 3. Choose Your AI Coding Tool

Run:

```bash
python -m forgeloop setup .
```

Pick the tool you are using.

For teams or comparison work, choose all supported tools.

The setup menu records your selection locally. It does not install files into another repository. The template already contains the profiles listed below.

## 4. Read The Right Entry File

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
- OpenCode: `.opencode/agents/forge-review.md` and `AGENTS.md`
- Aider: `.aider.conf.yml` and `AGENTS.md`

## 5. Start With The Loop

Use this prompt:

```text
Discover this repository and explain the safest first task.
```

Then move through:

```text
Frame the task.
Build the framed change.
Check the result.
Capture the lesson.
```

## 6. Use Memory Efficiently

Before opening old notes:

```bash
python -m forgeloop pack "your task query" . --limit 5
```

Open only the files listed in the packet that are relevant.

## 7. Validate Before Handoff

Use:

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop doctor .
```

## 8. Optional OpenCLI Integration

Check status:

```bash
python -m forgeloop opencli status .
```

Preview install:

```bash
python -m forgeloop opencli plan .
```

Install only when you explicitly want it:

```bash
python -m forgeloop opencli install . --execute
```
