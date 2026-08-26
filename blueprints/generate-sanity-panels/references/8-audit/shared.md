# Audit — shared

Stage 8. In: `previewUrl`, `draftPatch`, `pageWithMedia` path, `domainSnapshot`, `definitionBundle` (seed identifier). Out: `auditResult.json`

Applies to **all targets**. Target overlays add surface-specific checklist rows only.

**Hard:** Audit subagent MUST open `previewUrl` in browser. No pass without preview evidence. Soft skip forbidden — browser unavailable → fail `preview_unavailable`.

## Process

1. Navigate `previewUrl` — fail `preview_host` if forbidden production host
2. Scroll **full surface** top→bottom
3. Screenshot hero + every image/matrix/FAQ block
4. **Refinement pass (mandatory before checklist):** edit `draftPatch` / re-push if needed:
   - **Section titles + subtitles:** user-facing questions/benefits + one-line frame on every major panel; comparison title in question form (`page-structure.md`)
   - **Heading char limits** and **scannable body** per `copy-voice.md` — split dense paragraphs; cut CMS jargon
   - **Hero product clarity** — what the product is + why it matters (not intrigue-only)
   - Strip all em-dashes from copy (`references/shared/copy-voice.md`)
   - Shorten `thinBanner` bodies; fix dark-on-dark CTA contrast
   - Trim `publisherComparison` to ≤4 columns with full row cells
   - **Skip if row:** ensure present; rewrite long/harsh/dead-end cells per `copy-voice.md`
   - Split maker quotes into testimonials; add creator `thinBanner` with outbound link (only one maker CTA job)
   - Remove markdown syntax from plain string fields; enforce 3-line max per markdown paragraph
   - Remove jobs panels and store-policy FAQ items from product strips
   - Re-check comparison last column on preview (empty slot = fail)
   - **CRE pass:** hero clarity, outcome headlines, safe-step CTAs, hesitation gap coverage, no chrome repetition, cross-sell harmony, What Next closing, one maker CTA (`cre-conversion.md`)
5. Run **deterministic checklist** against **visible preview + `draftPatch` JSON** (both required) — include Skip if + CRE ids
6. Prohibited content scan
7. Write `auditResult.json` — any checklist fail → `pass: false`

## Deterministic checklist

Each row: `pass` or `fail` + one-line `evidence`. Target overlays add rows only.

| id | Check | How |
|---|---|---|
| `preview_opened` | Preview loaded from `previewUrl` | Browser navigate + title/DOM |
| `preview_host` | Not forbidden production preview host | URL host vs `domainSnapshot` rules |
| `draft_id` | Doc uses `drafts.` prefix where required | `draftPatch` JSON |
| `no_markdown_panel` | No `markdown` `_type` in panels | JSON |
| `no_richtext_panel` | No `richText` `_type` in panels | JSON |
| `max_two_same_type` | ≤2 identical panel `_type` | count |
| `no_self_surface_links` | No link/CTA to seed content surface URL | JSON + preview vs seed identifier from `definitionBundle` / target constants |
| `no_commerce_chrome_copy` | No price/stock/availability/dispatch in panel copy | JSON + preview |
| `no_internal_ids_in_copy` | No raw `productId`, “product NNNNN”, or Sanity `_id` in reader text | JSON + preview |
| `human_entity_links` | Entity refs show human label + working **outbound** link/CTA | Preview |
| `matrix_column_align` | Matrix column header matches cell copy under it | Preview column-by-column |
| `matrix_no_empty_cells` | No empty, dash-only, or blank matrix cells | Preview + JSON |
| `matrix_row_labels` | `publisherComparison` rows have question label in `cells[0]` | JSON + preview |
| `variant_headers_clear` | Variant siblings show discriminating labels, not duplicate titles only | Preview |
| `ticks_cells_safe` | No `ticks` + prose `cells` in same row | Preview + JSON |
| `required_fields` | Schema-required fields present | JSON vs target overlay |
| `panel_cardinality` | Repeater panels match exact counts | JSON + preview |
| `image_source_policy` | Generated art = Sanity refs; catalogue = picker/CDN; no broken images | JSON + preview |
| `media_lock_honored` | Imaged blocks use Media-locked `_type` / dims | JSON compare |
| `domain_visual` | Domain imagery rules; safe zones readable | Preview screenshots |
| `no_em_dash` | No `—` `–` `\u2014` `\u2013` in reader copy | JSON scan + preview |
| `no_markdown_syntax` | No `>`, `**`, `[text](url)` in plain string fields | JSON |
| `banner_copy_short` | Each `thinBanner.bannerText` ≤ ~15 words | JSON + preview |
| `banner_cta_contrast` | Light CTA text on dark banner backgrounds | Preview + JSON colours |
| `comparison_max_four` | `publisherComparison` ≤4 columns, all cells filled | JSON + preview |
| `layout_rhythm` | No three consecutive text-only blocks; varied panel types | Preview scroll |
| `section_titles_visible` | No internal-only titles (`Hero`, `Maker spotlight`, `FAQ`) visible on preview | Preview scroll |
| `comparison_title_question` | `publisherComparison.title` is a shopper question (e.g. which book to choose) | JSON + preview |
| `image_not_distorted` | Covers/tiles not stretched or squashed | Preview screenshots |
| `no_cross_panel_tile_reuse` | No identical title+body (or same image `_ref`) across two panels | JSON scan of tile/grid items |
| `cardinality_fill_on_job` | Repeater counts filled with items matching **this** panel’s purpose only — never pad from another block | JSON purpose vs tile titles |
| `faq_no_rehash` | FAQ answers do not fully restate a prior panel’s primary beat | Preview scroll + draft |
| `dedup_preview_scroll` | No duplicate heading or tile body appearing twice on full scroll (A+ strip only) | Preview scroll |
| `commerce_pillars_preflight` | Commerce / Engagement / SEO / Conversion rows each have pass evidence (see `page-structure.md` pre-review checklist) | Checklist scores + evidence |
| `skip_if_row_present` | Works `publisherComparison` includes a `Skip if` (or `Not for you if`) row in `cells[0]` | JSON + preview |
| `skip_if_scannable` | Each Skip-if product cell is **5–8 words** (not a paragraph) | JSON word count + preview |
| `skip_if_use_case_not_flaw` | Skip-if copy is use-case / lifestyle need — not product put-downs (“low quality”, “bulky”, “cheap”) | Preview + JSON |
| `skip_if_points_to_alternative` | Each Skip-if cell logically matches another column’s `Best for` (no dead-end eliminations) | Column-by-column preview walk |
| `skip_if_upsell_ready` | Where a higher-tier / sibling need exists in findings, seed Skip-if steers toward that column’s job | Findings + matrix |
| `outcome_headlines` | Hero / key H2s are benefit-or-outcome, not buy-box title or page-count dumps | Preview + JSON |
| `safe_step_ctas` | Strip CTAs are low-friction outbound; no Add to basket / Buy now / Shop now on seed | JSON + preview |
| `hesitation_gap_covered` | Each `topHesitations` item answered once in FAQ or dedicated pathway block | `desiredPageContent.hesitationGapMap` + preview |
| `no_chrome_repetition` | Closing/mid panels add new context vs description/FBT clone | Preview scroll |
| `cross_sell_harmony` | Strip carousel (if any) does not duplicate FBT job; complements chrome | Preview + block purpose |
| `what_next_closing` | Late strip has clear What Next path (closing band or equivalent safe-step CTA) | Preview scroll |
| `customer_facing_copy` | No CMS/merchandising/meta jargon or Helpdesk placeholders in reader text | JSON scan + preview |
| `scannable_body` | Short paragraphs; one idea per para; no opening wall-of-facts; sentences ~≤30 words | JSON + preview |
| `markdown_paragraph_limit` | Markdown body fields: ≤3 lines per paragraph | JSON |
| `heading_char_limits` | Titles/subtitles within `copy-voice.md` character ranges | JSON char count |
| `section_subtitle_present` | Every major block has visible subtitle/subline on preview | Preview scroll |
| `panel_spacing` | No three consecutive text-heavy blocks without visual break | Preview scroll |
| `hero_product_clarity` | Hero communicates what the product is + why it matters (not intrigue-only) | Preview + JSON |
| `buy_question_per_block` | Each block `buyQuestion` maps to Why buy / Who for / Different | `desiredPageContent` + preview |
| `module_budget` | Product strip has 6–9 blocks unless documented exception | `desiredPageContent` |
| `one_maker_cta` | Single maker-catalogue CTA job on strip | JSON + preview |
| `no_jobs_widget` | No `featuredOrganisationJobs` / jobs search panel `_type` on product strip | JSON |
| `no_store_policy_faq` | FAQ has no generic returns/dispatch/Helpdesk policy dump | JSON + preview |
| `palette_consistency` | Banners/accents match locked `visualSystem.palette` from Stage 6 | Preview + JSON colours |

**Image policy:** fail broken images and generated slots using raw external URLs when Sanity asset required. Picker-backed catalogue covers OK.

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
    "screenshots": ["hero", "comparison", "faq"]
  },
  "scores": { "personas": 0, "briefFit": 0, "visual": 0 }
}
```

`flags[]` = failed checklist ids. Fail → orchestrator restarts Definition with `auditFlags`.

## Gate presentation (orchestrator)

Show checklist table: **id | pass/fail | evidence**. **No Gate 8 without `auditResult.json` and preview evidence.** Pass required before Publish.
