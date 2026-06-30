# Software Development Lifecycle

Task brief + PM sign-off = source of truth. Orchestration skills live in `orchestration/` — self-research from brief; no dependency on `documentation/` skills (those are optional user tools).

Plan artefact layout:

```
docs/feature/{feature}/
  {feature}-master-plan.md
  sub-plans/{step}-{task}-sub-plan.md
  test-plans/{step}-{task}-test-plan.md
```

| Phase | Philosophy | Skill | Artefact |
|-------|------------|-------|----------|
| Requirement Analysis | objectives, subtasks, prioritise | `/construct-master-plan` | `{feature}-master-plan.md` |
| System Design | research, unknowns, edge cases, test categories | `/construct-master-plan` + `/construct-sub-plan` | `sub-plans/{step}-{task}-sub-plan.md` |
| Test Design | unit/integration specs + manual checklist **before Build** (per sub) | `/construct-test-plan` | `test-plans/{step}-{task}-test-plan.md` |
| Implementation | amend plans → Cursor Build + `/ponytail` | human + Agent (sub-plan Build block) | code diff |
| Integration & Testing | run Gates + tick manual rows from test-plan | human | test-plan `[ ]` ticks |
| Post-Build QA | diff review, scope, standards | `/review-implementation` | audit report |
| Reconcile | sync plan truth vs code | `/sync-plan` | updated master + sync log |
| Deployment | MR + gates | `/merge-plan` | MR description |
| Maintenance | master up to date in MR; monitor prod | `/merge-plan` + ops | MR overview, Sentry/Vercel/DB |

## Requirement Analysis

* starts with task brief
* optional: [task-refinement-prompt.md](task-refinement-prompt.md) in ChatGPT before `/construct-master-plan`
* outline objectives
* break down into subtasks
* prioritise subtasks

## System Design

* `/construct-master-plan` — repo recon, blast radius, unknowns from brief
* `/construct-sub-plan` — per sub: files, scaffold, TDD outline, Build block
* ask people for unknowns / technical info
* communicate blocks / priorities
* identify edge cases and tests (`/construct-test-plan` per sub)

## Implementation

* write master plan — context (SQL, file refs, sources; no secrets in git)
* `{feature}-master-plan.md` orchestrates sub plans + progress checkboxes
* sub plans per priority in `sub-plans/` — Build-ready scaffold
* test plans per sub in `test-plans/`
* manually read + amend plans
* unknowns / gaps → discuss team + `/handoff-plan` → new thread
* plan signed off → **Cursor Build** (`/caveman ultra` + `/ponytail`)
* plan errors → revert Build, rebuild sub plan
* sub complete → `/sync-plan` → feed back to master

## Integration & Testing

* `/construct-test-plan` per sub before Build — `/tdd` specs unbiased by impl
* after Build: run automated tests via STRUCTURE Gates
* tick manual rows in test-plan when verified
* fail → revert + refine master/sub plan

## Deployment

* pnpm Gates — lint, ts-check (per STRUCTURE)
* `/merge-plan` — MR body from master + all test-plan proofs
* remove incomplete / abandoned plan files

## Maintenance

* master plan reflects actual code — store in MR overview
* post-deploy: Sentry, Vercel, DB error logs

## Thread switch

`/handoff-plan` — copy-paste payload for new chat.

## Cursor workflow

See [cursor-plan-mode.md](cursor-plan-mode.md).
