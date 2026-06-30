---
name: construct-sub-plan
description: "SDLC subtask design; one master sub row → self-research repo → Build-ready scaffold + TDD outline; output {feature}-{subtask}-sub-plan.md. Use when expanding prioritized sub from master plan."
agents:
  - cursor
---

/caveman ultra

**Bind:** `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md`. Read `{feature}-{task}-master-plan.md` from artefact dir in master header.

**SDLC:** Subtask refinement → **Build-ready plan**. **No code.**

**Artefact path:** `docs/task/<feature-task-slug>/{feature}-{subtask}-sub-plan.md`

**Input:** one unchecked row from master Sub-Plan Orchestration — read `feature` slug + `{subtask}` slug from row.

---

## Phases

### 1. Scope lock
- this sub only — cite master Context + Impact
- explicit out-of-scope for this sub

### 2. Repo drill
- read exact files to touch (open them)
- note patterns from STRUCTURE — match neighbour style

### 3. Step-by-step strategy
- ordered impl steps — smallest diff posture
- deps on other subs explicit

### 4. Scaffold (Build-ready)
- files add / change (paths)
- public APIs, endpoints, exports
- data shapes, types
- extension points — no speculative layers

### 5. TDD outline
- test file paths
- `describe` / `it` names + assertion intent
- red-first — **no production code**, no impl bias

### 6. Done criteria
- STRUCTURE **Gates** (`pnpm lint`, `pnpm ts-check`, etc.)
- manual smoke bullets

### 7. Ambiguities
- list now
- blocking → stop; `/handoff-plan`

---

## Stop gates

- blocking ambiguity → stop before Build
- human amend plan → Cursor Build

---

## Next

`/construct-test-plan` if `{feature}-{task}-test-plan.md` missing or stale.
Else human amend → **Build**.

---

## Output template

Write file `{feature}-{subtask}-sub-plan.md`:

```md
# {Subtask Title}

| Slug | Value |
|------|-------|
| feature | {feature} |
| subtask | {subtask} |
| master | {feature}-{task}-master-plan.md |

## Goal
<!-- one paragraph -->

## Steps
1. ...
2. ...

## Files
| Action | Path | Notes |
|--------|------|-------|
| change | ... | ... |

## Scaffold
<!-- APIs, shapes, contracts — Build agent reads this -->

## Tests to Write
| File | describe/it | Assertion intent |
|------|-------------|------------------|
| ... | ... | ... |

## Done Criteria
- [ ] Gates green: ...
- [ ] Manual smoke: ...

## Ambiguities
<!-- empty if none -->

## Build
- Mode: Cursor Build (Agent)
- Skills: /caveman ultra + /ponytail
- Input: this sub-plan only; no scope creep vs master-plan
```
