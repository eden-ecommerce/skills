---
name: document-database
description: "Trace code to tables/joins; output ER mermaid; DB truth only via user-approved commands in STRUCTURE."
agents:
  - cursor
---

/caveman full

**Repo cockpit:** `.cursor/STRUCTURE.md` (ORM layout, container + `SHOW CREATE` / introspection recipe) + `.cursor/CONTEXT.md` (bounded context names).

**Bind:** STRUCTURE for ORM layout + **how** to run `SHOW CREATE` / introspection (container, user, ssl flag).

1. From entry file: list queries (ORM, SQL, repos).
2. Follow to models; collect table + join keys.
3. Closure or time-box; mark unresolved edges.
4. **Iteration rules** — if STRUCTURE documents special result-set API (e.g. no `foreach` on driver handle), note in legend.

**Output:** `erDiagram` or flowchart; dashed = inferred; open questions for DBA — **complete** for traced scope.

Read-only unless user approves writes.
