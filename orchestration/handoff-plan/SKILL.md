---
name: handoff-plan
description: "SDLC thread switch; zero-loss copy-paste payload — master/sub/test status, paths, gates, exact next step. Use on unknowns, context loss, or new chat."
agents:
  - cursor
---

/caveman ultra

**Bind:** `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md`. Read all plan artefacts in `docs/task/<feature-task-slug>/`.

**SDLC:** Preserve context across thread switch. **No code.**

**Trigger:** unknowns block progress, plan review in new chat, context window full.

---

## Extract

1. **Slugs** — feature, task, subtask from master header
2. **Master status** — `{feature}-{task}-master-plan.md` done vs pending subs
3. **Active sub** — `{feature}-{subtask}-sub-plan.md` path + Goal one-liner
4. **Test-plan** — `{feature}-{task}-test-plan.md` approved? manual ticks open?
5. **Architecture** — file paths, DB tables, API routes from plans (no secrets)
6. **Last gates** — pass/fail + command output summary if failed
7. **Next action** — exact step: skill invoke, amend file, or Build

---

## Output

Single copy-paste block only:

```md
## HANDOFF — {feature}-{task}

### Slugs
- feature: {feature}
- task: {task}
- active_subtask: {subtask}

### Master ({feature}-{task}-master-plan.md)
- done: [x] ...
- pending: [ ] ...

### Active Sub ({feature}-{subtask}-sub-plan.md)
- goal: ...
- blocking: none | ...

### Test Plan ({feature}-{task}-test-plan.md)
- approved: yes/no
- manual open: N rows

### Key Paths
- files: ...
- schema: ...

### Gates
- last run: pass/fail — ...

### NEXT (run this first)
→ {exact command: e.g. /construct-sub-plan for {subtask} | amend {file} | Build from {sub-plan path}}
```
