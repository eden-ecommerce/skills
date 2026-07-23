# LCP fix

Target: ≤ 2.5s p75. Fix dominant subpart from `02-diagnose.md`.

**One change per cycle.** Remeasure subparts in `08-verify.md`.

## 1. Identify LCP element

DevTools Performance, PSI, or GTmetrix → LCP element selector + URL (if image).

Common: hero `img`, H1 text block, poster image, CSS background image.

## 2. Resource load delay — discover early

LCP resource must be in **initial HTML** for preload scanner.

**Good:**

- `<img src="…" width height fetchpriority="high">` in server HTML
- `<link rel="preload" as="image" href="…" fetchpriority="high">` for CSS bg LCP
- Font preload for text LCP

**Bad:**

- LCP `img` injected by client JS
- `loading="lazy"` on LCP candidate
- `data-src` lazy libs hiding real `src`
- LCP only in external CSS `background-image` without preload

**Fix (pick one):**

- Move LCP image to server-rendered markup
- Remove `loading="lazy"` from LCP element
- Add `fetchpriority="high"` on LCP `img` / preload link
- Preload LCP background image in `<head>`

## 3. Resource load duration — right bytes

See `07-images-cache.md` — `w`, `fit=max`, `auto=format`, `q`.

Next fleet: `next/image` `unoptimized` → CDN params do the work.

## 4. Element render delay — unblock paint

- Defer non-critical JS (`next/script` strategy, `defer`/`async`)
- Inline critical CSS or reduce render-blocking stylesheets
- Avoid hiding LCP until JS hydrates
- `font-display: swap` + preload for text LCP fonts

GTmetrix **Eliminate render-blocking resources** → often `_next/static/…css`. One lever: reduce CSS on route, split, or ensure static shell ships without waiting on dynamic holes.

## 5. TTFB — LCP floor

Slow TTFB → LCP cannot pass. See `05-fcp-ttfb.md`.

Next 16: `cacheComponents: true` + `use cache` on stable shell; dynamic in `Suspense` — [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents).

## 6. Verify subpart moved

After fix: resource load delay should shrink first if discovery fix; duration if size fix. Headline LCP alone insufficient — compare all four subparts.
