# Audit — shared

Stage 8. In: `previewUrl`, `draftPatch`, `pageWithMedia` path, `domainSnapshot`. Out: `auditResult.json`

**Hard:** Audit subagent MUST open `previewUrl` in browser (Cursor browser / MCP). No pass without preview evidence. Soft skip forbidden — if browser unavailable, fail with `preview_unavailable`.

## Process

1. Navigate `previewUrl` — fail `preview_host` if forbidden production host (e.g. `www.eden.co.uk` for Eden drafts)
2. Scroll **full page** top→bottom
3. Screenshot hero + every image/matrix/FAQ block (or equivalent full-page capture set)
4. Run **deterministic checklist** below against **visible preview + `draftPatch` JSON** (both required)
5. Prohibited content scan — profanity, explicit, dangerous, hate
6. Write `auditResult.json` — any checklist fail → `pass: false`

## Deterministic checklist

Each row: `pass` or `fail` + one-line `evidence`. Target overlays add schema-specific rows only.

| id | Check | How |
|---|---|---|
| `preview_opened` | Preview loaded from `previewUrl` | Browser navigate + title/DOM |
| `preview_host` | Not forbidden production preview host | URL host vs `domainSnapshot` rules |
| `draft_id` | Doc uses `drafts.` prefix where required | `draftPatch` JSON |
| `no_markdown_panel` | No `markdown` `_type` in `panelsUsed[]` | JSON |
| `max_two_same_type` | ≤2 identical panel `_type` | count |
| `no_commerce_chrome_copy` | No price/stock/availability/dispatch strings in panel copy | JSON string scan + preview text |
| `no_internal_ids_in_copy` | No raw `productId`, “product NNNNN”, or Sanity `_id` in reader-visible text | JSON + preview FAQ/body |
| `human_entity_links` | Entity refs show human label (title, format/variant, maker) + working link/CTA | Preview |
| `matrix_column_align` | Each comparison/matrix column header matches cell copy under it | Preview column-by-column |
| `matrix_no_empty_cells` | No empty, dash-only, or blank comparison cells — every column in every row has real copy or intentional tick only | Preview + JSON (`cells[]` length = column count; no `""` / `"—"` placeholders) |
| `variant_headers_clear` | Same-title variants show discriminating labels (format/tier), not duplicate titles only | Preview |
| `ticks_cells_safe` | No ticks+prose mashup that shifts columns | Preview + JSON |
| `required_fields` | Schema-required fields present (see target overlay) | JSON vs known required list |
| `panel_cardinality` | Repeater panels match exact counts (e.g. 3-up = 3 images) | JSON + preview |
| `image_source_policy` | Generated art = Sanity refs; catalogue = picker IDs or CDN (no wasted cover re-upload); no broken images on preview | JSON + preview |
| `media_lock_honored` | Imaged blocks use Media-locked `_type` / dims from `pageWithMedia.imageBrief` | JSON compare |
| `domain_visual` | Domain imagery rules; hero not raw catalogue paste; safe zones readable | Preview screenshots |

**Image policy:** fail broken images and generated slots using raw external URLs when Sanity asset required. Catalogue covers resolved via `edenProductPicker` / CDN are OK — do not fail picker-backed panels for lacking Sanity cover uploads.

## Out

```json
{
  "pass": true,
  "flags": [],
  "checklist": [
    { "id": "preview_opened", "result": "pass", "evidence": "..." }
  ],
  "previewEvidence": {
    "url": "https://...",
    "screenshots": ["hero", "comparison-format", "comparison-works", "faq"]
  },
  "scores": { "personas": 0, "briefFit": 0, "visual": 0 }
}
```

`flags[]` = stable ids of failed checklist items. Fail → orchestrator restarts Definition with `auditFlags`.

## Gate presentation (orchestrator)

Show checklist table: **id | pass/fail | evidence** — not vibes summary alone. Pass required before Publish.
