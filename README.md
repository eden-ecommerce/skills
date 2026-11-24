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

Master/sub plan workflow. Artefact root: `docs/feature/<feature>/`.

```
docs/feature/{feature}/
  {feature}-master-plan.md
  {feature}-delivered-feature-plan.md
  sub-plans/{step}-{task}-sub-plan.md
  test-plans/{step}-{task}-test-plan.md
```

| Invoke | When | Output |
|--------|------|--------|
| `/construct-master-plan` | Task brief, next sub, or "sub complete" | `{feature}-master-plan.md`, then the delivered file at the end |
| `/construct-sub-plan` | Expand one prioritized sub, after both master gates are acknowledged | `sub-plans/{step}-{task}-sub-plan.md` |
| `/construct-test-plan` | Before Build — TDD specs + manual checklist (per sub) | `test-plans/{step}-{task}-test-plan.md` |
| `/handoff-plan` | Thread switch, open gate, unknowns | copy-paste HANDOFF block |
| `/review-implementation` | After Build | audit report (`/ponytail-review`) |
| `/sync-plan` | Sub complete | updated master + sync log (`/ponytail-audit`) |
| `/merge-plan` | Optional split of the ready-for-deployment step | `{feature}-delivered-feature-plan.md` + MR description |
| `/vertically-slice-changes` | A change is too large for one review | Stacked pull requests, each with its own test and deploy steps |

Path: [`orchestration/vertically-slice-changes/`](orchestration/vertically-slice-changes/). This skill does not start with `/caveman ultra`. The others do. Build uses `/ponytail` (per sub-plan Build block).

## Blueprint skills

End-to-end implementation playbooks. Invoke directly in Cursor Agent — no SDLC artefact required.

| Invoke | When |
|--------|------|
| `/add-publisher-panel` | New `publisher*` panel across API, hub, UI, Storybook, storefront (`panelProducts`) |

Path: [`blueprints/add-publisher-panel/`](blueprints/add-publisher-panel/). Starts `/caveman ultra`. Wireframe gate before code.

## Optional skills (not orchestration deps)

**Optimisations** (`optimisations/`):

| Invoke | When |
|--------|------|
| `/optimise-bundles` | Route JS budget / `firstLoadUncompressedJsBytes` CI failure |
| `/optimise-core-web-vitals` | CLS, LCP, INP, FCP, TTFB, TBT, layout shift, render-blocking, GTmetrix/Lighthouse/CrUX, reimplement vitals |
| `/core-web-vitals-excellence` | Deploy CWV `.cursorrules` pack to microsites (nextjs or lovable) |

Path: [`rules/core-web-vitals-excellence/`](rules/core-web-vitals-excellence/). Compose: `node rules/core-web-vitals-excellence/scripts/compose-cursorrules.mjs <nextjs|lovable> <repo-path>`.

**Documentation** (`documentation/`): `/document-current-state`, `/document-database`, `/document-flow`, `/generate-changelog`, `/generate-overview`, `/prepare-review`, `/refine-rules`, `/generate-handoff-doc` — invoke separately when needed.

`/prepare-review` — before handing a branch over: diff vs `origin/main`, flag breaking changes and migrations, fill the MR/PR overview (summary, features, test, deploy, revert).

**Design** (`design/`): `/ux-redesign` — propose an incremental or radical redesign of a page, feature or journey before building it.

**Other**: `/generate-changelog` for deploy notes.

## Developer steps

| Step | Where | What |
|------|-------|------|
| 1 | **Slack List** | Paste raw task (`brief`) — no interpretation |
| 2 | **ChatGPT** | [task-refinement-prompt.md](docs/task-refinement-prompt.md) — `TASK_TITLE`, `REPORTED_BY`, `TASK_DESCRIPTION` |
| 3 | **Slack List Thread** | Clarifications → **written sign-off** |
| 4 | **Cursor Plan** | `/caveman ultra` → `/construct-master-plan` |
| 5 | **Human** | Approve matrix and flows; answer ambiguities; confirm the agent's restatement |
| 6 | **Same skill** | Walks the next unchecked sub and stops |
| 7 | **Cursor Build** | Build that sub only |
| 8 | **Human** | Says the sub is complete; confirms the agent's restatement of the diff |
| 9 | **Same skill** | Writes As built, matrix status, and a Sync Log row, then walks the next sub |
| 10 | **Human** | When every sub is checked: Gates green, acknowledge ready for deployment |
| 11 | **Same skill** | Writes the delivered feature plan, then the MR |
| 12 | **Slack + Deploy** | Peer review, staging, production (`deploy`) |

See [cursor-plan-mode.md](docs/cursor-plan-mode.md) and [software-development-lifecycle.md](docs/software-development-lifecycle.md) for detail.

## Target repo setup

Copy [docs/AGENTS.md](docs/AGENTS.md) to repo root as `AGENTS.md`. Maintain `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md` per repo.
