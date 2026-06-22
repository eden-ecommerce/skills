---
name: review-worker-proxy
description: >-
  Review v0/Next app for Cloudflare Worker reverse-proxy prod readiness. User supplies
  public route root and upstream origin. Quant audit, scored issues, phased plan split
  app vs worker vs infra. Use when user says review-worker-proxy, review v0 project
  for worker deploy, proxy readiness, or namespace sub-site behind CF Worker.
---

/caveman ultra

# Review worker proxy

Goal: **user defines route map** → **count** blockers → **score** → **phase plan** → split **APP** / **WORKER** / **INFRA**.

## Trigger

`/review-worker-proxy` or user ask: review v0 for worker deploy, proxy readiness, safe to proxy, prod gate.

## Step 0 — User intake (BLOCK until filled)

**No audit, no grep, no plan until route profile complete.**

Use `AskQuestion` when available; else ask in chat. **Do not invent** URLs — user must supply.

### Required fields

| Field | Key | What to ask | Example (events only) |
|-------|-----|-------------|-------------------------|
| App repo root | `APP_ROOT` | Path to Next/Vercel app | `eden-ecommerce/events` |
| Public route root | `PUBLIC_ROUTE_ROOT` | Full URL users hit via Worker | `https://www.eden.co.uk/events` |
| Upstream origin | `UPSTREAM_ORIGIN` | Bare deploy host (no path) | `https://events-snowy-phi.vercel.app` |
| Path mapping | `PATH_MAP` | How Worker rewrites path | `preserve` / `strip` / `root` |

### Derived (compute from answers; confirm with user)

```
PUBLIC_HOST     = host(PUBLIC_ROUTE_ROOT)           # www.eden.co.uk
ROUTE_PREFIX    = pathname(PUBLIC_ROUTE_ROOT)       # /events  ("" if root mount)
UPSTREAM_HOST   = host(UPSTREAM_ORIGIN)             # events-snowy-phi.vercel.app

# preserve (most common): path unchanged end-to-end
UPSTREAM_ROUTE_ROOT = UPSTREAM_ORIGIN + ROUTE_PREFIX
  → https://events-snowy-phi.vercel.app/events

# strip: public /foo → upstream /foo (prefix removed)
UPSTREAM_ROUTE_ROOT = UPSTREAM_ORIGIN

# root: public prefix maps to upstream /
UPSTREAM_ROUTE_ROOT = UPSTREAM_ORIGIN + "/"
```

**Confirm mapping in one line before scan:**

> `PUBLIC_ROUTE_ROOT` → Worker → `UPSTREAM_ROUTE_ROOT` (`PATH_MAP`)

### Optional fields (ask; defaults ok)

| Field | Key | Default |
|-------|-----|---------|
| Worker repo root | `WORKER_ROOT` | ask or search workspace |
| Worker match rule | `WORKER_MATCH` | unknown until worker repo read |
| Asset prefix in code | `ASSET_PREFIX_VAR` | grep `assetPrefix` / `ASSET_*_URL` |
| Namespace const in code | `NS_CONST` | grep `NAMESPACE_PATH` / `ROUTE_PREFIX` |
| Package manager | `PKG` | `pnpm` / `npm` / `yarn` from lockfile |
| Auth cookie names | `AUTH_COOKIES` | user list e.g. `PHPSESSID,csrft` |
| Login + session check URLs | `AUTH_FLOW` | user paths for E2E |
| Plan output path | `PLAN_OUT` | `<APP_ROOT>/docs/deployment-readiness-plan.md` |

### Path mapping modes

| Mode | Public request | Upstream request |
|------|----------------|------------------|
| **preserve** | `{PUBLIC_ROUTE_ROOT}/page` | `{UPSTREAM_ORIGIN}{ROUTE_PREFIX}/page` |
| **strip** | `{PUBLIC_ROUTE_ROOT}/page` | `{UPSTREAM_ORIGIN}/page` |
| **root** | `{PUBLIC_ROUTE_ROOT}/page` | `{UPSTREAM_ORIGIN}/page` (app mounted at `/`) |

App `assetPrefix` / link prefix must match **public** URL (`PUBLIC_ROUTE_ROOT`), not bare `UPSTREAM_ORIGIN`.

### Intake template (paste in plan doc header)

```markdown
## Route profile (user-supplied)

| Key | Value |
|-----|-------|
| APP_ROOT | |
| PUBLIC_ROUTE_ROOT | |
| UPSTREAM_ORIGIN | |
| UPSTREAM_ROUTE_ROOT | |
| PATH_MAP | preserve \| strip \| root |
| WORKER_ROOT | |
| AUTH_COOKIES | |
| AUTH_FLOW | |
```

**If any required field blank → stop, ask user.**

## Phase 0 — Quant scan (run all; record numbers)

Substitute `<APP_ROOT>`, `<ROUTE_PREFIX>`, `<UPSTREAM_HOST>`, `<PUBLIC_ROUTE_ROOT>`, `<PKG>` from profile.

**Do not guess.** Execute; paste counts in report.

### A. Build & type gate

```bash
cd <APP_ROOT> && <PKG> run ts-check 2>&1 | tail -5
cd <APP_ROOT> && <PKG> run lint 2>&1 | tail -20
cd <APP_ROOT> && <PKG> run build 2>&1 | tail -10
```

Record: `ts_errors`, `lint_errors`, `lint_warnings`, `build_ok`, `ignoreBuildErrors` (y/n).

Verify code constants match profile:

```bash
rg -n 'assetPrefix|ASSET_.*ORIGIN|ASSET_.*URL|NAMESPACE|ROUTE_PREFIX' <APP_ROOT>/lib <APP_ROOT>/next.config.ts 2>/dev/null
```

Flag P1 if prod asset origin ≠ `PUBLIC_ROUTE_ROOT` (trailing slash rules — note both forms).

### B. Deploy-critical URL rules

```bash
# Root-relative asset/link literals (break proxy)
rg -n 'src="/|href="/|url: "/' --glob '*.{tsx,ts,jsx,js}' <APP_ROOT> \
  | rg -v 'NsLink|NAMESPACE|assetUrl|apiUrl|<ROUTE_PREFIX>' | wc -l

# Client fetch /api without route prefix (adjust pattern if ROUTE_PREFIX empty)
rg -n 'fetch\(["\`]/api/' --glob '*.{tsx,ts}' <APP_ROOT> | wc -l

# Cookie minting in app
rg -n 'Set-Cookie|cookies\(\)\.set|document\.cookie\s*=' --glob '*.{tsx,ts}' <APP_ROOT> | wc -l
```

Post-build:

```bash
rg -l 'src="/_next' <APP_ROOT>/.next --glob '*.html' 2>/dev/null | wc -l
rg -c '<UPSTREAM_HOST>' <APP_ROOT>/.next --glob '*.html' 2>/dev/null | awk -F: '{s+=$2} END {print s+0}'
```

Record: `url_literal_hits`, `bad_fetch_api`, `cookie_mint_hits`, `html_root_next`, `html_upstream_origin_leak`.

Expected prod HTML assets: under `PUBLIC_ROUTE_ROOT`, never bare `UPSTREAM_HOST`.

### C. API surface

```bash
find <APP_ROOT>/app -path '*/api/*/route.ts' | wc -l
find <APP_ROOT>/app/api -name 'route.ts' 2>/dev/null | wc -l
```

Namespaced routes — adapt path to `ROUTE_PREFIX`:

```bash
# ROUTE_PREFIX=/events → app/events/api
find <APP_ROOT>/app -path "*<ROUTE_PREFIX_TRIM>/api*" -name 'route.ts' | wc -l
```

(`ROUTE_PREFIX_TRIM` = prefix without leading `/`, e.g. `events`)

Per top-level `app/api/*`: auth? (none / api-key / session). Bare `UPSTREAM_ORIGIN/api/*` = **origin bypass** — not behind Worker public path.

Proxy-facing APIs must resolve to `{PUBLIC_ROUTE_ROOT}/api/*` in client code.

### D. CI vs deploy gate gap

Check `<APP_ROOT>/.github/workflows/*.yml` + `package.json`:

| Gate | CI? | Host build? | predeploy? |
|------|-----|-------------|------------|
| ts-check | | | |
| lint | | | |
| build | | | |
| post-build security grep | | | |
| audit high | | | |
| Playwright vs `PUBLIC_ROUTE_ROOT` | | | |

Score: `ci_gates_n` / 6.

### E. Secrets

```bash
rg -n 'password|api[_-]?key|Bearer |Basic [A-Za-z0-9+/=]{8,}' --glob '*.md' <APP_ROOT> | wc -l
rg -n '@[a-z0-9.-]+:[^@]+@' --glob '*.{md,env*,ts,tsx}' <APP_ROOT> | wc -l
```

Never echo secrets — count + file:line only.

### F. Worker repo (`WORKER_ROOT` if known)

Read routing + proxy fn:

- `PUBLIC_ROUTE_ROOT` / `ROUTE_PREFIX` match rule exists?
- Maps to `UPSTREAM_ORIGIN` / `UPSTREAM_ROUTE_ROOT` per `PATH_MAP`?
- Cookie forward all backends? (y/n)
- `Set-Cookie` rewrite? (y/n)
- Match: `startsWith` vs segment boundary?

Record: `worker_route_confirmed`, `worker_cookie_passthrough`, `worker_path_ambiguity_risk`.

## Phase 1 — Score matrix

| Pri | Meaning |
|-----|---------|
| P0 | Ship blocker — creds in git, unauth mutating API on bare origin |
| P1 | Proxy break — wrong asset prefix, `/_next` leak, route map mismatch |
| P2 | Gate gap — CI red, no post-build grep, no live E2E |
| P3 | Debt — import lint, dead code |

**Required table:**

```markdown
| Category | Count | P0 | P1 | P2 | P3 |
|----------|------:|---:|---:|---:|---:|
| Route map | | | | | |
| URL/asset | | | | | |
| API/origin | | | | | |
| Auth/cookie | | | | | |
| CI/gates | | | | | |
| Secrets | | | | | |
| Worker | | | | | |
| Tests | | | | | |
| **Total** | | | | | |
```

## Phase 2 — Scope split

| Bucket | Ships in |
|--------|----------|
| **APP** | app repo PR |
| **WORKER** | worker repo PR |
| **INFRA** | dashboard / console ticket |

Green app tests ≠ safe worker cookie policy.

## Phase 3 — Iterative plan output

Write `<PLAN_OUT>`. Bullets ≤20 words.

```markdown
# [Project] — worker-proxy readiness plan

## Route profile
[user intake table]

## Quant snapshot
[Phase 1 table]
Scanned: [date]

## Mapping contract
- Public: `PUBLIC_ROUTE_ROOT`
- Upstream: `UPSTREAM_ROUTE_ROOT` (PATH_MAP: …)
- E2E base URL: `PUBLIC_ROUTE_ROOT`

## Sign-off split
- **App:** …
- **Worker:** …
- **Infra:** …

## Phase 1 — Green CI (APP)
- [ ] …

## Phase 2 — Security contract (APP)
- [ ] post-build grep: no `src="/_next`, no `<UPSTREAM_HOST>` in HTML
- [ ] `assetPrefix` / constants = `PUBLIC_ROUTE_ROOT`
- [ ] auth-gate or delete bare `app/api/*`
- [ ] CI: ts-check → lint → build → security-check

## Phase 3 — Proxy E2E (APP)
- [ ] smoke `PUBLIC_ROUTE_ROOT`
- [ ] asset URLs use public prefix not upstream host
- [ ] auth flow per `AUTH_FLOW` + `AUTH_COOKIES` (if user supplied)
- [ ] no `Set-Cookie` for `AUTH_COOKIES` from public path responses
- [ ] dispatch/nightly before `main` gate

## Phase 4 — Worker routing (WORKER)
- [ ] `ROUTE_PREFIX` → `UPSTREAM_ORIGIN` per PATH_MAP
- [ ] path boundary fix if `startsWith` ambiguous
- [ ] cookie / Set-Cookie policy doc or impl

## Phase 5 — Infra (INFRA)
- [ ] deployment protection on `UPSTREAM_ORIGIN`
- [ ] third-party key restrictions
- [ ] rotate leaked creds

## Phase 6 — Prod gate
- [ ] App + Worker + Infra sign-off separate
- [ ] runbook: public URL, upstream, rollback

## Out of scope
…
```

Phase order: 1 → 2 → 3; 4 parallel after 1 green; 6 last.

## Full checklist (all checks; use route profile vars)

Substitute `PUBLIC_ROUTE_ROOT`, `UPSTREAM_ORIGIN`, `ROUTE_PREFIX`, `PATH_MAP`, `UPSTREAM_HOST`, `AUTH_COOKIES`.

### Intake — block if incomplete

| # | Check | Pri if fail |
|---|-------|-------------|
| 0 | User supplied `PUBLIC_ROUTE_ROOT` | stop |
| 0b | User supplied `UPSTREAM_ORIGIN` | stop |
| 0c | `PATH_MAP` confirmed (preserve/strip/root) | stop |
| 0d | `UPSTREAM_ROUTE_ROOT` derived + confirmed | stop |

### APP — route map & assets

| # | Check | Pri if fail |
|---|-------|-------------|
| 1 | `assetPrefix` / asset const = `PUBLIC_ROUTE_ROOT` | P1 |
| 2 | Code namespace matches `ROUTE_PREFIX` | P1 |
| 3 | No `src="/_next` in build HTML | P1 |
| 4 | No `UPSTREAM_HOST` in prod HTML assets | P1 |
| 5 | Links use route prefix not site root | P1 |
| 6 | Client API → `{PUBLIC_ROUTE_ROOT}/api` not bare `/api` | P1 |
| 7 | No app cookie mint for `AUTH_COOKIES` | P0 |

### APP — API origin exposure

| # | Check | Pri if fail |
|---|-------|-------------|
| 8 | Count `app/api/*` (bare origin routes) | info |
| 9 | Unauth mutating route on `UPSTREAM_ORIGIN/api/*` | P0 |
| 10 | Proxy APIs under `app/{prefix}/api/*` or equivalent | P2 |
| 11 | Client `apiUrl()` vs filesystem path alignment | P2 |
| 12 | Public POST rate limits | P2 |

### APP — CI & deploy

| # | Check | Pri if fail |
|---|-------|-------------|
| 13 | ts-check in CI | P2 |
| 14 | lint in CI | P2 |
| 15 | build in CI | P2 |
| 16 | post-build security grep after build | P2 |
| 17 | audit high fail-closed | P2 |
| 18 | E2E vs `PUBLIC_ROUTE_ROOT` | P2 |
| 19 | host build skips lint (document if ok) | P3 |

### APP — secrets & tests

| # | Check | Pri if fail |
|---|-------|-------------|
| 20 | Creds in committed docs/env | P0 |
| 21 | Smoke `PUBLIC_ROUTE_ROOT` 200 + styled | P2 |
| 22 | Auth E2E per user `AUTH_FLOW` | P1/P2 |
| 23 | No `AUTH_COOKIES` Set-Cookie from public path | P1 |

### WORKER — separate repo

| # | Check | Pri if fail |
|---|-------|-------------|
| 24 | Rule routes `ROUTE_PREFIX` → `UPSTREAM_ORIGIN` | P1 |
| 25 | `PATH_MAP` matches worker rewrite | P1 |
| 26 | Path boundary (prefix vs prefix+foo) | P2 |
| 27 | Full cookie jar to upstream | risk doc |
| 28 | Set-Cookie passthrough | risk doc |

### INFRA

| # | Check | Pri if fail |
|---|-------|-------------|
| 29 | Deployment protection on `UPSTREAM_ORIGIN` | P1 |
| 30 | Third-party key restrictions | P2 |

### Sign-off

| Layer | Ready when |
|-------|------------|
| App | P0=0, route map P1=0, Phases 1–3 |
| Worker | rule matches profile + risk doc |
| Infra | 29–30 verified or ticket |

## Agent rules

1. **Ask first** — route profile before scan.
2. **Run cmds** — numbers not vibes.
3. **Re-scan** after impl — diff counts in plan.
4. **WORKER items** — never mark done in app repo.
5. **Auth E2E** — only if user gave `AUTH_COOKIES` + `AUTH_FLOW`; else flag gap P2.
6. **Checklist** — tick items in **Full checklist** section above; every finding → score table.
7. User summary: `/caveman ultra`.

## Verdict logic

```
if missing required intake → STOP
if P0 > 0 → NOT prod ready
elif route map mismatch (constants vs profile) → NOT prod ready
elif P1 > 0 → NOT prod ready
elif ci_gates < 4 → soft NOT ready
elif worker_cookie_passthrough and no risk doc → APP ok, WORKER/INFRA open
else → APP ready pending Phase 4–5
```

## Example intake (reference only — always ask user)

```
PUBLIC_ROUTE_ROOT  = https://www.eden.co.uk/events
UPSTREAM_ORIGIN    = https://events-snowy-phi.vercel.app
PATH_MAP           = preserve
UPSTREAM_ROUTE_ROOT= https://events-snowy-phi.vercel.app/events
```

