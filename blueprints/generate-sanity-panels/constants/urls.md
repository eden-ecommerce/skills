# URLs and run credentials

**Nothing is hardcoded.** Collect every value at FIRST RUN / Definition (same gate as `productId`). Pass them on every script via env prefix (`VAR=value python3 …`) or `--flags`. Never commit values. Never paste tokens into gate summaries or artifacts.

| Credential | Env var | CLI flag | When |
|---|---|---|---|
| Sanity project id | `NEXT_PUBLIC_SANITY_PROJECT_ID` | `--project-id` | Always |
| Sanity dataset | `NEXT_PUBLIC_SANITY_DATASET` | `--dataset` | Always |
| Sanity editor token (read+write) | `SANITY_API_EDITOR_TOKEN` | `--token` | Draft, upload, query, publish |
| Sanity preview token | `SANITY_PREVIEW_TOKEN` | (preview URL only) | Building `previewUrl` |
| Preview / gallery host | `NEXT_NEXT_EDEN_BASE_URL` | — | Web surfaces (product, most galleries) |
| Blog / article host | `EDEN_BLOG_BASE_URL` | — | `target=article` |
| Schema JSON URL | — | `fetch_schema.sh <schemaUrl>` | Always |
| Algolia app id | `ALGOLIA_APP_ID` | `--algolia-app-id` | Catalogue is Algolia (`target=product` on Eden) |
| Algolia search key | `ALGOLIA_SEARCH_KEY` | `--algolia-search-key` | Same as app id |

Domain files under `constants/domains/` describe **patterns** (`{NEXT_NEXT_EDEN_BASE_URL}/panels/product`). Substitute user-supplied hosts at Definition into `domainSnapshot.urls`.

Create a Sanity editor token in [Sanity manage](https://www.sanity.io/manage) → API → Tokens (read+write). Preview token is whatever the storefront `/api/preview` route expects.

`scripts/.env.example` lists names only. Do not fill it in the skill tree.
