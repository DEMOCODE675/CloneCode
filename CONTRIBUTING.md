# Contributing to DevSetup

Thanks for contributing.

## Local setup

```bash
pip install -e .[dev]
pre-commit install
```

## Expectations

- Keep modules small and focused.
- Add or update tests for behavior changes.
- Prefer typed interfaces and dependency injection.
- Keep plugin logic inside plugin modules, not the core package.

## Workflow

1. Add or modify the smallest relevant module.
2. Run `ruff check src tests`, `mypy src/devsetup`, and `pytest`.
3. Update docs if the CLI or plugin contract changes.

## Plugin rules

- Every plugin must implement the shared `Plugin` interface.
- New ecosystems should be added as a new folder under `src/devsetup/plugins/`.
- Avoid hardcoding package-manager behavior in the core package.