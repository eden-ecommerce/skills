# Draft — product

Panel field: `panels[]` on `product` doc. Seed identifier: `productId`. Seed surface = Eden catalogue path for that id.

Load [`references/6-media/panel-dimensions.md`](../6-media/panel-dimensions.md) when mapping assets.

## Catalogue link (preview resolution)

Eden preview resolves the Sanity `product` doc by **ISBN-prefixed title**, not by `productId` field:

`{ISBN} - {Product name}` e.g. `9781850787235 - Bacon Sandwiches and Salvation`

- Set `title` on the draft (and published doc if preview still misses the strip) via `draftPatch` top-level `title` / `set.title` — `patch_sanity_draft.py` merges these into the patch `set`.
- Source ISBN from Algolia `manuf_ref` / catalogue facts — never invent.
- Fail Stage 8 `panels_visible_on_preview` if the strip is empty because the title does not match this pattern.

## Panel mapping (product-specific)

| Content job | Typical `_type` | Notes |
|---|---|---|
| Hero / banner | `imageWithOverlayAndTextV2` | Generated asset — not raw catalogue paste |
| Maker spotlight | `publisherSingleImageWithText` or gallery equivalent | Generated or credited URL |
| Theme tiles 3-up | `publisherImage300x300V2` | **Exactly 3** generated 300×300 |
| Theme tiles 4-up | `publisherImage220x220V2` | **Exactly 4** generated 220×220 |
| Variant chooser | `publisherComparisonChart` | Text cells + row `label`; discriminating column headers |
| Distinct works comparison | `publisherComparison` | Picker IDs; prose-only rows; **no ticks** when cells have text |
| Sibling carousel | `productCarousel` | Other titles only; omit seed + variant siblings from `products` **and** `sponsoredProducts`; `showPrice: false` |
| FAQ | `publisherFaq` | Objections only — no full rehash of earlier panels |
| Audience pathways 4-up | `publisherImage220x220V2` | **4 distinct pathways** — never pad with theme/voice tiles from another panel |
| Theme tiles 3-up | `publisherImage300x300V2` | **3 on-job tiles** only |

Map `imageBrief[].targetPanelType` → `_type` **1:1**. Gallery-first — use other `_type`s when they fit the content job better. If Media locked a 4-up but Desired Content only has 2 pathways, **remap** to a fitting panel or invent 2 more on-job pathways — never duplicate.

## Required fields before mutate

| Panel `_type` | Set |
|---|---|
| `imageWithOverlayAndTextV2` | `locale: { locale: "All", localeTitle: "<short hero label>" }` |
| `publisherImage300x300V2` | `images[]` length **3**, all on-job |
| `publisherImage220x220V2` | `images[]` length **4**, all on-job |

## Variant siblings

Same title, different format/size — near-identical covers. Use `publisherComparisonChart` (not picker `publisherComparison`). Link variant columns to **other** SKU URLs — never seed surface URL. Cover **all** live formats named in findings (print / ebook / audio / edition) via chart columns or FAQ.

## Links before mutate

- Remove seed-column `edenLink` when `linkValue` matches seed product path (empty link or omit Shop Now)
- Hero / closing CTAs → maker page, sibling product, or external — not seed PDP
- Ensure draft doc is the one preview resolves for this `productId` (`panels_visible_on_preview`)
