---
name: generate-handoff-doc
description: >-
  Explore @file scope → write greenfield rebuild handoff for dev in new project.
  Creds, SEO, tracking, external IDs, data flow. Trigger: handoff doc, rebuild
  guide, reimplementation, generate-handoff-doc.
disable-model-invocation: true
---

# generate-handoff-doc

Greenfield rebuild handoff. User gives `@file` + short context. Explore. Write. No rigid template.

**Output:** `docs/{feature}-handoff.md` unless user says otherwise.

Missing scope → one ask → else infer from files.

## Explore

1. Read `@files` → follow imports until data, layout, config are clear
2. Parallel explore if scope is wide
3. Trace backend/CMS in workspace — don't guess IDs
4. Grep env vars from code; note if `.env.example` missing

Don't edit plan files. Don't commit unless asked.

## Write only tribe secrets

Stuff easy to miss in code search. Delete anything dev finds in one file.

- **Routes** — internal path vs public URL; ISR/cache; proxy/rewrite rules outside repo
- **Data** — who fetches what; auth per endpoint
- **Creds** — env name → purpose; server-only vs public; OAuth scopes
- **External IDs** — Sanity `_id`/`_type`, CMS doc IDs, category/dept IDs, memcache keys
- **SEO** — canonical pattern, metadata source, JSON-LD
- **Tracking** — GTM/Sentry/beacon/Algolia; page vs layout chrome; env vars; what's NOT in repo
- **Packages** — feature deps vs site shell
- **Rebuild checklist** — phased bullets dev can tick off

Mermaid/snippets/tables when they clarify. Real code, repo-relative paths.

## Eg

```
@articles/page.tsx @article/[articleId]/page.tsx
@eden/.../EdenApi.php

Blog pages — greenfield, same Eden API backend.
```
