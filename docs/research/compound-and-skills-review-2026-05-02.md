---
type: research
status: current
tags: [research, compatibility, skills, compound-engineering, matt-pocock]
valid_from: 2026-05-02
---

# Compound And Skills Review

This note records what ForgeLoop should borrow as ideas, not copied wording or code.

## Sources Reviewed

- EveryInc `compound-engineering-plugin`: https://github.com/EveryInc/compound-engineering-plugin
- Matt Pocock `skills`: https://github.com/mattpocock/skills
- Attached transcript: `Software Fundamentals Matter More Than Ever - Matt Pocock.txt`
- Gemini CLI memory command docs: https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md
- Windsurf memories and rules: https://docs.windsurf.com/plugins/cascade/memories
- Cline rules and Memory Bank docs: https://docs.cline.bot/customization/cline-rules and https://docs.cline.bot/features/memory-bank
- JetBrains AI project rules: https://www.jetbrains.com/help/ai-assistant/configure-project-rules.html
- Kiro steering: https://kiro.help/docs/kiro/steering
- OpenCode agents and permissions: https://opencode.ai/docs/agents/
- AGENTS.md convention: https://agents.md/

## Useful Ideas To Adapt

EveryInc shows that AI workflows benefit from a strong setup flow, health checks, specialised reviewers, and multi-tool conversion paths.

ForgeLoop should adapt the idea as:

- one source workflow
- tool-native entry files
- a compatibility report
- local setup profiles
- no remote installer until the repo is stable

Matt Pocock's repo and transcript reinforce four product lessons:

- shared understanding before implementation
- shared language to reduce verbose planning
- feedback loops before diagnosis
- deep modules with simple public interfaces

ForgeLoop should adapt these into original names and files:

- `docs/standards/shared-language-standard.md` later
- `docs/standards/feedback-loop-standard.md` later
- architecture review rules that reward simple interfaces
- token reports that prove savings rather than market them

## Product Decision

Do not add 40 skills yet.

Add production foundations first:

- native profiles for popular tools
- token measurement with honest exact flags
- stricter validation
- concise compatibility docs
- a capture note after each meaningful system improvement

## Security Decision

Native tool profiles must be short and must point back to `AGENTS.md`.

Long duplicated rule files become stale, expensive, and hard to audit.

## Originality Decision

ForgeLoop will not copy plugin manifests, skill text, slash command names, review schemas, or branding from either repository.

It will keep the five-stage ForgeLoop model and build original implementation around that model.
