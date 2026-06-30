# Cursor skills

Each target repo needs `.cursor/STRUCTURE.md` and `.cursor/CONTEXT.md`. Task brief + PM sign-off = source of truth.

## Install

```bash
npx skills@latest add eden-ecommerce/skills -a cursor --global --skill '*' -y
npx skills@latest add mattpocock/skills -a cursor --global --skill '*' -y
npx skills@latest add JuliusBrussee/caveman -a cursor --global --skill '*' -y
npx skills@latest add DietrichGebert/ponytail -a cursor --global --skill '*' -y
```

Choose **Global** when prompted. Reload Cursor (`Ctrl+Shift+P` → **Developer: Reload Window**).

## Docs (human reference)

| File | Purpose |
|------|---------|
| [docs/software-development-lifecycle.md](docs/software-development-lifecycle.md) | SDLC philosophy + skill mapping |
| [docs/cursor-plan-mode.md](docs/cursor-plan-mode.md) | Plan → Build → review workflow |
| [docs/task-refinement-prompt.md](docs/task-refinement-prompt.md) | ChatGPT task interrogation (step 2) |
| [docs/AGENTS.md](docs/AGENTS.md) | `AGENTS.md` template for target repos |

## Orchestration skills

Master/sub plan workflow. Plan files: `{feature}-{task}-{plan-type}-plan.md` in `docs/task/<feature-task-slug>/`.

| Invoke | When | Output |
|--------|------|--------|
| `/construct-master-plan` | Task brief received | `{feature}-{task}-master-plan.md` |
| `/construct-sub-plan` | Expand one prioritized sub | `{feature}-{subtask}-sub-plan.md` |
| `/construct-test-plan` | Before Build — TDD specs + manual checklist | `{feature}-{task}-test-plan.md` |
| `/handoff-plan` | Thread switch, unknowns | copy-paste HANDOFF block |
| `/review-implementation` | After Build | audit report (`/ponytail-review`) |
| `/sync-plan` | Sub complete | updated master + sync log (`/ponytail-audit`) |
| `/merge-plan` | All subs done | MR description |

All orchestration skills start `/caveman ultra`. Build uses `/ponytail` (per sub-plan Build block).

## Optional skills (not orchestration deps)

**Documentation** (`documentation/`): `/document-current-state`, `/document-database`, `/document-flow`, `/generate-changelog`, `/refine-rules`, `/generate-handoff-doc` — invoke separately when needed.

**Other**: `/generate-changelog` for deploy notes.

## Developer steps

| Step | Where | What |
|------|-------|------|
| 1 | **Slack List** | Paste raw task (`brief`) — no interpretation |
| 2 | **ChatGPT** | [task-refinement-prompt.md](docs/task-refinement-prompt.md) — `TASK_TITLE`, `REPORTED_BY`, `TASK_DESCRIPTION` |
| 3 | **Slack List Thread** | Clarifications → **written sign-off** |
| 4 | **Cursor Plan** | `/caveman ultra` → `/construct-master-plan` |
| 5 | **Cursor Plan** | `/construct-sub-plan` per prioritized sub |
| 6 | **Cursor Plan** | `/construct-test-plan` |
| 7 | **Human** | Read + amend plans in `docs/task/<feature-task-slug>/` |
| 8 | **Cursor Build** | Agent + `/ponytail` from sub-plan Build block |
| 9 | **Cursor Agent** | `/review-implementation` → `/sync-plan` |
| 10 | **Human** | Tick manual test-plan rows; Gates green |
| 11 | **Cursor** | `/merge-plan` when all subs synced |
| 12 | **Slack + Deploy** | Peer review, staging, production (`deploy`) |

See [cursor-plan-mode.md](docs/cursor-plan-mode.md) and [software-development-lifecycle.md](docs/software-development-lifecycle.md) for detail.

## Target repo setup

Copy [docs/AGENTS.md](docs/AGENTS.md) to repo root as `AGENTS.md`. Maintain `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md` per repo.
