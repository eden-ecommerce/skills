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
- reconciled `{feature}-{task}-master-plan.md`
- `{feature}-{task}-test-plan.md` tick summary
- green STRUCTURE **Gates**
- git diff (final)

---

## Phases

### 1. Read truth
- master plan = source for Summary + Architecture
- test-plan Pass Criteria + ticked rows = Verification Proof
- diff confirms files match master Research Notes

### 2. Cleanup note
- list abandoned `{feature}-{subtask}-sub-plan.md` files removed
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
<!-- from test-plan: automated pass, manual ticks, gates run -->

## Maintenance
<!-- Sentry, Vercel, DB CPU, alerts — from master Impact -->

## Plan Artefacts
- master: docs/task/{feature-task-slug}/{feature}-{task}-master-plan.md
- abandoned plans removed: ...
```

Post-merge: master plan content lives in MR overview per SDLC Maintenance phase.
