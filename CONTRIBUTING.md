# Contributing To ForgeLoop

Thank you for helping improve ForgeLoop.

ForgeLoop is meant to be simple enough for beginners and strong enough for serious builders. Contributions should improve the workflow, memory system, review quality, or documentation without making the product feel heavy.

## Good Contributions

Good contributions usually do one of these things:

- make a stage clearer
- improve a template
- add a useful reviewer
- capture a repeated lesson
- simplify setup
- improve safety
- make the memory palace easier to use

## Contribution Loop

Use ForgeLoop to improve ForgeLoop:

1. Discover the issue or opportunity.
2. Frame the change clearly.
3. Build in small steps.
4. Check the result.
5. Capture the reusable lesson.

## Pull Request Checklist

Before opening a pull request, check:

- the change has a clear purpose
- the pull request solves one problem
- unrelated files were not changed
- documentation was updated where needed
- templates still make sense for beginners
- any new rule belongs in the right place
- any repeated pattern was promoted to a skill, template, agent, hook, or standard
- risks or trade-offs are written down
- skill changes include evaluation evidence or a new eval example
- tool support changes include an acceptance prompt or transcript
- public claims include measured command output

## Required Commands

Run:

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop index . --check
python -m forgeloop secrets check .
```

## Style

- Use UK English.
- Keep writing direct and practical.
- Prefer short sections and clear lists.
- Avoid hype.
- Avoid copying wording from other products.
- Make examples realistic.

## Adding A New Skill

Add project skills under `.claude/skills/<skill-name>/SKILL.md`.

Every skill should include:

- clear YAML frontmatter
- when to use it
- what it should produce
- where outputs should be saved
- what safety checks matter

Also add or update a skill evaluation note in `examples/skill-evals/`.

## Adding A New Reviewer

Add reviewers under `.claude/agents/`.

Every reviewer should:

- focus on one domain
- avoid editing files
- return P1, P2, and P3 findings
- include file-specific findings when possible
- state when no issue is found

## Licence

By contributing, you agree that your contribution is licensed under the MIT Licence.
