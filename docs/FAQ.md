# FAQ

## Is ForgeLoop only for Claude Code?

No. Claude Code has the richest native support through skills and agents, but ForgeLoop also includes portable entry files for Codex and other coding tools.

## Does ForgeLoop store secrets?

No. ForgeLoop keeps only `.env.example` in the repository. Real secrets live outside the repo.

## Does ForgeLoop store personal data or make compliance claims?

No. ForgeLoop rejects personal data in Git-tracked memory Markdown. It can check governance metadata that points to an external store and keep a local metadata-only, hash-chained audit log. It is not legal advice, a compliance certification, or proof of deletion from third-party systems. Read `governance/README.md`.

## Can ForgeLoop prove a right-to-erasure request is complete?

Not on its own. The audit log can record the governance event, but every embedding store, graph, cache, backup, export, provider, Git history, fork, and replica must be handled separately. Record erasure only after the responsible providers supply appropriate evidence.

## Does ForgeLoop make token usage lower?

ForgeLoop reduces memory loading by using pointer-first context packets. Use `python -m forgeloop tokens "<query>" .` to measure a specific task. Do not make public percentage claims without the command output.

## Does ForgeLoop include OpenCLI?

No. ForgeLoop integrates OpenCLI as an optional peer plugin. OpenCLI installs only when the user explicitly runs the install command.

## Can beginners use it?

Yes. The GitHub template is the complete distribution. Existing repositories can use the preview-first `adopt` command to add allowlisted tool entry files without overwriting conflicts, but that does not install the full CLI/runtime or provide managed updates.

## Can I install it into an existing project?

Use `python -m forgeloop adopt PATH --tool TOOL` from a ForgeLoop source checkout to preview, then add `--apply` to copy absent profile files. Existing differences are preserved and reported. The `setup` command only records a local preference; it does not install files. The adopter does not merge conflicts or install the complete ForgeLoop CLI/runtime.

## Can I run `pip install forgeloop`?

No. That PyPI name belongs to an unrelated project. ForgeLoop is distributed from GitHub as a source template; no PyPI package is published.

## Does `forgeloop compat` prove my AI tool works with ForgeLoop?

No. It confirms that expected profile files are present. A live clean-session check must be run in the actual external tool and recorded before claiming verified compatibility.

## Can teams use it?

Yes. Use the setup menu, compatibility report, doctor command, contribution guide, and CI workflow.

## How are contributions approved?

Contributors open a pull request. Automation tests the change, then a maintainer reviews it. Passing checks do not auto-approve or auto-merge a contribution. The complete rules are in `../GOVERNANCE.md`.

## Are Dependabot or AI-authored changes trusted automatically?

No. They use the same tests, security checks, human review, and approval rules as any other contribution.

## Where are the GitHub setup instructions?

Use `GITHUB_SETUP.md` for the current repository controls and source-release process. The repository is already public; PyPI publishing is intentionally disabled.

## Are hooks active by default?

No. Hooks are documented and simulated first. Active automation should be opt-in after review.

## What should I run before pushing?

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop doctor .
python -m forgeloop compat .
python -m forgeloop index . --check
python -m forgeloop secrets check .
```

## How do maintainers publish a source release?

Read `docs/PUBLISHING.md`.

ForgeLoop source releases are created on GitHub after a matching version tag passes the release workflow.
