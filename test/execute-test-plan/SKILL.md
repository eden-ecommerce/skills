---
name: execute-test-plan
description: "Run construct-test-plan rows: Cursor browser tab + MCP or manual; actual vs expected, severity, proposed fix, owner."
agents:
  - cursor
---

/caveman full

**Repo cockpit:** `.cursor/STRUCTURE.md` (base URL, browser policy) + `.cursor/CONTEXT.md`.

**Bind:** Input = markdown / file from **`test/construct-test-plan`** (same task scope). Base URL from STRUCTURE or user.

**Output:** One table row **per** checklist row (happy path, abuse, responsive). Columns:

`step_id` | `action` | `expected` | `actual` | `pass_fail` | `severity` | `proposed_fix` | `owner`

- **step_id** — stable id or row index from plan.
- **proposed_fix** — concrete change or ticket ref; empty only if pass.
- **owner** — who fixes or `—` if pass.

**Browser (UI steps):**

**Cursor browser tab** — Cursor ships **Browser** (Simple Browser / agent browser tab). Agent may drive live UI there via **browser MCP** when enabled — same session user sees; no separate test runner required.

1. Write **expected** UI state per step before click (from plan).
2. Browser MCP against that tab: navigate → snapshot → act → snapshot (MCP server lock/snapshot rules).
3. Fill table row: **actual** vs **expected**; **severity** if fail.
4. Abuse cases after happy path (STRUCTURE minimum count; default double submit, refresh, back).

**Blockers** (login, captcha, missing env) — blocker row; **stop**; no fake creds.

**No browser** — same table; `actual` empty; `pass_fail` pending; human fills.
