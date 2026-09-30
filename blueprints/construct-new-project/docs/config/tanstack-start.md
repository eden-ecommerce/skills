# Config — TanStack Start

Applies when root `package.json` lists `@tanstack/react-start` (typical for Lovable-hosted repos). Record in `docs/CONFIG.md` § Stack (`STACK = tanstack-start`). Stack choice is effectively irreversible once a builder owns the repo — confirm at intake.

| Item | Value |
|---|---|
| Routes | `src/routes/` (file-based) |
| Route-only UI | `src/routes/.../-components/`, `-sections/` |
| Dev / E2E port | `5173` (`vite.config.ts` `strictPort`; Playwright must match) |
| Ship gate | `pnpm check && pnpm build` — no `predeploy` |
| `vercel.json` | `"framework": "tanstack-start"` — `templates/vercel.json.tanstack.template` |
| Deploy adapter (Nitro) | build-only in `vite.config.ts`; never during `vite dev` |
| Lovable | `.lovable/project.json`; keep the repo's own `vite.config.ts` — don't swap in a builder wrapper config |
| Server mutation | `createServerFn` in `data/<Capability>/` |
| Server read | route `loader` calling `get*Server.ts` |
| Client read | `get*Client.ts` + TanStack Query |
| Server-only code | `*.server.ts` |
| Client env | `import.meta.env.VITE_*` only |
| Images / assets | Vite imports |
| Links | router `Link` / `redirect({ to })` |
| Private shared packages | usually none — builders lack the registry token |

## Review checks

- Ship command is `check` + `build`
- `vite.config.ts` has build-only deploy adapter, fixed port
- Playwright port matches dev port
- `docs/CONFIG.md` exists, `STACK = tanstack-start`

## Not for Next.js apps

`app/`, `predeploy`, `next/image`, `next.config.ts`.
