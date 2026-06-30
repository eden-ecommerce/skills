# Cursor Plan Mode

Plan mode + orchestration skills. See [software-development-lifecycle.md](software-development-lifecycle.md).

## Steps

1. `/caveman ultra`
2. `/construct-master-plan` → `docs/task/<feature-task-slug>/{feature}-{task}-master-plan.md`
3. `/construct-sub-plan` per prioritized unchecked sub → `{feature}-{subtask}-sub-plan.md`
4. `/construct-test-plan` → `{feature}-{task}-test-plan.md`
5. Human read + amend all plans
6. **Build** (Agent) — sub-plan Build block: `/caveman ultra` + `/ponytail`
7. `/review-implementation` — `/ponytail-review` on diff
8. `/sync-plan` — `/ponytail-audit` milestone; update master
9. more subs? → step 3. else → `/merge-plan`
10. Tick manual test-plan rows; run Gates until green

## Model hints

| Step | Mode | Model |
|------|------|-------|
| 2–4 | Plan | high (e.g. Sonnet 4.5) |
| 6 | Agent Build | efficiency (e.g. Composer 2.5) |
| 7–9 | Agent or Plan | per preference |

## Thread switch

Unknowns or context loss → `/handoff-plan` → paste into new chat.

## Repo files

- `.cursor/STRUCTURE.md` — dirs, patterns, Gates
- `.cursor/CONTEXT.md` — terms, invariants
- `docs/AGENTS.md` — copy into target repo root as `AGENTS.md` template

## Optional (not in pipeline)

- `documentation/` skills — user invokes separately
- `/grill-me`, `/grill-with-docs` — user optional; not required by orchestration
