# 08 — Also check

Gaps step 1–7 miss. Run when class unclear or fix weak.

| Check | Why | How |
|-------|-----|-----|
| **Metric scope** | CI = client JS graph only | Ignore image/CSS/font bytes for this fail |
| **Clean build** | Cache lie | Delete `.next`, re-run `turbo-analyse-ci` |
| **Barrel files** | `index.ts` re-export pulls siblings | Import leaf path, not barrel |
| **sideEffects** | Side-effect import keeps module | Drop unused CSS/polyfill imports; check package `sideEffects` |
| **Dup packages** | Two versions same lib | Analyse / lockfile; dedupe |
| **Wrong entry** | CJS / full build of dep | Prefer `exports` ESM; check `transpilePackages` |
| **Package attribution** | Know which npm owns bytes | `experimental-analyze` edges / chunk grep package strings |
| **Global providers** | Shared class masquerades as route | Diff many routes; inspect root layout |
| **Third-party scripts** | Outside chunk metric or inflate client | `next/script` / analytics audit separate |

Not in scope here: LCP, SSR HTML weight, network waterfalls — different playbook.
