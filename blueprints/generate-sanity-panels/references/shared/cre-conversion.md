# CRE conversion — bottom-of-PDP strips

Conversion Rate Experts (Win Reports) principles for **product content strips** below live buy-box chrome. Applies to Research Strategy (3), Findings (4), Desired Content (5), Draft (7), and Audit (8).

Load with `copy-voice.md` and `page-structure.md`. Does not replace Skip-if, chrome-overlap, or self-link rules.

## Core principles

### 1. Safe Step & What Next?

Users who scroll past cross-sells have not dropped off. They are still looking for direction.

- The strip is a **What Next?** path for shoppers not ready to click Add to Basket.
- Every **late** block (pathway tiles, comparison, FAQ, closing band) must offer a clear next step: who it is for, compare editions, read maker story, browse related titles.
- **Never** duplicate the buy box as a second purchase push in the strip.
- **One maker-catalogue CTA job** on the whole strip — not repeated banners to the same destination.

### 2. Reduce cognitive load

Removing clutter and reframing complex topics lifts engagement.

- **Hero product clarity:** hero must communicate **what the product is** and **why it matters** — curiosity hooks are optional sublines, not the only signal.
- **Outcome headlines:** reframe the purchase as story or benefit (`Encounter Jesus through those who knew him best`), not specs (`288-page hardback`) or intrigue-only (`The story he almost never told` with no product type).
- **One idea per band:** banners ~15 words; body in short paragraphs (max 3 lines each in markdown fields); no redundant trust ribbons that restate buy-box bullets.
- **One job per section:** do not merge unrelated persuasion beats into one panel.
- **Title + subtitle per block** so every scroll stop is a labelled content area.

### 3. Gap analysis (unanswered objections)

Users keep scrolling when doubts remain unresolved.

- Identify the **top 2–3 hesitations** for this SKU (accessibility, audience fit, academic vs readable, gift vs self, format, trust).
- Answer each **once** in a dedicated pathway tile, comparison row, or FAQ item.
- Do not bury objections only in a description clone the live PDP already shows.
- **Product-fit FAQ only** — not store-wide returns, dispatch, or Helpdesk policy (live support owns those).

## Checklist (product strips)

### Strategic purpose

- [ ] **What Next role:** strip captures undecided scrollers; offers read/compare/browse paths, not a second buy box.
- [ ] **Unresolved doubts:** top 2–3 hesitations answered in strip copy.
- [ ] **No repetition:** strip adds maker, themes, choose-or-skip, objections — not buy-box title, price, or FBT clone.
- [ ] **Module budget:** 6–9 blocks; every block earns its scroll.

### Copywriting

- [ ] **Hero clarity:** product type + benefit visible in hero title/subtitle.
- [ ] **Outcome copy:** key H2s are benefit/story-led, not SKU title or page-count dumps.
- [ ] **Buy-question coverage:** each block maps to Why buy / Who for / Different.
- [ ] **Safe-step CTAs:** low-friction labels (`See who it's for`, `More from [maker]`, `Compare editions`, `Browse related titles`). Ban `Buy now`, `Add to basket`, `Shop now` on seed PDP in strip.
- [ ] **Concise density:** punchy banners; scannable paragraphs; cut ~20–30% from fact-heavy first drafts.
- [ ] **Customer-facing only:** no CMS/merchandising jargon (`copy-voice.md` fourth-wall ban).

### Cross-sell harmony

- [ ] Strip **complements** live FBT / For you / related chrome — does not compete as a second product grid with the same job.
- [ ] If a strip carousel exists, job = **maker catalogue discovery** or format/edition routing — not FBT duplicate.
- [ ] Prefer decision modules (comparison, FAQ, closing band) after commerce chrome.

### Category & audience fit

- [ ] Pathway tiles and FAQ reflect category signals (gift, church, seeker, institutional, comparison shopper).
- [ ] Gift and institutional personas get distinct beats when findings support them.

### Technical content (skill scope)

- [ ] All strip copy is **complete in draft JSON** — no "load on scroll" placeholders or deferred copy.
- [ ] Audit confirms panels **visible in preview DOM** (crawlers and assistive tech read embedded content).

## Stage outputs

| Stage | CRE artifact |
|---|---|
| 3 Research Strategy | High-priority topic: **buyer hesitations / unanswered objections** |
| 4 Research Findings | `topHesitations[]` (2–3): `hesitation`, `source`, `stripBeat` |
| 5 Desired Content | `hesitationGapMap`: hesitation → `blockId`; Conversion pillar scored with CRE evidence; `buyQuestion` per block |
| 8 Audit | Checklist ids: `hero_product_clarity`, `outcome_headlines`, `safe_step_ctas`, `hesitation_gap_covered`, `no_chrome_repetition`, `cross_sell_harmony`, `what_next_closing`, `one_maker_cta`, `customer_facing_copy`, `scannable_body` |

## Safe-step CTA examples

| Good | Bad |
|---|---|
| More from Bear Grylls | Buy now |
| See who it's for | Add to basket |
| Compare editions | Shop this book |
| Browse related titles | Order today |
| Explore Eden Plus for churches | View hardback on Eden (seed PDP) |

Outbound only — never seed product URL. Live buy box owns purchase.
