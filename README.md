# DevSetup

[![CI](https://github.com/DEMOCODE675/CloneCode/actions/workflows/ci.yml/badge.svg)](https://github.com/DEMOCODE675/CloneCode/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

**DevSetup** is a cross-platform command-line tool for getting GitHub projects ready to run. Give it a repository URL or a local project directory and it will identify the technology stack, install dependencies, and report project health with clear Rich-powered output.

```bash
devsetup https://github.com/owner/project
```

## Why DevSetup?

Starting an unfamiliar repository usually means figuring out its language, framework, package manager, install command, and basic health checks by hand. DevSetup turns that first-run workflow into one consistent command while keeping the detection and installation logic modular.

## Features

- Clone and bootstrap a GitHub repository in one command
- Detect project language, framework, and package manager from repository files
- Install dependencies using ecosystem-specific plugin logic
- Run health checks with the `doctor` command
- Scan projects without changing them
- Inspect discovered plugins from the command line
- Keep cache and state data in platform-appropriate user directories
- Extend support with built-in, entry-point, or filesystem plugins
- Run on Python 3.12 and newer

## Supported ecosystems

DevSetup currently includes plugins for:

**Angular · Astro · Django · Express · FastAPI · Flutter · Go · Java · Laravel · NestJS · Next.js · Node.js · PHP · Python · Rails · React · Remix · Ruby · Rust · Spring · Svelte · Vue**

Detection is based on project metadata such as manifests, lock files, source layout, and framework-specific files. When no plugin matches, DevSetup reports the project as unknown instead of guessing.

## Installation

DevSetup is currently installed from a checkout:

```bash
git clone https://github.com/DEMOCODE675/CloneCode.git
cd CloneCode
python -m pip install -e .
```

For development, install the test and quality tools too:

```bash
python -m pip install -e ".[dev]"
```

After installation, the `devsetup` command is available in your environment.

## Quick start

### Clone, install, and validate a repository

```bash
devsetup setup https://github.com/owner/project
```

You can choose a destination explicitly:

```bash
devsetup setup https://github.com/owner/project --destination ~/src/project
```

### Use the short form

Passing a repository URL directly performs the same bootstrap flow:

```bash
devsetup https://github.com/owner/project
```

### Analyze an existing checkout

```bash
devsetup scan /path/to/project
devsetup doctor /path/to/project
```

`scan` reports the detected language, framework, and package manager. `doctor` runs the available health checks without cloning the project.

## Command reference

| Command | Purpose |
| --- | --- |
| `devsetup <repo-url>` | Clone, detect, install, and validate a repository |
| `devsetup setup <repo-url>` | Run the full setup flow with progress output |
| `devsetup clone <repo-url>` | Clone a repository without installing dependencies |
| `devsetup scan [path]` | Detect the stack for a local project |
| `devsetup doctor [path]` | Run health checks for a local project |
| `devsetup plugins` | List discovered plugins |
| `devsetup clean` | Remove DevSetup cache and state directories |
| `devsetup cache clear` | Clear cached DevSetup data |
| `devsetup version` | Print the installed version |

Run `devsetup --help` for the latest command and option details.

## How it works

1. **Clone** — fetch the repository when a URL is provided.
2. **Scan** — collect relevant files while ignoring generated directories and dependency folders.
3. **Detect** — score the available plugins and select the best matching ecosystem.
4. **Install** — run the selected plugin's dependency and SDK checks.
5. **Validate** — display the resulting health checks and the next command to run.

The core package owns orchestration, scanning, configuration, and reporting. Plugins own ecosystem-specific detection and commands, so adding support for a new stack does not require coupling it to the core workflow.

## Development

```bash
python -m pip install -e ".[dev]"
python -m ruff check src tests
python -m mypy src/devsetup
python -m pytest
```

The repository also runs these checks in GitHub Actions for Python 3.12 and 3.13.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup, coding expectations, testing requirements, and plugin guidelines.

## License

No license file is currently included in this repository. Add a license before distributing DevSetup or accepting external contributions under explicit reuse terms.
