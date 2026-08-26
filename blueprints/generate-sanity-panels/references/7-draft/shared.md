# Draft — shared

Stage 7. In: `pageWithMedia`, `target`, `template`, `domainSnapshot`. Out: `draftPatch`, `previewUrl`, `panelsUsed[]`

Applies to **all targets**. Target overlays name panel field + seed identifier only.

## Process

1. `bash scripts/fetch_schema.sh <domainSnapshot.cms.schemaUrl>` if cache stale — read `.cache/*-panels.json` for **active target** allowlist only
2. Fetch gallery from `domainSnapshot.urls.gallery` — parse `#panel-catalogue` JSON
3. Screenshot key `_type`s at 375 / 768 / 1280 if browser available
4. **Gallery-first mapping:** map `pageWithMedia` sections to best-fit panel by **content job** — honor each block's `sectionTitle` + `sectionSubtitle` on the panel fields that render as H2 + subline (see `references/shared/page-structure.md`)
5. Honor `imageBrief[].targetPanelType` **1:1** — no silent remap after Media
6. Never more than 2 identical `_type` on surface
7. **Reject banned panel types:** never `markdown` or `richText` `_type` — pick gallery alternatives. On product strips: never `featuredOrganisationJobs`, `organisationJobSearch`, `appJobs`
8. Query current doc via HTTP — patch draft — see `http-sanity.md`
9. Overwrite catalogue facts from `products[]` after LLM copy
10. Build `previewUrl` from `domainSnapshot.urls.preview`
11. **Reader copy:** human labels + **outbound** links from `products[]` — strip raw internal IDs
12. **Link policy:** remove or replace any `edenLink` / CTA URL pointing to seed content surface (see target overlay for seed key)
13. **Fill schema-required fields** before mutate (see target overlay) — **on-job only**; never copy tiles from another panel to satisfy cardinality
14. **Comparison matrices:** max **4 product columns**; `cells[0]` = row label; include **`What it is` / `Best for` / `Skip if`** on works comparison; Skip-if cells 5–8 words, use-case framed, each pointing to another column; no dash placeholders; no `ticks` + prose `cells` same row; seed column has **no** Shop Now / seed PDP link
15. **Copy voice:** apply `references/shared/copy-voice.md` — fourth-wall ban, scannable body, heading char limits, markdown 3-line paragraph cap; strip em-dashes, markdown syntax in plain fields; short banners; accessible CTA colours; maker quotes in testimonials + creator banner panel; **Skip if** conversion rules
16. **Section titles:** map `sectionTitle` / `sectionSubtitle` / `headline` to reader-facing `title`, `heading`, `subheading`, or `text`; never ship internal labels (`Hero`, `Maker spotlight`, `FAQ`) as visible titles (`references/shared/page-structure.md`)
17. **Dedup before mutate:** scan all tile/grid `title`+`body` (+ image `_ref`); fail and remap if any pair repeats across panels
18. **FAQ trim:** drop or shorten items that fully rehash a prior panel’s primary answer
19. **Carousel:** omit seed id from `products` and `sponsoredProducts`; `showPrice: false`

## Image assets

- **Generated/custom:** Sanity `asset._ref` from `mediaPlan.sanityAssetRef`
- **Catalogue:** `edenProductPicker.productIds` when schema supports — storefront resolves covers; do not upload catalogue covers to Sanity
- Reject generated assets that failed domain visual check

## Out (single canonical artifact set)

Write **one** `draftPatch.json` + **one** `draftResult.json`. Do not write parallel `draft-panels.json`, `panelsUsed.json`, or stub `draftResult` without panel bodies.

```json
{
  "draftPatch": { "documentId": "drafts....", "panels": [...] },
  "previewUrl": "https://...",
  "panelsUsed": [ { "_type": "...", "purpose": "..." } ]
}
```

One write path only — do not duplicate panel trees in `mutations[].patch.set` and top-level `set`.

Gate: user checks preview link summary before audit.
