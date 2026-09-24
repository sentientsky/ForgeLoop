# How To Use ForgeLoop

ForgeLoop helps Claude Code work like a disciplined engineering team.

The loop is:

1. Discover
2. Frame
3. Build
4. Check
5. Capture

Use it when you want AI coding to move quickly without losing memory, review quality, or control.

For the short product explanation, read `docs/WHAT_IT_IS.md`.

For first setup, read `docs/GETTING_STARTED.md`.

## First Setup

Create a new repository from the [ForgeLoop GitHub template](https://github.com/sentientsky/ForgeLoop/generate), clone it, and open its root folder in your AI coding tool. Then run the setup menu:

```bash
python -m forgeloop setup .
```

Choose the AI coding tool you are using.

The supported options are:

- Claude Code
- Codex
- Cursor
- GitHub Copilot
- Gemini
- Windsurf
- Cline / Roo Code
- JetBrains AI
- Kiro
- OpenCode
- Aider
- All supported tools

The menu also shows coming-soon tools so you can see the roadmap.

The menu records your local tool preference; it does not install files. To preview adding the selected tool's allowlisted profile files to an existing project, run `python -m forgeloop adopt ../my-project --tool codex` from a ForgeLoop source checkout. Add `--apply` only after reviewing the preview. Existing conflicts are preserved; this does not install the full CLI/runtime or manage future updates. See `docs/INSTALLATION.md` for the complete boundary.

For a non-interactive preview:

```bash
python -m forgeloop setup . --tool codex --dry-run
```

Then ask your tool to read its entry file:

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

Then run:

```bash
python -m forgeloop validate .
python -m forgeloop setup . --list
python -m forgeloop compat .
python -m forgeloop doctor .
python -m forgeloop tokens "memory validation" . --limit 5
python -m unittest discover -s tests
```

If both pass, the repository structure is healthy.

## Starting A Task

Begin with a simple prompt:

```text
/discover I want to add an export button
```

Claude should inspect the repository and write a discovery note in `docs/discoveries/`.

Then frame the work:

```text
/frame Use the latest discovery and make a safe build plan
```

The frame should explain scope, affected files, risks, tests, and rollback.

Build only after the frame is clear:

```text
/build Implement the framed change in small steps
```

Then check the result:

```text
/check Review the change with architecture, security, testing, and docs viewpoints
```

Finally capture the learning:

```text
/capture Store the reusable lesson and any changed facts
```

## Advanced Skills

Use these only when the task needs them:

- `/align` when the goal or terms are fuzzy.
- `/probe` when debugging needs a repeatable signal.
- `/tdd` when a risky behaviour slice should be tested first.
- `/deepen` when architecture boundaries need attention.
- `/simplify` when release polish or duplicated guidance is the problem.
- `/refresh-memory` when old notes conflict or may be stale.

## Using Memory Without Wasting Tokens

Before loading old notes, use a compact context packet:

```bash
python -m forgeloop pack "export button security review" . --limit 5
```

This prints an FCP/1 packet.

The packet is not the full memory. It is a small pointer list. Claude should open only the files listed in the packet that matter for the current task.

This keeps context smaller while preserving exact knowledge in markdown.

The packet also reports measured UTF-8 byte savings. Use those numbers before making any public claim about token reduction.

Example fields:

- `FCP_BYTES`: rendered packet size
- `SELECTED_SRC_BYTES`: bytes in the selected source files
- `ALL_MEMORY_BYTES`: bytes in all indexed memory files
- `SAVE_SELECTED`: measured savings against selected source files
- `SAVE_ALL`: measured savings against all indexed memory

Token estimates use a simple bytes divided by 4 approximation.

For tool-specific token reporting, run:

```bash
python -m forgeloop tokens "export button security review" . --tool codex --limit 5
```

The report says whether the count is exact or estimated. Do not make public token-saving claims unless the command, tool profile, and exact flag are included.

## Creating Notes

Use the CLI instead of hand-creating routine notes:

```bash
python -m forgeloop new discover "Export button" .
python -m forgeloop new frame "Export button" .
python -m forgeloop new check "Export button" .
python -m forgeloop new capture "Export button lesson" .
python -m forgeloop new solution "Safe export button pattern" .
```

The CLI uses templates, safe file names, and overwrite protection.

## Updating The Memory Index

After adding captures, solutions, entities, timelines, or palace drawers, run:

```bash
python -m forgeloop index .
python -m forgeloop index . --check
```

The index files live in `docs/palace/indexes/`.

## Secrets

Do not put real secrets in the repository.

Use:

```bash
python -m forgeloop secrets init .
python -m forgeloop secrets path .
python -m forgeloop secrets check .
```

ForgeLoop keeps only `.env.example` in the repo. Real `.env`-style files should live outside the project folder.

## Governed Memory

Do not put personal information in ForgeLoop Markdown notes, Git commits, prompts, or audit events.

When a project needs to point to personal or special-category data stored in an external provider, start with `templates/governed-memory-template.md` and run:

```bash
python -m forgeloop governance audit .
python -m forgeloop governance log access . --actor-ref OPERATOR-001 --record-ref STORE-EXTERNAL-001 --subject-ref SUBJ-EXAMPLE-001
python -m forgeloop governance verify .
```

The metadata must record the provenance, purpose, lawful basis, jurisdiction, retention deadline, and external storage reference. `subject_ref` must be an opaque identifier, never a name, email address, phone number, or account ID.

ForgeLoop cannot delete data from third-party embeddings, graphs, backups, or Git history. Obtain evidence from every store before recording an `erase` event. Read `docs/governance/README.md` for the full boundary.

## OpenCLI Integration

OpenCLI is optional.

ForgeLoop integrates it as an external peer plugin, not as copied source.

Check local readiness:

```bash
python -m forgeloop opencli status .
```

Preview the install:

```bash
python -m forgeloop opencli plan .
```

Install or update the latest OpenCLI package only when you explicitly choose:

```bash
python -m forgeloop opencli install . --execute
```

Include OpenCLI's AI skills only when you want them added to the local AI-agent skill system:

```bash
python -m forgeloop opencli install . --execute --with-skills
```

Browser-backed OpenCLI commands reuse your logged-in Chrome or Chromium session, so treat them as privileged. Ask before posting, deleting, buying, messaging, or changing account state.

## Hooks

Hooks are powerful but risky.

ForgeLoop keeps them inactive by default. Test hook behaviour first:

```bash
python -m forgeloop hook-simulate PreCompact .
python -m forgeloop hook-simulate Stop . --interval 15
```

Only activate hooks when they are reviewed, limited, and tested.

## Release Checklist

Before sharing or pushing to GitHub, run:

```bash
python -m unittest discover -s tests
python -m forgeloop doctor .
python -m forgeloop validate .
python -m forgeloop compat .
python -m forgeloop opencli status .
python -m forgeloop tokens "memory validation" . --limit 5
python -m forgeloop index .
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m forgeloop governance audit .
python -m forgeloop governance verify .
python -m compileall forgeloop tests
```

Use `docs/RELEASE_GUIDE.md` for the full public-release checklist.

Then check:

- no real secrets are present
- no generated cache files are committed
- memory index files are up to date
- optional integrations are checked
- new behaviour has docs
- non-trivial work has a capture note

## What To Improve Next

The next production improvements are:

- optional local full-text search
- safe opt-in context hooks
- larger public benchmark set
- live clean-session deployment eval refreshes as tools evolve
