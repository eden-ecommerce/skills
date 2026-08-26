# Desired Content — shared

Stage 5. In: `target`, `brief`, `personas`, `findings`, `products`. Out: `desiredPageContent.json`

Applies to **all targets** (`product`, `article`, `email`). Target overlays add surface chrome boundaries and seed identifier shape only.

## Creative mandate

Unconstrained design for **content hierarchy + persuasion** — not unimplemented web-app motion. Senior content / ecommerce design voice.

Load **`references/shared/page-structure.md`** for section architecture, visible titles, and scroll rhythm. Load **`references/shared/copy-voice.md`** for copy rules. Load **`references/shared/cre-conversion.md`** for bottom-of-PDP conversion (product target).

- **No Sanity panel `_type` limits at design time** — Draft maps blocks later (`targetPanelType` hint OK). **Never design for `markdown` or `richText` panel types.**
- **No obligation to mirror live chrome, retailer strip conventions, or template spine** — invent the ideal surface for the brief. Do not copy retailer A+/layout models because the brief mentioned a retailer.
- **Product module budget:** 6–9 blocks in `blocks[]` unless `narrativeNote` documents an exception (`page-structure.md`)
- Ground **facts** in `findings` + `products` only — no invented endorsements or ratings
- **Never render live commerce chrome in copy** — no prices, stock, availability, dispatch (they change; live surface often already shows them). Entity modules: title, maker, format/variant, cover, **outbound** link only
- **Reader-facing copy** — human labels + **outbound** URLs. Never raw internal IDs in body/FAQ/CTA text
- Respect `sourcePolicy` for attributed claims
- **Do not specify** `motionIntent`, parallax, sticky surface chrome, accordion JS — Draft maps to real panels only

## Link policy (all targets)

**Never link to the seed content surface the user is already on.**

| Allowed | Not allowed |
|---|---|
| Maker / brand catalogue page on domain | Seed surface URL (same slug, `productId` path, article URL, email landing) |
| Publisher / imprint / organisation page | CTA that only reloads current surface |
| **Other** catalogue entities (siblings, alternatives, variant SKUs) | Seed column / hero link when URL = seed surface |
| Trusted external (publisher site, cited review source) | Domain home with no navigation value |

Every `ctaUrl` and inline link must be **outbound** from the seed surface. Target overlay names the seed key (`productId`, slug, campaign URL).

## Panel type bans

Never specify or imply these panel `_type`s in `imageIntent.targetPanelType` or Draft mapping:

- `markdown`
- `richText`
- `featuredOrganisationJobs` (product strips — conversion leak)
- `organisationJobSearch`, `appJobs` (product strips)

Use structured panels: hero overlays, highlight grids, FAQ panels, labelled comparison charts, tile grids, carousels, testimonial blocks, CTA bands, image+text sidebars.

## Comparison / matrix modules (when used)

Use `layoutKind: comparison` in Stage 5 — not a fixed Sanity `_type` name.

**Section title must be a shopper question**, e.g. `Which Bear Grylls book should you choose?` — not a vague label or seed-product claim alone.

- Column **i** describes entity **i** — header and cells must align
- **No empty cells** — every row fills every column (no blank, no dash filler)
- **Max 4 columns** on product-picker comparisons — storefront grid shows empty slots beyond four
- **Comparison shopper rows:** `cells[0]` = shared question label (`What it is`, `Best for`, **`Skip if`** — all three required on works comparison); `cells[1…n]` = selective per-product answers. See `references/shared/copy-voice.md` (**Skip if** = use-case elimination, 5–8 words, must point to another column — no dead ends, no product put-downs)
- **Short row labels** (2–4 words) in `cells[0]` — e.g. `What it is`, `Best for`, `Skip if`. Answers in `cells[1…n]` only; do not repeat the label in every answer cell
- **Skip if conversion job:** honest negative constraints that cure analysis paralysis, build trust, enable upsell to adjacent columns, and reduce wrong-product returns — never a bounce trap
- **Variant siblings** (same item, different format/size/tier/pack): discriminating column headers + text-led chooser — not cover-vs-cover
- **Never** mix `ticks` + prose `cells` on the same row (storefront column shift)

## Copy voice

Load `references/shared/copy-voice.md` — **hard rules** for all blocks:

- **No em-dashes** in reader copy (AI tell — use commas, colons, or new sentences)
- **No markdown** in plain string fields (`body`, `bannerText`, FAQ answers)
- **Short banners** (~15 words max); light CTA text on dark bands
- **Comparison max 4 columns**, every cell substantive
- **Maker quote** → testimonial panel; **creator browse** → separate banner/CTA panel

## Copy structure (no markdown dump panels)

Engage with panel-native structure:

- **Every block:** `sectionTitle` + `sectionSubtitle` + `buyQuestion` (`Why buy?` | `Who is it for?` | `What makes it different?`)
- Section headings and subheadings in panel title/heading fields — character limits in `copy-voice.md`
- Short scannable paragraphs — max 3 lines per paragraph in markdown fields; one idea per paragraph in plain fields
- Bullet-like lists via highlight grids, icon grids, or FAQ items
- Pull quotes in testimonial / quote panels — not `>` blockquotes in `body`
- CTAs with real **outbound** URLs on dedicated CTA panels (`thinBanner`, `buttonCardV2`, `edenLink`)
- **Fourth-wall ban:** customer-facing copy only — no CMS/merchandising jargon (`copy-voice.md`)

## Design brief (always apply)

1. **One composition** — first viewport = one idea (voice + promise + path)
2. **Engagement** — scannable hierarchy, progressive disclosure, proof near claims, clear next actions
3. **SEO / discoverability** — entity-clear headings (who / what / for whom / why), FAQ-ready answers, internal links to maker/catalogue URLs (**outbound** from seed)
4. **Web guidelines** — accessible contrast intent, mobile-first stacking, readable line lengths
5. **Emotion + trust** — match `domainSnapshot.tone` and personas
6. **Panel-aware imagery** — `imageIntent.safeZones` for overlay text, carousel chrome, tile captions

## Role

Use `editorRole` from target constants — then design beyond it.

## Process

1. Re-imagine ideal surface from personas + findings + brief
2. **Chrome overlap map (required):** list live surface chrome jobs already present (title, price, buy box, FBT, related carousel, reviews aggregate, description, bulk table, sticky ATB). Strip blocks must **not** take those as primary beats — add what chrome cannot: maker story, themes, audience pathways, choose-or-skip, FAQ objections.
3. Invent sections that maximise engagement within what panels can render — **one job per block**
4. Write **near-final shippable copy** — headlines, bodies, CTA labels + **outbound** URLs
5. Annotate **`imageIntent`** per block — Stage 6 locks type + dimensions. **Cardinality:** if hinting a panel that needs N tiles, supply N **on-job** items now (or choose a layout whose count matches). Never plan to pad later from another block.
6. Weave catalogue entities into commerce modules — never bake in price or stock text
7. SEO outline: primary entity phrase, supporting heading intents, FAQ entities (one FAQ home in `blocks[]`). FAQ = objections not already answered above (`faq_no_rehash`).
8. **CRE hesitation gap:** map each `topHesitations[]` item to one block in `hesitationGapMap`; ensure closing band is a **What Next** safe step (`cre-conversion.md`).
9. Produce **`pageStructure`** wireframe map + **`chromeOverlapMap`** for Gate 5
10. Score **Commerce / Engagement / SEO / Conversion** pillars (`page-structure.md`) — fix weak pillars before Gate 5; Conversion must cite CRE evidence

## Out (flexible schema)

`blocks[]` = single source of truth — no parallel top-level `faq[]`.

Minimum shape:

```json
{
  "pageTitle": "...",
  "seo": {
    "primaryEntity": "...",
    "metaTitle": "...",
    "metaDescription": "...",
    "h1": "...",
    "secondaryHeadings": ["..."]
  },
  "designConcept": "visual direction + engagement strategy + locked palette tokens from domain",
  "chromeOverlapMap": {
    "liveChromeJobs": ["title", "price", "buyBox", "fbt", "forYou", "reviewsAggregate", "description", "bulkTable"],
    "stripJobs": ["makerStory", "themes", "audiencePathways", "socialProofQuotes", "formatChooser", "worksComparison", "faqObjections", "closingCta"],
    "doNotDuplicate": ["buyBoxTitleAsHeroH1Clone", "reviewsStarAggregateOnly", "fbtCarouselInStrip"]
  },
  "hesitationGapMap": [
    { "hesitation": "Is this too academic for a seeker?", "blockId": "audience-pathways", "beat": "Pathway tile: seeker-readable eyewitness narrative" }
  ],
  "pageStructure": [
    {
      "order": 1,
      "blockId": "hero-...",
      "layoutKind": "heroOverlay | makerSpotlight | faq | carousel | comparison | ctaBand | ...",
      "purpose": "one job for this area",
      "image": { "role": "hero|maker|brand|catalogue|none", "srcIntent": "..." },
      "text": { "title": "...", "body": "full near-final copy...", "ctaLabel": "...", "ctaUrl": "https://..." }
    }
  ],
  "blocks": [ {
    "id": "...",
    "layout": "...",
    "sectionTitle": "Reader-visible H2 — question or benefit",
    "sectionSubtitle": "One-line frame under the title — mandatory",
    "buyQuestion": "Why buy? | Who is it for? | What makes it different?",
    "purpose": "one job (internal)",
    "headline": "...",
    "body": "...",
    "ctaLabel": "...",
    "ctaUrl": "...",
    "imageIntent": { ... }
  } ],
  "narrativeNote": "top→bottom story beats"
}
```

**Forbidden fields:** `motionIntent`, sticky-commerce-as-surface-chrome, parallax/JS specs, top-level `faq[]`, unmapped `modules[]`.

## Gate presentation (orchestrator MUST show)

Wireframe mockup top→bottom — **every block shows `sectionTitle` + `sectionSubtitle`**:

```
[sectionTitle]: Which Bear Grylls book should you choose?
[sectionSubtitle]: Compare gospel narrative, devotion, kids, and autobiography paths
  layoutKind: comparison / buyQuestion: What makes it different?
  comparison rows: What it is | Best for | Skip if
  products: ...

[sectionTitle]: What readers and reviewers say
[sectionSubtitle]: Named endorsements from publisher and press — not star ratings alone
  layoutKind: testimonials
  ...
```

Reject if: outline-only copy, missing `sectionTitle` or `sectionSubtitle` on blocks, missing `buyQuestion`, missing `hesitationGapMap` (product), missing CRE safe-step CTAs on closing/mid blocks, internal labels only (`Hero`, `FAQ`, `Maker spotlight`), `designConcept` missing (incl. palette), `chromeOverlapMap` missing, raw internal IDs, self-surface links, CMS/merchandising jargon, store-policy FAQ, jobs panel types, module budget >9 without exception note, planned tile padding from another block, or gate cannot render as mockup above.
