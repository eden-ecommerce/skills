# Desired Content — product

Seed identifier: Eden `productId`. Content strip sits **below live buy-box chrome** — do not duplicate title, price, buy box, or core spec table on the strip.

Facts only from `findings` / `products`. Maker may be author or manufacturer by product type.

## Overlay deltas (shared rules apply)

- **Module budget:** 6–9 blocks — see `templates/product.md` buyer-intent spine
- **Hero:** product clarity + benefit in `sectionTitle`/`sectionSubtitle` — not intrigue-only or buy-box title clone
- **Title + subtitle:** mandatory on every block; map to panel fields at Draft (`page-structure.md`)
- **Variant siblings** (same title, different format/size): text-led chooser with discriminating labels — not cover-vs-cover comparison
- **Seed surface URL:** canonical Eden product path for `productId` — **never** use as CTA or `edenLink` target in strip copy
- **Comparison picker:** seed may appear as the **display** first column for choose-or-skip — **no Shop Now / seed PDP link** on that column; link other columns only
- **Carousel:** omit seed `productId` and same-title format/edition siblings entirely (`carousel_no_seed`)
- **Audience / pathway grids:** every tile must be a distinct persona or use-case pathway — never reuse theme/eyewitness tile copy to fill cardinality
- **Format coverage:** if findings list print + ebook + audio (+ seasonal edition), the format chooser **or** FAQ must name all of them
- **FAQ:** product-fit objections only — **no** generic returns, dispatch, or Helpdesk policy (live support owns those)
- **Jobs panels:** never `featuredOrganisationJobs`, `organisationJobSearch`, or `appJobs` on product strips
- **One maker CTA:** single outbound maker-catalogue browse path on the strip
- **CRE What Next:** closing band + at least one mid-strip block offer safe-step outbound CTAs (`cre-conversion.md`); no Buy now / Add to basket in strip
- **CRE outcome headlines:** hero and pathway section titles reframe purchase as outcome/story + product clarity, not SKU specs
- **CRE hesitation gap:** `hesitationGapMap` covers all `topHesitations[]` from findings (2–3 items, one block each)
- **CRE cross-sell harmony:** if carousel present, job = maker catalogue discovery — not FBT/For you duplicate
- **Palette:** `designConcept` must name locked Eden tokens from `constants/domains/eden.md`; Stage 6 `visualSystem` must match

## Encouraged layout kinds

Hero overlay, pathway/highlight ribbon, theme tile grid, social proof (attributed only), variant chooser (`layoutKind: comparison`), distinct-works comparison, gift panel (when persona supports), FAQ hub, catalogue sibling carousel, closing CTA band — mix panel families; avoid one-family pages and editorial biography walls.

Prefer **more smaller blocks** (titled tiles) over one dense maker essay.

## Cardinality rule (product grids)

| Hinted panel | Count | Rule |
|---|---|---|
| `publisherImage300x300V2` | exactly 3 | All 3 tiles serve **this** block’s job |
| `publisherImage220x220V2` | exactly 4 | All 4 tiles serve **this** block’s job |

If you only have 2 real pathways, do **not** pick the 4-up panel — use a 3-up with a third on-job pathway, highlight grid, or FAQ items instead.

## Example Gate 5 rows (layoutKind only — not Sanity `_type`)

```
heroOverlay: Opening promise
  sectionTitle: «what it is + why it matters»
  sectionSubtitle: «one-line buyer frame»
  buyQuestion: Why buy?
  image: thematic hero (not raw catalogue paste)
  CTA: More from this maker → https://www.eden.co.uk/.../author/...

highlightGrid: Who it's for
  sectionTitle: Who will enjoy this book?
  sectionSubtitle: «pathway frame»
  buyQuestion: Who is it for?

comparison: Works chooser
  sectionTitle: Which [maker] book should you choose?
  sectionSubtitle: «compare paths in one view»
  buyQuestion: What makes it different?

faq: Objections
  sectionTitle: Questions before you buy
  sectionSubtitle: «format, audience, genre — not returns policy»
  buyQuestion: Who is it for?

ctaBand: Closing What Next
  sectionTitle: (in bannerText)
  CTA: More from [maker] → outbound catalogue URL
```

Do not specify sticky buy box, retailer A+ mimicry, or `motionIntent`.
