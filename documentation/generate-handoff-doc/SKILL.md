---
name: generate-handoff-doc
description: >-
  Explore a file or a process and write a handoff a developer can trust.
  Rebuild guide, or a process explainer for a master plan. Creds, routes,
  data flow, external IDs. Trigger: handoff doc, rebuild guide, reimplementation,
  generate-handoff-doc, explain this process.
disable-model-invocation: false
---

# generate-handoff-doc

Two modes. The user gives `@file` and a short context, or a master-plan skill names a process.

**Rebuild** (default): greenfield handoff for a new project. Output `docs/{feature}-handoff.md` unless the user says otherwise.

**Process explainer:** how a process works in this codebase, for a master plan. Output `docs/feature/{feature}/references/{topic}-handoff.md`. Use this mode when construct-master-plan asks, or when the user says "explain this process".

Missing scope → one question → otherwise infer from the files.

## Explore

1. Read the `@files`. Follow imports until data, layout, and config are clear.
2. Use parallel exploration when the scope is wide.
3. Trace the backend or CMS in the workspace. Do not guess ids.
4. Grep env var names from the code. Note a missing `.env.example`.

Do not edit plan files. Do not commit unless asked.

## Write only what search misses

Delete anything a developer finds in one file.

- **Routes** — internal path and public URL; cache; proxy or rewrite rules outside the repo
- **Data** — who fetches what; auth on each endpoint
- **Creds** — env name and purpose; server-only or public; OAuth scopes. Never write secret values.
- **External IDs** — Sanity `_id` / `_type`, CMS doc ids, category ids, cache keys
- **SEO** — canonical pattern, metadata source, JSON-LD
- **Tracking** — GTM, Sentry, beacon, Algolia; what is not in the repo
- **Packages** — feature deps and the site shell
- **Process** — actor, input, output, and the branch that changes the outcome. Cite `path:line`.
- **Rebuild checklist** — phased bullets, in rebuild mode only

Use a mermaid diagram, a snippet, or a table when it makes the path clearer. Real code. Paths relative to the repo.

## Example

```
@articles/page.tsx @article/[articleId]/page.tsx
@eden/.../EdenApi.php

Blog pages — greenfield, same Eden API backend.
```
