# Draft — MCP Sanity

Sanity via `manus-mcp-cli`. Server `sanity`. Project/dataset from `domainSnapshot.cms` (resolved from `NEXT_PUBLIC_SANITY_PROJECT_ID` / `NEXT_PUBLIC_SANITY_DATASET` at Definition).

Requires env loaded: `set -a && source scripts/.env && set +a`

## Query document

```bash
manus-mcp-cli tool call query_documents --server sanity --input '{
  "query": "*[_type == \"product\" && product_id == \"<ID>\"][0]",
  "resource": { "projectId": "'"$NEXT_PUBLIC_SANITY_PROJECT_ID"'", "dataset": "'"$NEXT_PUBLIC_SANITY_DATASET"'" }
}'
```

Article:

```bash
manus-mcp-cli tool call query_documents --server sanity --input '{
  "query": "*[_type == \"article\" && slug.current == \"<slug>\"][0]",
  "resource": { "projectId": "'"$NEXT_PUBLIC_SANITY_PROJECT_ID"'", "dataset": "'"$NEXT_PUBLIC_SANITY_DATASET"'" }
}'
```

Prefer substituting `domainSnapshot.cms.projectId` / `dataset` when already resolved.

## Patch draft

Use `patch_documents` with `drafts.{publishedId}` when published doc exists.

Panels array: unique `_key` per item. Image fields = Sanity asset refs.

## Upload asset

`create_asset` or domain equivalent when MCP exposes it. Else stage 6 must supply refs.

## Fallback (when `manus-mcp-cli` unavailable)

Use deprecated helpers under `skills/deprecated/manus/generate-sanity-panels/scripts/`:

- `upload_image.mjs` — local file or URL → Sanity asset ref
- Query/mutate via Sanity HTTP API with write token (hub `Sanity.tsx` token only as local-dev fallback)

Still draft-only. Never publish here.
