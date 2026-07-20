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

## Review And Approval

Opening a pull request does not grant permission to merge it. Automated checks never auto-approve a contribution.

The normal path is:

1. A contributor opens a focused pull request.
2. CI, package smoke tests, and security scanning run.
3. A maintainer reviews the code, docs, risks, and evidence.
4. The contributor resolves requested changes and conversations.
5. A maintainer merges only after the required checks and approvals pass.

Dependabot and AI-authored changes use the same process. See `GOVERNANCE.md` for maintainer roles, high-risk changes, waiting periods, and release authority.

## Required Commands

Install the development tools, then run:

```bash
python -m pip install -e ".[dev]"
python -m ruff check forgeloop tests
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop index . --check
python -m forgeloop secrets check .
python -m build
python -m twine check dist/*
python tests/package_smoke.py dist .
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
