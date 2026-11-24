---
name: handoff-plan
description: "Copy-paste handoff when a thread switches. Master, active sub, ready gate, and the next command. Use on context loss or a new chat. No code."
agents:
  - cursor
---

**No code.** Read the plan files in `docs/feature/<feature>/`. Read the **Repos** row for the active sub before naming gates.

## Extract

1. Feature, home repo, and the first unchecked **Subs** row.
2. `ready` from **Approvals**.
3. The first unchecked `## Sub` heading, its outcome, and `Needs`.
4. That sub's Tests table: manual rows still open.
5. **Deviations** rows.
6. Key paths from that sub's Files table. No secrets.
7. Last Sync Log line.

## Output

One block:

```md
## HANDOFF — {feature} / {step}-{repo}-{task}

### Master
- file: docs/feature/{feature}/{feature}-master-plan.md
- ready: pending | {date}
- pending subs: 02, 03

### Active sub
- heading: ## Sub {step}
- outcome:
- needs:
- rules:

### Tests
- manual open: N

### Deviations
- rows: none | ids

### Gates
- last run:

### NEXT
→ {finish construct-master-plan | Build via implement-plan | /merge-plan | /vertically-slice-changes on step NN}
```

The next command is Build when `ready` is a date and a sub is still open. It is `/merge-plan` when every sub is built and gates passed. It is finish planning when `ready` is pending.
