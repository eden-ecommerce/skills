# Baseline — freeze before edit

Copy this block. Same recipe every remeasure.

## Record

```text
URL:
Date:
Tool: Lighthouse | GTmetrix | PSI | Playwright | CrUX
Device: mobile | desktop
Throttle: none | Slow 4G | custom
Cache: cold | warm
Tool version:

LCP:    s  (element: )
CLS:
INP:    ms (field only)
FCP:    s
TTFB:   ms
TBT:    ms (lab)

LCP subparts (ms):
  TTFB:
  resource load delay:
  resource load duration:
  element render delay:

Top audits (impact + name):
1.
2.
3.
```

## Capture steps

### 1. Field first (when available)

- [PageSpeed Insights](https://pagespeed.web.dev/) — CrUX section top
- Search Console → Core Web Vitals
- Prefer URL-level over origin-level

Lab ≠ field. CrUX wins when they disagree.

### 2. Lab — LCP element + subparts

Chrome DevTools → Performance → record load → Insights → LCP breakdown.

Or PSI/Lighthouse → Diagnostics → **Largest Contentful Paint element**.

### 3. Audit list

GTmetrix/Lighthouse: filter by failing metric. Copy High/Med impact rows only.

Example map (LCP 3.3s, CLS 0):

| Audit | Metric |
|-------|--------|
| Eliminate render-blocking resources | FCP, LCP |
| Reduce unused JavaScript | LCP |
| Properly size images | LCP |
| Reduce initial server response time | FCP, LCP |

### 4. HTML stream order (CLS suspect)

```bash
curl -s "https://<host>/<route>" | python3 -c "
import sys
html = sys.stdin.read()
for needle in ['min-h-dvh', 'aria-busy', '<footer', 'loading=']:
    print(needle, html.find(needle))
"
```

Footer/chrome before main shell → CLS risk. See `04-cls.md`, `appendix-eden-footer.md`.

## Freeze rule

No code edit until baseline block filled. Stale baseline → re-freeze after deploy.
