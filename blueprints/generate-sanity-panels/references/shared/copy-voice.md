# Copy voice — all stages

Professional ecommerce content design voice. Applies to Desired Content (5), Draft (7), and Audit refinement (8).

## Em-dash ban (hard)

**Never** use em-dash or en-dash as punctuation in reader-facing copy:

| Banned | Use instead |
|---|---|
| `—` `\u2014` em-dash | comma, colon, period, or parentheses |
| `–` `\u2013` en-dash (non-numeric) | comma or "to" (ranges: `8 to 12` not `8–12`) |

Scan JSON and preview before Gate 8. Fail audit `no_em_dash` if any remain.

**Why:** em-dash clusters are a common AI tell on UK Christian retail copy.

## Fourth-wall ban (hard)

Speak **to** the shopper — never like CMS notes, merchandising logs, or research output.

| Banned phrasing | Do instead |
|---|---|
| `Eden categorises`, `Eden merchandises`, `On Eden he appears as` | Plain customer language about the product or recipient |
| `Catalogue fit`, `credited author of this autobiography` | Who the author is and why they matter to the reader |
| `Always confirm current Helpdesk copy`, `prior authorisation required` | Omit store-policy detail — live Helpdesk owns it |
| Raw taxonomy paths (`Biography > Autobiography`) | Everyday category words (`memoir`, `life story`) |
| `No named … endorsement was found` (research-log tone) | Customer guidance only when findings require a trust caveat |

No draft, placeholder, or meta disclaimers in reader fields. **FAQ tone is the gold standard** for all body copy: short, direct, question-led.

## Plain string fields are not markdown

Fields like `body`, `bannerText`, FAQ `answer`, tile `body` are **plain text** in Sanity — not markdown renderers.

| Do not | Do instead |
|---|---|
| `> blockquote` | `testimonials` / `testimonialItem` |
| `[Browse Eden](url)` | `edenLink`, `thinBanner`, `buttonCardV2` |
| `**bold**` | panel `heading` / `header` fields |
| `### Heading` | panel `title` / `heading` |

## Markdown body fields (when schema uses markdown)

Some product text fields accept markdown. When used:

- **Max 3 lines per paragraph** — split with a blank line between paragraphs; never one dense wall.
- No markdown headings in body — use panel `title` / `heading` / `sectionTitle` instead.
- No `>`, tables, or inline links in markdown body — use structured panels and `edenLink` CTAs.
- Same fourth-wall and buy-question rules apply.

Fail audit `markdown_paragraph_limit` if any markdown paragraph exceeds 3 lines.

## Heading character limits (hard)

Count characters including spaces. Fail audit `heading_char_limits` when out of range.

| Field | Min | Max | Notes |
|---|---|---|---|
| Hero `heading` / hero `sectionTitle` | 28 | 70 | Must name product type + benefit — not intrigue-only |
| Section `sectionTitle` (H2) | 24 | 60 | Shopper question or decision |
| Section `sectionSubtitle` | 40 | 120 | One-line frame under the title — mandatory on every block |
| Tile / pathway `title` | 12 | 40 | Scannable label |
| Tile / pathway `body` | — | 180 | 1–2 short sentences |
| `thinBanner.bannerText` | — | ~90 chars (~15 words) | One idea |
| Comparison row label (`cells[0]`) | 6 | 24 | 2–4 words |
| FAQ question | 20 | 80 | Natural search phrasing |

## Scannable body rules (hard)

- **One idea per paragraph** — prefer ≤2 short sentences.
- **Soft sentence cap ~30 words** — shorten or split longer sentences.
- **Lead with customer value** — biography only as proof for a buy question.
- **Cut-test:** every paragraph must answer **Why buy?**, **Who is it for?**, or **What makes it different?** — else delete.
- Aim **20–30% shorter** than “include every interesting fact” first drafts.
- FAQ answers: 1–3 sentences; no policy dumps.

Fail audit `scannable_body` on opening wall-of-facts, multi-idea paragraphs, or average sentence length far above ~30 words in a body field.

## Section structure

- **Every block:** `sectionTitle` + **`sectionSubtitle`** (reader-visible title + subline that frames the block).
- **Maker spotlight:** `publisherSingleImageWithText` with `heading` = section title; `subheading` or first body line = `sectionSubtitle`; `body` = 2–4 short **buying-framed** paragraphs (why this maker matters for this purchase — not a magazine feature).
- **Attributed quote + source:** `testimonialItem` with `quote` + `citation` — not inline in maker `body`.
- **Creator / catalogue CTA:** separate `thinBanner` or `buttonCardV2` with outbound link — not buried at end of maker paragraph. **One maker-catalogue CTA job** on the whole strip.

## Outcome headlines (CRE)

Load `references/shared/cre-conversion.md`. Headlines reframe the purchase as story or benefit, not specs.

| Bad (spec / SKU / intrigue-only) | Good (outcome + clarity) |
|---|---|
| `The story he almost never told` (no product signal) | `John Lennox's memoir: faith, reason, and a life of apologetics` |
| `288-page hardback gospel retelling` | `Encounter Jesus through those who knew him best` |
| `The Greatest Story Ever Told by Bear Grylls` (buy-box clone) | `Jesus' story, told by five eyewitnesses` |

Hero `heading` and major section `title`/`sectionTitle` must pass the outcome test **and** communicate what the product is.

## Safe-step CTAs (CRE)

Strip CTAs are **low-friction next steps** for undecided scrollers — not a second buy box.

| Allowed labels | Banned in strip |
|---|---|
| More from [maker] | Buy now |
| See who it's for | Add to basket |
| Compare editions | Shop now |
| Browse related titles | Order today |

All outbound — never seed PDP URL. Live buy box owns purchase.

## Banner panels (`thinBanner`)

- **One idea per band:** max ~15 words in `bannerText` (one short line or two very short lines).
- **Accessible contrast:** on dark bands (e.g. Eden green `#2F6B4F`), `bannerTextColour` and `buttonTextColour` must be light (`#FFFFFF` or `#FFFBF4`). Never dark grey/black button text on dark green.
- **Outbound CTA:** `link` + `buttonText` point to maker page, sibling SKU, or trusted external — never seed PDP URL.
- **No commerce chrome:** not "Add to basket", price, or stock in banner copy.

## Product comparison (`publisherComparison`)

Designed for the **comparison shopper** persona: a **clear section title** (question form) plus shared row labels down the left, selective answers per product across the row.

- **Section `title`:** shopper question — e.g. `Which Bear Grylls book should you choose?` Not vague (`comparison`, seed title only).
- **Max 4 product columns** — prefer 3–4 well-filled columns.
- **Required row set (works comparison):** `What it is`, `Best for`, **`Skip if`** — all three unless Stage 5 documents why a row is omitted.
- **Optional depth rows** when findings support (no invention): `Reading level`, `Best occasion`, `Tone`.
- **Row label in `cells[0]`** — short comparison question (2–4 words): e.g. `What it is`, `Best for`, `Skip if`. This is the storefront's leading label column; never leave it empty.
- **Product answers in `cells[1…n]`** — one selective answer per product column; answers only (do not repeat the question word in every cell).
- Column *i* header, picker `productIds[i]`, `links[i]`, and `cells[i + 1]` must align.
- Every cell substantive — no blank cells, no dash-only placeholders.
- Never mix `ticks` + prose `cells` on the same row.
- Use **customer vocabulary** — not internal publishing jargon (`science-and-religion argument book` → `Explores science and Christian faith`).

**Example rows:**
```json
"cells": ["Best for", "Gospel-sharing and church read", "Daily devotion habit", "Child or tween gift", "Adventure autobiography fans"]
```
```json
"cells": ["Skip if", "You want daily devotion", "You want immersive Jesus story", "Adult seeker or church read", "Gospel-sharing is your goal"]
```

### `Skip if` row (conversion — hard rules)

`Skip if` (or `Not for you if`) uses **negative constraints**: honest elimination that cures analysis paralysis, builds trust, enables upsell, and reduces wrong-product returns.

| Do | Don't |
|---|---|
| Frame **use-case / lifestyle** (“limited desk space”, “need wide margins for journaling”) | Frame as **product flaws** (“bulky”, “low quality”, “not good”) |
| Keep each cell **5–8 words** (scannable tie-breaker) | Write a paragraph per column |
| Make each Skip-if cell **point to another column’s Best for** (adjacent alternative) | Leave a dead end with no better-fit column in the same table |
| Use objective need language (“professional-grade durability”, “beginner-first guide”) | Harsh or subjective put-downs (“cheap”, “for people who don’t care”) |
| Use Skip if to **upsell / cross-sell** calmly toward the right column | Push every shopper to the seed column |

**Dead-end fail:** If Skip if says the reader is a beginner (or gift buyer, or kids reader) and no other column in the table is the beginner/gift/kids fit, rewrite columns or Skip-if cells until every elimination lands on an alternative in-table.

**Upsell pattern:** On a basic SKU column, Skip if = the need that the higher-tier / adjacent column satisfies (e.g. “wide margins for journaling” → journaling edition column).

Format choosers (`publisherComparisonChart`) may use `Choose when` / `Skip if` with the same rules when comparing formats.

## Layout rhythm

See `page-structure.md` for full section architecture. Before sign-off:

- Alternate visual weight (hero → ribbon → image+text → grid → comparison → social proof → FAQ → closing band).
- **Visible chapter breaks:** every block has title + subtitle; alternate panel families — no three text-heavy blocks back-to-back.
- **Panel spacing:** each major block reads as its own content area on scroll (title/subtitle pair + visual break before the next block).
- Images use locked Media dimensions — no stretched or squashed covers in tile/comparison slots.

## Accessibility intent

- Readable contrast on all text-on-colour panels.
- Short line lengths in body copy (break into paragraphs).
- CTAs are visible link labels, not paragraph-sized text blocks.
