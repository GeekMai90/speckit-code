---
name: speckit-code
description: Spec-Driven Development (GitHub Spec Kit) workflow + executor guardrails. Use when starting or running a complex coding project and you want to enforce a spec→plan→tasks workflow in the repo (Spec Kit directory structure) before implementing. Also use when you must drive implementation via an execution agent (default: Codex CLI; optional: Claude Code) that is only allowed to work against tasks.md and must write results back.
---

# Speckit Code

Enforce **GitHub Spec Kit / Spec-Driven Development (SDD)** in a repo, then use an **executor CLI** (default: **Codex CLI**) to implement strictly from `tasks.md`.

## Operating rules (non-negotiable)

1) **No executor run before `tasks.md` exists.**
2) Executor scope is **only** what is in the current feature’s `tasks.md` (plus referenced plan/spec/contracts).
3) After each task, write back:
   - task status (done/blocked)
   - files changed
   - how to verify (commands + expected outcome)
   - any spec/plan drift (if drift: stop and update spec/plan first)

## Default directory structure (Spec Kit-compatible)

- `.specify/` (templates/scripts/memory)
- Agent command files (one of): `.codex/commands/`, `.claude/commands/`, `.github/agents/`, etc.
- `specs/<feature>/` (feature artifacts)
  - `spec.md`
  - `plan.md`
  - `tasks.md`
  - optional: `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

## Workflow (SDD → executor)

### Step 0 — Bootstrap Spec Kit into the repo

In the target repo root:

- Install Specify CLI (recommended):
  ```bash
  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
  ```
- Initialize Spec Kit templates for your agent:
  ```bash
  specify init --here --ai codex
  # or
  specify init --here --ai claude
  ```

If updating an existing repo, use `--force` (but **back up** `.specify/memory/constitution.md` first).

Helper: `scripts/bootstrap_spec_kit.sh`.

### Step 1 — Constitution (project governing principles)

Run:
- `/speckit.constitution …`

Output lives at: `.specify/memory/constitution.md`

### Step 2 — Specify (WHAT/WHY)

Run:
- `/speckit.specify …`

Rule: stay at requirements level; avoid tech stack.

### Step 3 — Plan (HOW)

Run:
- `/speckit.plan …`

Rule: plan must be readable; push deep details into `implementation-details/` (if used).

### Step 4 — Tasks (executable task list)

Run:
- `/speckit.tasks`

Hard gate: do not implement until `tasks.md` exists and is actionable.

### Step 5 — Implement via executor (default: Codex CLI)

Hard gate: do not implement until `specs/<feature>/tasks.md` exists and is actionable.

#### Pick next task
```bash
python3 skills/speckit-code/scripts/next_task.py specs/<feature>/tasks.md
```

#### Build a constrained executor prompt
```bash
python3 skills/speckit-code/scripts/build_executor_prompt.py specs/<feature>
```

#### Run Codex CLI executor (recommended: OpenClaw background + PTY)
From the **repo root** (must be a git repo):
```bash
bash pty:true workdir:/path/to/repo background:true command:"./skills/speckit-code/scripts/run_codex_executor.sh specs/<feature>"
```

(If you are running manually in a terminal: `./skills/speckit-code/scripts/run_codex_executor.sh specs/<feature>`)

#### Executor selection
- default executor: **Codex CLI**
- optional executor: **Claude Code** only when explicitly requested

## Troubleshooting & safety

- If executor output suggests changes not covered by spec/plan/tasks: **stop**, update artifacts first.
- If repo is non-git or branch detection fails: set `SPECIFY_FEATURE=<feature-dir>` before planning steps.

## Bundled resources

- `scripts/bootstrap_spec_kit.sh`: bootstrap/upgrade helper
- `scripts/next_task.py`: extract the next incomplete task from tasks.md
