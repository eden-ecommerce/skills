# Draft — product

`panels[]` on `product` doc. Draft rules: `constants/targets/product.md`.

Load [`references/6-media/panel-dimensions.md`](../6-media/panel-dimensions.md) when mapping assets to panel types.

## Image mapping

| Panel role | Asset rule |
|---|---|
| Hero / banner overlay | **Generated** asset from `mediaPlan` — not raw catalogue cover paste |
| Maker spotlight | Generated portrait/thematic OR credited official URL |
| Theme tiles (`publisherImage300x300V2`) | **Exactly 3** generated 300×300 assets |
| Theme tiles (`publisherImage220x220V2`) | **Exactly 4** generated 220×220 assets |
| Product carousel / comparison (distinct works) | **`edenProductPicker.productIds`** — no cover upload |
| Text panels | No image |

Map `imageBrief[].targetPanelType` → panel `_type` **1:1**. Do not remap after Media (e.g. 300×300 → 220×220).

## Required fields before mutate

| Panel `_type` | Set |
|---|---|
| `imageWithOverlayAndTextV2` | `locale: { locale: "All", localeTitle: "<short hero label>" }` |
| `publisherImage300x300V2` | `images[]` length **3** |
| `publisherImage220x220V2` | `images[]` length **4** |

## Format siblings (hardback / ebook / audiobook)

Same title in different formats share **near-identical covers**. Do **not** use `publisherComparison` with product picker for format siblings.

| Do | Don't |
|---|---|
| `publisherComparisonChart` with columns **Hardback** / **Ebook** (discriminating headers), full prose per cell, links in copy | `publisherComparison` with two `productIds` for HB + ebook |
| FAQ or `buttonGrid` with titled links: “View ebook edition → URL” | Bare `product 7355311` in reader copy |
| Compare **different works** in `publisherComparison` — picker IDs; every cell filled | Format siblings as unrelated catalogue alternatives |
| Related carousel = other titles only; omit seed + format siblings; `showPrice: false` | Seed + ebook in carousel |

## Comparison matrix rules

- `cells[]` length = column count per row
- **No empty cells** — no `""`, no `"—"`, no trailing blank column
- Prefer **prose-only rows** OR **ticks-only rows** — do not mix `ticks` + descriptive `cells` in same row (shifts columns on storefront)
- Column headers: use discriminating labels when titles collide (Hardback | Ebook, not My Story | My Story)

Live PDP already exposes format switching in chrome — content strip explains the **choice**, not duplicate format tiles.
