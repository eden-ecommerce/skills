# INP + TBT fix

INP target: ≤ 200ms p75 (field). TBT = lab proxy — long main-thread tasks.

## 1. Measure

- Field: CrUX INP, `web-vitals` `onINP`
- Lab: Lighthouse TBT, Performance panel long tasks (>50ms)

## 2. Long tasks — common causes

| Cause | Fix |
|-------|-----|
| Large JS parse/execute | Code-split, defer, `optimise-bundles` |
| Heavy hydration | Server-render static; shrink client tree |
| Third-party scripts | Defer, `async`, load after interaction |
| Main-thread layout | Batch DOM reads/writes; avoid sync layout thrash |
| Event handlers | Debounce; move work off click path |

## 3. Third-party

GTmetrix/Lighthouse → Reduce impact of third-party code.

- Load analytics/chat after `load` or user gesture
- `next/script` `strategy="lazyOnload"` for non-critical
- Self-host if CDN slow

## 4. Hydration (React)

- Smaller client islands — `"use client"` only where needed
- Avoid hydrating invisible below-fold widgets on first paint
- `startTransition` for non-urgent state updates after interaction

## 5. INP vs TBT

TBT green, INP red → field interaction path slow (handler, not load). Profile Interaction in DevTools.

TBT red, INP unknown → fix JS execution first; remeasure lab then field.

## 6. One change

Pick one: defer one script, split one chunk, or move one handler off main path. Remeasure.
