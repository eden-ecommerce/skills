# Config

## Stack

Per-project answers, filled at intake — agents read this before stack-specific work (`../rules/project-config.mdc`).

| Key | Value |
|---|---|
| STACK | `nextjs` \| `tanstack-start` |
| Ship gate | `predeploy` \| `check` + `build` |
| Dev / E2E port | `3000` \| `5173` |
| Lovable / v0 contributors | yes \| no (yes ⇒ no private-registry deps) |
| Deploy target | from `DEPLOYMENT_STRATEGY.md` § 1 |

Local: repo-root `.env.local` (copy from `.env.example`). GitHub check stages (TypeScript / Lint / Test / Build) — no Cloud SQL. Cloud Run: GSM via `terraform/service.yaml` `secrets:` (import with `pnpm sync:secrets:staging` / `pnpm sync:secrets:production` from `.env.staging` / `.env.production`). Migrate/seed: Cloud Run Jobs only (`docs/private/ops/database-cloud-run.md`). Never commit secrets. Blank GSM values are treated as unset.

## Plugin credentials (SSOT)

Runtime operations resolve **encrypted** `plugins.credentials_json` only (`PLUGIN_CREDENTIAL_SECRET` AES-GCM). No env merge at resolve time.

- **Seed / bootstrap:** `getDefaultPlugins()` reads `process.env` once and `upsertDefaultPlugins` encrypts into the DB. Secrets must never be hardcoded in seed source files.
- **Operators:** Configure → Plugins (edit by id decrypts for the form; browse list exposes `credentialKeys` only).
- **Signals:** live rows from **custom API** requests that have a `signal_projection_json`. Not a builtin news plugin. Host, path, and credentials live on the plugin definition + saved request.

## Enablement

Tenant plugin `health` (`healthy` / `disabled` / `misconfigured` / `unreachable`) gates runtime use. Missing DB credentials → disabled/misconfigured, not a site crash.

Prefer **flags in `env:`**, **secret values in `secrets:`** for seed jobs. Model ids / provider / image size live in [`services/env/ai-constants.ts`](../../services/env/ai-constants.ts) — not GSM.

## DATABASE_*

| Var | Purpose |
|-----|---------|
| DATABASE_HOST | MySQL host (required at runtime) |
| DATABASE_PORT | default 3306 |
| DATABASE_USER | user |
| DATABASE_PASSWORD | password |
| DATABASE_NAME | `CONTENT_STUDIO` (local compose) |

## PLUGIN_CREDENTIAL_SECRET

| Var | Purpose |
|-----|---------|
| PLUGIN_CREDENTIAL_SECRET | AES-GCM encrypt plugin `credentials_json` (required for seed + resolve) |

## Seed-time provider env (optional after Plugins UI filled)

Used only by seed / `upsertDefaultPlugins` to fill empty credential keys. Runtime does not read these.

| Var | Plugin |
|-----|--------|
| ALGOLIA_APP_ID / ALGOLIA_ADMIN_API_KEY | algolia |
| SANITY_PROJECT_ID / SANITY_DATASET / SANITY_API_EDITOR_TOKEN | sanity |
| GEMINI_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY | gemini (capability `ai`) |
| EDEN_INTELLIGENCE_BASE_URL / EDEN_INTELLIGENCE_API_KEY | eden-intelligence |
| SUNSEEKER_BASE_URL / SUNSEEKER_API_KEY | sunseeker (email delivery) |
| SUNSEEKER_AUDIENCE_TRIBE | campaign schedule audience; not stored on the plugin row |
| SENDER_EMAIL / RECIPIENT_EMAIL | plugin From address and the locked test-send inbox |

## NEXT_PUBLIC_ALGOLIA_*

| Var | Purpose |
|-----|---------|
| NEXT_PUBLIC_ALGOLIA_APP_ID | browser InstantSearch |
| NEXT_PUBLIC_ALGOLIA_SEARCH_KEY | public search key |

## SANITY_PREVIEW_TOKEN

| Var | Purpose |
|-----|---------|
| SANITY_PREVIEW_TOKEN | preview token substitution in brand URL templates |

## GEMINI_BASE_URL / model constants

Model ids live in `ai-constants.ts`. `GEMINI_BASE_URL` may remain for OpenAI-compatible Gemini endpoint config.
