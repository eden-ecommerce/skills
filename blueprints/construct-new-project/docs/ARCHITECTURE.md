# Architecture

System design, file organisation, module ownership, and shared-package/integration strategy — one file. For "how do I run this locally" see [SETUP.md](./SETUP.md). For "how does this ship to production" see [DEPLOYMENT_STRATEGY.md](./DEPLOYMENT_STRATEGY.md).

This file is the index. It states each law once and points at the verbatim source (`../rules/*.mdc`) rather than repeating it — read the named rule file before applying it, do not paraphrase from memory.

## Stack — worked example, not a law

| Layer | content-studio (source instance) |
|---|---|
| Framework | Next.js App Router, React, single app at repo root |
| Language | TypeScript strict — no `any`, minimal `unknown` |
| DB | MySQL via Drizzle ORM |
| Validation | Zod |
| Data fetching | TanStack Query (client) + Server Actions / Route Handlers (server) |
| Styling | Tailwind CSS + tailwind-merge + tailwind-variants, shadcn token set |
| Testing | Vitest (unit), Playwright (e2e) |

Re-derive this table for the new project's actual stack at intake (see `../SKILL.md` § Framework adaptation) — do not assume Next.js/MySQL/Drizzle.

## Repo layout

Single app at repo root. No `apps/<name>` nesting unless the brief is explicitly a multi-app monorepo.

| Path | Role |
|---|---|
| `app/` (or the chosen framework's route root) | Routes, thin. Compose feature views, never business logic. |
| `features/<entity>-<objective>/` | User-job folders. Noun-first (`brand-browse`, not `create-brand`). |
| `data/` | Mutations/server actions + `dto`/`dpo`/`dal` per entity |
| `domain/` | Business rules, no UI, no direct DB driver import |
| `services/` | Infra adapters — DB pool, external-call registry, background-job runtime |
| `drizzle/` (or the chosen ORM's schema dir) | Schema + migrations |
| `utilities/` | Root shared pure helpers |
| `packages/plugins/*` | Thin 3rd-party API clients, in-repo workspace — only if the project has enough distinct 3rd-party clients to isolate |
| `packages/libraries/*` | Framework-free engines, in-repo workspace — only once logic is reused outside the main app |

Full enforced law (verbatim): `../rules/layers.mdc`, `../rules/project-structure.mdc`.

```
app / feature   → data actions, domain, services
data actions    → dpo, dto, dal, domain, services
dpo             → gates, dal, dto
dto             → (pure)
dal             → services/db, ORM
domain/<entity> → services, utilities   (NOT data, NOT ORM, NOT sibling domain)
services        → utilities, data/*/dal, packages/plugins
services/db     → ORM (pool / migrate / probe only)
```

Forbidden: shared-package → app. domain → feature. libraries → plugins. feature → sibling feature views/controllers. Barrel `index.ts` re-exports anywhere.

## Feature folder shape

```text
features/{entity}-{objective}/
  models/              schema for this job only
  views/pages/          one page (or none if the route composes)
  views/components/     presentational
  views/phases/<phase>/ optional multi-phase workspace panels
  controllers/          form + list controllers
  hooks/                non-form UI hooks
  api/                  client data-fetching for this job
  utilities/             pure helpers — not in views/
  types/                 only if not inferable from models
  tests/                 colocated tests — never `foo.test.ts` beside `foo.ts`
  config.ts or config/   optional
```

Omit empty dirs — an empty `views/phases/` on a feature with no phases is scope creep, not scaffolding. Naming law (verbatim): `../rules/naming.mdc`. Always-on coding standards (verbatim): `../rules/general.mdc`.

## Writing your own annotated domain/services tree

Once `domain/` and `services/` have more than a handful of folders, write one short internal doc that lists each folder with **one inline comment**, not prose paragraphs — this is the format, adapt the content per project:

```
domain/pricing/          ← discount + tax calculation, no I/O
domain/orders/           ← order lifecycle rules + status transitions
services/payments/       ← payment-provider adapter (routes through external-integrations registry)
services/db/             ← connection pool / migrate / probe only
```

### Worked request trace (format to copy, not the literal route)

Picking one real request and tracing it through every layer is the fastest way to prove the layer law actually holds. Example shape, from content-studio's own trace:

`GET /build/[id]/[phase]/[step]`:

1. **app** — the route file awaits params, renders a page component. Thin, per the layer law.
2. **feature** — the page component calls a `get*Server` (data) and a domain helper to evaluate business rules.
3. **data** — the `get*Server` function calls its DAL, which imports the DB client and ORM tables directly.
4. **domain** — a pure function evaluates guards/rules with no DB import of its own.
5. **services** — the DAL layer reaches into the DB pool and ORM schema directly — `data → services/db, domain`, never `domain → data`.

Write the equivalent trace for one real route in the new project once routing exists — it belongs in the project's own `docs/domain-rundown.md` (or similar), not in this handoff file.

## Module ownership pattern (only for 2+ distinct journeys)

Skip this section for a single-journey app. When a product has multiple operator/user journeys that barely touch each other, name each one a **module** with an explicit owns / does-not-own table — one deploy, boundaries enforced by folder + import law, not a repo split.

Worked example (content-studio — labelled, not literal for a new project):

| Module | Owns | Does not own |
|---|---|---|
| **idea-studio** (Plan) | Signals, campaign ideas, idea snapshot | Panel mapping, image models, ESP send |
| **Build** | Brief through preview (seeded pipeline snapshot) | ESP send, CMS publish, Ads APIs |
| **Deliver** | Send / publish / download | Outline, panel pick, image models |
| **Automations** | Inject brief into Build, or finished payload into Deliver | Skipping the first Build step; writing draft content; calling the send provider itself |

Rebuild this exact table shape with the new project's own journeys and boundaries.

## Shared-package strategy (only once a second consumer exists)

Skip this section entirely for a single, standalone app. It only earns its keep once a design system or integration library is shared across two or more apps.

**Decision** — where new code goes:

| Kind of change | Home |
|---|---|
| Visual look, variants, layout, chrome | A shared, props-only design package |
| Fetch / GROQ / SQL getters, env guards, shared hooks, formatters | A shared integrations/lib package |
| Feature logic, domain rules, this app's own screens | This repo only |

**Package law:**

- Shared packages live in their **own repo**, published via a package registry (npm, GitHub Packages, or private registry) — never a git submodule, never `workspace:*`/`file:`/`link:` from a consumer, never a gitignored clone
- Consumer pins an **exact semver** (`"0.3.0"`, not `^0.3.0`) — the lockfile must resolve to the registry tarball
- In-repo workspaces (`packages/plugins/*`, `packages/libraries/*`) stay `workspace:*` — those live in this git tree, not the registry
- A shared design package is **props-only** — no fetch, no env, no CMS SDK inside it; the consuming app fills its slots
- Deep imports only, folder-per-component (`{Name}/{Name}.tsx`) — no package-root barrel import

**Change loop:**

1. Decide home (table above)
2. Edit + prove in the package's own repo (its own Storybook / tests)
3. Publish (changeset → tag → registry)
4. Bump the exact pin in every consumer, in the same change as any resulting import/prop fix
5. Commit `package.json` + lockfile only for the bump commit

Full rules (verbatim, once this tier exists): `../rules/design.mdc`, `../rules/storybook.mdc`, `../rules/shared-integrations.mdc`, `../rules/ownership.mdc`. Which registry host serves the tarball (GitHub Packages, npm, a private registry) is a deployment-target detail, not part of this pattern — see `DEPLOYMENT_STRATEGY.md` and the matching `docs/environment/<target>.md` (e.g. `environment/github.md` § GitHub Packages).

## External integrations and AI calls

Any call that leaves the process — a payment provider, a search index, a CMS, an AI model — goes through one closed, typed operation registry. Full pattern (verbatim, generic): `../rules/external-integrations.mdc`. Only add this tier once the project actually calls an external API or a model; a project with zero external calls skips it.

## Background / durable jobs

Any unit of work that can outlive one request (bulk export, AI generation step, a scheduled send) is enqueued to a DB-backed queue and drained by a separate worker — never awaited inline past the platform's request timeout. Full pattern (verbatim, generic): `../rules/background-jobs.mdc`. Only add this tier once the project has work that genuinely needs to survive past one request.

## Rules index — generic vs instance-specific

Every rule file below lives verbatim in `../rules/`. **Generic** = the law transfers to any new project as-is. **Generic, conditional** = transfers, but only wire it in once the matching tier exists (see sections above). **Generic pattern** = the shape transfers; reword the worked example's product nouns.

| Rule file | Scope | Kind |
|---|---|---|
| `general.mdc` | Always-on coding standards | Generic |
| `layers.mdc` / `project-structure.mdc` | Layer law + repo layout | Generic |
| `naming.mdc` | Naming conventions | Generic |
| `no-deprecated.mdc` | Delete dead code same-change, no alias maps | Generic |
| `no-barrels.mdc` | Deep imports only | Generic |
| `database.mdc` | Schema types, migrations, runtime-config SSOT, storage split | Generic |
| `testing.mdc` | Test colocation convention | Generic |
| `hooks.mdc` | TanStack Query client/server split pattern | Generic, conditional (TanStack Query) |
| `forms.mdc` | Formik + Zod controller pattern | Generic, conditional (Formik) |
| `accessibility.mdc` | WCAG basics | Generic |
| `interaction.mdc` | Destructive confirm, async pending, multi-step flows, nav, content truncation | Generic |
| `performance.mdc` | RSC-first, dynamic import, virtualise lists | Generic pattern (React/Next specific) |
| `error-pages.mdc` | Plain-English error copy, no HTTP codes in UI | Generic |
| `copy.mdc` | UI copy voice | Generic |
| `page-tabs.mdc` | URL-synced tabs for multi-section pages | Generic pattern |
| `theme.mdc` | Design token contract | Generic pattern, retint per brand |
| `predeploy.mdc` / `pull-requests.mdc` | Ship gate + PR/MR body law | Generic — host-agnostic, see `DEPLOYMENT_STRATEGY.md` |
| `documentation.mdc` | Keep public docs + manifest in sync | Generic |
| `software-development-lifecycle.mdc` | Master/sub-plan SDLC flow | Generic |
| `generated.mdc` | Generated code is read-only | Generic |
| `scripts.mdc` | Canonical script verbs | Generic — drop verbs with no matching infra |
| `external-integrations.mdc` | Closed registry for 3rd-party + AI calls | Generic, conditional |
| `background-jobs.mdc` | Durable queue + worker pattern | Generic, conditional |
| `dev-checks.mdc` | `check` script + pre-push hook + CI + host checks, all same script names | Generic |
| `ai-contributors.mdc` | v0 / Lovable / Cursor / Claude Code contribution guard rails, protected paths | Generic |
| `project-environment.mdc` | Lists the `docs/environment/*.md` docs for the chosen deploy target + local dev (filled from `templates/project-environment.mdc.template`) | Generic |
| `project-overview.mdc` | Objective, import law, on-demand rule table — the body that used to sit in CLAUDE.md (filled from `templates/project-overview.mdc.template`) | Generic |
| `project-config.mdc` | Detect stack from `package.json`, read `docs/config/<stack>.md` | Generic |
| `tanstack-start.mdc` | TanStack Start routes, server fns, env, build-only adapter, port | Generic, conditional (TanStack Start) |
| `design.mdc` / `storybook.mdc` / `shared-integrations.mdc` / `ownership.mdc` | Shared design/lib package law | Generic pattern, conditional (2+ consumers) |

## Deployment-target docs (`docs/environment/<target>.md`)

Every rule above is target-agnostic. Target-specific mechanics live in **docs, not rules**: `docs/environment/<target>.md`, structured like `docs/config/<stack>.md`. The project's `.cursor/rules/project-environment.mdc` lists only the docs for the environments it picked, so an agent never reads guidance for a target the project doesn't use. Terraform, Docker, a specific git host, a specific package registry — anything that's true of *one* deployment choice and not another — lives in its own `docs/environment/<target>.md`, read only when `DEPLOYMENT_STRATEGY.md` § 1 actually picks that target. This repo shipped one real worked set (Cloud Run + Terraform + Docker + GitHub); a different choice needs its own file written with that target's real mechanics, never this set reworded to sound generic.

| Doc | Target | Kind |
|---|---|---|
| `environment/terraform.md` | Cloud Run + Terraform infra-as-code, incl. first-time setup checklist | Worked example, conditional |
| `environment/docker.md` | Cloud Run container/Dockerfile requirements | Worked example, conditional |
| `environment/developer.md` | Day-to-day dev workflow for that Cloud Run + Terraform + Docker setup | Worked example, conditional |
| `environment/github.md` | GitHub-specific PR CLI, Actions CI wiring, GitHub Packages registry | Worked example, conditional |
| `environment/vercel.md` | Vercel: `vercel.json`, Checks, frozen lockfile, env pull, preview vs prod | Worked example (from a shipped Vercel repo), conditional |

No `environment/gitlab.md` / etc. exist here — there was no verbatim source for them. Write one, in this same shape, the first time a project actually picks that target; do not invent one from guesswork to fill a gap.

## What this doc is not

Not a copy of content-studio's product decisions. The worked examples above are labelled and exist to show format — replace every labelled example with the new project's own answer, never paste the label's content into an unrelated project.
