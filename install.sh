#!/usr/bin/env bash
# DevSetup macOS & Linux One-Line Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/DEMOCODE675/CloneCode/v2/install.sh | bash

set -e

REPO_URL="git+https://github.com/DEMOCODE675/CloneCode.git@v2"
INSTALL_BASE="${HOME}/.devsetup"
BIN_DIR="${HOME}/.local/bin"

echo -e "\033[36m🐾 Installing DevSetup CLI...\033[0m"

# 1. Try pipx if available
if command -v pipx >/dev/null 2>&1; then
    echo -e "\033[32mFound pipx, installing globally in isolated environment...\033[0m"
    pipx install --force "${REPO_URL}"
    echo -e "\033[32mDevSetup installed successfully via pipx!\033[0m"
    devsetup cat || true
    exit 0
fi

# 2. Try uv if available
if command -v uv >/dev/null 2>&1; then
    echo -e "\033[32mFound uv, installing tool...\033[0m"
    uv tool install --force "${REPO_URL}"
    echo -e "\033[32mDevSetup installed successfully via uv!\033[0m"
    devsetup cat || true
    exit 0
fi

# 3. Check for python3
PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
fi

if [ -z "${PYTHON_CMD}" ]; then
    echo -e "\033[31mError: Python 3.12+ was not found on your system.\033[0m"
    echo "Please install Python 3 from https://www.python.org/ or via your system package manager."
    exit 1
fi

echo -e "\033[36mSetting up isolated DevSetup environment in ${INSTALL_BASE}...\033[0m"
mkdir -p "${INSTALL_BASE}"
VENV_DIR="${INSTALL_BASE}/venv"
${PYTHON_CMD} -m venv "${VENV_DIR}"

VENV_PYTHON="${VENV_DIR}/bin/python"
VENV_DEVSETUP="${VENV_DIR}/bin/devsetup"

echo -e "\033[36mInstalling latest DevSetup CLI from repository...\033[0m"
"${VENV_PYTHON}" -m pip install --quiet --upgrade pip
"${VENV_PYTHON}" -m pip install --quiet --upgrade "${REPO_URL}"

mkdir -p "${BIN_DIR}"
ln -sf "${VENV_DEVSETUP}" "${BIN_DIR}/devsetup"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":${BIN_DIR}:"* ]]; then
    echo -e "\033[33mNote: ${BIN_DIR} is not in your current PATH.\033[0m"
    echo "Add the following line to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo -e "\n\033[32m✨ DevSetup is installed and ready to use!\033[0m\n"
"${VENV_DEVSETUP}" cat || true

