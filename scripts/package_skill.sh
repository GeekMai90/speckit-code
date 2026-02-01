#!/usr/bin/env bash
set -euo pipefail

# One-command packager for this skill.
# Uses uv to supply runtime deps (PyYAML) without requiring global installs.
# Output: ../dist/skills/speckit-code.skill (relative to clawd workspace)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAWD_DIR="$(cd "${ROOT_DIR}/.." && pwd)"

SKILL_DIR="${CLAWD_DIR}/skills/speckit-code"
OUT_DIR="${CLAWD_DIR}/dist/skills"

mkdir -p "${OUT_DIR}"

uv run --with pyyaml python3 \
  /opt/homebrew/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  "${SKILL_DIR}" "${OUT_DIR}"

echo
echo "Packed: ${OUT_DIR}/speckit-code.skill"
