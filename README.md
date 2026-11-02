# DevSetup 🐾

DevSetup is a universal, cross-platform CLI for bootstrapping GitHub projects with one command.

```text
# ------------------------------------------------------------------------
# ........................................................................
# .........................      /\_____/\      ..........................
# ........................     /  /\   /\  \     .........................
# ......................    (   (o)   (o)   )     '.......................
# ................... \  / .. (  (*)  .  (*)  ) .. \  /...................
# .................. ===  ... (     .w.     ) ...  === ...................
# .................. /  \ .... \           / .... /  \ ...................
# ........................    /     | |     \    .........................
# ........................   |      | |      |   .........................
# ........................   |    ( | | )    |   .........................
# ........................   (____( | | )____)   .........................
# ........................................................................
# ............[ DevSetup Universal Environment Bootstrapper ].............
# ------------------------------------------------------------------------
```

---

## 🚀 Quick Run (No Clone or Setup Needed!)

You can run `devsetup` immediately in your terminal without cloning or saving any files:

### Run ephemerally (like `npx`):
```bash
# Using uv (fastest):
uvx --from git+https://github.com/DEMOCODE675/CloneCode.git@v2 devsetup

# Or using pipx:
pipx run --spec git+https://github.com/DEMOCODE675/CloneCode.git@v2 devsetup
```

---

## 📦 One-Line Global Install

Install `devsetup` permanently to your system with a single command:

### Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/DEMOCODE675/CloneCode/v2/install.ps1 | iex
```

### macOS & Linux:
```bash
curl -fsSL https://raw.githubusercontent.com/DEMOCODE675/CloneCode/v2/install.sh | bash
```

### Via `pipx` or `pip`:
```bash
pipx install git+https://github.com/DEMOCODE675/CloneCode.git@v2
# or
pip install git+https://github.com/DEMOCODE675/CloneCode.git@v2
```

Once installed, just type:
```bash
devsetup
```

---

## 💻 Usage

```bash
devsetup setup https://github.com/user/project
```

It scans the repository, detects the language, framework, and package manager, then runs the install and health-check flow with Rich progress output.

### Clone only
```bash
devsetup clone https://github.com/user/project
```

### Scan a project
```bash
devsetup scan .
```

### Run diagnostics
```bash
devsetup doctor .
```

### Show mascot cat banner
```bash
devsetup cat
# Or modern card style:
devsetup banner --style card
```

### List installed plugins
```bash
devsetup plugins
```

### Clear cache
```bash
devsetup cache clear
```

### Clean generated files
```bash
devsetup clean
```

### Show version
```bash
devsetup version
```

---

## ✨ Highlights

- Python 3.12+
- Typer CLI with Rich output & cute mascot cat terminal splash screen
- Universal one-line installer for Windows, macOS, and Linux
- Plugin-driven architecture
- Automatic package manager and framework detection

---

## 🛠️ Development

To develop locally:

```bash
git clone https://github.com/DEMOCODE675/CloneCode.git
cd CloneCode
pip install -e .[dev]
```

Run checks:
```bash
ruff check src tests
pytest
```
