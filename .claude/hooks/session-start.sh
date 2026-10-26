#!/bin/bash
# Installs the graphify CLI in Claude Code cloud sessions so the /graphify skill
# and the graphify hook-guard hooks work there. Pinned to the reviewed version.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

GRAPHIFY_VERSION="0.9.92"

if [ "$(graphify --version 2>/dev/null)" != "graphify $GRAPHIFY_VERSION" ]; then
  if command -v uv >/dev/null 2>&1; then
    uv tool install --force "graphifyy==$GRAPHIFY_VERSION"
  else
    python3 -m pip install --user "graphifyy==$GRAPHIFY_VERSION"
  fi
fi

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$HOME/.local/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi
