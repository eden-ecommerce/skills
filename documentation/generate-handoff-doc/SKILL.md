---
name: generate-handoff-doc
description: >-
  Explore @file scope → write greenfield rebuild handoff for dev in new project.
  Creds, SEO, tracking, external IDs, data flow. Trigger: handoff doc, rebuild
  guide, reimplementation, generate-handoff-doc.
disable-model-invocation: true
---

# generate-handoff-doc

Handoff doc to developer rebuilding in **brand new project**.

User gives `@file` + short context. You explore. You write. No rigid template.

## Input

- `@file` — pages, layouts, API, config (whatever anchors scope)
- context — what feature, what's in/out, optional output path
- default output: `docs/{feature}-handoff.md`

Missing scope → one ask → else infer from files.

## Goal

Dev with zero repo context can: install deps, set creds, call right APIs, match public URLs, skip traps.

## How to work

1. Read `@files` → follow imports until data + layout + config clear
2. Explore parallel if wide (pages + API + analytics separate)
3. Trace backend/CMS if in workspace — don't guess IDs
4. Grep env vars from code; note if `.env.example` missing
5. Write handoff md. Don't edit plan files. Don't commit unless asked.

**No fixed section order.** Structure what you find. Shorter beats longer.

## Must capture (short notes each)

Only stuff easy to miss in code search:

| Area | What to note |
|------|----------------|
| **Pages** | internal route vs public URL; ISR/cache |
| **Infra traps** | proxy/worker/rewrite outside repo; slug parsing rules |
| **Data** | who fetches what; auth on each endpoint |
| **Creds** | env var name → purpose; server-only vs public; OAuth scopes |
| **External IDs** | Sanity `_id`/`_type`, CMS doc IDs, category/dept IDs, memcache keys — whatever system uses fixed IDs |
| **SEO** | canonical pattern, metadata source, JSON-LD types |
| **Tracking** | GTM/Sentry/beacon/Algolia/etc — page-level vs layout chrome; env vars; no blog-specific events? say so |
| **Packages** | required for feature vs site shell only |
| **Rebuild checklist** | phased bullets — dev ticks off |

Delete anything dev finds by reading one file. Keep tribe secrets.

## Diagrams + snippets

Use when they clarify — not mandatory count.

- mermaid: UI flow, fetch sequence, cache invalidation chain
- snippets: `.env.local` minimum, `next.config` traps, API shape, GROQ/query, URL helper

Real code from repo. Repo-relative paths.

## Style

- concise. fragments OK.
- tables OK for env/IDs/routes — keep rows tight
- no filler intro. no "this document aims to..."
- separate **feature** vs **site chrome** (header analytics ≠ page analytics)

## Done when

- creds list complete for scoped feature
- public URL ≠ internal route explicit if they differ
- fixed external IDs written down (prod/dev if both exist)
- SEO + tracking noted (including what's NOT in repo — e.g. GA4 in GTM only)
- dev can start greenfield without asking "where's the API?"

## Trigger

handoff doc · rebuild handoff · greenfield reimplementation · developer rebuilding in new project · `/generate-handoff-doc`

## Invoke eg

```
@articles/page.tsx @article/[articleId]/page.tsx
@eden/.../EdenApi.php

Blog pages — greenfield, same Eden API backend.
```
