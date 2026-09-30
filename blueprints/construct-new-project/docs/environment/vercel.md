# Vercel (this target)

Loaded only when `docs/DEPLOYMENT_STRATEGY.md` § 1 picked a serverless platform = Vercel. Generic gates: `predeploy.mdc`, `dev-checks.mdc`.

## `vercel.json`

Committed at repo root. Templates: `templates/vercel.json.nextjs.template`, `templates/vercel.json.tanstack.template`.

| Key | Value |
|---|---|
| `$schema` | `https://openapi.vercel.sh/vercel.json` |
| `framework` | `nextjs` or `tanstack-start` — must match the root `package.json` dependency |
| `buildCommand` | the project's `build` script (`pnpm build`) |
| `installCommand` | only when needed (private registry token) — must fail loudly on a missing token, then `pnpm install --frozen-lockfile` |

**Root Directory = empty** (repo root) in Vercel project settings. "No Next.js version detected" almost always means it points at a subfolder.

## Vercel Checks

- Scripts named exactly `lint` and `typecheck` must exist and pass. A missing `typecheck` is **skipped, not passed**; `ts-check` is not recognised.
- AI builders (v0, Lovable) can compile with TS errors — Vercel Checks won't. Run `check` before merging their branches.
- New server-side `fetch()` file → add it to the lint fetch-allowlist if the project has one, or lint fails on Vercel.

## Install + lockfile

- Vercel installs with `--frozen-lockfile`: commit `pnpm-lock.yaml` with every dependency, override, or `audit:fix` change (`ERR_PNPM_LOCKFILE_CONFIG_MISMATCH` otherwise).
- `packageManager` in `package.json` pins the pnpm version; `corepack enable` locally.
- Private registry (only if the shared-package tier exists): token env var must not start with `GITHUB_` (GitHub forbids such secrets) — see `docs/environment/github.md`.

## Environment

- Source of truth = Vercel project env. Local: `vercel link` once, then `pnpm pull:env` → `.env.local` (gitignored).
- `.env.example` lists every variable, with no real values. Add a var there in the same change that reads it.
- Browser-exposed vars: `NEXT_PUBLIC_*` (Next) / `VITE_*` (TanStack Start) only. Everything else is server-only.
- Separate values per environment (Development / Preview / Production) — never reuse a production secret in Preview.
- Validate required production env at build time (throw in `next.config.ts` / `vite.config.ts`) so a missing var fails the build, not the first request. CI supplies placeholder values so the build compiles.

## Preview vs production

- Every PR gets a Preview deployment: put its URL in the PR body (`pull-requests.mdc`).
- Production = pushes to `main` only. Rollback = redeploy the previous deployment or revert the merge commit.
- Don't add `export const dynamic = "force-dynamic"` to force runtime rendering (Next) — isolate request-time APIs in `<Suspense>` instead; see `performance.mdc`.

## Do not

- Hardcode a deploy origin in source — read it from env.
- Commit `.vercel/` or `.env*.local`.
- Loosen `framework`/`buildCommand` to make a failing build pass.
