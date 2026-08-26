# Media — shared

Stage 6. In: `desiredPageContent`, `domainSnapshot`, `researchFindings`. Out: `pageWithMedia.json`

Load: `domainSnapshot` visual rules, target `panel-dimensions` table (product: `references/6-media/panel-dimensions.md`), `references/6-media/style-refs/` when Eden product.

## Image source policy

| Image kind | Action |
|---|---|
| Generated hero / thematic / author scene | Generate → crop to target pixels → upload Sanity asset |
| Official logo / credited portrait (non-catalogue) | Upload once or reuse existing asset |
| Catalogue / related product covers | **Picker `productIds` or CDN URL** — **do not upload** to Sanity when storefront resolves by ID |
| FAQ / comparison / text blocks | `generate: false` |

## Process (two phases)

### Phase A — Image brief (per block) — lock before generate

Before generating or uploading, produce **`imageBrief[]`** — one row per block that needs an image.

**Required on every row:** `targetPanelType`, `dimensions`, `aspectRatio` from panel-dimensions table. Draft must honor these — remap = Media re-run.

```json
{
  "imageBrief": [
    {
      "blockId": "hero-breakfast-thesis",
      "blockTopic": "Joke-thesis + Vintage Plass A–Z promise",
      "imageConcept": "Eden split hero: lifestyle + product cluster right, text-safe left",
      "targetPanelType": "imageWithOverlayAndTextV2",
      "dimensions": "970×300",
      "aspectRatio": "16:9",
      "safeZones": "left 40% text-safe; no busy detail under headline",
      "referenceImages": [
        { "role": "style", "path": "references/6-media/style-refs/eden-hero-split-safezone.png" },
        { "role": "productCover", "url": "https://www.eden.co.uk/images/300/9781850787235.webp", "note": "composition reference only — do not upload as final asset" }
      ],
      "generate": true,
      "promptIntent": "Professional UK Christian retail hero banner; generated scene echoing cover colours; no foreign readable titles"
    }
  ]
}
```

**Per-block topic rules**

| Block theme | Safe generate ideas |
|---|---|
| Author / maker | Professional portrait, speaking, writing desk — **no invented readable book titles** |
| Publisher / brand | Imprint logo from official URL, or neutral brand texture |
| Product themes | Abstract motifs, typography textures, thematic objects **without** off-domain symbols |
| Church / ministry | Empty pew, hymn book stack (spines blank), church hall — respectful |
| Commerce / related | **Catalogue via picker** — `products[].imageUrl` as reference only; `generate: false`, `source: catalogue` |
| FAQ / comparison / text | `generate: false` |

### Phase B — Generate, gate, plan

1. Define **visualSystem** (palette, photography) from `designConcept` + domain rules — **one locked palette for the whole strip**; every `imageBrief` and banner colour must use the same tokens (`eden.md`)
2. For each `imageBrief` where `generate: true`:
   - Use reference images (style ref + product cover URL as composition/colour reference)
   - **Generate a new image** — never paste catalogue cover as final hero/spotlight
   - **Crop/resize to `dimensions`** before upload — reject tool-default sizes (e.g. 1536×1024 for 970×300 hero)
   - Run **domain visual gate** before upload
3. For carousel/comparison with product picker: `source: catalogue`, `generate: false`, record `productId` + `imageUrl` in `mediaPlan` — **no Sanity cover upload**
4. Text-led blocks: explicit `generate: false`
5. Upload **generated/custom** assets to Sanity via `scripts/upload_sanity_image.py` (CLI `--project-id` / `--dataset` / `--token` from FIRST RUN); record `sanityAssetRef` in `mediaPlan`
6. Apply **asset naming + reuse** rules below

## Asset naming (generated/custom uploads only)

```
{target}-{productId|slug}__{role}__{short-desc}.{ext}
```

Examples: `product-6854250__hero__eyewitness-split.png`, `product-6854250__author__bear-grylls.png`

**Reject** generic names (`media-hero.png`, `media-tile.png`). Record `originalFilename` in `mediaPlan`.

Do **not** name or upload `__cover__{productId}` when Draft uses `edenProductPicker.productIds`.

## Reuse before generate

Do **not** generate a new author/publisher image when a credited official asset already exists in findings or was uploaded earlier in this run under `__author__` / `__publisher__`.

Set `generate: false` + `source: url|reuse|catalogue` when reusing. Note `reusesAsset` when applicable.

## Hard image rules

1. **Domain faith constraints** — every prompt includes `domainSnapshot` visual rules
2. **Reference ≠ paste** — style refs + seed cover inform **new** hero/thematic art
3. **Reuse credited maker/publisher** — upload once under naming convention
4. **Panel dimensions** — Phase A locks `targetPanelType` + `dimensions`; crop before upload
5. **Visual gate** — reject off-domain props before upload; regenerate if failed
6. **Media lock** — Draft must use locked `targetPanelType`; Audit fails on remap

## Out

Keep all `desiredPageContent` fields. Add:

```json
{
  "visualSystem": {
    "palette": {
      "ground": "#FFFFFF",
      "groundAlt": "#F5F5F2",
      "primary": "#2F6B4F",
      "secondary": "#2B5F8A",
      "highlight": "#F5C518",
      "textOnDark": "#FFFFFF"
    },
    "photography": "",
    "styleRef": "..."
  },
  "imageBrief": [ ... ],
  "mediaPlan": [
    {
      "blockId": "...",
      "assets": [
        {
          "role": "hero|portrait|thematic|cover|none",
          "source": "generate|catalogue|url|reuse|none",
          "targetPanelType": "imageWithOverlayAndTextV2",
          "dimensions": "970×300",
          "productId": null,
          "imageUrl": null,
          "sanityAssetRef": null,
          "originalFilename": "product-6854250__hero__eyewitness-split.png",
          "notes": "safe zones; domain check passed"
        }
      ]
    }
  ]
}
```

Gate: user approves **image brief + media plan + visual system** before Draft.

**Palette gate:** `visualSystem.palette` must match `designConcept` tokens from Stage 5. Audit fails `palette_consistency` if banners, bands, or generated art drift to unrelated colour schemes.
