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

## Add A Profile To An Existing Repository

From a ForgeLoop source checkout, preview the native entry files for the tool you use:

```bash
python -m forgeloop adopt ../my-project --tool claude-code
```

The command is preview-only unless `--apply` is supplied. Review the proposed files and conflicts, then apply:

```bash
python -m forgeloop adopt ../my-project --tool claude-code --apply
```

Replace `claude-code` with a supported tool id such as `codex`, or use `all-supported` for a multi-tool team. The adopter copies only the selected profile's allowlisted entry files. Identical files are left alone; differing files are reported and preserved. It rejects path traversal, symlinks, and Windows junction/reparse-point paths, and rolls back files created by the current run if a later write fails. Review the destination diff before committing.

This is a safe additive profile installer, not a content merger or managed updater. It does not replace conflicting instructions, install a ForgeLoop CLI into the destination, create backups of user files, or automatically update/uninstall files later. To use ForgeLoop's full CLI, memory system, and maintained documentation, create a project from the GitHub template. For an existing project, resolve each reported conflict deliberately.

The `setup` command remains a local preference selector; it does not install files.

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
