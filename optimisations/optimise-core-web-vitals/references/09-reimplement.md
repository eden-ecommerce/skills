# Reimplement — same content, perfect vitals

When incremental one-change cycles plateau (2+ hypotheses reverted or <5% gain): **Plan mode** — no Agent shotgun rebuild.

## Trigger

- LCP still Poor after 3 verified cycles on same route
- Architecture blocks fixes (full CSR page, footer stream race, monolithic client bundle)
- User asks "rebuild for vitals"

## Plan output (required before code)

### 1. Content inventory

- Routes, copy, images, metadata, schema.org, OG tags
- CMS fields, API deps
- Third-party scripts

### 2. Rendering model (per route)

| Route | Model | Why |
|-------|-------|-----|
| | static shell + Suspense holes | SEO + LCP in HTML |
| | SSR | personalised |
| | CSR only | justify |

Next: `cacheComponents` + `use cache` on stable chrome; dynamic data in smallest `Suspense` boundary — [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents).

### 3. Vitals checklist (all must pass plan review)

- [ ] LCP element in server HTML; `fetchpriority="high"`; no lazy
- [ ] Images: CDN `w` + `auto=format` + reserved dimensions
- [ ] `loading.tsx` / skeleton mirrors final layout (`min-h-dvh` minimum)
- [ ] Footer/chrome after main content in stream order
- [ ] Render-blocking CSS/JS minimised per route
- [ ] Cache-Control: HTML `no-cache`, hashed assets `immutable`
- [ ] Metadata + Open Graph + JSON-LD on server
- [ ] Link `aria-label` / visible text; image `alt` on all content images
- [ ] Client islands minimal — `"use client"` only for interaction
- [ ] Verify recipe from `08-verify.md` attached to plan

### 4. Verify plan

- Baseline URL frozen
- Target metrics per route
- Playwright script + PSI run after each sub-phase

### 5. Build gate

Human approves plan → Build in subs (one metric or route per sub) → `/optimise-core-web-vitals` verify each sub.

Align with `docs/cursor-plan-mode.md` orchestration when feature-sized.

## Do not

- Rewrite entire app in one Agent session
- Change content/copy unless user asks
- Skip baseline remeasure between subs
