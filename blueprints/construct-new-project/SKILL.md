---
name: construct-new-project
description: Scaffold a brand new project (repo, app, or package) that follows this fleet's engineering conventions — layer boundaries, noun-first feature-folder MVC, naming law, no-deprecated/no-barrels discipline, predeploy gates. Intakes project name, framework stack, and a brief, then runs question sets on expected pages, features, domains, integrations, style/design aesthetic, user UX, and deployment strategy before writing the agent entry files (CLAUDE.md/AGENTS.md/PROJECT_RULES.md), STRUCTURE.md, .cursor/rules, docs, and the initial folder tree. Use when starting a brand new repo, "scaffold a new project", "set up a new app following our conventions", or "spin up a new studio/service".
---

# CONSTRUCT NEW PROJECT

Thin orchestrator over a frozen architecture snapshot from `content-studio`. Everything this skill enforces is real, working convention copied verbatim from a shipped repo — not invented boilerplate. Load only what the current stage needs; rules are not duplicated in this file.

Source of truth, in reading order: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) (system design index) → [`docs/SETUP.md`](docs/SETUP.md) (local dev) → [`docs/DEPLOYMENT_STRATEGY.md`](docs/DEPLOYMENT_STRATEGY.md) (shipping) → [`docs/CONTEXT.md`](docs/CONTEXT.md) (glossary pattern) → [`docs/CONFIG.md`](docs/CONFIG.md) (env/secrets) → `rules/*.mdc` (verbatim Cursor rules, generic-only — every instance-specific rule was already stripped or generalized). Read the named source file before applying a rule to the new project — this file only points at it.

## HARD RULES

- Never scaffold a `Record<OldId, NewId>` alias map, a "legacy" fallback path, or a TODO-remove-later shim. `rules/no-deprecated.mdc` applies from commit one, even with no old code yet — it means: don't build the shim pattern into the new project either.
- Deep imports only, no barrel `index.ts` re-exports, from the first file written. See `rules/no-barrels.mdc`.
- Every identifier under 7 words, full English words, no abbreviations. See `rules/naming.mdc`.
- Runtime config that will ever need to change without a redeploy (feature catalogs, allow-lists, step/pipeline definitions) belongs in the database from day one — never a TypeScript literal the team plans to "migrate to DB later." See `rules/database.mdc` § Runtime config.
- Do not copy content-studio's domain specifics (Eden, panels, Sunseeker, Sanity, Algolia) into an unrelated new project. Copy the *pattern*, reword the *instance*. `docs/ARCHITECTURE.md`'s rules index marks every rule Generic vs Generic-conditional vs Generic-pattern for exactly this reason.
- Do not scaffold speculative structure. Only create feature folders, domains, and rule files the intake session actually surfaced. An empty `views/phases/` for a feature with no phases violates `rules/general.mdc`'s KISS line, not a courtesy.
- Never silently pick a framework-adaptation mapping. If the chosen stack has no row in § Framework adaptation, ask before inventing folder names.
- Do not wire the external-integrations, background-jobs, or shared-package rule tiers (`rules/external-integrations.mdc`, `rules/background-jobs.mdc`, `rules/design.mdc`+siblings) unless Stage 2 actually surfaced a need for them — see `docs/ARCHITECTURE.md`, each section says when to skip it.

## STAGE 1 — INTAKE

Collect three things before any question set:

| Field | What | How to resolve |
|---|---|---|
| **project name** | Repo/app name, kebab-case | Ask user |
| **framework stack** | Next.js App Router / TanStack Start / other | Ask user; see § Framework adaptation |
| **project brief** | One paragraph: what it does, who it's for | Ask user |

Confirm the three back to the user in one line before moving to Stage 2.

## STAGE 2 — QUESTION SETS

Ask these as a batched set of questions (not one at a time), scoped by what the brief already answered — skip a question the brief already made obvious, but confirm your read of it back to the user rather than silently assuming.

| Set | Ask | Feeds |
|---|---|---|
| **Pages / routes** | What screens does a user land on? Which are public vs behind auth? | route tree |
| **Features / entities** | What are the nouns a user creates, browses, edits? (e.g. "brand", "order", "campaign") | `features/<entity>-<objective>/` folders, `docs/CONTEXT.md` glossary rows |
| **Domains** | What business rules exist independent of any one screen? (pricing, eligibility, scoring, a pipeline/workflow) | `domain/<entity>/` folders |
| **Integrations** | Any 3rd-party APIs (payment, CMS, search, email, AI model)? | whether `rules/external-integrations.mdc` applies; `packages/plugins/*` |
| **Background work** | Any job that outlives one request (bulk export, AI generation, scheduled send)? | whether `rules/background-jobs.mdc` applies |
| **Style / design aesthetic** | Existing design system to reuse, or new? Brand colour/type direction? Tone (playful, clinical, editorial)? | `rules/theme.mdc` pattern, token table |
| **User / UX** | Who is the primary user? What's the one job they're trying to finish fastest? Any multi-step flow (wizard, pipeline, checkout)? | `rules/interaction.mdc`, `rules/page-tabs.mdc` vs a stepper pattern |
| **Data** | Relational DB? Which engine? Any values that must be per-tenant? | schema shape, `rules/database.mdc` |
| **Multiple journeys?** | Does this product have 2+ distinct user journeys that barely touch each other? | whether the module-ownership pattern applies (`docs/ARCHITECTURE.md` § Module ownership pattern) |
| **AI contributors** | Will designers/other devs contribute via v0, Lovable, Cursor, or Claude Code? Which? | `rules/ai-contributors.mdc` (always), `docs/CONFIG.md` § Stack `Lovable: yes\|no`, private-registry constraint; Lovable ⇒ TanStack Start row |
| **Deployment strategy** | Where will this actually run in production — a target platform in mind, or unsure? | `docs/DEPLOYMENT_STRATEGY.md` § 1 — see below, this one always gets an answer, even a proposed one |

**Deployment strategy is not optional to skip.** If the user has a target platform, record it. If the user is unsure, **propose** a strategy from `docs/DEPLOYMENT_STRATEGY.md` § 1 based on the stack and brief, state the recommendation and its trade-off in one line, and get an explicit yes/override before Stage 3 — this gives the scaffold (and everything built after it) a real first-MVP shipping target instead of an implicit "figure it out later."

Do not proceed to Stage 3 until every row above has an answer or an explicit "not applicable."

## Framework adaptation

Content-studio is Next.js App Router. Map its layer folders to the chosen stack. Ask the user before inventing a row not listed here.

| Concept | Next.js App Router (source) | TanStack Start | Generic SPA + API server |
|---|---|---|---|
| Route root | `app/` | `app/routes/` (file-based) | `src/pages/` or router config + separate `server/` |
| Server mutation | Server Actions in `data/<Capability>/` | Server Functions (`createServerFn`) in `data/<Capability>/` | REST/RPC handler in `server/<capability>/` |
| Server read | `get*Server.ts`, React Server Component | Loader (`loader` on the route) calling `get*Server.ts` | API endpoint + client fetch |
| Client read | `get*Client.ts` + TanStack Query | Same — TanStack Start ships TanStack Query | `get*Client.ts` + TanStack Query |
| Background/durable job | see `rules/background-jobs.mdc` | Same pattern | Same pattern |

Per-stack detail (ports, ship gate, env, `vercel.json` framework value): [`docs/config/nextjs.md`](docs/config/nextjs.md) / [`docs/config/tanstack-start.md`](docs/config/tanstack-start.md). Copy only the chosen one, plus `rules/project-config.mdc`; TanStack Start also gets `rules/tanstack-start.mdc`.

Everything below "Route root" in the layer law (`data/`, `domain/`, `services/`, `packages/plugins/*`, `packages/libraries/*`) is framework-agnostic — copy as-is regardless of the row picked above.

## STAGE 3 — SCAFFOLD

Run in order. Each step writes real files — confirm the file list with the user before the first write if this is a shared/existing repo, not a fresh `git init`.

1. **Directories.** Create only the `app/` (or mapped root) / `features/` / `data/` / `domain/` / `services/` roots, plus `packages/plugins/` and `packages/libraries/` only if Stage 2 "Integrations" or "Background work" surfaced enough to isolate. Do not pre-create empty dirs Stage 2 gave no content for.
2. **Feature folders.** For each entity-objective pair from Stage 2 "Features", create `features/<entity>-<objective>/` with only the slots that entity needs right now (see `docs/ARCHITECTURE.md` § Feature folder shape) — omit `views/phases/` unless "User / UX" named a multi-phase flow.
3. **`.cursor/rules/project-overview.mdc`.** Fill [`templates/project-overview.mdc.template`](templates/project-overview.mdc.template) from Stage 1/2 answers (objective, import law, on-demand rule table). Drop the `## {{MODULES_HEADING}}` section unless Stage 2 "Multiple journeys?" was yes. Project prose lives here, never in an entry file.
4. **Agent entry files.** Fill [`templates/ENTRY.md.template`](templates/ENTRY.md.template) once and write the identical result to `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex + generic agents) and `PROJECT_RULES.md` (v0). They only point at `.cursor/rules/` and `docs/` — one home for rules, every agent forced through it. `{{ALWAYS_ON_RULES_LIST}}` = one bullet per copied rule with `alwaysApply: true`, filled after step 6. Wire [`templates/check-entry-files.mjs.template`](templates/check-entry-files.mjs.template) as `scripts/check-entry-files.mjs` into `check` so the three copies can't drift.
5. **`.cursor/STRUCTURE.md`.** Fill [`templates/STRUCTURE.md.template`](templates/STRUCTURE.md.template) — scripts table from § Scripts below, routes from Stage 2 "Pages / routes", docs index pointing at the new project's own `docs/config/<stack>.md`, `docs/environment/*.md`, `docs/ARCHITECTURE.md`, `docs/SETUP.md`, `docs/DEPLOYMENT_STRATEGY.md`, `docs/CONTEXT.md`, `docs/CONFIG.md`.
6. **`.cursor/rules/*.mdc`.** Copy from `rules/` — always copy every file marked **Generic** in `docs/ARCHITECTURE.md`'s rules index (reword file paths/stack names inside as needed for the new framework); copy a **Generic, conditional** or **Generic pattern, conditional** file only when its condition matched Stage 2 (`external-integrations.mdc`, `background-jobs.mdc`, the shared-package cluster); target-specific mechanics are **docs, not rules** — copy only the `docs/environment/<target>.md` files for the deployment target and local-dev setup Stage 2 picked (see `docs/ARCHITECTURE.md` § Deployment-target docs) into the project's `docs/environment/`, write a new one in that same shape if the target has no worked example here yet, then fill [`templates/project-environment.mdc.template`](templates/project-environment.mdc.template) with one row per copied doc and copy `rules/project-config.mdc`. Never invent a new instance-specific rule file at scaffold time. Reword each copied file's product-specific nouns to the new project's own canonical nouns from `docs/CONTEXT.md`.
7. **Core docs.** Write the new project's own `docs/ARCHITECTURE.md`, `docs/SETUP.md`, `docs/DEPLOYMENT_STRATEGY.md`, `docs/CONTEXT.md`, `docs/CONFIG.md` using this skill's four docs as the section shape, filled with this project's real Stage 1/2/3 answers — never the content-studio example text. `DEPLOYMENT_STRATEGY.md` § 1 gets the strategy locked (or proposed-and-confirmed) in Stage 2.
8. **Package scripts.** Wire the verb table from `rules/scripts.mdc`, dropped to only the scripts the chosen stack and Stage 2 answers actually need (no `sync:secrets:*` without a secret manager, no `db:*` without a DB).
9. **Gates.** Wire a single pipeline script (`predeploy`/`pipeline` alias) chaining typecheck → lint → test → build → e2e, matching `rules/predeploy.mdc`. Add a PR/MR body template if the repo will take PRs, matching `rules/pull-requests.mdc`.
10. **Enforced checks.** Per `rules/dev-checks.mdc`: `check` script; `.githooks/pre-push` from [`templates/pre-push.template`](templates/pre-push.template); `scripts/setup-git-hooks.mjs` from [`templates/setup-git-hooks.mjs.template`](templates/setup-git-hooks.mjs.template), called from `setup` and `postinstall`; `.github/workflows/ci.yml` from [`templates/ci.yml.template`](templates/ci.yml.template) (drop it if the git host isn't GitHub — write that host's equivalent). Never scaffold docs-only gates.
11. **Deploy config.** If Stage 2 picked Vercel: `vercel.json` from the matching `templates/vercel.json.*.template` + `docs/environment/vercel.md` (referenced from `project-environment.mdc`). Always copy `rules/ai-contributors.mdc`.
12. **Confirm.** List every file written, and call out any Stage 2 answer that had no scaffold consequence (so the user can catch a dropped requirement).

## § Scripts

Canonical verb table lives in `rules/scripts.mdc` — reuse the verb names (`setup`, `dev`, `build`, `lint`, `typecheck`, `test`, `test:e2e`, `pipeline`/`predeploy`) so any future tooling shared across projects keeps working; drop verbs like `sync:secrets:*` unless the new project actually has that infra.

## Do not

- Do not run Stage 3 before Stage 1 + Stage 2 are both confirmed back to the user, including an explicit deployment-strategy answer.
- Do not invent a module-ownership table when Stage 2 said there is only one journey — that's `docs/ARCHITECTURE.md` § Module ownership pattern misapplied.
- Do not wire the shared-package tier for a single, standalone app with no sibling consumer — that tier exists to keep multiple apps in sync, not to add ceremony to one.
- Do not leave template placeholders (`{{LIKE_THIS}}`) in a written file — every placeholder must resolve to a real Stage 1/2 answer or the line is deleted.
