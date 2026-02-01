#!/usr/bin/env bash
set -euo pipefail

# Run Codex CLI as the executor for the next task in a Spec Kit feature.
#
# Usage:
#   ./run_codex_executor.sh specs/001-my-feature
#
# Notes:
# - Must be run inside a git repo (Codex requirement).
# - Prefer running this via OpenClaw exec with pty:true + background:true for long tasks.

FEATURE_DIR="${1:?feature_dir required (e.g., specs/001-my-feature)}"

PROMPT=$(python3 "$(dirname "$0")/build_executor_prompt.py" "$FEATURE_DIR" --executor codex)

# --full-auto keeps it non-interactive for typical edits (still PTY recommended)
codex exec --full-auto "$PROMPT"
