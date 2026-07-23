---
name: optimise-core-web-vitals
description: >-
  Measure, diagnose, fix Core Web Vitals on any web app. One change per cycle —
  freeze baseline, hypothesis, smallest fix, remeasure. CLS, LCP, INP, FCP, TTFB,
  TBT. Triggers: core web vitals, CLS, LCP, layout shift, render-blocking, slow
  LCP, GTmetrix, Lighthouse, CrUX, reimplement vitals.
argument-hint: "<URL or route optional>"
---

# Optimise Core Web Vitals

**Scope:** any site — Next.js, React SPA, Lovable. Eden fleet patterns → `references/appendix-eden-footer.md`.

**Method:** measure → isolate → **one fix** → verify → keep or revert. No shotgun.

Load **one** ref per phase. Thresholds: `references/00-thresholds.md`.

---

## Workflow

| Step | Ref | Out |
|------|-----|-----|
| 0 Thresholds | `00-thresholds.md` | Pass bars + links |
| 1 Baseline | `01-baseline.md` | Frozen scores, LCP element, subparts, audit list |
| 2 Diagnose | `02-diagnose.md` | One primary hypothesis |
| 3 Fix | `03`–`07` by metric | **Single small change** |
| 4 Verify | `08-verify.md` | Δ vs baseline; ship or revert |
| 5 Reimplement | `09-reimplement.md` | Plan-mode rebuild when fixes plateau |

Route JS budget → `optimise-bundles` skill. Not here.

---

## Quick start

```bash
# 1. Freeze baseline — 01-baseline.md (URL, tool, throttle, cold/warm)
# 2. Identify failing metric + LCP subparts
# 3. One fix from 03–07
# 4. Remeasure — 08-verify.md (same recipe)
```

---

## One-change rule

1. Record baseline before edit.
2. Change **one** thing.
3. Remeasure same URL, tool, throttle, cache mode.
4. Δ better → keep. Flat/worse → revert, next hypothesis.

Never stack fixes without remeasure between.

---

## Ask before edit

1. Which URL reproduces failure?
2. Failing metric — LCP, CLS, INP, FCP, TTFB?
3. Lab only or CrUX field data too?
4. Stack — Next, CRA, Lovable?

---

## After each fix

1. `08-verify.md` before/after table
2. LCP subparts compared, not headline only
3. Project type-check/lint if code touched
4. Document in PR: hypothesis, change, Δ
