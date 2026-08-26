# Product target

| Field | Value |
|---|---|
| id | `product` |
| sanityDoc | `product` |
| seed identifier | Eden `product_id` (`productId`) |
| seed surface | Canonical Eden product URL for `productId` — **no links back** |
| panelField | `panels[]` |
| algolia | yes — `products` index |
| galleryKey | `gallery.product` |
| previewType | `product` |
| editorRole | professional product page editor |

## Requirements

| Key | Required | Notes |
|---|---|---|
| `productId` | **yes** | Block Definition until set. |

## Spine

See `templates/product.md`.

## Draft identifiers

- Patch `drafts.{publishedId}` when published doc exists
- Overwrite catalogue facts from Algolia after LLM copy
- Shared hard rules: max 2 same `_type`; never `markdown` / `richText` panel types; no self-surface links
