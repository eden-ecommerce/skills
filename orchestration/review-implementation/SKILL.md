---
name: review-implementation
description: "SDLC post-Build QA gate; /ponytail-review on diff + plan scope check + Gates + AGENTS standards; audit report before sync. Use after Cursor Build, before /sync-plan."
agents:
  - cursor
---

/caveman ultra

**Bind:** `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md` + `docs/AGENTS.md` (repo copy if present).

**SDLC:** Post-Build quality gate — pre-sync. **No auto-fix** unless user asks.

**Input:** git diff + `{feature}-master-plan.md` + active `sub-plans/{step}-{task}-sub-plan.md`.

---

## Phases

### 1. /ponytail-review
- apply `/ponytail-review` on current diff
- one line per finding: `L<n>: <tag> <what>. <replacement>.`
- tags: delete, stdlib, native, yagni, shrink
- end: `net: -<N> lines possible.` or `Lean already. Ship.`

### 2. Scope check
- diff vs master + sub-plan — flag scope creep, unrelated files
- every changed file traceable to sub-plan Files table?

### 3. Gates + security
- run STRUCTURE **Gates** (`pnpm lint`, `pnpm ts-check`, etc.) — must pass
- scan diff for hardcoded secrets, tokens, credentials

### 4. AGENTS standards
- GB English spelling (`colour`, `organise`, `behaviour`)
- naming: descriptive, concise (`getUserServer` not `getUsrSrv`)
- KISS, DRY — no new abstractions without need

### 5. Atomic components (UI changes)
- 1 file = 1 responsibility
- guard clauses: early return for loading/error before main return
- reject: components inside render methods; nested ternaries in final return
- fix path: extract conditional UI to own component file

---

## Stop gates

- Gates fail → list fixes; no `/sync-plan` until green
- ponytail-review findings with severity → refactor list

---

## Next

`/sync-plan` when audit passes.

---

## Output template

```md
# Review — {step}-{task}

## Ponytail Review
<!-- one-line findings -->

## Scope
- [ ] matches sub-plan
- creep: ...

## Gates
- lint: pass/fail
- ts-check: pass/fail

## Security
- secrets: none found / FLAG: ...

## Standards
<!-- GB English, naming, atomic UI issues -->

## Required Refactors
<!-- empty if ship-ready -->
```
