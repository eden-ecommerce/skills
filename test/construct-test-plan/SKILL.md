---
name: construct-test-plan
description: "Manual QA plan: matrix, personas, abuse, regression, sign-off, viewport/UI shell rows; browser steps get expected state before action."
agents:
  - cursor
---

/caveman full

**Repo cockpit:** `.cursor/STRUCTURE.md` (output path e.g. `docs/qa/`, environments, roles, **viewport widths**, **theme switch procedure**, base URL if UI) + `.cursor/CONTEXT.md`.

**Bind:** STRUCTURE for checklist output path + viewport list + theme procedure + base URL when UI in scope.

**Sections (complete for scope; no `…` placeholders):**

- Scope / out-of-scope
- Personas + roles
- Data matrix (empty, huge, unicode, slow network)
- **Ordered steps + expected** — each row = observable outcome, not “works”
- **Browser steps (UI in scope)** — per row: **expected UI state before click/action**; step written for later MCP run (navigate → snapshot → act → snapshot). Include **action** column intent in step text where helpful.
- **Abuse** — double submit, refresh, back (STRUCTURE may add minimum count); same expected-before-action rule if browser
- **Regression list**
- **Responsive + UI shell** — bind STRUCTURE viewports (default mental model: mobile / tablet / desktop; add **wide** if STRUCTURE says tables / wide grids). Per viewport rows or sub-matrix for: **horizontal + vertical overflow**; **touch targets** (min size / spacing); **theme switch** (light/dark if app has); **skeleton vs layout jump** after load; **error copy** visible + correct; **deep link refresh** (URL → same state). Each cell outcome observable; `N/A` + reason only when truly not applicable.
- Sign-off line

**Output (responsive block):** Markdown table — `area` | `viewport` | `pass/fail` | `notes` — **all** cells filled for scope.

**Rule:** Every checklist row = observable outcome.
