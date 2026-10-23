# Cursor Plan Mode

Plan mode + orchestration skills. See [software-development-lifecycle.md](software-development-lifecycle.md).

## Artefact layout

```
docs/feature/{feature}/
  {feature}-master-plan.md
  {feature}-delivered-feature-plan.md
  sub-plans/{step}-{task}-sub-plan.md
  test-plans/{step}-{task}-test-plan.md
```

`{feature}-delivered-feature-plan.md` is written by `/construct-master-plan` after the user acknowledges the feature is ready for deployment.

## Steps

1. `/caveman ultra`
2. `/construct-master-plan` → `docs/feature/<feature>/{feature}-master-plan.md` (phases, input/output matrix, current + proposed flows, ambiguities)
3. Human gate — approve the matrix and flows (`matrix-flow`)
4. Human gate — answer each ambiguity; agent restates the decisions and waits (`ambiguity-echo`)
5. Stay in `/construct-master-plan`. It walks the first unchecked sub, writes that sub-plan if missing, and stops
6. Build that sub only
7. User says the sub is complete. The same skill restates what the diff shows, then writes As built, matrix status, and a Sync Log row into the master plan
8. It walks the next unchecked sub. Repeat from step 6
9. All subs checked, Gates green, user acknowledges ready for deployment
10. The same skill writes `{feature}-delivered-feature-plan.md` from the diff (original matrix and diagrams kept beside as-shipped), then the MR body

`/construct-sub-plan`, `/construct-test-plan`, `/sync-plan`, and `/merge-plan` are optional splits of the same loop. They are not required when this skill is driving the feature.

## Model hints

| Step | Mode | Model |
|------|------|-------|
| 2–5 | Plan | high (e.g. Sonnet 4.5) |
| 6 | Agent Build | efficiency (e.g. Composer 2.5) |
| 7–10 | Agent or Plan | per preference |

## Thread switch

Open approval gate, unknowns, or context loss → `/handoff-plan` → paste into new chat. The handoff names the open gate. It does not close it.

## Repo files

- `.cursor/STRUCTURE.md` — dirs, patterns, Gates
- `.cursor/CONTEXT.md` — terms, invariants
- `docs/AGENTS.md` — copy into target repo root as `AGENTS.md` template

## Optional (not in pipeline)

- `documentation/` skills — user invokes separately
- `/grill-me`, `/grill-with-docs` — user optional; not required by orchestration
