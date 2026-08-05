# Panel image dimensions (product content strip)

Strip max width **970px** on desktop. **Generate/crop to these exact targets before Sanity upload** — do not ship tool-default sizes (e.g. 1536×1024 for a 970×300 hero). Always leave **safe zones** for overlay text and carousel chrome.

Load gallery: `{NEXT_NEXT_EDEN_BASE_URL}/panels/product` — verify before Draft.

## By panel `_type`

| Panel `_type` | Target size | Aspect | Generate notes |
|---|---|---|---|
| `imageWithOverlayAndTextV2` | **970 × 300** (banner) | ~3.2:1 | Hero/banner. **Left ~40% text-safe** (light/neutral). Lifestyle + product on right. See `style-refs/eden-hero-split-safezone.png` |
| `imageWithTextOverlay` | **970 × 300** (banner) | ~3.2:1 | Same as above — full-bleed + overlay copy |
| `publisherImageGrid900x300` | **900 × 300** | 3:1 | Single wide landscape banner |
| `publisherImage970x300V2` | **970 × 300** | ~3.2:1 | Wide banner with optional copy |
| `publisherImage300x300V2` | **300 × 300** | 1:1 | **Exactly 3** tiles required; caption below — keep bottom 15% calm |
| `publisherImage220x220V2` | **220 × 220** | 1:1 | **Exactly 4** tiles required; title/body below each tile |
| `publisherSingleImageWithText` | **~480 × 360** | 4:3 landscape | Beside markdown body; portrait or thematic scene |
| `publisherSingleImageWithSidebar` | **~480 × 360** | 4:3 | Image + sidebar copy |
| `publisherBrandLogo` | **~300 × 120** | ~2.5:1 | Imprint logo on neutral — prefer official asset URL |
| `thinBanner` | **970 × 120** | ~8:1 | Closing CTA band; text overlay zone |
| `productCarousel` | **300 × 463** (cover) | book cover ratio | **Picker `productIds`** — storefront resolves cover; do not upload to Sanity |
| `publisherComparison` | per cell | cover thumb | Distinct works only — picker resolves covers; fill all cells; no empty cells |
| `publisherComparisonChart` | none | — | Format/variant chooser — text cells only; discriminating column headers |
| `testimonials` | none / texture | — | Text-led; optional soft texture only |
| `highlightBlock` | none | — | Text-led |
| `publisherFaq` | none | — | Text-led |
| `richText` | none | — | Text-led |

## Safe zones (all image panels)

| Zone | Rule |
|---|---|
| Overlay text (hero/banner) | Left **40%** clear or low-contrast wash |
| Carousel | L/R **10%** margin — no focal detail under arrows |
| Tile captions | Bottom **15%** unbusy — title/body render below image |
| Mobile crop | Centre-weight subject; avoid critical detail at edges |

## Generation aspect_ratio hints (image tool)

| Use case | Suggested ratio |
|---|---|
| Hero / banner | Generate/crop to **970×300** before upload (3.2:1) |
| Square tile | `1:1` |
| Author / maker portrait | `4:3` landscape or `3:4` portrait beside text |
| Wide texture / church mood | `16:9` |
