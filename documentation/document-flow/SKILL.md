---
name: document-flow
description: "Document control flow: sequence or activity mermaid from code + user flow."
agents:
  - cursor
---

/caveman full

**Repo cockpit:** `.cursor/STRUCTURE.md` (entrypoint conventions: HTTP handler, job, click handler) + `.cursor/CONTEXT.md`.

**Bind:** STRUCTURE for entrypoint conventions (HTTP handler, job, click handler).

1. Trace sync call chain to store / queue / outbound HTTP.
2. Mark async boundaries (webhook, worker).
3. Mark authz / validation gates on diagram.

**Output:** `sequenceDiagram` or `flowchart`; mermaid IDs camelCase no spaces. `TODO` node if code missing — no invention. Cover **all** branches called out in scope.
