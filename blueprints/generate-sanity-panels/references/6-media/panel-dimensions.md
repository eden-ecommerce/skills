# Panel image dimensions

**Generate/crop to exact targets before Sanity upload** — not tool-default sizes. Leave **safe zones** for overlay text and carousel chrome.

Load gallery from `domainSnapshot.urls.gallery` — verify before Draft. Tables below are **product strip** defaults; other targets use gallery + cache for active target.

## Forbidden panel types (any target)

Do not map blocks to these `_type`s:

| `_type` | Reason |
|---|---|
| `markdown` | Catch-all text dump — use structured panels |
| `richText` | Same — use highlight, FAQ, image+text, grids |

## By panel role (product strip reference)

| Panel `_type` | Target size | Aspect | Notes |
|---|---|---|---|
| `imageWithOverlayAndTextV2` | **970 × 300** | ~3.2:1 | Hero. Left ~40% text-safe |
| `imageWithTextOverlay` | **970 × 300** | ~3.2:1 | Full-bleed + overlay |
| `publisherImage300x300V2` | **300 × 300** | 1:1 | **Exactly 3** tiles; calm bottom 15% |
| `publisherImage220x220V2` | **220 × 220** | 1:1 | **Exactly 4** tiles |
| `publisherSingleImageWithText` | **~480 × 360** | 4:3 | Beside text; portrait or scene |
| `publisherSingleImageWithSidebar` | **~480 × 360** | 4:3 | Image + sidebar |
| `publisherBrandLogo` | **~300 × 120** | ~2.5:1 | Official logo URL preferred |
| `thinBanner` | **970 × 120** | ~8:1 | Closing CTA band |
| `productCarousel` | picker cover | varies | **Picker IDs** — no Sanity cover upload |
| `publisherComparison` | cover thumb | — | Distinct works; fill all cells; no ticks+prose |
| `publisherComparisonChart` | none | — | Variant chooser; row `label` + text cells |
| `testimonials` | none | — | Text-led |
| `highlightBlock` | none | — | Text-led grid |
| `publisherFaq` | none | — | Text-led |

## Safe zones (all image panels)

| Zone | Rule |
|---|---|
| Overlay text | Left **40%** clear or low-contrast wash |
| Carousel | L/R **10%** margin |
| Tile captions | Bottom **15%** unbusy |
| Mobile crop | Centre-weight subject |

## Generation aspect_ratio hints

| Use case | Ratio |
|---|---|
| Hero / banner | Crop to **970×300** (3.2:1) |
| Square tile | `1:1` |
| Maker portrait | `4:3` or `3:4` |
| Wide mood | `16:9` |
