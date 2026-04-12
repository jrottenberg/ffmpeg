# Agent guidelines

## After every change

Run pre-commit before considering a task done:

```bash
pre-commit run --all-files
```

If a hook auto-fixes files (black, autoflake, isort, end-of-file-fixer, etc.) it will exit non-zero and report "files were modified". Re-run immediately — the second run must pass cleanly with all hooks green before the change is complete.

## What pre-commit enforces

| Hook | What it does |
|------|-------------|
| `flake8` | PEP8 + line length (max 90 chars) |
| `black` | Opinionated Python formatting (auto-fixes) |
| `isort` | Import ordering (auto-fixes) |
| `autoflake` | Removes unused imports/variables (auto-fixes) |
| `trailing-whitespace` | Strips trailing spaces (auto-fixes) |
| `end-of-file-fixer` | Ensures files end with a newline (auto-fixes) |
| `check-ast` | Validates Python syntax |
| `check-yaml` | Validates YAML syntax |
| `Generate Dockerfiles` | Runs `update.py` to regenerate `docker-images/` — confirms the generator is not broken |
