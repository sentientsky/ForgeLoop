# Auditor Review: Matt, Every, Superpowers, And ForgeLoop

Date: 2026-05-04

This is a stricter second-pass audit. The goal is to identify what ForgeLoop missed, where it is already stronger, and what ideas can be adapted from Superpowers without copying text, code, or branding.

## Sources Reviewed

### Matt Pocock skills

- Repository: https://github.com/mattpocock/skills
- Reviewed commit: `b843cb5ea74b1fe5e58a0fc23cddef9e66076fb8`
- Focus: small composable skills, shared language, TDD, diagnosis, architecture deepening, concise skill authoring.

### Every Compound Engineering plugin

- Repository: https://github.com/EveryInc/compound-engineering-plugin
- Reviewed commit: `06a7cee0ad68cb50cebdb8a2a864ec4148ffba78`
- Focus: strategy, ideation, brainstorm, plan, work, code review, doc review, compound memory, memory refresh, setup, installer safety, dynamic agents.

### Superpowers

- Repository: https://github.com/obra/superpowers
- Reviewed commit: `e7a2d16476bf042e9add4699c9d018a90f86e4a6`
- Version observed in `package.json`: `5.0.7`
- Focus: bootstrap skill discipline, brainstorming, writing plans, TDD, systematic debugging, verification before completion, subagent-driven development, worktrees, branch finishing, skill evals, cross-tool packaging.

## Superpowers Inventory

Superpowers is compact but forceful.

It ships:

- 14 core skills.
- 1 code reviewer agent.
- Claude, Codex, Cursor, Gemini, OpenCode, Copilot-facing install paths.
- Session-start hook bootstrap for Claude and Cursor.
- OpenCode plugin that injects bootstrap context and registers skills.
- Visual brainstorming companion.
- Skill triggering tests.
- Explicit skill request tests.
- Claude Code integration tests.
- Token usage analysis script for Claude sessions.

## Strong Ideas To Adapt From Superpowers

### 1. Bootstrap acceptance test

Superpowers treats a tool integration as real only if the skill system activates at session start and routes a normal prompt into the expected workflow.

ForgeLoop should add an acceptance test per target tool:

```text
"Let's build a small todo app"
Expected: ForgeLoop discovers intent and enters Discover or Align before code.
```

This is stronger than checking that files exist.

### 2. Skills as behaviour-shaping code

Superpowers treats skills like code that needs tests. A skill is not "good" because it sounds good. It is good when it changes agent behaviour under pressure.

ForgeLoop should add a skill eval harness:

- natural prompt trigger tests
- explicit skill request tests
- pressure scenarios
- before and after evidence
- transcript capture
- token usage report

### 3. Verification before completion

ForgeLoop has Check, but Superpowers has a sharper completion gate: no success claim without fresh verification evidence.

ForgeLoop should add this as a Check standard and possibly a skill.

### 4. Worktree lifecycle

Superpowers has a complete branch lifecycle:

- choose isolation location
- verify worktree folder is ignored
- run baseline setup
- verify clean tests before work
- finish with merge, PR, keep, or discard choices

ForgeLoop currently plans for small safe changes, but it does not yet have a complete isolated workspace lifecycle.

### 5. Two-stage task review

Superpowers subagent development reviews each task twice:

- spec compliance: did it build what was requested, no more and no less?
- code quality: is it clean, tested, maintainable, and safe?

ForgeLoop's Check stage can adapt this without copying the implementation.

### 6. Visual companion as an optional tool

Superpowers includes a local visual companion for brainstorming visual choices.

ForgeLoop should not copy the server. But it can adopt the principle:

- visual help is optional
- only use it when seeing beats reading
- keep user consent explicit
- make token and local-server cost visible

### 7. PR contributor gate

Superpowers has unusually strict contributor guidance for AI-generated PRs. The idea is worth adapting:

- one problem per PR
- real problem evidence required
- no speculative fixes
- no blank templates
- human review before submission
- skill changes require eval evidence

ForgeLoop should add this to contribution guidelines before public GitHub launch.

## Strong Ideas To Keep From Matt

Matt remains the best source for small composable thinking loops:

- shared project language
- tiny decision records
- one-question-at-a-time interrogation
- test-first tracer bullets
- diagnosis before guessing
- architecture deepening through interface quality

These should remain the intellectual centre of ForgeLoop V4.

## Strong Ideas To Keep From Every

Every remains the best source for full product workflow:

- strategy as durable upstream context
- ideation before brainstorm
- plan confidence checks
- dynamic review teams
- structured finding schemas
- headless and report-only review modes
- compound memory and memory refresh
- installer manifests, ownership gates, and cleanup safety

These should shape ForgeLoop's production tooling.

## ForgeLoop Strengths

ForgeLoop is already ahead in these areas:

1. Beginner-safe product shape
   - Five stages are simpler to explain than Every's broad skill graph or Superpowers' strict full methodology.

2. Memory architecture
   - ForgeLoop has a deliberate memory and palace structure.
   - Context packets avoid loading full memory folders.

3. Token accountability
   - ForgeLoop already reports packet size and estimated savings.
   - Public claims are gated behind measured reports.

4. Secret-safety posture
   - ForgeLoop keeps real secrets outside the repo.
   - It checks `.env` files and refuses symlinked config writes.

5. Broad repo-local compatibility
   - ForgeLoop already ships thin entry files for many AI coding tools.

6. Open source friendliness
   - MIT licence, contribution guidelines, security policy, README, HOW_TO_USE, and GitHub page text are in place.

## ForgeLoop Weaknesses

ForgeLoop is not yet ahead in these areas:

1. Deployment maturity
   - Superpowers and Every have real plugin packaging and marketplace-oriented install paths.
   - ForgeLoop has repo-local compatibility files, not a full plugin release system.

2. Skill behaviour tests
   - Superpowers has skill-trigger tests and integration tests.
   - ForgeLoop validates structure, but does not yet prove agent behaviour.

3. Workflow enforcement
   - Superpowers uses bootstrap hooks and a strong "use the skill" discipline.
   - ForgeLoop is more advisory today.

4. Worktree isolation
   - Superpowers and Every both have stronger branch/worktree execution patterns.
   - ForgeLoop needs an isolated workspace standard before heavy automation.

5. Review routing
   - Every is far ahead on dynamic reviewer selection and structured findings.
   - ForgeLoop has four reviewers and a plan to expand.

6. Skill authoring maturity
   - Matt and Superpowers both have stronger guidance for writing and testing skills.
   - ForgeLoop needs an original skill authoring standard.

## Deployment Verdict

ForgeLoop is not yet better than Superpowers or Every in deployment maturity.

ForgeLoop is better than the reviewed projects in two strategic areas:

- It is more explicitly memory-first.
- It is more honest about token measurement before public savings claims.

ForgeLoop can become better overall if V4.1 adds:

- skill eval harness
- deployment acceptance tests
- doctor command
- managed install manifests
- worktree lifecycle
- verification-before-completion gate
- dynamic review routing

## Auditor Recommendation

Do not add more broad features first.

The next production step should be a quality layer:

1. Add `doctor`.
2. Add skill eval tests.
3. Add deployment acceptance tests.
4. Add verification-before-completion.
5. Add worktree lifecycle docs and dry-run CLI checks.
6. Add dynamic review routing.

This makes ForgeLoop harder to fake, harder to misuse, and easier to trust.

