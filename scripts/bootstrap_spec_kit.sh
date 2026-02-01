#!/usr/bin/env bash
set -euo pipefail

# Bootstraps GitHub Spec Kit (Specify CLI + templates) into the current repo.
# Usage:
#   ./bootstrap_spec_kit.sh codex
#   ./bootstrap_spec_kit.sh claude

AI_AGENT="${1:-codex}"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found. Install uv first: https://docs.astral.sh/uv/" >&2
  exit 1
fi

echo "Installing/upgrading specify-cli via uv tool…"
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git

echo "Bootstrapping Spec Kit templates for agent: ${AI_AGENT}"
specify init --here --ai "${AI_AGENT}"

echo "Done. Next: run your agent and use /speckit.constitution → /speckit.specify → /speckit.plan → /speckit.tasks"
