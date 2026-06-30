---
name: construct-plan
description: "Bind STRUCTURE; 7-phase workflow: research docs → plan → grill-with-docs → scaffold → human gate → edge cases → verify vs docs; then implement, gates, handoff."
agents:
  - cursor
---

/caveman full

**Repo cockpit:** Read `.cursor/STRUCTURE.md` (dirs, patterns, **Gates**, rules load list) + `.cursor/CONTEXT.md` (terms, invariants). Greenfield → author both first; skills portable; **STRUCTURE wins** on conflict.

**Bind:** One repo root per run; load only `.cursor/rules/*.mdc` (or `.cursorrules`) paths STRUCTURE names. Multi-repo → rerun skill per root.

**Pipeline (order matters; no code until step 5 sign-off):**

1. **Research + document** — Artefact root `docs/feature/<task-slug>/` (STRUCTURE may override path). One `.md` per artefact type as needed — run skill prompts: **`/document-current-state`** (constraints / “ship today”), **`/document-database`** (ER / joins from code; DB truth only via STRUCTURE-approved commands), **`/document-flow`** (sequence or flowchart from code). No invented behaviour; mark inferred edges on diagrams per those skills.

2. **Construct plan** — ≤8 bullets: goal, contracts, files likely touched, risks, links to research files above. STRUCTURE + CONTEXT only for norms; no AGENTS bulk unless STRUCTURE points.

3. **Refine with docs memory** — Ambiguity on scope / authz / contract / UX → **`/grill-with-docs`** (one question at a time; update `.cursor/CONTEXT.md` + `docs/adr/` when decision lands). Do **not** use `/grill-me` for this skill.

4. **Output scaffold (pre-code)** — Literal list: files add/change, public methods or endpoints, data shapes, extension points. Constraints: SOLID, small units, KISS, DRY — short bullets, no essay.

5. **Human review gate** — User runs **`/grill-with-docs`** (or equivalent) until sign-off; terminology reflected in `CONTEXT.md`. Open ambiguity → stop implementation; park with ticket ref if needed.

6. **Edge cases pre-impl** — Expected outcomes vs failure modes; known shortcomings + out-of-scope for stakeholder; no surprise after merge.

7. **Verify vs research** — Checklist: each plan / scaffold line traceable to section or diagram in research `.md`; contradiction → fix doc or plan before code.

**After pipeline green:**

**Execute:** Implement from scaffold; smallest diff; match neighbour files STRUCTURE lists.

**Gates:** Copy-run every command in STRUCTURE **Gates** until green. Fail → paste error + fix + retry.

**Loop:** Diff vs STRUCTURE patterns; still fuzzy → **`/grill-with-docs`** again.

**Handoff:** **Exhaustive** — shipped behaviour, files touched, verify (commands + manual checks); suggest **`/construct-test-plan`** then **`/execute-test-plan`**; risks open, follow-ups (docs, migrations, contract regen if STRUCTURE says), owner questions. **No artificial bullet cap.** Still ambiguous → **`/grill-with-docs`** until closed or parked with ticket ref.

### Optional examples (non-normative)

**Generic file tree (adapt paths to STRUCTURE):**

```text
.cursor/
  STRUCTURE.md    ← dirs, patterns, Gates, which rules to load
  CONTEXT.md      ← product language, invariants
  rules/*.mdc
docs/task/<task-slug>/   ← research outputs this skill expects
src/ or app/      ← entrypoints per STRUCTURE
```
