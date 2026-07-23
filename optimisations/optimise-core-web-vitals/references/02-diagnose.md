# Diagnose — one primary hypothesis

## 1. Pick failing metric

| Symptom | Start ref |
|---------|-----------|
| Slow paint, hero late | `03-lcp.md` |
| Layout jump, footer jump | `04-cls.md` |
| Slow first paint, blocking CSS/JS | `05-fcp-ttfb.md` |
| Sluggish tap/click | `06-inp-tbt.md` |
| Oversized/wrong-format images | `07-images-cache.md` |

Multiple failures? Fix **one** metric per cycle. LCP usually beats CLS when both red in lab.

## 2. LCP — read subparts

From `01-baseline.md` subparts:

| Dominant subpart | Likely cause | Ref |
|------------------|--------------|-----|
| TTFB high | Server, CDN, cache miss, redirects | `05-fcp-ttfb.md` |
| Resource load delay high | LCP not in HTML, lazy, low priority, late discovery | `03-lcp.md` |
| Resource load duration high | Image too large, slow CDN, wrong format | `07-images-cache.md` |
| Element render delay high | JS blocks paint, font block, CSS hides LCP | `03-lcp.md`, `05-fcp-ttfb.md` |

## 3. Generic greps

```bash
# Lazy on above-fold images
rg -n 'loading="lazy"' app/ components/ --glob '*.{tsx,jsx,html}'

# h-auto on sized images (CLS)
rg -n 'h-auto' --glob '*.{tsx,jsx}' | rg -v 'lightbox|modal'

# Render-blocking scripts in head without defer/async
rg -n '<script' app/ --glob '*.{tsx,html}' | rg -v 'defer|async|next/script'

# Dynamic LCP via client-only render
rg -n '"use client"' app/ --glob 'page.tsx'
```

## 4. Rank hypotheses

| # | Hypothesis | Prediction | Test |
|---|------------|------------|------|
| 1 | | If true, subpart X drops | One fix in 03–07 |
| 2 | | | |

Pick **one** primary. Secondary = next cycle after verify.

## 5. Eden fleet footer CLS

If culprit is `<footer>` + stream order → `appendix-eden-footer.md` (not default path).
