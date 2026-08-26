# Article target

| Field | Value |
|---|---|
| id | `article` |
| sanityDoc | `article` |
| seed identifier | slug, doc id, or topic from brief |
| seed surface | Canonical article URL — **no links back** |
| panelField | `richText[]` (**Sanity field** for embeds — not the `richText` panel `_type`) |
| algolia | optional |
| galleryKey | `gallery.article` |
| previewType | `article` |
| editorRole | professional blog article editor |

## Requirements

Narrative brief enough — no hard IDs.

## Spine

See `templates/article.md`.

## Draft identifiers

- Embed panels in `richText[]` field using allowed gallery `_type`s only
- Shared hard rules apply
