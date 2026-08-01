# DevSetup

DevSetup is a cross-platform CLI for bootstrapping GitHub projects with one command.

```bash
devsetup https://github.com/user/project
```

It scans the repository, detects the language, framework, and package manager, then runs the install and health-check flow with Rich progress output.

## Highlights

- Python 3.12+
- Typer CLI with Rich output
- Plugin-driven architecture
- Detects package managers from manifests and lock files
- Ready for external plugins through entry points

## Install

```bash
pip install -e .[dev]
```

## Commands

- `devsetup <repo-url>` or `devsetup setup <repo-url>`
- `devsetup clone <repo-url>`
- `devsetup scan [path]`
- `devsetup doctor [path]`
- `devsetup plugins`
- `devsetup clean`
- `devsetup cache clear`
- `devsetup version`

## Development

Run the checks locally:

```bash
ruff check src tests
mypy src/devsetup
pytest
```

See [docs/Architecture.md](docs/Architecture.md) and [docs/CreatingPlugin.md](docs/CreatingPlugin.md) for the extension model.