# ForgeLoop Technical Steering

ForgeLoop is a dependency-light Python package.

Use the Python standard library unless a dependency removes real complexity.

Important commands:

```bash
python -m unittest discover -s tests
python -m forgeloop validate .
python -m forgeloop compat .
python -m forgeloop index . --check
python -m forgeloop secrets check .
```

Token work uses pointer packets first:

```bash
python -m forgeloop pack "<task query>" . --limit 5
python -m forgeloop tokens "<task query>" . --tool kiro --limit 5
```

Security priorities:

- no real `.env` files in the repository
- no symlinked repository files
- no active hooks by default
- no public savings claims without measured reports
