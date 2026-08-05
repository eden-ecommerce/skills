# Draft — shared

Stage 7. In: `pageWithMedia`, `target`, `template`, `domainSnapshot`. Out: `draftPatch`, `previewUrl`, `panelsUsed[]`

## Process

1. `bash scripts/fetch_schema.sh` if cache stale — read `.cache/*-panels.json` allowlist only
2. Fetch gallery page from `domainSnapshot.urls.gallery` — parse `#panel-catalogue` JSON
3. Screenshot key `_type`s at 375 / 768 / 1280 if browser available
4. Map `pageWithMedia` sections to best-fit panel previews — **honor `imageBrief[].targetPanelType`** (1:1; no silent remap)
5. Never more than 2 identical `_type` on page — use variations
6. Never `markdown` panel `_type` — use gallery alternatives
7. Query current doc via MCP — patch draft — see `mcp-sanity.md`
8. Overwrite catalogue facts from `products[]` after LLM copy
9. Build `previewUrl` from `domainSnapshot.urls.preview`
10. **Reader copy:** strip raw internal IDs from panel strings — use human labels + links from `products[]`
11. **Fill schema-required fields** before mutate (see target overlay)
12. **Comparison matrices:** every row × every column filled — no empty cells, no `—` placeholders; column i = entity i

## Image assets

- **Generated/custom:** Sanity `asset._ref` from `mediaPlan.sanityAssetRef`
- **Catalogue:** `edenProductPicker.productIds` — storefront resolves covers; do not upload catalogue covers to Sanity
- Reject generated assets that failed domain visual check

## Out (single canonical artifact set)

Write **one** `draftPatch.json` + **one** `draftResult.json` (wraps patch + previewUrl). Do not write parallel `draft-panels.json`, `panelsUsed.json`, or stub `draftResult` without panel bodies.

```json
{
  "draftPatch": { "documentId": "drafts....", "panels": [...] },
  "previewUrl": "https://...",
  "panelsUsed": [ { "_type": "...", "purpose": "..." } ]
}
```

Do not duplicate panel trees in both `mutations[].patch.set.panels` and top-level `set.panels` — one write path only.

Gate: user checks preview link summary before audit.
