# Matt Pocock Skills And Every Compound Engineering Deep Review

Date: 2026-05-02

This note records the deeper review used to shape ForgeLoop V4. It is research, not a copy plan. ForgeLoop should adopt principles, not wording, code, or private product assumptions from either project.

## Sources Reviewed

### Matt Pocock skills

- Repository: https://github.com/mattpocock/skills
- Reviewed commit: `b843cb5ea74b1fe5e58a0fc23cddef9e66076fb8`
- Local research clone: `%TEMP%\forgeloop-research\matt-skills`
- Files read in depth:
  - `README.md`
  - `CONTEXT.md`
  - `skills/engineering/grill-with-docs/SKILL.md`
  - `skills/engineering/grill-with-docs/CONTEXT-FORMAT.md`
  - `skills/engineering/grill-with-docs/ADR-FORMAT.md`
  - `skills/engineering/tdd/SKILL.md`
  - `skills/engineering/tdd/tests.md`
  - `skills/engineering/tdd/mocking.md`
  - `skills/engineering/tdd/deep-modules.md`
  - `skills/engineering/tdd/interface-design.md`
  - `skills/engineering/tdd/refactoring.md`
  - `skills/engineering/diagnose/SKILL.md`
  - `skills/engineering/improve-codebase-architecture/SKILL.md`
  - `skills/engineering/improve-codebase-architecture/LANGUAGE.md`
  - `skills/engineering/improve-codebase-architecture/DEEPENING.md`
  - `skills/engineering/improve-codebase-architecture/INTERFACE-DESIGN.md`
  - `skills/engineering/to-prd/SKILL.md`
  - `skills/engineering/to-issues/SKILL.md`
  - `skills/engineering/triage/SKILL.md`
  - `skills/engineering/zoom-out/SKILL.md`
  - `skills/productivity/caveman/SKILL.md`
  - `skills/productivity/write-a-skill/SKILL.md`
  - `skills/misc/git-guardrails-claude-code/SKILL.md`

### Every Compound Engineering plugin

- Repository: https://github.com/EveryInc/compound-engineering-plugin
- Reviewed commit: `d685f0794863a73ae3ca3620d2ae747510e9eaa0`
- Local research clone: `%TEMP%\forgeloop-research\compound-engineering-plugin`
- Files read in depth:
  - `README.md`
  - `CLAUDE.md`
  - `AGENTS.md`
  - `plugins/compound-engineering/skills/ce-strategy/SKILL.md`
  - `plugins/compound-engineering/skills/ce-ideate/SKILL.md`
  - `plugins/compound-engineering/skills/ce-brainstorm/SKILL.md`
  - `plugins/compound-engineering/skills/ce-plan/SKILL.md`
  - `plugins/compound-engineering/skills/ce-work/SKILL.md`
  - `plugins/compound-engineering/skills/ce-code-review/SKILL.md`
  - `plugins/compound-engineering/skills/ce-doc-review/SKILL.md`
  - `plugins/compound-engineering/skills/ce-debug/SKILL.md`
  - `plugins/compound-engineering/skills/ce-compound/SKILL.md`
  - `plugins/compound-engineering/skills/ce-compound-refresh/SKILL.md`
  - `plugins/compound-engineering/skills/ce-sessions/SKILL.md`
  - `plugins/compound-engineering/skills/ce-session-inventory/SKILL.md`
  - `plugins/compound-engineering/skills/ce-session-extract/SKILL.md`
  - `plugins/compound-engineering/skills/ce-simplify-code/SKILL.md`
  - `plugins/compound-engineering/skills/ce-optimize/SKILL.md`
  - `plugins/compound-engineering/skills/ce-product-pulse/SKILL.md`
  - `plugins/compound-engineering/skills/ce-setup/SKILL.md`
  - `plugins/compound-engineering/skills/ce-agent-native-architecture/SKILL.md`
  - `src/utils/detect-tools.ts`
  - `src/utils/secrets.ts`
  - `src/utils/symlink.ts`
  - `src/utils/json-config.ts`
  - `src/targets/codex.ts`

## What Matt Gets Right

Matt's repo is strong because the skills are small, sharp, and easy to combine. They do not try to own the entire engineering process. They improve one thinking loop at a time.

The strongest ideas to adapt:

1. Shared project language
   - A concise vocabulary file lets the agent use short, precise terms instead of re-explaining the domain every session.
   - This is a better path than inventing a hidden AI-only language. Humans must be able to read and correct the language.

2. Questioning before building
   - The agent challenges fuzzy terms, contradictions, and missing decisions before work starts.
   - Code-discoverable answers are found from the repo instead of pushed back to the user.

3. Tiny decision records
   - Decisions should be recorded only when they are hard to reverse, surprising later, and based on a real trade-off.
   - This prevents decision logs becoming paperwork.

4. Feedback loop first
   - Debugging starts by building a repeatable signal.
   - A fast repro, test, script, or harness beats speculative code reading.

5. Tracer bullet TDD
   - Build one visible behaviour at a time.
   - Avoid writing a huge wall of imagined tests before learning from the first implementation slice.

6. Architecture deepening
   - Good architecture hides useful behaviour behind a smaller interface.
   - Testing through the interface is the key discipline.

7. Skills should be compact
   - Keep `SKILL.md` short.
   - Move detailed rules into references that are loaded only when needed.

## What Every Gets Right

Every's plugin is strong because it treats agent work as a product workflow, not only a prompt collection. It adds structure around setup, review, plans, documents, sessions, and long-term learning.

The strongest ideas to adapt:

1. Strategy before execution
   - A small strategy file gives ideation and planning a durable anchor.
   - ForgeLoop can add this as optional product context, not a required step for every code task.

2. Ideation separated from planning
   - Generate many ideas, critique them, then only develop the survivors.
   - This prevents the agent from turning weak first thoughts into overbuilt plans.

3. Structured plan depth
   - A small task should not receive a giant plan.
   - A high-risk task should receive a stronger plan with risk, validation, and review routing.

4. Dynamic review teams
   - Always-on reviewers catch general defects.
   - Conditional reviewers join only when the diff touches security, performance, API contracts, data, reliability, migrations, or UI.

5. Review finding schema
   - Findings need severity, confidence, evidence, owner, and fix route.
   - This makes review output easier to merge, deduplicate, and act on.

6. Headless and report-only modes
   - A review system needs modes so it can run interactively, in automation, or as a read-only check.

7. Knowledge refresh
   - Capturing lessons is not enough. Old lessons need review, consolidation, replacement, and stale marking.

8. Health check setup
   - A `doctor` style command is more useful than asking users to inspect every file manually.

9. Safe installer design
   - Tool detection, managed manifests, ownership checks, symlink safety, and local config guards all matter.

10. Optional session history
   - Session history can help, but it must be opt-in because it may contain private context and can burn tokens fast.

## What ForgeLoop Should Not Copy

- Do not copy skill text, file names, agent prompts, or repo-specific implementation.
- Do not make the MVP as heavy as Every's full plugin.
- Do not use hidden AI-only language that humans cannot inspect.
- Do not auto-delete or auto-clean user files without a managed manifest and ownership proof.
- Do not make token-saving claims without measured packet reports.
- Do not add dozens of reviewers before there is a lightweight review router.

## ForgeLoop Gap Map

Current ForgeLoop is strong at:

- Five-stage workflow: Discover, Frame, Build, Check, Capture.
- Cross-tool instruction files for Claude Code, Codex, Cursor, Copilot, Gemini, Windsurf, Cline/Roo, JetBrains AI, Kiro, OpenCode, and Aider.
- Context packet indexing.
- Token packet reporting.
- External secrets metadata.
- Basic specialised reviewers.

Current ForgeLoop needs:

- A human-readable project language system.
- Tiny decision records.
- A stronger questioning loop inside Frame.
- A diagnosis loop for bugs.
- A TDD tracer bullet loop for risky changes.
- Architecture deepening as a first-class skill.
- Dynamic review routing instead of only four fixed reviewers.
- A memory refresh workflow.
- A doctor command for setup, portability, and security checks.
- Safer installer metadata for any future tool-wide writes.

## Recommended Direction

ForgeLoop should become a skill ladder:

- Core skills stay stable: Discover, Frame, Build, Check, Capture.
- Advanced skills are loaded only when the task needs them: Align, Probe, TDD, Deepen, Simplify, Refresh, Doctor.
- Shared language and decision records support the skills without bloating normal prompts.
- Packet-size reporting remains the evidence layer for token claims.

The product promise should be:

> Move fast with AI, but keep a durable trail of language, decisions, feedback, review, and lessons.

