---
name: review-worker-proxy
description: >-
  Review v0/Next app for CF Worker reverse-proxy prod readiness. User supplies public route + upstream.
  Quant audit, scored issues, phased plan — APP / WORKER / INFRA split.
  Trigger: review-worker-proxy, proxy readiness, namespace sub-site behind CF Worker.
---

/caveman ultra

# Review worker proxy

Goal: user route map → count blockers → score → phase plan → split **APP** / **WORKER** / **INFRA**.

## Trigger

`/review-worker-proxy` or ask: worker deploy, proxy readiness, safe to proxy, prod gate.

## Step 0 — Intake (BLOCK til filled)

No audit. No grep. No plan. Til route profile done.

`AskQuestion` if avail; else chat. **Never invent URLs** — user supplies.

### Required

| Field | Key | Ask | Example |
|-------|-----|-----|---------|
| App root | `APP_ROOT` | Next/Vercel path | `eden-ecommerce/events` |
| Public route | `PUBLIC_ROUTE_ROOT` | Full URL via Worker | `https://www.eden.co.uk/events` |
| Upstream | `UPSTREAM_ORIGIN` | Bare deploy host | `https://events-snowy-phi.vercel.app` |
| Path map | `PATH_MAP` | Worker rewrite | `preserve` / `strip` / `root` |

### Derived (compute + confirm)

```
PUBLIC_HOST     = host(PUBLIC_ROUTE_ROOT)
ROUTE_PREFIX    = pathname(PUBLIC_ROUTE_ROOT)    # /events or ""
UPSTREAM_HOST   = host(UPSTREAM_ORIGIN)

preserve → UPSTREAM_ROUTE_ROOT = UPSTREAM_ORIGIN + ROUTE_PREFIX
strip    → UPSTREAM_ROUTE_ROOT = UPSTREAM_ORIGIN
root     → UPSTREAM_ROUTE_ROOT = UPSTREAM_ORIGIN + "/"
```

Confirm one line before scan:

> `PUBLIC_ROUTE_ROOT` → Worker → `UPSTREAM_ROUTE_ROOT` (`PATH_MAP`)

### Optional

| Field | Key | Default |
|-------|-----|---------|
| Worker root | `WORKER_ROOT` | search workspace |
| Worker match | `WORKER_MATCH` | read worker repo |
| Asset prefix var | `ASSET_PREFIX_VAR` | grep `assetPrefix` / `ASSET_*` |
| Namespace const | `NS_CONST` | grep `NAMESPACE_PATH` |
| PKG | `PKG` | lockfile → pnpm/npm/yarn |
| Auth cookies | `AUTH_COOKIES` | e.g. `PHPSESSID,csrft` |
| Auth flow | `AUTH_FLOW` | E2E paths |
| Plan out | `PLAN_OUT` | `<APP_ROOT>/docs/deployment-readiness-plan.md` |

### PATH_MAP modes

| Mode | Public | Upstream |
|------|--------|----------|
| **preserve** | `{PUBLIC_ROUTE_ROOT}/page` | `{UPSTREAM_ORIGIN}{ROUTE_PREFIX}/page` |
| **strip** | `{PUBLIC_ROUTE_ROOT}/page` | `{UPSTREAM_ORIGIN}/page` |
| **root** | `{PUBLIC_ROUTE_ROOT}/page` | `{UPSTREAM_ORIGIN}/page` |

`assetPrefix` / links → **public** URL (`PUBLIC_ROUTE_ROOT`), not bare `UPSTREAM_ORIGIN`.

### Single namespace root (required)

Worker maps **one path prefix** → upstream. All user pages under that root.

| Location | Rule |
|----------|------|
| `app/{ROUTE_PREFIX_TRIM}/**` | All `page.tsx` (exceptions below) |
| `app/page.tsx` | OK only if redirect → `ROUTE_PREFIX` |
| `app/api/*` | Origin-only template — not behind Worker; auth-gate |
| `app/{ROUTE_PREFIX_TRIM}/api/*` | Proxy APIs — `apiUrl()` / `NAMESPACE_PATH` |

**P1** if pages or built routes outside `ROUTE_PREFIX` users would hit.

Nested apps (`/events/christian-festival-finder`) → same prefix; Worker `matchesPathPrefix`, not second rule.

### Intake template

```markdown
## Route profile
| Key | Value |
| APP_ROOT | |
| PUBLIC_ROUTE_ROOT | |
| UPSTREAM_ORIGIN | |
| UPSTREAM_ROUTE_ROOT | |
| PATH_MAP | preserve | strip | root |
| WORKER_ROOT | |
| AUTH_COOKIES | |
| AUTH_FLOW | |
```

Blank required field → **stop**, ask user.

## Phase 0 — Quant scan

Substitute `<APP_ROOT>`, `<ROUTE_PREFIX>`, `<UPSTREAM_HOST>`, `<PUBLIC_ROUTE_ROOT>`, `<PKG>`. **Run cmds. Paste counts.**

### A. Build + type gate

```bash
cd <APP_ROOT> && <PKG> run ts-check 2>&1 | tail -5
cd <APP_ROOT> && <PKG> run lint 2>&1 | tail -20
cd <APP_ROOT> && <PKG> run build 2>&1 | tail -10
rg -n 'ignoreBuildErrors' <APP_ROOT>/next.config.ts 2>/dev/null
```

Record: `ts_errors`, `lint_errors`, `lint_warnings`, `build_ok`, `ignoreBuildErrors`.

**`ignoreBuildErrors` must be `false`.** Missing block = OK (Next default false). `true` = **P2** — set `false` or delete block.

```bash
rg -n 'assetPrefix|ASSET_.*ORIGIN|ASSET_.*URL|NAMESPACE|ROUTE_PREFIX' <APP_ROOT>/lib <APP_ROOT>/next.config.ts 2>/dev/null
```

Prod asset origin ≠ `PUBLIC_ROUTE_ROOT` → **P1**.

### B. URL / asset rules

```bash
rg -n 'src="/|href="/|url: "/' --glob '*.{tsx,ts,jsx,js}' <APP_ROOT> \
  | rg -v 'NsLink|NAMESPACE|assetUrl|apiUrl|<ROUTE_PREFIX>' | wc -l
rg -n 'fetch\(["\`]/api/' --glob '*.{tsx,ts}' <APP_ROOT> | wc -l
rg -n 'Set-Cookie|cookies\(\)\.set|document\.cookie\s*=' --glob '*.{tsx,ts}' <APP_ROOT> | wc -l
```

Post-build:

```bash
rg -l 'src="/_next' <APP_ROOT>/.next --glob '*.html' 2>/dev/null | wc -l
rg -c '<UPSTREAM_HOST>' <APP_ROOT>/.next --glob '*.html' 2>/dev/null | awk -F: '{s+=$2} END {print s+0}'
```

Record: `url_literal_hits`, `bad_fetch_api`, `cookie_mint_hits`, `html_root_next`, `html_upstream_origin_leak`.

Prod HTML assets → `PUBLIC_ROUTE_ROOT`, never bare `UPSTREAM_HOST`.

### C. API surface

```bash
find <APP_ROOT>/app -path '*/api/*/route.ts' | wc -l
find <APP_ROOT>/app/api -name 'route.ts' 2>/dev/null | wc -l
find <APP_ROOT>/app -path "*<ROUTE_PREFIX_TRIM>/api*" -name 'route.ts' | wc -l
```

`ROUTE_PREFIX_TRIM` = prefix sans leading `/` (e.g. `events`).

Bare `UPSTREAM_ORIGIN/api/*` = origin bypass. Client proxy APIs → `{PUBLIC_ROUTE_ROOT}/api/*`.

### C2. Single namespace root

```bash
find <APP_ROOT>/app -name 'page.tsx' ! -path 'app/page.tsx' \
  ! -path "app/<ROUTE_PREFIX_TRIM>/*" 2>/dev/null | wc -l
NAMESPACE=<ROUTE_PREFIX_TRIM> node -e "
const m=require('<APP_ROOT>/.next/routes-manifest.json');
const p='/' + process.env.NAMESPACE;
const pages=[...(m.staticRoutes||[]),...(m.dynamicRoutes||[])].map(r=>r.page);
const rogue=pages.filter(x=>x!=='/'&&!x.startsWith('/_')&&!x.startsWith('/api/')&&x!==p&&!x.startsWith(p+'/'));
console.log(rogue.length);
"
```

Record: `pages_outside_namespace`, `built_routes_outside_namespace`. Target **0** (P1).

Ship `e2e/namespace-contract.ts` + `e2e/namespace-routes.spec.ts` + `security-check` grep if missing.

### D. CI vs deploy gate

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

Count + file:line only. Never echo secrets.

### F. Worker (`WORKER_ROOT`)

- `ROUTE_PREFIX` match rule?
- Maps `UPSTREAM_ORIGIN` / `UPSTREAM_ROUTE_ROOT` per `PATH_MAP`?
- Cookie forward all backends?
- `Set-Cookie` rewrite?
- `startsWith` vs segment boundary?

Record: `worker_route_confirmed`, `worker_cookie_passthrough`, `worker_path_ambiguity_risk`.

## Phase 1 — Score matrix

| Pri | Meaning |
|-----|---------|
| P0 | Ship blocker — creds in git, unauth mutating API bare origin |
| P1 | Proxy break — wrong asset prefix, `/_next` leak, route mismatch, namespace leak |
| P2 | Gate gap — CI red, `ignoreBuildErrors: true`, no security grep |
| P3 | Debt — lint style, dead code |

```markdown
| Category | Count | P0 | P1 | P2 | P3 |
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
| **INFRA** | dashboard ticket |

Green app tests ≠ safe worker cookie policy.

## Phase 3 — Plan output

Write `<PLAN_OUT>`. Bullets ≤20 words.

```markdown
# [Project] — worker-proxy readiness plan
## Route profile
## Quant snapshot
## Mapping contract
## Sign-off split (App / Worker / Infra)
## Phases 1–6 checklists
## Action items
## Out of scope
```

Phase order: 1 → 2 → 3; 4 parallel after 1 green; 6 last.

## Full checklist

Substitute profile vars.

### Intake

| # | Check | Fail |
|---|-------|------|
| 0 | `PUBLIC_ROUTE_ROOT` supplied | stop |
| 0b | `UPSTREAM_ORIGIN` supplied | stop |
| 0c | `PATH_MAP` confirmed | stop |
| 0d | `UPSTREAM_ROUTE_ROOT` derived | stop |

### APP — route map + assets

| # | Check | Pri |
|---|-------|-----|
| 1 | `assetPrefix` = `PUBLIC_ROUTE_ROOT` | P1 |
| 2 | `NAMESPACE` = `ROUTE_PREFIX` | P1 |
| 2b | All `page.tsx` under `app/{ROUTE_PREFIX_TRIM}/` | P1 |
| 2c | Built routes under `ROUTE_PREFIX` (exc `/`, `/_*`, `/api/*`) | P1 |
| 3 | No `src="/_next` in HTML | P1 |
| 4 | No `UPSTREAM_HOST` in prod HTML | P1 |
| 5 | Links use route prefix | P1 |
| 6 | Client API → `{PUBLIC_ROUTE_ROOT}/api` not bare `/api` | P1 |
| 7 | No cookie mint for `AUTH_COOKIES` | P0 |
| 7b | `ignoreBuildErrors: false` in `next.config.ts` | P2 |

### APP — API

| # | Check | Pri |
|---|-------|-----|
| 8 | Count `app/api/*` | info |
| 9 | No unauth mutating bare origin API | P0 |
| 10 | Proxy APIs under `app/{prefix}/api/*` | P2 |
| 11 | `apiUrl()` absolute paths — **correct**; flag bare `/api` fetch only | — |
| 12 | Public POST rate limits | P2 |

### APP — CI

| # | Check | Pri |
|---|-------|-----|
| 13–17 | ts-check, lint, build, security grep, audit high | P2 |
| 18 | E2E manual (`pnpm test:e2e:proxy`) | P2 unless user wants CI |
| 19 | Host build skips lint | P3 |

### APP — secrets + tests

| # | Check | Pri |
|---|-------|-----|
| 20 | No creds in git | P0 |
| 21 | Smoke `PUBLIC_ROUTE_ROOT` styled | P2 |
| 22 | Auth E2E per `AUTH_FLOW` | P1/P2 |
| 23 | No `AUTH_COOKIES` Set-Cookie from public path | P1 |

### WORKER

| # | Check | Pri |
|---|-------|-----|
| 24 | Rule `ROUTE_PREFIX` → `UPSTREAM_ORIGIN` | P1 |
| 25 | `PATH_MAP` matches rewrite | P1 |
| 26 | Path boundary (`matchesPathPrefix`) | P2 |
| 27–28 | Cookie jar / Set-Cookie passthrough | risk doc |

### INFRA

| # | Check | Pri |
|---|-------|-----|
| 29 | Deployment protection on `UPSTREAM_ORIGIN` | P1 |
| 30 | Third-party key restrictions | P2 |

### Sign-off

| Layer | Ready when |
|-------|------------|
| App | P0=0, P1=0, phases 1–3 |
| Worker | rule matches + risk doc |
| Infra | 29–30 verified or ticket |

## Agent rules

1. Intake first — no scan til profile filled.
2. Run cmds — numbers not vibes.
3. Re-scan after fix — diff counts.
4. WORKER fixes → worker repo only.
5. Auth E2E → only if user gave `AUTH_COOKIES` + `AUTH_FLOW`; else P2 gap.
6. Every finding → score table + checklist tick.
7. Chat summary → `/caveman ultra`.
8. **Action items required** — end every audit with `## Action items`; file + pri + fix + snippet.
9. **`ignoreBuildErrors`** — must be **`false`**. `true` or unset after v0 edit → **P2**; fix `next.config.ts`. v0 may re-add — still flag.
10. **`apiUrl()` absolute paths** — correct for proxy. Flag bare `/api` in client only.
11. **E2E** — manual `pnpm test:e2e:proxy` unless user wants CI gate.
12. **Single namespace root** — P1 if pages/routes outside `ROUTE_PREFIX`.

### E2E hardcoded prefix grep

```bash
rg -n '"/events|/events/' e2e/ | rg -v 'routes\.ts|NAMESPACE' || true
```

Adapt to `ROUTE_PREFIX_TRIM`.

## Action items (required output)

End chat + plan with this. One bullet per real fix. Snippet so user judges necessity.

```markdown
## Action items

### APP
- [ ] **{issue}** — `{file}` — `{Pri}`
  - Fix: `{change}`
  - Snippet: `{before → after}`

### WORKER
- [ ] **{issue}** — `{file}` — `{Pri}`
  - Fix: `{change}`
  - Snippet: `{diff}`

### INFRA
- [ ] **{issue}** — `{console}` — `{Pri}`
  - Fix: `{step}`

### Not actionable
- `apiUrl()` absolute paths — intentional
- Proxy E2E — manual unless user requests CI
```

**Example — ignoreBuildErrors:**

```markdown
- [ ] **`ignoreBuildErrors: true`** — `next.config.ts` — P2
  - Fix: set false (or delete `typescript` block — default false)
  - Snippet:
    ```ts
    typescript: { ignoreBuildErrors: false },
    ```
```

**Example — Worker boundary:**

```markdown
- [ ] **`startsWith` hits `/eventsomething`** — `routing.ts` — P1
  - Fix: `matchesPathPrefix(ctx.pathname, "/events")`
```

**Example — namespace root:**

```markdown
- [ ] **Page outside Worker root** — `app/marketing/page.tsx` — P1
  - Fix: move → `app/{ROUTE_PREFIX_TRIM}/marketing/page.tsx`
  - Snippet: only `app/page.tsx` redirect allowed outside namespace
```

## Verdict

```
missing intake → STOP
P0 > 0 → NOT prod ready
route map mismatch → NOT prod ready
P1 > 0 → NOT prod ready
ci_gates < 4 → soft NOT ready
worker cookie passthrough + no risk doc → APP ok, WORKER/INFRA open
else → APP ready pending Phase 4–5
```

## Example intake (reference — always ask user)

```
PUBLIC_ROUTE_ROOT  = https://www.eden.co.uk/events
UPSTREAM_ORIGIN    = https://events-snowy-phi.vercel.app
PATH_MAP           = preserve
UPSTREAM_ROUTE_ROOT= https://events-snowy-phi.vercel.app/events
```
