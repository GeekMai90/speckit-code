#!/usr/bin/env python3
"""Build a constrained executor prompt from Spec Kit artifacts.

Usage:
  build_executor_prompt.py <feature_dir> [--executor codex|claude] [--task "..."]

- Reads specs/<feature>/{spec.md,plan.md,tasks.md}
- Chooses the next task from tasks.md (or uses --task)
- Emits a single prompt to stdout

This script is intentionally simple: it does not modify files.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("feature_dir", help="Path like specs/001-something")
    ap.add_argument("--executor", default="codex", choices=["codex", "claude"])
    ap.add_argument("--task", default=None, help="Override next-task selection")
    args = ap.parse_args()

    feature_dir = Path(args.feature_dir)
    spec = feature_dir / "spec.md"
    plan = feature_dir / "plan.md"
    tasks = feature_dir / "tasks.md"

    missing = [p for p in (spec, plan, tasks) if not p.exists()]
    if missing:
        raise SystemExit(f"Missing required file(s): {', '.join(str(p) for p in missing)}")

    task_text = args.task
    if not task_text:
        # Import next_task helper via filesystem call to avoid package complexity
        import subprocess
        here = Path(__file__).resolve().parent
        nxt = here / "next_task.py"
        r = subprocess.run(["python3", str(nxt), str(tasks)], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit("No incomplete task found in tasks.md")
        task_text = r.stdout.strip()

    prompt = f"""You are the implementation executor ({args.executor}).

Repo context:
- Feature directory: {feature_dir}
- Source of truth: {spec}, {plan}, {tasks}

HARD CONSTRAINTS:
1) Implement ONLY the task below. Do not add features, refactors, or cleanup unless the task explicitly asks.
2) If the task cannot be completed because spec/plan/tasks are unclear or contradictory, STOP and explain what must be clarified/updated.
3) Keep changes minimal and aligned with the Spec Kit artifacts.
4) After implementation, update {tasks} to mark the task done (and ONLY the relevant task lines).

TASK TO IMPLEMENT (verbatim intent):
{task_text}

REQUIRED OUTPUT:
- Summary of what you did
- List of changed files
- Verification commands you ran (or would run) + expected result
"""

    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
