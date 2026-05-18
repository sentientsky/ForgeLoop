# ForgeLoop Rule For Roo Code

Use `AGENTS.md` as the shared repository instruction file.

For non-trivial work, follow Discover, Frame, Build, Check, Capture.

Planning rules:

- Ask clarifying questions only when blocked.
- Prefer small vertical slices.
- Keep module interfaces simple and testable.
- Build a fast feedback loop before diagnosing bugs.

Memory rules:

- Run `python -m forgeloop pack "<task query>" . --limit 5` before reading broad memory.
- Run `python -m forgeloop tokens "<task query>" . --tool cline-roo --limit 5` for measured token reports.
- Capture lessons in `docs/captures/` or reusable patterns in `docs/solutions/`.

Security rules:

- Do not write secrets into repo files.
- Do not run destructive Git commands without explicit user instruction.
- Validate with `python -m forgeloop validate .` and `python -m unittest discover -s tests`.
