# Media — product

Load [`panel-dimensions.md`](panel-dimensions.md). Phase A **required** fields per block before generate.

## Generate vs catalogue

| Block type | Final asset |
|---|---|
| Hero / banner (`imageWithOverlayAndTextV2`, `imageWithTextOverlay`) | **Generate** — `style-refs/eden-hero-split-safezone.png` + seed `imageUrl` as **reference only** → crop to **970×300** |
| Maker spotlight (`publisherSingleImageWithText`) | **Generate** or credited official URL — **480×360** (4:3) |
| Theme tiles (`publisherImage300x300V2`) | **Generate** — **exactly 3** tiles at **300×300** each |
| Theme tiles (`publisherImage220x220V2`) | **Generate** — **exactly 4** tiles at **220×220** each |
| Publisher / brand | Official logo URL upload or one neutral generate |
| Atmospheric | **Generate** — no readable books |
| Product carousel / comparison (distinct works) | **Picker `productIds` only** — storefront pulls `imageUrl`; **no Sanity cover upload** |
| Format chooser (same title) | **No images** — `generate: false`; text/chart/buttons only |

## Eden hero / banner (generate)

1. Generate to **970×300** (or generate 16:9 then crop to 970×300 before upload)
2. **Left ~40%**: text-safe wash — headline/subhead/CTA in overlay
3. **Right**: lifestyle + visual echo of seed cover colours — not pixel-perfect catalogue paste
4. No off-domain props; no invented readable competing titles

## Author / maker portraits

- Check findings for credited official image — upload once as `product-{id}__author__{slug}.…`, reuse `sanityAssetRef`
- Else generate one portrait (4:3) — do not mint duplicates for FAQ/CTA blocks

## Caps

- Generate only what reuse cannot cover: typically **1 hero** + **0–1 author** + **0–1 publisher** + thematic tiles per panel cardinality
- **Never upload** `__cover__{productId}` when Draft panel uses `edenProductPicker`
- Reject and regenerate if domain gate fails or dimensions wrong

## Draft handoff

- `imageBrief[].targetPanelType` is locked — Draft maps 1:1 to panel `_type`
- Catalogue panels: `mediaPlan` stores `productId` + `imageUrl`; picker resolves covers on storefront
