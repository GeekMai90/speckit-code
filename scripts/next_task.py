#!/usr/bin/env python3
"""Extract the next incomplete task from a Spec Kit tasks.md.

Goal: deterministic helper for an executor loop.

Heuristics:
- Prefer GitHub-style checkboxes: - [ ] ...
- If none found, fall back to first list item starting with '-' that is not marked done.

Output:
- Prints the task line (trimmed). Exit code 0 if found, 2 if not.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


CHECKBOX_TODO = re.compile(r"^\s*[-*]\s+\[\s\]\s+(.*\S)\s*$")
CHECKBOX_DONE = re.compile(r"^\s*[-*]\s+\[[xX]\]\s+")
BULLET = re.compile(r"^\s*[-*]\s+(.*\S)\s*$")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: next_task.py <path/to/tasks.md>", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    # 1) checkbox todos
    for line in lines:
        m = CHECKBOX_TODO.match(line)
        if m:
            print(m.group(1).strip())
            return 0

    # 2) fallback bullets that aren't obviously done
    for line in lines:
        if CHECKBOX_DONE.match(line):
            continue
        m = BULLET.match(line)
        if m:
            text = m.group(1).strip()
            # skip headings/empty-ish bullets
            if text and not text.startswith("#"):
                print(text)
                return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
