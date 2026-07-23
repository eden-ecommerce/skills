# CWV thresholds

p75 field data, 28-day window. Pass = all three Core metrics Good.

## Core (ranking)

| Metric | Good | Needs improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| INP | ≤ 200ms | 200–500ms | > 500ms |
| CLS | ≤ 0.1 | 0.1–0.25 | > 0.25 |

## Diagnostic (not Core — guide fixes)

| Metric | Good | Role |
|--------|------|------|
| FCP | ≤ 1.8s | Render-blocking, first paint |
| TTFB | ≤ 800ms | LCP floor — slow server caps LCP |
| TBT | lab only | Long tasks proxy for INP |

## LCP subparts (relative)

| Subpart | Target share |
|---------|--------------|
| TTFB | ~40% |
| Resource load delay | <10% |
| Resource load duration | ~40% |
| Element render delay | <10% |

Large delay subparts = fix before chasing image bytes.

## Sources

- [web.dev/vitals](https://web.dev/articles/vitals)
- [PageSpeed Insights thresholds](https://developers.google.com/speed/docs/insights/v5/about)
- [Optimize LCP](https://web.dev/articles/optimize-lcp)
