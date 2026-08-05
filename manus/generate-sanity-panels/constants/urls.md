# URLs

| Constant | Env var | Example |
|---|---|---|
| Next Eden base | `NEXT_NEXT_EDEN_BASE_URL` | `https://eden-xi.vercel.app` |
| Eden Blog base | `EDEN_BLOG_BASE_URL` | `https://eden-blog-beta.vercel.app` |
| Sanity project | `NEXT_PUBLIC_SANITY_PROJECT_ID` | (from `scripts/.env`) |
| Sanity dataset | `NEXT_PUBLIC_SANITY_DATASET` | (from `scripts/.env`) |
| Sanity schema | — | `https://cms.eden.co.uk/schema.json` |

Domain-specific gallery + preview paths live in `constants/domains/{id}.md`.
Resolve CMS `projectId` / `dataset` from env (never hardcode in refs).
