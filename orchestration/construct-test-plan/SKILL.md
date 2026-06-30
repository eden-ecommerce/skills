---
name: construct-test-plan
description: "SDLC test design pre-Build; edge cases + /tdd specs (no impl bias) + manual tick checklist; output test-plans/{step}-{task}-test-plan.md per sub. Use before Cursor Build when test plan missing or stale."
agents:
  - cursor
---

/caveman ultra

**Bind:** `.cursor/STRUCTURE.md` + `.cursor/CONTEXT.md`. Read slugs from master plan header + active sub-plan.

**SDLC:** Test design **before Build** — unbiased by impl code or diff. **One test-plan per sub-plan.**

**Artefact path:** `docs/feature/<feature>/test-plans/{step}-{task}-test-plan.md`

**Input:** brief + `{feature}-master-plan.md` + active `sub-plans/{step}-{task}-sub-plan.md`.

**Do not:** read impl diff, open production files written for this task, invoke execute-test skill.

---

## Phases

### 1. Edge cases
- 5+ non-obvious cases: nulls, race, auth fail, timeout, abuse, double-submit, refresh, back nav
- tie each to master Impact + sub-plan Goal

### 2. /tdd bind
- unit + integration **specs only**
- columns: file path | `describe`/`it` | assertion intent | red-first?
- no production code — specs describe expected behaviour from **plan**, not from existing impl

### 3. Manual matrix
- UI / flow steps human ticks after Build
- columns: step_id | action | expected | `[ ]`

### 4. Human gate
- approve test-plan before Build
- gaps → amend sub-plan or master; do not Build until aligned

---

## Stop gates

- human approves test-plan
- open test gaps vs sub-plan scaffold → amend plans first

---

## Next

Human amend all plans → Cursor Build (`/caveman ultra` + `/ponytail` per sub-plan Build block).

User runs automated tests via Gates during/after Build; ticks manual `[ ]` rows when verified.

---

## Output template

Write file `test-plans/{step}-{task}-test-plan.md`:

```md
# Test Plan — {step}-{task}

| Slug | Value |
|------|-------|
| feature | {feature} |
| step | {step} |
| task | {task} |
| master | {feature}-master-plan.md |
| sub | sub-plans/{step}-{task}-sub-plan.md |

## Edge Cases
1. ...
2. ...

## Automated Tests (/tdd specs)
| File | describe/it | Assertion intent | Red-first |
|------|-------------|------------------|-----------|
| ... | ... | ... | yes |

## Manual Checklist
| step_id | action | expected | pass |
|---------|--------|----------|------|
| 1 | ... | ... | [ ] |

## Pass Criteria (for merge-plan)
<!-- summary bullets for Verification Proof section -->
```
