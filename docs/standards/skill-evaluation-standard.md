---
type: standard
date: 2026-05-11
status: current
tags: [skills, evaluation, behaviour, quality]
---

# Skill Evaluation Standard

ForgeLoop skills are behaviour, not decoration.

Every new or changed skill should pass three checks before it is treated as reliable.

## Checks

1. Trigger check
   - A natural prompt should make the skill relevant.
   - An explicit skill request should load the skill directly.

2. Behaviour check
   - The skill should change what the agent does.
   - It should avoid vague advice and produce a concrete output.

3. Pressure check
   - The skill should still work when the task is rushed, ambiguous, or high-risk.
   - The agent should not skip the rule just because completion feels close.

## Evidence

Use `templates/skill-eval-template.md`.

Store examples in `examples/skill-evals/`.

## Release Rule

Do not claim a skill is production ready until it has at least one passing trigger example and one pressure example.

