---
name: handoff-plan
description: "SDLC thread switch; zero-loss copy-paste payload — master/sub/test status, paths, gates, exact next step. Use on unknowns, context loss, or new chat."
agents:
  - cursor
---

/caveman ultra

**Bind:** `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md`. Read all plan artefacts in `docs/feature/<feature>/`.

**SDLC:** Preserve context across thread switch. **No code.**

**Trigger:** unknowns block progress, plan review in new chat, context window full.

---

## Extract

1. **Slugs** — feature, step, task from master header + active sub row
2. **Master status** — `{feature}-master-plan.md` done vs pending subs
3. **Approvals** — `matrix-flow` and `ambiguity-echo` status from the master Approvals table
4. **Active sub** — `sub-plans/{step}-{task}-sub-plan.md` path + Goal one-liner
5. **Test-plan** — `test-plans/{step}-{task}-test-plan.md` approved? manual ticks open?
6. **Architecture** — file paths, DB tables, API routes from plans (no secrets)
7. **Last gates** — pass/fail + command output summary if failed
8. **Next action** — if either approval is not `acknowledged`, the next action is to answer that gate. Else: skill invoke, amend file, or Build

---

## Output

Single copy-paste block only:

```md
## HANDOFF — {feature} / {step}-{task}

### Slugs
- feature: {feature}
- step: {step}
- task: {task}

### Master ({feature}-master-plan.md)
- done: [x] ...
- pending: [ ] ...

### Approvals
- matrix-flow: pending | acknowledged
- ambiguity-echo: pending | acknowledged

### Active Sub (sub-plans/{step}-{task}-sub-plan.md)
- goal: ...
- blocking: none | ...

### Test Plan (test-plans/{step}-{task}-test-plan.md)
- approved: yes/no
- manual open: N rows

### Key Paths
- files: ...
- schema: ...

### Gates
- last run: pass/fail — ...

### NEXT (run this first)
→ {answer gate matrix-flow | answer gate ambiguity-echo | /construct-sub-plan for {step}-{task} | amend {file} | Build from sub-plans/{step}-{task}-sub-plan.md}
```
