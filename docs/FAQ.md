# FAQ

## Is ForgeLoop only for Claude Code?

No. Claude Code has the richest native support through skills and agents, but ForgeLoop also includes portable entry files for Codex and other coding tools.

## Does ForgeLoop store secrets?

No. ForgeLoop keeps only `.env.example` in the repository. Real secrets live outside the repo.

## Does ForgeLoop make token usage lower?

ForgeLoop reduces memory loading by using pointer-first context packets. Use `python -m forgeloop tokens "<query>" .` to measure a specific task. Do not make public percentage claims without the command output.

## Does ForgeLoop include OpenCLI?

No. ForgeLoop integrates OpenCLI as an optional peer plugin. OpenCLI installs only when the user explicitly runs the install command.

## Can beginners use it?

Yes. Start with `docs/GETTING_STARTED.md` and the five-stage loop.

## Can teams use it?

Yes. Use the setup menu, compatibility report, doctor command, contribution guide, and CI workflow.

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

