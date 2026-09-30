# Setup — local development

Everything needed to clone this repo and get it running on a developer's machine. Production shipping strategy lives in [DEPLOYMENT_STRATEGY.md](./DEPLOYMENT_STRATEGY.md) — keep the two separate; this file never grows a "then deploy to prod" section.

## Prereqs

- Runtime + package manager pinned in `package.json` (`packageManager` field) — everyone installs the same version, no "works on my machine" drift
- A registry read token if the project consumes a private shared package (see `ARCHITECTURE.md` § Shared-package strategy) — otherwise skip
- DB reachable with credentials in `.env.local`, if the project has one

## First-time setup

```bash
git clone <url>
# only if a private shared-package registry is in play:
export NPM_REGISTRY_TOKEN=...
pnpm config set //<registry-host>/:_authToken "$NPM_REGISTRY_TOKEN"

pnpm setup   # install + seed .env.local from .env.example
```

Fill required env vars in `.env.local`. See `CONFIG.md` for the full var table and secrets-handling law.

**CI static-analysis jobs (typecheck/lint/test/build) should never need a live DB or a cloud secret manager** — keep those steps runnable against nothing but the checked-out repo. Only migration/seed jobs against a real environment need real credentials.

## Database

```bash
pnpm db:generate   # only when schema changes
pnpm db:migrate
pnpm db:seed
```

`pnpm dev` may apply pending migrations and run a one-time seed automatically when the core table is empty (an `AUTO_MIGRATE` / `AUTO_SEED` flag, on by default in development) — document the exact flag name here once the project has one.

## Day-to-day (host)

```bash
pnpm dev          # dev server
pnpm db:migrate   # when schema changes
pnpm db:seed
```

`pnpm install` fetches any pinned shared-package tarballs. No local clone checkout, no yalc, no package git hooks needed for day-to-day work.

## Docker / containerised local dev (optional profile)

If the project runs a local container profile (DB + app in Compose), keep one command that does the whole thing:

```bash
pnpm dev:docker   # compose up: DB + migrate/seed + app in a container
```

Document, once real: default DB choice, the host port the app binds to, and what to do when a dependency change makes the container report "module not found" (usually: the `node_modules` volume is stale — rebuild, or drop the named volume). Keep an escape hatch for an isolated local DB (its own Compose profile/port) separate from any shared team DB, so a developer never has to touch a shared environment to get running.

## After a shared-package release

Only relevant once the project has a shared design/lib package (see `ARCHITECTURE.md`):

```bash
pnpm add @org/design@X.Y.Z @org/lib@A.B.C --save-exact
```

Commit `package.json` + the lockfile only. Fix any resulting import breaks in the same change.

## Test

```bash
pnpm test
pnpm test:e2e
```
