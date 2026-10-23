# Software Development Lifecycle

Task brief + PM sign-off = source of truth. Orchestration skills live in `orchestration/` — self-research from brief; no dependency on `documentation/` skills (those are optional user tools).

Plan artefact layout:

```
docs/feature/{feature}/
  {feature}-master-plan.md
  {feature}-delivered-feature-plan.md
  sub-plans/{step}-{task}-sub-plan.md
  test-plans/{step}-{task}-test-plan.md
```

| Phase | Philosophy | Skill | Artefact |
|-------|------------|-------|----------|
| Requirement Analysis | objectives, deliverable phases, prioritise | `/construct-master-plan` | `{feature}-master-plan.md` |
| System Design | input/output matrix, process flows, ambiguity gates | `/construct-master-plan` then `/construct-sub-plan` | master plan, then `sub-plans/{step}-{task}-sub-plan.md` |
| Test Design | unit/integration specs + manual checklist **before Build** (per sub) | `/construct-test-plan` | `test-plans/{step}-{task}-test-plan.md` |
| Implementation | amend plans → Cursor Build + `/ponytail` | human + Agent (sub-plan Build block) | code diff |
| Integration & Testing | run Gates + tick manual rows from test-plan | human | test-plan `[ ]` ticks |
| Post-Build QA | diff review, scope, standards | `/review-implementation` | audit report |
| Reconcile | sync plan truth vs code | `/sync-plan` | updated master + sync log |
| Deployment | ready ack → delivered record + MR | `/merge-plan` | `{feature}-delivered-feature-plan.md`, MR description |
| Maintenance | master + delivered plan in MR; monitor prod | `/merge-plan` + ops | MR overview, Sentry/Vercel/DB |

## Requirement Analysis

* starts with task brief
* optional: [task-refinement-prompt.md](task-refinement-prompt.md) in ChatGPT before `/construct-master-plan`
* outline objectives
* break down into deliverable phases. Each phase names tests that already exist and must still pass
* prioritise subtasks under those phases

## System Design

* `/construct-master-plan` — repo recon, blast radius, one input/output row per combination, current and proposed flow per phase
* human approves the matrix and flows before anything else (`matrix-flow`)
* ambiguities sit at the bottom of the master plan. The user answers each one. The agent restates the choices and waits before writing Decisions (`ambiguity-echo`)
* `/construct-master-plan` then walks one unchecked sub at a time. It writes that sub-plan itself. Cite phase and matrix row ids; do not copy the matrix
* communicate blocks / priorities
* identify edge cases and tests (`/construct-test-plan` per sub)

## Implementation

* write master plan — context (SQL, file refs, sources; no secrets in git)
* `{feature}-master-plan.md` orchestrates phases, the matrix, the flows, and progress checkboxes
* sub plans per priority in `sub-plans/` — Build-ready scaffold
* test plans per sub in `test-plans/`
* manually read + amend plans
* unknowns / gaps → discuss team + `/handoff-plan` → new thread
* plan signed off → **Cursor Build** (`/caveman ultra` + `/ponytail`)
* plan errors → revert Build, rebuild sub plan
* user says the sub is complete → `/construct-master-plan` restates the diff, then writes As built, matrix status, and a Sync Log row on the master, then walks the next sub

## Integration & Testing

* `/construct-test-plan` per sub before Build — `/tdd` specs unbiased by impl
* after Build: run automated tests via STRUCTURE Gates
* tick manual rows in test-plan when verified
* fail → revert + refine master/sub plan

## Deployment

* pnpm Gates — lint, ts-check (per STRUCTURE)
* user acknowledges the feature is complete and ready for deployment
* `/construct-master-plan` writes `{feature}-delivered-feature-plan.md` from the diff: original matrix and diagrams kept, as-shipped matrix and diagrams beside them, then the MR body from that file + all test-plan proofs
* remove incomplete / abandoned plan files

## Maintenance

* master plan stays the planning record. `{feature}-delivered-feature-plan.md` is what shipped. Store both in the MR overview
* post-deploy: Sentry, Vercel, DB error logs

## Thread switch

`/handoff-plan` — copy-paste payload for new chat. Includes `matrix-flow` and `ambiguity-echo` status. An open gate stays open until the user answers it.

## Cursor workflow

See [cursor-plan-mode.md](cursor-plan-mode.md).
