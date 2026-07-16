---
name: optimise-bundles
description: >-
  Debug and cut next-next-eden route JS via measure, chunk diff, grep,
  import-graph surgery, regression class, fix patterns. Use when CI fails
  firstLoadUncompressedJsBytes, PDP/org route regression, or code-split plan.
  Triggers: optimise bundles, debug bundle size, route chunk graph,
  tree shaking next.js, experimental-analyze, component boundaries bundle.
argument-hint: "<route optional, e.g. /product/[id]>"
---

# Optimise bundles

**Hard scope:** `apps/next-next-eden` or standalone `next-next-eden` only.

**Metric:** `firstLoadUncompressedJsBytes` = every client chunk reachable from route React tree — includes `await import()` targets. Graph surgery, not hope-import.

**Never** edit `scripts/analyse-route-bundles.js` thresholds unless user approve baseline bump.

Load **one** reference per phase. Site facts: `references/next-next-eden.md`.

---

## Workflow

| Step | Reference | Out |
|------|-----------|-----|
| 0 Freeze | `references/01-measure.md` | Copy stats before edit |
| 1 Measure | same | Fail routes, kB vs threshold, siblings |
| 2 Diff | `references/02-chunk-diff.md` | Target-only chunks + sizes |
| 3 Grep | `references/03-chunk-grep.md` | Module names in chunks |
| 4 Trace | `references/04-import-trace.md` | Static import chain |
| 5 Class | `references/05-classify.md` | route \| shared \| dependency |
| 6 Fix | `references/06-fix.md` | Smallest edge cut |
| 7 Verify | `references/07-verify.md` | Remeasure + siblings + ts/lint |

Also check: `references/08-also-check.md` (barrels, sideEffects, dup packages, clean build).

---

## Quick start

```bash
cd apps/next-next-eden   # or standalone next-next-eden root
pnpm run ts-check
pnpm turbo-analyse-ci
```

Chunk diff: `references/02-chunk-diff.md`.

---

## Ask before edit

1. Routes/files change?
2. Expected chunk impact?
3. Permission refactor?

---

## After each fix

1. `pnpm turbo-analyse-ci`
2. Bundle Impact Summary (`references/07-verify.md`)
3. Sibling routes still green
4. `pnpm run ts-check` && `pnpm run lint`
5. `packages/ui` touched → `review-standards`
