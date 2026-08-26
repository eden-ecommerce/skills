# Page structure — all stages

Generic rules for **section architecture**, **visible headings**, and **content refinement**. Applies to Desired Content (5), Draft (7), and Audit (8). Target overlays add field mapping only — do not duplicate these rules.

## Design philosophy

- **Buyer-intent spine (product):** default order in `templates/product.md` — adapt per brief, do not skip beats without reason.
- **One job per section:** each block answers one shopper question or serves one persuasion beat — never merge unrelated jobs into one panel.
- **Progressive disclosure:** promise → proof → differentiation → choice → confidence → action.
- **Refinement is continuous:** Stages 5–8 all produce **near-final reader copy**. Stage 8 is not “validation only” — it polishes titles, body text, comparison rows, and banner copy before sign-off.
- **More smaller blocks:** prefer splitting dense biography into titled tiles/highlights over one long `publisherSingleImageWithText` wall.

## Product module budget (soft ceiling)

Product strips: **6–9 content blocks** in `blocks[]`. Each block must justify its scroll with a unique buy question in `purpose`.

| Count | Action |
|---|---|
| ≤5 | OK if brief is narrow — document why in `narrativeNote` |
| 6–9 | Target range |
| ≥10 | Fail audit `module_budget` unless `narrativeNote` documents a documented exception |

Omit filler blocks (redundant maker CTA, duplicate theme grid, store-policy FAQ).

## Section titles + subtitles (hard)

Every block needs **two reader-visible lines** before body content:

| Field | Role | Maps to (Draft) |
|---|---|---|
| `sectionTitle` | H2 — shopper question or decision | panel `title` or `heading` |
| `sectionSubtitle` | One-line frame under the title | panel `subheading`, `text`, or first intro line |

Character limits: `copy-voice.md` → `heading_char_limits`. Gate 5 mockup must show **both** per block.

| Bad (internal / theme-only) | Good (title + subtitle) |
|---|---|
| `Hero` / (none) | **Title:** `Why this autobiography matters` **Subtitle:** `A memoir for readers who love honest faith and sharp thinking` |
| `Maker spotlight` / (none) | **Title:** `Who is John C. Lennox?` **Subtitle:** `The mathematician and apologist behind decades of public debate` |
| `Faith forged in conflict` / (none) | **Title:** `Who will enjoy this book?` **Subtitle:** `Seekers, gift buyers, and readers who want story before argument` |
| `FAQ` / (none) | **Title:** `Questions before you buy` **Subtitle:** `Format, audience, and how this differs from his other books` |

### Title field map (Draft)

Populate the schema field that **renders as the section H2** on preview:

| Panel family | Title | Subtitle |
|---|---|---|
| `publisherComparison` | `title` | `text` or intro line |
| `publisherComparisonChart` | `title` | `text` or intro line |
| `highlightBlock` | `title` | `heading` or `text` |
| `testimonials` | `title` | `heading` |
| `publisherFaq` / FAQ panels | `title` | `text` intro line |
| `publisherSingleImageWithText` | `heading` | `subheading` or short intro before `body` |
| `imageWithOverlayAndTextV2` | `heading` | `subheading` or overlay subline |
| `thinBanner` | `bannerText` | n/a (band is one line) |
| Tile grids (`publisherImage300x300V2`, etc.) | `title` | `text` or grid intro line |

**Rule:** if a field renders on the storefront, it must read like a **question, benefit, or decision** — never a production note.

## Panel spacing on the scroll

Users should **see distinct chapters** as they scroll:

- Every block opens with **title + subtitle** — a clear content-area header before tiles, body, or matrix.
- Alternate panel families — no three consecutive text-only blocks without imagery or a scannable grid between them.
- Alternate visual weight: hero → trust ribbon → image+text → grid/tiles → format chooser → product comparison → social proof → FAQ → closing band.
- Max 2 identical `_type` on one surface — different **titles, subtitles, and layout jobs** so repeats feel distinct.
- Draft: do not stack panels without the title/subtitle pair visible on preview.

Fail audit `section_subtitle_present` if any major block lacks a subtitle on preview. Fail `panel_spacing` if three text-heavy blocks run together without a visual break.

## Comparison shopper sections

When a `comparison` block exists, treat it as a **dedicated decision module**:

1. **Section title (question form):** `Which [maker] book should you choose?`, `Which format should you choose?`, `How does this compare to other [maker] titles?`
2. **Section subtitle:** one line framing the decision (e.g. `Compare memoir, devotion, and apologetics paths from the same author`).
3. **Row labels in `cells[0]`:** `What it is`, `Best for`, **`Skip if`** (required on works comparison — see `copy-voice.md` Skip if rules).
4. **Answers in `cells[1…n]`** — selective, scannable, no repeated question words. Skip-if cells = use-case elimination (5–8 words) that **point to another column**, never a dead end.

Format chooser (`publisherComparisonChart`) uses the same title discipline: `Hardback or ebook: which should you choose?`

## Pre-review checklist (before opening preview URL)

Run against `desiredPageContent.json` + `draftPatch.json` first. Audit Stage 8 re-checks on preview.

### Commerce (AOV / right product)
- [ ] Works comparison present with choose-or-skip across real alternatives
- [ ] **`Skip if` row present** on works comparison; each cell steers to another column (upsell / cross-sell), not a bounce
- [ ] Format/edition coverage complete (print / ebook / audio / seasonal as applicable)
- [ ] Carousel omits seed; seed comparison column has no Shop Now
- [ ] No price / stock / dispatch in panel copy
- [ ] **No jobs panels** on product strip

### User engagement
- [ ] Title + subtitle on every block; character limits respected
- [ ] One job per section; no tile reuse across panels
- [ ] Maker / themes / pathways / proof are distinct beats
- [ ] Comparison cures decision fatigue (Best for + Skip if as tie-breakers), not a feature dump
- [ ] FAQ does not fully rehash earlier panels
- [ ] Module budget 6–9 blocks (or documented exception)

### SEO
- [ ] Hero heading = product clarity + benefit, not buy-box title clone or intrigue-only
- [ ] Comparison H2 is a shopper question
- [ ] Outbound internal links (maker, category, programmes)
- [ ] FAQ long-tail objections only — **no store-policy dumps**

### Conversion
- [ ] Skip if uses **use-case language**, not product put-downs; **5–8 words** per cell
- [ ] No Skip-if **dead ends** (elimination without an in-table alternative)
- [ ] Product-fit objections covered once in FAQ — **not** generic returns/dispatch
- [ ] **One** outbound maker-catalogue CTA job on strip
- [ ] **CRE What Next:** late strip offers safe-step path for undecided scrollers (`cre-conversion.md`)
- [ ] **CRE outcome headlines:** hero/key H2s are benefit/story + product clarity
- [ ] **CRE hesitation gap:** top 2–3 `topHesitations` each answered once in pathway or FAQ
- [ ] **CRE cross-sell harmony:** strip carousel (if any) complements FBT/For you, not duplicate job
- [ ] **Palette consistency** across bands and accents (`eden.md` + `visualSystem`)

## Stage 5 output contract

Each `blocks[]` entry must include:

```json
{
  "id": "comparison-bear-grylls",
  "layout": "comparison",
  "sectionTitle": "Which Bear Grylls book should you choose?",
  "sectionSubtitle": "Compare gospel narrative, devotion, kids, and autobiography in one view",
  "purpose": "Comparison shopper: choose-or-skip across same-author catalogue",
  "buyQuestion": "What makes it different?",
  "personaFit": ["Comparison shopper"],
  "headline": "Which Bear Grylls book should you choose?",
  "body": "One-line frame only if subtitle is not enough.",
  "comparisonRows": [
    { "label": "What it is", "answers": ["...", "..."] },
    { "label": "Best for", "answers": ["...", "..."] },
    { "label": "Skip if", "answers": ["...", "..."] }
  ]
}
```

`sectionTitle` and `sectionSubtitle` are mandatory for every block. `buyQuestion` = one of `Why buy?` | `Who is it for?` | `What makes it different?`. Gate 5 mockup must show title + subtitle per block, not only `blockId` or `purpose`.

## Stage 7 mapping

- Map `blocks[].sectionTitle` → panel `title` or `heading` (per table above).
- Map `blocks[].sectionSubtitle` → panel `subheading`, `text`, or intro line — never drop on mutate.
- Never drop section titles during panel mapping.
- `panelsUsed[].purpose` = internal; panel `title`/`heading`/`subheading` = reader-facing.

## Quality pillars (Gate 5 + Gate 8)

Score each pillar with evidence before sign-off:

| Pillar | Strip must deliver | Must not |
|---|---|---|
| **Commerce** | Choose-or-skip vs other titles; **Skip if** steers to adjacent columns / upsell; format/edition coverage; outbound maker/category links | Seed Shop Now; seed in carousel; price/stock/dispatch copy; Skip if with no alternative column; jobs widgets |
| **Engagement** | Title + subtitle per block; maker authority, themes, distinct pathways; comparison as tie-breaker; scannable short copy | Duplicate tiles; FAQ rehash; three text walls; intrigue-only hero |
| **SEO** | Benefit H2s, FAQ long-tail, outbound internal links; comparison title as shopper question | Second buy-box title as hero; keyword stuffing; CMS jargon |
| **Conversion** | Skip if use-case language (5–8 words), no dead ends; product-fit objections FAQ; one maker CTA; trust via honest elimination; **CRE:** outcome headlines, safe-step CTAs, hesitation gap covered, What Next closing, cross-sell harmony | Self-PDP CTAs; harsh Skip if; garbled policy copy; Buy now / Add to basket in strip; FBT-clone carousel; duplicate maker CTAs |

## Dedup rules (hard)

- **One job per block** — voices/themes ≠ audience pathways ≠ social proof ≠ FAQ
- **No tile reuse** — identical `title`+`body` or same image `_ref` across panels = fail
- **Cardinality fill on-job** — N required tiles → N items for **this** panel’s purpose
- **FAQ no rehash** — FAQ answers objections not already solved above
- **One outbound maker CTA job** — single catalogue browse path (any panel family) unless jobs differ clearly
- **Hero ≠ buy-box title clone** — hero heading is promise + product clarity

## Stage 8 refinement (titles + copy)

Before checklist, verify on preview scroll:

- [ ] Every major section has visible **title + subtitle**
- [ ] Heading character limits (`copy-voice.md`)
- [ ] Comparison module title is a **clear question** (not “comparison” or maker name only)
- [ ] Row labels present: `What it is`, `Best for`, **`Skip if`**
- [ ] Skip if cells: 5–8 words, use-case not flaw, each points to another column (no dead ends)
- [ ] Copy voice rules (`copy-voice.md`) applied — fourth-wall ban, scannable body, markdown 3-line limit
- [ ] No cross-panel tile reuse; audience tiles are distinct pathways
- [ ] Carousel omits seed; seed comparison column has no Shop Now
- [ ] FAQ does not fully rehash earlier panels; no store-policy FAQ
- [ ] Module budget respected; panel spacing readable
- [ ] A+ panels **visible** on seed product preview

Fail audit `section_titles_visible`, `section_subtitle_present`, `heading_char_limits`, `panel_spacing`, `comparison_title_question`, `no_cross_panel_tile_reuse`, `carousel_no_seed`, `faq_no_rehash`, or `panels_visible_on_preview` if any check fails.
