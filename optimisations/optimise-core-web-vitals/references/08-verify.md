# Verify — objective compare

Target: same recipe as `01-baseline.md`. One fix → remeasure → table.

## Before/after table (required)

| Metric | Before | After | Δ | Keep? |
|--------|--------|-------|---|-------|
| LCP (ms) | | | | |
| CLS | | | | |
| FCP (ms) | | | | |
| TTFB (ms) | | | | |
| TBT (ms) | | | | |
| INP (ms) | | | field | |

LCP subparts:

| Subpart | Before | After | Δ |
|---------|--------|-------|---|
| TTFB | | | |
| Resource delay | | | |
| Resource duration | | | |
| Render delay | | | |

**Keep** if primary metric improved ≥5% or crossed Good threshold. **Revert** if flat or worse.

## Playwright — CLS + LCP

```bash
node - <<'NODE'
const { chromium } = require('@playwright/test');

const URL = process.env.CWV_URL || 'http://localhost:3000/';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.addInitScript(() => {
    window.__cwv = { cls: 0, lcp: null, clsEntries: [] };
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) {
        if (e.hadRecentInput) continue;
        window.__cwv.cls += e.value;
        const n = e.sources?.[0]?.node;
        window.__cwv.clsEntries.push({
          value: +e.value.toFixed(4),
          tag: n?.tagName,
          text: n?.innerText?.slice(0, 60),
        });
      }
    }).observe({ type: 'layout-shift', buffered: true });

    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const last = entries[entries.length - 1];
      if (last) window.__cwv.lcp = Math.round(last.startTime);
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  });

  await page.goto(URL, { waitUntil: 'networkidle', timeout: 120000 });
  await page.waitForTimeout(3000);
  console.log(await page.evaluate(() => window.__cwv));
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
NODE
```

Throttle (optional, before `goto`):

```js
const client = await page.context().newCDPSession(page);
await client.send('Network.emulateNetworkConditions', {
  offline: false, latency: 150, downloadThroughput: 1.5 * 1024 * 1024 / 8,
  uploadThroughput: 750 * 1024 / 8,
});
```

## web-vitals (optional)

```js
import { onCLS, onLCP, onINP } from 'web-vitals';
onLCP(console.log);
onCLS(console.log);
onINP(console.log);
```

## Lab tools

- PSI/Lighthouse — filter audits to failing metric only
- GTmetrix — same URL, same location, compare History
- CrUX — field truth; lab confirms direction

## Pass criteria

| Check | Pass |
|-------|------|
| CLS | < 0.1 |
| LCP | < 2500ms (lab) or CrUX Good |
| Primary hypothesis | Subpart moved in right direction |
| Regression | No other Core metric crossed to Poor |
| Type-check | Clean if code touched |

Document hypothesis + change + table in PR.

## Stream order (CLS)

```bash
curl -s "$URL" | python3 -c "
import sys
html = sys.stdin.read()
for n in ['min-h-dvh', 'aria-busy', '<footer']:
    print(n, html.find(n))
"
```

Loading shell index < footer index.
