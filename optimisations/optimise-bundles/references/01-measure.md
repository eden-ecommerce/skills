# 01 — Measure

App root: `apps/next-next-eden` or standalone `next-next-eden`.

```bash
pnpm run ts-check
pnpm turbo-analyse-ci
```

## Freeze baseline

Before any edit, copy:

- `.next/diagnostics/route-bundle-stats.json`
- Failing route kB + threshold + %

Stale numbers? Clean `.next` then re-run analyse.

## Read output

- `❌` / `✅` per route — kB + % vs frozen threshold
- Script: `scripts/analyse-route-bundles.js` — fail if **>2% above** or **>2% below**

## Record

- Target route
- Measured kB / threshold kB / delta %
- Sibling guard: `/home`, `/o/*` (or same-layout peers)

## Manifest

`.next/diagnostics/route-bundle-stats.json`

```json
{
  "route": "/product/[id]",
  "firstLoadUncompressedJsBytes": 1756096,
  "firstLoadChunkPaths": [".next/static/chunks/....js"]
}
```

## Module edges

Same build:

```bash
pnpm next experimental-analyze --output
```

Inspect: `.next/diagnostics/analyze/data/<route-segment>/analyze.data`

Use when chunk list not enough — need package/module edges.
