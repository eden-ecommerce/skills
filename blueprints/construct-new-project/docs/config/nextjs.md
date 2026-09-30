# Config — Next.js App Router

Applies when root `package.json` lists `next` and not `@tanstack/react-start`. Record the choice in `docs/CONFIG.md` § Stack (`STACK = nextjs`).

| Item | Value |
|---|---|
| Routes | `app/` |
| Route-only UI | `app/<route>/_components/` |
| Dev / E2E port | `3000` (`playwright.config.ts` must match) |
| Ship gate | `pnpm predeploy` (`pipeline` alias). Vercel Checks: `lint` + `typecheck` |
| `vercel.json` | `"framework": "nextjs"` — `templates/vercel.json.nextjs.template` |
| Server mutation | Server Actions in `data/<Capability>/` |
| Server read | `get*Server.ts` from a React Server Component |
| Client read | `get*Client.ts` + TanStack Query |
| Images | `next/image` with explicit `width` + `height` |
| Links | `next/link` |
| Env | `NEXT_PUBLIC_*` for browser; validate required production env in `next.config.ts` |
| Vercel env | `vercel link` → `pnpm pull:env` → `.env.local` |

## Review checks

- Ship command is `predeploy`; CI runs typecheck → lint → build
- No request-time API (`cookies`, `headers`, `draftMode`) outside `<Suspense>`; no `force-dynamic`
- `docs/CONFIG.md` exists, `STACK = nextjs`

## Not for TanStack Start apps

`app/`, `predeploy`, `next/image`, `next.config.ts`.
