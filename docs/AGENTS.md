# AGENTS.md template

Copy into target repo root. Adjust per project.

## Context

- you MUST use `/caveman ultra`
- Cursor Build: you MUST use `/ponytail`
- post-Build review: `/ponytail-review`; milestone sync: `/ponytail-audit`
- follow active sub-plan: `docs/task/<feature-task-slug>/{feature}-{subtask}-sub-plan.md`
- run project scripts via `pnpm` in correct docker container (per STRUCTURE)
- styling: tailwindcss — tailwind-merge, tailwind-variants
- network requests: react query hook files
- page performance: component boundaries, server/client tradeoffs, Suspense / PPR
- icons: LucideIcons pnpm package

## Coding Standards

- never `any` or `unknown` — infer types from method result, API SDK, or package types
- react hooks: strict usage — `useCallback` usually unnecessary; avoid `setTimeout` prefer awaited promises; `useEffect` chains renders; `useMemo` only for stable expensive data
- SOLID + atomicity — one concern per component
- methods: unit testable, one measurable outcome
- dynamic keys: extendable switch + exhaustive check + `assertNever()`
- KISS — minimal diff, no excess casting/validation
- DRY — reuse existing Presenter components and structures

## File Structure

- `hooks` — react query: getKey, getOptions, server fetchMethod, client useHook
- `app` — Next.js routes, page entry server logic
- `components` — hierarchical dirs e.g. `forms/CreateUserForm/sections/BasicSection/` — ui, zod schema, hook per section
- `data` — server actions; `data/User/CreateUser` with dal/dto/dpo per model
