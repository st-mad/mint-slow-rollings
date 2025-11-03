#!/usr/bin/env zsh
# Setup script for macOS (zsh). Installs system deps (Graphviz via brew), creates a venv, and installs pip deps.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REQUIREMENTS="$ROOT_DIR/requirements.txt"
VENV_DIR="$ROOT_DIR/.venv"

echo "Project root: $ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Please install Python 3 (via Homebrew or from python.org) and re-run."
  exit 1
fi

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew not found. If you want to install system packages with brew, install Homebrew first:
  /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"
  "
  echo "Proceeding without brew. Make sure Graphviz is installed (needed for pygraphviz/pydot)."
else
  echo "Checking Graphviz..."
  if ! brew list graphviz >/dev/null 2>&1; then
    echo "Installing graphviz via brew (may ask for sudo)."
    brew install graphviz
  else
    echo "Graphviz already installed via brew."
  fi
fi

echo "Creating virtualenv at $VENV_DIR (Python 3)"
python3 -m venv "$VENV_DIR"
echo "Activating venv"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

if [ -f "$REQUIREMENTS" ]; then
  echo "Installing pip requirements from $REQUIREMENTS"
  pip install --upgrade pip
  pip install -r "$REQUIREMENTS"
else
  echo "No requirements.txt found at $REQUIREMENTS"
fi

echo "Setup complete. To activate the venv run:"
echo "  source $VENV_DIR/bin/activate"
