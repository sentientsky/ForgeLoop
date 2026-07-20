# Summary

What changed and why?

## ForgeLoop Stage

- [ ] Discover
- [ ] Frame
- [ ] Build
- [ ] Check
- [ ] Capture

## Validation

Paste safe command output or explain why a command could not run.

- [ ] `python -m unittest discover -s tests`
- [ ] `python -m ruff check forgeloop tests`
- [ ] `python -m coverage run -m unittest discover -s tests`
- [ ] `python -m coverage report`
- [ ] `python -m forgeloop validate .`
- [ ] `python -m forgeloop doctor .`
- [ ] `python -m forgeloop compat .`
- [ ] `python -m forgeloop index . --check`
- [ ] `python -m forgeloop secrets check .`
- [ ] Package build and isolated wheel smoke test, when packaging changed.

## Risk

- [ ] No real secrets added.
- [ ] Public claims include measured evidence.
- [ ] Optional integrations remain explicit.
- [ ] Docs updated when behaviour changed.
- [ ] GitHub Actions remain pinned to full commit SHAs.

## Capture

Link to capture, solution, decision, or benchmark note if needed.
