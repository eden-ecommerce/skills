# FCP + TTFB fix

Diagnostics for LCP floor and first paint. Target: FCP ≤ 1.8s, TTFB ≤ 800ms (PSI).

## TTFB high

Causes: slow origin, redirects, no CDN, cache miss, cold serverless, geo latency.

**Checks:**

```bash
curl -sI "https://<host>/<route>" | rg -i 'cache-control|x-vercel-cache|age|cf-cache-status'
```

**Fixes (one per cycle):**

- Static/ISR shell — HTML cacheable at edge
- Reduce redirects (one hop max)
- `cacheComponents` / static generation for public routes (Next)
- Warm serverless / edge region
- CDN in front of origin

TTFB is LCP floor — fix before image tweaks if TTFB > ~40% of LCP.

## FCP high (TTFB OK)

Large delta TTFB → FCP = render-blocking assets.

**Audits:** Eliminate render-blocking resources.

**Fixes:**

- Defer/async non-critical JS
- Critical CSS inline or split per route
- Remove unused CSS from initial bundle
- Preconnect to CDN/font origins:

```html
<link rel="preconnect" href="https://cdn.sanity.io" crossorigin>
```

## Cache-Control

| Asset | Header |
|-------|--------|
| HTML document | `Cache-Control: no-cache` — revalidate, never stale shell |
| Hashed JS/CSS | `public, max-age=31536000, immutable` |
| Images (CDN) | long TTL at CDN; version via URL params |

Sources: [MDN Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control), [web.dev love-your-cache](https://web.dev/articles/love-your-cache).

Never `immutable` on HTML — users stuck on old asset hashes.

## FCP vs LCP gap

FCP fast, LCP slow → LCP resource late or low priority. → `03-lcp.md`.

FCP and LCP both slow, TTFB OK → blocking CSS/JS. Fix render-blocking first.
