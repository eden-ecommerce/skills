---
name: construct-master-plan
description: "SDLC req analysis + system design; self-research brief vs repo → blast radius → prioritized subs → unknowns; output {feature}-{task}-master-plan.md. Use when starting feature, task brief received, or master plan needed."
agents:
  - cursor
---

/caveman ultra

**Bind:** `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md`. Task brief + PM sign-off = truth. One repo root per run.

**SDLC:** Requirement analysis + system design. **No code. No impl.**

**Artefact path:** `docs/task/<feature-task-slug>/{feature}-{task}-master-plan.md`

**Naming:** derive kebab-case `feature` (product area) + `task` (ticket scope) from brief. Write both slugs in plan header — sub/test skills reuse prefix.

**Input:** user brief. Human may paste prior ChatGPT output from `docs/task-refinement-prompt.md` — read only; do not invoke external skills.

---

## Phases

### 1. Repo recon
- `git status` + `git diff` — what already changed
- grep brief keywords — where code lives
- read neighbour files per STRUCTURE patterns
- map blast radius, shared deps, arch conflicts

### 2. Req extract
- objectives from brief (verbatim where possible)
- scope in / scope out
- acceptance hints, constraints

### 3. Prioritize
- break into logical subtasks
- order by execution priority + deps between subs
- each sub row must name `{subtask}` slug → `{feature}-{subtask}-sub-plan.md`

### 4. System design
- technical limits, platform constraints
- unknowns — block sub-plans until answered
- edge-case **categories** (not full test matrix)
- test categories pointer → `/construct-test-plan` later

### 5. Impact
- migration / rollout risks
- backwards compat concerns
- who to ask for unknowns (role, not person)

---

## Stop gates

- open unknowns → `/handoff-plan`; stop sub-plans
- human OK on master plan before `/construct-sub-plan`

---

## Next

`/construct-sub-plan` — highest-priority unchecked sub row.

---

## Output template

Write file `{feature}-{task}-master-plan.md`:

```md
# {Feature Title}

| Slug | Value |
|------|-------|
| feature | {feature} |
| task | {task} |
| artefact_dir | docs/task/{feature-task-slug}/ |

## Context
<!-- SQL snippets, file paths, env var names — NO secrets -->

## Impact & Blast Radius
<!-- global risks, shared deps, arch conflicts -->

## Research Notes
<!-- files read, grep hits, what inferred vs verified -->

## Sub-Plan Orchestration
- [ ] {subtask-slug} — {one-line description} → `{feature}-{subtask-slug}-sub-plan.md`
- [ ] ...

## Unknowns
<!-- block sub-plans until resolved; who to ask -->

## Test Categories
<!-- unit / integration / manual areas — detail in test-plan -->
```
