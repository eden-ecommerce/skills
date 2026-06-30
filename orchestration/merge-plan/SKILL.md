---
name: merge-plan
description: "SDLC deployment; reconciled master + test-plan ticks + Gates → MR description with verification proof + maintenance targets. Use when all subs synced."
agents:
  - cursor
---

/caveman ultra

**Bind:** `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md`.

**SDLC:** Deployment / merge request. All subs checked off in master.

**Input:**
- reconciled `{feature}-master-plan.md`
- all `test-plans/{step}-{task}-test-plan.md` tick summaries
- green STRUCTURE **Gates**
- git diff (final)

---

## Phases

### 1. Read truth
- master plan = source for Summary + Architecture
- aggregate Pass Criteria + ticked rows from all test-plans = Verification Proof
- diff confirms files match master Research Notes

### 2. Cleanup note
- list abandoned `sub-plans/{step}-{task}-sub-plan.md` files removed
- list obsolete `test-plans/{step}-{task}-test-plan.md` files removed
- incomplete plans deleted from artefact dir

### 3. Write MR body
- raw markdown — paste to Git platform

---

## Output template

```md
## Summary
<!-- 2-3 sentences from master Goal + Context -->

## Architectural Changes
<!-- bullets: structural updates, DB, API — from master + diff -->

## Verification Proof
<!-- from all test-plans: automated pass, manual ticks, gates run -->

## Maintenance
<!-- Sentry, Vercel, DB CPU, alerts — from master Impact -->

## Plan Artefacts
- master: docs/feature/{feature}/{feature}-master-plan.md
- sub-plans: docs/feature/{feature}/sub-plans/
- test-plans: docs/feature/{feature}/test-plans/
- abandoned plans removed: ...
```

Post-merge: master plan content lives in MR overview per SDLC Maintenance phase.
