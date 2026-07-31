---
name: generate-sanity-panels
description: Build SEO product panel drafts from Algolia data, schema, and panel gallery. Use when user wants Sanity product panels, PDP content from product ID, draft publish, or preview verify.
---

# GENERATE SANITY PANELS

## HARD RULES

- Draft only (`_id` prefix `drafts.`). Publish only after explicit user yes.
- No Storybook. No next-design prototype. No Studio `previewUrl`.
- Panel images → Sanity assets only. No external URLs in final draft.
- Preview token sensitive. Never log or store in public files.
- Preview: `https://eden-xi.vercel.app/api/preview?type=product&token=<TOKEN>&slug=<ID>`

## FLOW

### 1 — ALGOLIA

Product ID from user.

```bash
python3 scripts/fetch_algolia.py <PRODUCT_ID>
```

→ [2-fetch-product-data-from-algolia.md](references/2-fetch-product-data-from-algolia.md)

### 2 — RESEARCH

Wide/deep on product + author/publisher: image/video assets, themes, related products, publisher/author bios and official links.

### 3 — PAGE PLAN

Desired PDP by section (author, themes, specs, FAQs, related products, video, org/C360, hotspots). Per section: purpose, content, asset needs.

### 4 — SCHEMA + GALLERY

```bash
curl -s https://cms.eden.co.uk/schema.json -o schema.json
python3 scripts/extract_panels.py schema.json
```

Browse `https://eden-xi.vercel.app/panels/product`. Map title → `product.panels` `_type`. Note responsive layout, variants, schema field intent.

→ [1-fetch-product-sanity-panels.md](references/1-fetch-product-sanity-panels.md)

### 5 — FIT

Map page plan sections → panel types by gallery visual + schema fields. Drop section if no fit. Fewer strong panels beats filler.

### 6 — DRAFT

1. Fetch prod product doc. Get `_id`, existing `panels`.
2. Upload images → Sanity assets.
3. Build `panels` array. Unique `_key` per item. Valid asset refs.
4. Patch draft: `manus-mcp-cli tool call patch_documents --server sanity --input '{...}'`

→ [3-fetch-product-document-from-sanity.md](references/3-fetch-product-document-from-sanity.md)

### 7 — PREVIEW + FIX

Preview URL. Scroll full page. Verify vs page plan: order, content, images, responsive, name/price vs Algolia. Mismatch → patch → re-preview.

→ [4-view-product-preview-in-sanity.md](references/4-view-product-preview-in-sanity.md)

### 8 — PUBLISH

User permission → `manus-mcp-cli tool call publish_documents --server sanity --input '{...}'`. Project `bct7esy7`. Dataset `eden`.
