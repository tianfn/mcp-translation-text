#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-.env}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

if [[ -f "${ENV_FILE}" ]]; then
  echo "Loading environment variables from ${ENV_FILE}"
  grep -vE '^\s*(#|$)' "${ENV_FILE}" | while IFS='=' read -r name value; do
    if [[ -n "${name}" ]]; then
      export "${name}"="${value}"
    fi
  done
fi

if [[ ! -d .venv ]]; then
  echo "Creating uv virtual environment..."
  uv venv
fi

echo "Installing project dependencies..."
uv pip install -e .

echo "Starting MCP translation server..."
uv run python server.py
