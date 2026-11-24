# AGENTS.md template

Copy into target repo root. Adjust per project.

## Context

- you MUST use `/caveman ultra` in chat. Plan files and merge request bodies stay in normal sentences
- Cursor Build: you MUST use `/ponytail`
- post-Build review: `/ponytail-review`
- follow the active sub in the master plan: `docs/feature/<feature>/<feature>-master-plan.md`, heading `## Sub {step}`
- rules for this repo are listed on the master plan **Repos** row. Read that list before planning or editing. It includes `.cursorrules`, this file, and `.cursor/rules/`

## Git

Hard human gate. A person lands code on `main` and `master`.

- Before `git push`, read `git branch --show-current`. Stop when that branch is `main` or `master`.
- Stop when the refspec is `main`, `master`, `HEAD:main`, or `HEAD:master`.
- Do not `gh pr merge` or `glab mr merge`.
- Do not commit on `main` or `master`. Use a feature branch.
- Do not change git config. Do not pass `--author` or `--trailer`.
- Message is one line: `type(entity): outcome`. Type is `fix`, `chore`, `doc`, or `feature`. Entity is the table or the domain. Outcome is the task result, caveman, no filler.
- No `Co-authored-by`. No `Signed-off-by`. No model provider as author or committer.
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
