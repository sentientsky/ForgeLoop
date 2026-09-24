# Installation And First Use

ForgeLoop is currently distributed as a GitHub source template, not as a PyPI package.

## Start A New Project

1. Open [sentientsky/ForgeLoop](https://github.com/sentientsky/ForgeLoop) and choose **Use this template**, then **Create a new repository**.
2. On the new repository page, copy its HTTPS clone URL. In a terminal, run `git clone` followed by that URL, then change into the folder Git created.

3. Confirm Python 3.10 or later is available, then run:

```bash
python -m forgeloop doctor .
python -m forgeloop setup .
```

4. Open that repository in Claude Code, Codex, or another tool. ForgeLoop's project instructions and profiles are already in the template; the setup command records your local tool choice in a Git-ignored file.

5. Begin with `docs/GETTING_STARTED.md`.

On Windows, use `py -3` instead of `python` if the `python` command is unavailable.

## Try ForgeLoop Without Creating A Project

```bash
git clone https://github.com/sentientsky/ForgeLoop.git
cd ForgeLoop
python -m forgeloop doctor .
python -m forgeloop setup .
```

This opens the ForgeLoop source repository as a workspace. Do not commit personal experiments to the upstream repository.

## Use With An Existing Repository

There is not yet an automated installer that safely merges ForgeLoop files into an existing project. The setup menu only records a tool selection; it does not install or merge instruction files. Do not assume that running it in an unrelated repository enables ForgeLoop. For now, review the relevant entry files and copy or adapt them deliberately, resolving conflicts with existing instructions yourself. A conflict-aware installer is a planned follow-up.

## Python Development Environment

The CLI works directly from the repository root and does not need a global install. Contributors should use an isolated virtual environment to avoid conflicts with other Python projects:

```bash
python -m venv .venv
```

Activate it (`.venv\\Scripts\\Activate.ps1` in PowerShell, or `source .venv/bin/activate` on macOS/Linux), then install the locked CI tools and editable local package:

```bash
python -m pip install --require-hashes -r .github/requirements-ci.txt
python -m pip install --no-deps --no-build-isolation -e .
```

Do not use `pip install forgeloop` from the public package index. That distribution name is owned by an unrelated project. ForgeLoop does not publish to PyPI.

## Optional Integrations

Node.js and npm are needed only for the optional OpenCLI integration. Preview before installing:

```bash
python -m forgeloop opencli plan .
python -m forgeloop opencli install . --execute
```

Exact Codex-style token counts require the optional `tiktoken` package. Other token reports remain labelled estimates unless a matching local tokenizer is available.
