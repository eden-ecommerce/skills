---
name: sync-plan
description: "SDLC post-Build reconcile; /ponytail-audit milestone + Gates → diff vs plans → update master checkboxes → tick test-plan; close sub. Use after /review-implementation passes."
agents:
  - cursor
---

/caveman ultra

**Bind:** `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md`. Read slugs from master plan header.

**SDLC:** Reconcile plan truth after Build. Sub-plan execution complete for current slice.

**Input:** green review + git diff + plan artefacts in `docs/feature/<feature>/`.

---

## Phases

### 1. Audit
- apply `/ponytail-audit` — milestone scan; ranked cut list
- run STRUCTURE **Gates** — lint, ts-check, tests per STRUCTURE
- all must pass before sync

### 2. Consolidate reality
- read actual diff vs `{feature}-master-plan.md`
- read vs active `sub-plans/{step}-{task}-sub-plan.md`
- document deviations + why

### 3. Sync master
- rewrite master sections to reflect **actual** impl
- check off completed sub row in Sub-Plan Orchestration
- archive or delete obsolete `sub-plans/{step}-{task}-sub-plan.md` files

### 4. Sync test-plan
- tick automated rows in `test-plans/{step}-{task}-test-plan.md` if tests now exist
- note manual rows still open for human

---

## Branch

- more unchecked subs → `/construct-sub-plan` for next row
- all subs done → `/merge-plan`

---

## Next

Next sub or `/merge-plan`.

---

## Output

Update plan files in place. Append sync note to master:

```md
## Sync Log
### {date} — {step}-{task}
- deviations: ...
- gates: pass
- test-plan: automated N/M; manual open: ...
```
