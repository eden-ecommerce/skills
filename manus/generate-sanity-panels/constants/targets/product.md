# Product target

| Field | Value |
|---|---|
| id | `product` |
| sanityDoc | `product` |
| identifier | Eden `product_id` |
| panelField | `panels[]` |
| algolia | yes — `products` index |
| galleryKey | `gallery.product` |
| previewType | `product` |
| editorRole | professional product page editor |

## Requirements

| Key | Required | Notes |
|---|---|---|
| `productId` | **yes** | Eden `product_id`. Collect at first-run outline. Block Definition until set. |

## Spine default

See `templates/product.md`.

## Draft rules

- Patch `drafts.{publishedId}` when published doc exists
- Never `drafts.skill-test-*` on live slug without user sign-off
- Overwrite price, URL, title, cover, availability from catalogue after LLM copy
- Max 2 identical `_type` on final page
- Never use `markdown` panel `_type`
