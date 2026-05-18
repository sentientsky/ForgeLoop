# External Secrets Workflow

ForgeLoop keeps real secrets outside the repository.

## 1. Check The Example File

The repo includes `.env.example`.

It lists the keys ForgeLoop may need, but all values are blank.

## 2. Create The External File

Run:

```bash
python -m forgeloop secrets init .
```

ForgeLoop creates a per-repository file outside the project folder.

## 3. Open The External File

Run:

```bash
python -m forgeloop secrets path .
```

Open that path and fill in only the secrets you actually use.

## 4. Check Before Sharing

Run:

```bash
python -m forgeloop secrets check .
python -m forgeloop validate .
```

If a real `.env` file appears inside the repo, validation fails.

## 5. Use GitHub Secrets Later

When ForgeLoop is pushed to GitHub, use GitHub repository or organisation secrets for CI/CD.

Do not copy your local external secrets file into GitHub.

